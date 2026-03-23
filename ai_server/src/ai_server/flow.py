import os
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from .crew import NewsBriefingCrew


# ① State 정의 — Pydantic으로 타입 보장
class BriefingState(BaseModel):
    topic: str = ""
    briefing: str = ""
    retry_count: int = 0


# ② Flow 정의
class NewsBriefingFlow(Flow[BriefingState]):

    @start()
    def prepare(self):
        print(f"[시작] 주제: {self.state.topic}")

    @listen(prepare)
    def run_crew(self):
        print("[Crew 실행 중...]")
        result = (
            NewsBriefingCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic})
        )
        self.state.briefing = result.raw

    @router(run_crew)
    def check_quality(self):
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
        print("[저장 완료] outputs/briefing.md")
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)  # 폴더가 없으면 생성
        with open(os.path.join(output_dir, "briefing.md"), "w", encoding="utf-8") as f:
            f.write(self.state.briefing)
        return self.state.briefing

    @listen("retry")
    def handle_retry(self):
        self.run_crew()

    @listen("give_up")
    def handle_give_up(self):
        print("[실패] 3번 재시도 후 품질 미달")
        return "브리핑 생성 실패"

 