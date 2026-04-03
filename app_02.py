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
1. 주요 문제 유형
- 문제 유형: DB 커넥션 누수
- 발생 원인:
  - PostgresSaver의 pool 관리 로직 문제
  - JDBC 드라이버 버전 문제 여부
  - LangGraph 내부의 pool_size 설정 미흡
- 해결 방법:
  - LangGraph 내부의 pool 관리 로직 수정
  - JDBC 드라이버 버전 업그레이드
  - pool_size 설정 반영 및 최적화

- 문제 유형: JDBC 드라이버 버전 문제
- 발생 원인: JDBC 드라이버 버전 문제로 인한 커넥션 누수
- 해결 방법:
  - JDBC 드라이버 버전 업그레이드
  - LangGraph 내부의 JDBC 드라이버 버전 호환성 확인

- 문제 유형: DB 트랜잭션 격리 수준 설정
- 발생 원인: 트랜잭션 격리 수준이 높을 경우 데드락 발생
- 해결 방법:
  - 트랜잭션 격리 수준을 READ COMMITTED로 설정

2. 반복적으로 발생하는 실수
- 실수: JDBC 드라이버 버전 미흡으로 인한 커넥션 누수
- 실수: LangGraph 내부의 pool_size 설정 미흡으로 인한 커넥션 누수
- 실수: 트랜잭션 격리 수준 설정에 대한 무지

3. 설정 및 사용 시 주의사항
- PostgresSaver 설정:
  - pool_size 설정 반영 및 최적화
  - LangGraph 내부의 pool 관리 로직 확인
- JDBC 드라이버 설정:
  - JDBC 드라이버 버전 업그레이드
  - LangGraph 내부의 JDBC 드라이버 버전 호환성 확인
- DB 트랜잭션 격리 수준 설정:
  - 트랜잭션 격리 수준을 READ COMMITTED로 설정

4. 베스트 프랙티스 체크리스트
- PostgresSaver 사용 시:
  - pool_size를 적절하게 설정하세요.
  - LangGraph 내부의 pool 관리 로직을 확인하세요.
- JDBC 드라이버 버전 업그레이드:
  - JDBC 드라이버 버전을 최신으로 업데이트 하세요.
  - LangGraph 내부의 JDBC 드라이버 버전 호환성을 확인하세요.
- 트랜잭션 격리 수준 설정:
  - 트랜잭션 격리 수준을 READ COMMITTED로 설정하세요.
[1] (issue)
title: PostgresSaver 사용 시 연결 누수 문제
content: LangGraph에서 PostgresSaver를 사용하여 체크포인트를 저장할 때, 루프가 반복될수록 DB 커넥션 숫자가 계속 증가합니다. close가 제대로 안 되는 것 같아요.

[2] (comment)
title: Re: PostgresSaver 사용 시 연결 누수 문제
content: 네, pool_size를 5로 설정했는데도 20개가 넘는 커넥션이 active 상태입니다.

[3] (comment)
title: Re: PostgresSaver 사용 시 연결 누수 문제
content: 해당 문제는 JDBC 드라이버 버전보다는 LangGraph 내부의 pool 관리 로직 문제로 보입니다. 혹시 `pool_size` 설정을 따로 하셨나요?

[4] (issue)
title: MySQL EXPLAIN 결과 해석 요청
content: 특정 쿼리에서 MUL 키가 잡히는데 인덱스 스캔 속도가 느립니다. 실행 계획 첨부합니다.

[5] (comment)
title: Re: Vector Store 검색 결과 중복 제거
content: `as_retriever(search_type='mmr', search_kwargs={'k': 5, 'fetch_k': 20})` 방식으로 설정하세요.

[6] (issue)
title: Vector Store 검색 결과 중복 제거
content: ChromaDB에서 검색 결과가 동일한 문서의 다른 섹션일 때 중복이 많습니다. mmr 설정을 어떻게 하나요?

[7] (comment)
title: Re: JDBC Shop 프로젝트에서 Connection Leak
content: DB 서버의 최대 연결 수가 금방 꽉 차서 더 이상 새로운 요청을 처리할 수 없게 되어 서비스가 중단됩니다. 항상 try-with-resources를 쓰세요.

[8] (issue)
title: MySQL Isolation Level 설정 문의
content: 프로젝트에서 트랜잭션 격리 수준을 REPEATABLE READ로 쓰고 있는데, 체크포인트 저장 시 데드락이 발생합니다. READ COMMITTED가 권장되나요?

[9] (comment)
title: Re: Docker-compose로 MySQL 8.0 환경 구성
content: MySQL 8.0부터 인증 방식이 바뀌었습니다. `command: --default-authentication-plugin=mysql_native_password` 옵션을 추가하세요.

[10] (comment)
title: Re: MySQL Isolation Level 설정 문의
content: 맞습니다. LangChain의 SQL 기반 체크포인터는 높은 동시성을 요구하므로 READ COMMITTED를 권장합니다.

[11] (issue)
title: Docker-compose로 MySQL 8.0 환경 구성
content: 제공해주신 docker-compose 파일로 실행하면 `mysql_native_password` 인증 에러가 납니다.

[12] (comment)
title: Re: LangGraph recursion_limit 초과 현상
content: `get_graph().draw_mermaid_png()`를 사용하여 로직을 먼저 확인해보세요. 의도치 않은 루프가 생성된 것 같습니다.
"""