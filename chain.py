from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_core.documents import Document
load_dotenv()
#문제 1. 특정 에러 메시지(예: Tool Choice 에러)가 포함된 이슈와 댓글을 모두 찾아, 원인과 최종 해결책을 하나의 리포트로 요약하는 체인을 구성하시오.
SYSTEM_PROMPT_REPORT = '''
당신은 코딩 에러 분석 전문가입니다.

주어진 [참고 문서]를 기반으로 하나의 통합 리포트를 작성하세요.

반드시 아래 형식을 따르세요:

1. 문제 개요
2. 원인 분석
3. 해결 과정 (댓글 포함)
4. 최종 해결 방법

규칙:
- 반드시 참고 문서 기반으로만 작성
- 추측 금지
- 간결하고 명확하게 작성

[참고 문서]
{context}
'''

def build_report_chain(vectorstore:FAISS):
    llm = ChatGroq(
        model='llama-3.1-8b-instant'
    )

    prompt = ChatPromptTemplate.from_messages([
        ('system',SYSTEM_PROMPT_REPORT),
        ('human',"{input}"),
    ])

    retriever = get_retriever(vectorstore)

    chain = (
        {"input": RunnablePassthrough()}
        | RunnablePassthrough.assign(
            docs=lambda x: retriever.invoke(x["input"])
        )
        | RunnablePassthrough.assign(
            context=lambda x: format_docs(x["docs"])
        )
        | RunnablePassthrough.assign(
            answer=(
                {
                    "context": lambda x: x["context"],
                    "input": lambda x: x["input"],
                }
                | prompt
                | llm
                | StrOutputParser()
            )
        )
        | (lambda x: {
            "context": x["context"],
            "answer": x["answer"]
        })
    )
    return chain

#문제 2 특정 기술(예: PostgresSaver)의 이슈(ID 1)와 연관된 다른 DB 설정 이슈(ID 10, 11)를 찾아, 해당 기술 도입 시 주의해야 할 '통합 체크리스트'를 생성하는 RAG를 구현하시오.
SYSTEM_PROMPT_CHECKLIST = """
당신은 소프트웨어 아키텍처 및 트러블슈팅 전문가입니다.
단순 요약이 아니라 "문제 패턴을 재구성"하는 것이 목표입니다.

주어진 문서를 기반으로 특정 기술을 넘어
DB, connection, pooling, transaction 등
연관된 시스템 문제를 통합한 체크리스트를 작성하세요.

---

출력 형식:

1. 주요 문제 유형
각 항목은 반드시 아래 구조:
- 문제 유형:
- 발생 원인:
- 해결 방법:

※ 규칙:
- 단순 나열 금지
- 유사 문제는 하나로 통합

---

2. 반복적으로 발생하는 실수
- 공통적으로 반복되는 실수만 작성
- 중복 금지

---

3. 설정 및 사용 시 주의사항
- 시스템 관점에서 작성 (DB, connection, pooling 포함)
- 연관된 설정은 묶어서 설명

---

4. 베스트 프랙티스 체크리스트
- 실행 가능한 형태 (예: ~하라)
- 중복 금지

---

규칙:
- 초기 키워드에 제한되지 말 것
- 확장된 문서를 반드시 반영할 것
- 요약이 아니라 재구성할 것

---

[참고 문서]
{context}
"""

def build_checklist_chain(vectorstore: FAISS):
    llm = ChatGroq(model='llama-3.1-8b-instant')

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_CHECKLIST),
        ("human", "{input}")
    ])

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def first_retrieval(x):
        docs = retriever.invoke(x["input"])
        return {
            "input": x["input"],
            "seed_docs": docs
        }

    expand_prompt = ChatPromptTemplate.from_template("""
        다음 이슈들을 기반으로, 관련된 더 넓은 기술 영역까지 포함하는
        검색 쿼리를 3개 생성하라.

        요구사항:
        - 원래 기술에서 다른 기술 영역으로 확장할 것
        - (예: Postgres → DB → connection → pool → SQL 등)
        - 서로 다른 관점으로 작성

        이슈:
        {context}

        출력 형식:
        - query1
        - query2
        - query3
        """)

    def generate_queries(x):
        context = "\n".join([doc.page_content for doc in x["seed_docs"]])

        queries_text = (
            RunnableLambda(lambda x:{"context": x})
            | expand_prompt
            | llm
            | StrOutputParser()
        ).invoke(context)

        queries = [
            q.strip("- ").strip()
            for q in queries_text.split("\n")
            if q.strip()
        ]

        return {
            "input": x["input"],
            "seed_docs": x["seed_docs"],
            "queries": queries
        }

    def expand_retrieval(x):
        expanded_docs = []

        for q in x["queries"]:
            results = retriever.invoke(q)
            expanded_docs.extend(results)

        all_docs = x["seed_docs"] + expanded_docs

        seen = set()
        unique_docs = []

        for doc in all_docs:
            key = doc.metadata.get("row")

            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)

        return {
            "input": x["input"],
            "docs": unique_docs [:12]
        }

    chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"input": x})
        | RunnableLambda(first_retrieval)
        | RunnableLambda(generate_queries)
        | RunnableLambda(expand_retrieval)
        | RunnablePassthrough.assign(
            context=lambda x: format_docs(x["docs"])
        )
        | RunnablePassthrough.assign(
            answer=(
                {
                    "context": lambda x: x["context"],
                    "input": lambda x: x["input"]
                }
                | prompt
                | llm
                | StrOutputParser()
            )
        )
        | (lambda x: {
            "context": x["context"],
            "answer": x["answer"]
        })
    )

    return chain



def get_retriever(vectorstore:FAISS):
    def retrieve_both(query: str):
        issues = vectorstore.similarity_search(
            query,
            k=3,
            filter={"type": "issue"}
        )

        comments = vectorstore.similarity_search(
            query,
            k=3,
            filter={"type": "comment"}
        )
        return issues + comments

    retriever = RunnableLambda(retrieve_both)
    return retriever

def format_docs(docs: list[Document]) -> str:
    if not docs:
        return "관련 문서를 찾지 못했습니다."

    sections = []

    for i, doc in enumerate(docs, 1):
        doc_type = doc.metadata.get("type", "없음")

        section = f"[{i}] ({doc_type})\n{doc.page_content}"
        sections.append(section)

    return "\n\n".join(sections)
