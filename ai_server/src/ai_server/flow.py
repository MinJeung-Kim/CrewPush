import os
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from .crew import NewsBriefingCrew

class BriefingState(BaseModel):
    topic: str = ""
    briefing: str = ""
    retry_count: int = 0
    memory: dict = {}  # state 기반 memory 필드 추가
class NewsBriefingFlow(Flow[BriefingState]):
    @start()
    def prepare(self):
        print(f"[시작] 주제: {self.state.topic}")
        # state.memory에 값 저장 예시
        self.state.memory['prepare_called'] = True
        self.state.memory['topics_seen'] = self.state.memory.get('topics_seen', []) + [self.state.topic]

    @listen(prepare)
    def run_crew(self):
        print("[Crew 실행 중...]")
        streaming = (
            NewsBriefingCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic})
        )
        full_result = ""
        for chunk in streaming:
            print(chunk.content, end="", flush=True)
            full_result += chunk.content
        print('최종 결과 출력 = ', full_result)  # 최종 결과 출력
        self.state.briefing = full_result
        # state.memory에 결과 저장 예시
        self.state.memory['last_briefing'] = full_result

    @router(run_crew)
    def check_quality(self):
        # memory에서 값 읽기 예시
        print(f"[메모리] 이전에 본 토픽들: {self.state.memory.get('topics_seen')}")
        print(f"[메모리] 마지막 브리핑: {self.state.memory.get('last_briefing', '')[:30]}...")
        if len(self.state.briefing) >= 100:
            print(f"[품질 OK] {len(self.state.briefing)}자")
            return "good"

        self.state.retry_count += 1
        print(f"[품질 미달] {self.state.retry_count}번째 재시도")

        if self.state.retry_count >= 3:
            return "give_up"
        return "retry"

    @listen("good")
    def save_result(self):
        # 항상 프로젝트 루트 기준 outputs/briefing.md에 저장
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        output_dir = os.path.join(base_dir, "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "briefing.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.state.briefing)
        print(f"[저장 완료] {output_path}")
        return self.state.briefing

    @listen("retry")
    def handle_retry(self):
        self.run_crew()

    @listen("give_up")
    def handle_give_up(self):
        print("[실패] 3번 재시도 후 품질 미달")
        return "브리핑 생성 실패"

 