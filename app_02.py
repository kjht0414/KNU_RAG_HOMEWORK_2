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

불러오는 중
1. **관련 기술 패턴**
- **PostgresSaver**는 LangGraph에서 체크포인트를 저장하기 위해 사용되는 기술입니다.
- **DB 커넥션 풀링**은 PostgresSaver를 사용할 때 DB 커넥션을 효율적으로 관리하기 위해 중요합니다.
- **JDBC 드라이버 버전**은 LangGraph 내부의 pool 관리 로직과 연관이 있으며, 문제를 해결하는 데 도움이 될 수 있습니다.
- **LangGraph** 내부의 pool 관리 로직은 JDBC 드라이버 버전보다는 중요한 문제입니다.

2. **실수 패턴**
- **pool_size** 설정을 따로 하지 않아서 커넥션 숫자가 계속 증가하는 현상이 발생함.
- **DB 커넥션 풀링**을 사용하지 않아서 DB 커넥션 관리가 어려움.
- **JDBC 드라이버 버전**과 LangGraph 내부의 pool 관리 로직이 맞지 않아서 문제가 발생함.

3. **설정 및 사용 시 주의사항**
- **pool_size** 설정은 LangGraph 내부의 pool 관리 로직과 관련이 있으며, 적절한 수치로 설정해야 함.
- **DB 커넥션 풀링**을 사용하여 DB 커넥션을 효율적으로 관리해야 함.
- **JDBC 드라이버 버전**과 LangGraph 내부의 pool 관리 로직이 맞지 않아서 문제가 발생할 수 있으므로, 확인하고 설정해야 함.
- **LangGraph** 내부의 pool 관리 로직은 중요하므로, 확인하고 설정해야 함.

4. **권장 설정 및 베스트 프랙티스 체크리스트**
- **pool_size** 설정은 LangGraph 내부의 pool 관리 로직과 관련이 있으며, 적절한 수치로 설정해야 함.
- **DB 커넥션 풀링**을 사용하여 DB 커넥션을 효율적으로 관리해야 함.
- **JDBC 드라이버 버전**은 LangGraph 내부의 pool 관리 로직과 관련이 있으며, 확인하고 설정해야 함.
- **LangGraph** 내부의 pool 관리 로직은 중요하므로, 확인하고 설정해야 함.
- **try-with-resources**를 사용하여 DB 커넥션을 관리해야 함.
- **set_error_handler** 인터페이스를 구현하거나, 노드 출력값에 error 메시지를 포함하여 조건부 에지로 분기 처리하는 것을 추천합니다.

**체크리스트**
- LangGraph 내부의 pool 관리 로직 확인
- JDBC 드라이버 버전 확인
- pool_size 설정 확인
- DB 커넥션 풀링 사용
- try-with-resources 사용
- set_error_handler 인터페이스 구현 또는 조건부 에지로 분기 처리
- LangGraph 내부의 pool 관리 로직 설정 확인

**참고**
- LangGraph 문서에서 pool_size 설정에 대한 설명을 확인하여야 함.
- JDBC 드라이버 버전과 LangGraph 내부의 pool 관리 로직이 맞지 않아서 문제가 발생할 수 있으므로, 확인하고 설정해야 함.
- LangGraph 내부의 pool 관리 로직은 중요하므로, 확인하고 설정해야 함.
[1] (issue)
title: PostgresSaver 사용 시 연결 누수 문제
content: LangGraph에서 PostgresSaver를 사용하여 체크포인트를 저장할 때, 루프가 반복될수록 DB 커넥션 숫자가 계속 증가합니다. close가 제대로 안 되는 것 같아요.

[2] (comment)
title: Re: PostgresSaver 사용 시 연결 누수 문제
content: 네, pool_size를 5로 설정했는데도 20개가 넘는 커넥션이 active 상태입니다.

[3] (comment)
title: Re: PostgresSaver 사용 시 연결 누수 문제
content: 해당 문제는 JDBC 드라이버 버전보다는 LangGraph 내부의 pool 관리 로직 문제로 보입니다. 혹시 `pool_size` 설정을 따로 하셨나요?

