## Basis Crew
### 프로젝트 개요
Basis Crew는 CrewAI 프레임워크 기반의 멀티 에이전트 AI 뉴스 브리핑 자동화 시스템입니다. 사용자가 입력한 주제에 대해, 여러 에이전트가 협력하여 최신 뉴스를 수집·정리하고, 읽기 쉬운 브리핑을 자동으로 생성합니다.

### 폴더 구조
```
basis/
├── src/
│   └── basis/
│       ├── crew.py         # 에이전트/태스크/크루 정의
│       ├── flow.py         # 전체 뉴스 브리핑 플로우 정의
│       ├── main.py         # 실행 진입점
│       ├── config/
│       │   ├── agents.yaml # 에이전트 역할/목표/배경 정의
│       │   └── tasks.yaml  # 태스크 설명/출력/담당 에이전트 정의
│       └── tools/
│           └── custom_tool.py # 커스텀 도구 예시
├── outputs/                # 결과물 저장 폴더 (직접 생성 필요)
├── README.md
├── .gitignore
└── pyproject.toml
```

### 주요 동작 방식
1. 에이전트/태스크/크루 정의 (crew.py, agents.yaml, tasks.yaml)
   - `agents.yaml`: researcher(뉴스 수집), writer(브리핑 작성) 등 역할/목표/배경 정의
   - `tasks.yaml`: research_task(뉴스 정리), writing_task(브리핑 작성) 등 태스크 설명 및 담당 에이전트 지정
   - `crew.py`: 위 설정을 바탕으로 실제 Agent, Task, Crew 객체를 생성
2. 전체 플로우 (flow.py)
   - `BriefingState`: 주제, 브리핑 결과, 재시도 횟수 등 상태 관리
   - `NewsBriefingFlow`:
      - **prepare**: 주제 출력
      - **run_crew**: Crew 실행(뉴스 수집 및 브리핑)
      - **check_quality**: 브리핑 길이(100자 이상) 검사, 부족하면 최대 3회까지 재시도
      - **save_result**: 성공 시 briefing.md 저장
      - **handle_retry/handle_give_up**: 재시도/실패 처리
3. 실행 진입점 (main.py)
   - 사용자에게 주제 입력받아 Flow 실행
   - 최종 브리핑 결과 출력
4. 커스텀 도구 예시 (tools/custom_tool.py)
   - BaseTool을 상속받아 에이전트가 사용할 수 있는 커스텀 도구 구현 가능

### 실행 방법
1. Python 3.10~3.13 환경 준비
2. 의존성 설치
    ```bash
    pip install uv
    python -m venv .venv
    .venv\Scripts\activate # 가상환경 활성화
    crewai install
    ```
3. 환경변수(.env)에 OPENAI_API_KEY 등 입력
4. 프로젝트 루트에서 실행
    ```bash
    python -m ai_server.main
    ```
5. 주제 입력 → 자동 뉴스 브리핑 생성

### 결과물 저장
- 브리핑 결과는 기본적으로 briefing.md로 저장됩니다.
- outputs/ 폴더를 만들어 그 안에 저장하도록 커스터마이징할 수 있습니다.

### 커스터마이징 포인트
- `config/agents.yaml`, `config/tasks.yaml`에서 역할/태스크 자유롭게 추가·수정
- `crew.py`에서 도구(tool) 및 LLM 설정 변경 가능
- `tools/`에 커스텀 도구 추가 가능
- Flow 구조를 확장해 다양한 자동화 시나리오 구현 가능

### 기타
- .gitignore에 outputs/ 등 결과물 폴더 추가 권장
- 동적 에이전트/태스크 생성, 프롬프트 엔지니어링 등 고급 기능도 적용 가능