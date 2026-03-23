from dotenv import load_dotenv
from src.ai_server.flow import NewsBriefingFlow

load_dotenv()


def main():
    topic = input("브리핑 주제를 입력하세요: ") or "AI 반도체"

    flow = NewsBriefingFlow()
    # flow.plot()
    result = flow.kickoff(inputs={"topic": topic})

    print("\n" + "=" * 50)
    print("최종 브리핑")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()