[4] (comment)
title: Re: Vector Store 검색 결과 중복 제거
content: `as_retriever(search_type='mmr', search_kwargs={'k': 5, 'fetch_k': 20})` 방식으로 설정하세요.

[5] (issue)
title: Vector Store 검색 결과 중복 제거
content: ChromaDB에서 검색 결과가 동일한 문서의 다른 섹션일 때 중복이 많습니다. mmr 설정을 어떻게 하나요?

[6] (issue)
title: MySQL EXPLAIN 결과 해석 요청
content: 특정 쿼리에서 MUL 키가 잡히는데 인덱스 스캔 속도가 느립니다. 실행 계획 첨부합니다.

[7] (comment)
title: Re: Docker-compose로 MySQL 8.0 환경 구성
content: MySQL 8.0부터 인증 방식이 바뀌었습니다. `command: --default-authentication-plugin=mysql_native_password` 옵션을 추가하세요.

[8] (comment)
title: Re: MySQL Isolation Level 설정 문의
content: 맞습니다. LangChain의 SQL 기반 체크포인터는 높은 동시성을 요구하므로 READ COMMITTED를 권장합니다.

[9] (issue)
title: Docker-compose로 MySQL 8.0 환경 구성
content: 제공해주신 docker-compose 파일로 실행하면 `mysql_native_password` 인증 에러가 납니다.

[10] (comment)
title: Re: LangGraph recursion_limit 초과 현상
content: `get_graph().draw_mermaid_png()`를 사용하여 로직을 먼저 확인해보세요. 의도치 않은 루프가 생성된 것 같습니다.

[11] (comment)
title: Re: H2 Database 콘솔 접속 암호 분실
content: H2는 기본적으로 암호가 없는 경우가 많습니다. 혹은 DB 파일(`.mv.db`)을 삭제하고 다시 컨테이너를 띄우면 초기화됩니다.

[12] (comment)
title: Re: LangGraph의 State Graph 업데이트 방식
content: TypedDict 정의 시 해당 필드에 `operator.add` 어노테이션을 사용하면 자동으로 리스트가 병합됩니다.

[13] (issue)
title: LangGraph의 State Graph 업데이트 방식
content: State에 리스트를 추가할 때 덮어씌워지지 않고 append 되게 하려면 어떻게 정의하나요?

[14] (issue)
title: AgentExecutor vs LangGraph 선택 기준
content: 간단한 챗봇을 만드는데 AgentExecutor를 써도 될까요? 아니면 무조건 LangGraph로 가야 하나요?

[15] (comment)
title: Re: AgentExecutor vs LangGraph 선택 기준
content: 현재 LangChain에서는 AgentExecutor를 유지보수 모드로 전환 중입니다. 새 프로젝트라면 유연성이 높은 LangGraph를 권장합니다.

[16] (issue)
title: JDBC Shop 프로젝트에서 Connection Leak
content: 교수님 과제 중인 학생인데, ConnectionUtil 클래스에서 conn.close()를 안 하면 어떤 일이 벌어지나요?

[17] (comment)
title: Re: JDBC Shop 프로젝트에서 Connection Leak
content: DB 서버의 최대 연결 수가 금방 꽉 차서 더 이상 새로운 요청을 처리할 수 없게 되어 서비스가 중단됩니다. 항상 try-with-resources를 쓰세요.

[18] (comment)
title: Re: Custom ToolNode에서 에러 핸들링
content: `set_error_handler` 인터페이스를 구현하거나, 노드 출력값에 error 메시지를 포함하여 조건부 에지로 분기 처리하는 것을 추천합니다.

[19] (comment)
title: Re: Groq API 사용 시 Context Window 초과
content: `MapReduce` 방식을 사용하여 문서를 요약한 뒤 최종 답변을 생성하거나, Llama-3-70b-8192 모델의 긴 컨텍스트 버전을 사용하세요.

[20] (issue)
title: LangGraph recursion_limit 초과 현상
content: 복잡한 조건부 에지(Conditional Edge)를 짰는데, 순환 고리에 빠져서 25회 제한에 걸립니다. 시각화 도구가 필요합니다.
"""