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
