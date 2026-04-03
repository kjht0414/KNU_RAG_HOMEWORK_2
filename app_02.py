from vectorstore import init_vectorstore, load_vector_from_local
from chain import build_checklist_chain

vectorstore = init_vectorstore()
chain = build_checklist_chain(vectorstore=vectorstore)

q1 = "PostgresSaver 및 관련 기술 도입 체크리스트 작성"
result = chain.invoke(q1)

print(result['answer'])
print(result['context'])


"""
실행결과

"""