from vectorstore import init_vectorstore, load_vector_from_local
from chain import build_report_chain

init_vectorstore()

vectorstore = load_vector_from_local()
chain = build_report_chain(vectorstore=vectorstore)

q1 = "Tool Choice 에러에 대한 리포트 작성"
result = chain.invoke(q1)

print(result['answer'])
print(result['context'])

print('='*50)

q2 = "docker-compose에서 mysql_native_password 에러에 대한 리포트 작성"
result = chain.invoke(q2)

print(result['answer'])
print(result['context'])


"""
실행결과

**Tool Choice 에러 리포트**

**1. 문제 개요**

Groq 모델을 사용하여 Tool 호출을 시도하면 'Invalid tool call' 에러가 빈번하게 발생합니다. 특히 bind_tools를 사용할 때 심하네요.

**2. 원인 분석**

Groq API 연동 시 Tool Choice 에러는 OpenAI와 Groq API의 함수 호출 형식 차이로 인한 문제로 여겨집니다.

**3. 해결 과정**

- **Groq API 연동 시 함수 호출 형식 명시**: Groq 모델을 사용하여 Tool 호출 시, prompt에 system message로 tool 사용 형식을 명시하도록 수정합니다. 예를 들어, "Tool: <tool_name>을 사용하세요."

**4. 최종 해결 방법**

Groq API 연동 시 Tool Choice 에러는 Groq API의 함수 호출 형식 명시를 통해 해결할 수 있습니다. 이 방법을 적용하면 'Invalid tool call' 에러가 발생하는 문제를 해결할 수 있습니다.

**참고**

- [4] (comment): Groq은 현재 function calling 형식이 OpenAI와 미세하게 다릅니다. prompt에 system message로 tool 사용 형식을 명시해보세요.
- [1] (issue): Groq 모델을 사용하여 Tool 호출을 시도하면 'Invalid tool call' 에러가 빈번하게 발생합니다. 특히 bind_tools를 사용할 때 심하네요.
[1] (issue)
title: Groq API 연동 시 Tool Choice 에러
content: Groq 모델을 사용하여 Tool 호출을 시도하면 'Invalid tool call' 에러가 빈번하게 발생합니다. 특히 bind_tools를 사용할 때 심하네요.

[2] (issue)
title: Custom ToolNode에서 에러 핸들링
content: ToolNode 실행 중 예외가 발생하면 전체 그래프가 멈춥니다. try-except 없이 노드 수준에서 핸들링하는 방법이 있나요?

[3] (issue)
title: 한국어 프롬프트 템플릿 최적화 제안
content: 번역 툴을 만들 때 한국어 조사가 깨지는 현상이 있습니다. Few-shot 예제를 한국어로 구성했을 때 성능이 훨씬 좋습니다.

[4] (comment)
title: Re: Groq API 연동 시 Tool Choice 에러
content: Groq은 현재 function calling 형식이 OpenAI와 미세하게 다릅니다. prompt에 system message로 tool 사용 형식을 명시해보세요.

[5] (comment)
title: Re: Custom ToolNode에서 에러 핸들링
content: `set_error_handler` 인터페이스를 구현하거나, 노드 출력값에 error 메시지를 포함하여 조건부 에지로 분기 처리하는 것을 추천합니다.

[6] (comment)
title: Re: Groq API 사용 시 Context Window 초과
content: `MapReduce` 방식을 사용하여 문서를 요약한 뒤 최종 답변을 생성하거나, Llama-3-70b-8192 모델의 긴 컨텍스트 버전을 사용하세요.

====================================

**문제 개요**

Docker-compose로 MySQL 8.0 환경을 구성했을 때 `mysql_native_password` 인증 에러가 발생하는 문제에 대해 해결 방법을 찾습니다.

**원인 분석**

참고 문서 [1]에서 제공된 내용에 따르면, MySQL 8.0부터 인증 방식이 바뀌어 `mysql_native_password` 인증 에러가 발생할 수 있습니다.

**해결 과정**

참고 문서 [4]의 댓글을 통해 `command: --default-authentication-plugin=mysql_native_password` 옵션을 추가하면 인증 에러를 해결할 수 있습니다.

**최종 해결 방법**

Docker-compose 파일에 `command: --default-authentication-plugin=mysql_native_password` 옵션을 추가하여 MySQL 8.0 환경을 구성하면 `mysql_native_password` 인증 에러가 해결됩니다.

```yml
version: '3'
services:
  mysql:
    image: mysql:8.0
    command: --default-authentication-plugin=mysql_native_password
    # ... (나머지 설정)
```

이 방법으로 MySQL 8.0 환경을 구성할 수 있습니다.
[1] (issue)
title: Docker-compose로 MySQL 8.0 환경 구성
content: 제공해주신 docker-compose 파일로 실행하면 `mysql_native_password` 인증 에러가 납니다.

[2] (issue)
title: H2 Database 콘솔 접속 암호 분실
content: Docker로 띄운 H2 데이터베이스의 sa 계정 암호를 잊어버렸습니다. 초기화 방법이 있나요?

[3] (issue)
title: MySQL Isolation Level 설정 문의
content: 프로젝트에서 트랜잭션 격리 수준을 REPEATABLE READ로 쓰고 있는데, 체크포인트 저장 시 데드락이 발생합니다. READ COMMITTED가 권장되나요?

[4] (comment)
title: Re: Docker-compose로 MySQL 8.0 환경 구성
content: MySQL 8.0부터 인증 방식이 바뀌었습니다. `command: --default-authentication-plugin=mysql_native_password` 옵션을 추가하세요.

[5] (comment)
title: Re: MySQL Isolation Level 설정 문의
content: 맞습니다. LangChain의 SQL 기반 체크포인터는 높은 동시성을 요구하므로 READ COMMITTED를 권장합니다.

[6] (comment)
title: Re: H2 Database 콘솔 접속 암호 분실
content: H2는 기본적으로 암호가 없는 경우가 많습니다. 혹은 DB 파일(`.mv.db`)을 삭제하고 다시 컨테이너를 띄우면 초기화됩니다.
"""