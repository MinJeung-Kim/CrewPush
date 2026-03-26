import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class MyTrainingCrew:
    """Training 테스트용 Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

     # ---- vLLM 직접 설정 추가 ---- 
    # 커스텀 LLM을 클래스 변수로 정의하여 모든 Agent에서 공유하도록 설정
    custom_llm = LLM(
        model=os.environ.get("MODEL"),
        base_url=os.environ.get("OPENAI_API_BASE"),
        api_key=os.environ.get("OPENAI_API_KEY")
    ) 

    # -------------------------
    # Agents
    # -------------------------
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            llm=self.custom_llm,
            verbose=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],  # type: ignore[index]
            llm=self.custom_llm,
            verbose=True,
        )

    # -------------------------
    # Tasks
    # -------------------------
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
            # human_input: true 는 tasks.yaml 에서 설정
            # 여기서 중복 설정해도 무방 → yaml 값이 config 로 들어옴
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],  # type: ignore[index]
            output_file="report.md",
        )

    # -------------------------
    # Crew
    # -------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )