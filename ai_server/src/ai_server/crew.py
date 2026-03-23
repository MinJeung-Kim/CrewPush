import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List 

@CrewBase
class NewsBriefingCrew:
    """뉴스 브리핑 생성 Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
 
    # ---- vLLM 직접 설정 추가 ---- 

    custom_llm = LLM(
        model=os.environ.get("MODEL"),
        base_url=os.environ.get("OPENAI_API_BASE"),
        api_key=os.environ.get("OPENAI_API_KEY")
    ) 

    # ---- Agent 정의 ----

    @agent
    def researcher(self) -> Agent:
        return Agent( 
            config=self.agents_config["researcher"],  # YAML에서 CrewBase가 자동으로 읽어옴
            tools=[SerperDevTool()],                  # 도구는 코드에서 주입
            verbose=True,
            llm=self.custom_llm
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # YAML에서 CrewBase가 자동으로 읽어옴
            verbose=True,
            llm=self.custom_llm
        )

    # ---- Task 정의 ----

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # YAML에서 CrewBase가 자동으로 읽어옴
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'], # YAML에서 CrewBase가 자동으로 읽어옴
            context=[self.research_task()],             # research_task 결과 참고
        )

    # ---- Crew 정의 ----

    @crew
    def crew(self) -> Crew: 
        return Crew(
            agents=self.agents, # @agent 데코레이터로 자동 수집
            tasks=self.tasks, # @task 데코레이터로 자동 수집
            process=Process.sequential,
            verbose=True,
        )
