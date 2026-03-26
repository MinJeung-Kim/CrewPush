#!/usr/bin/env python
"""
CrewAI Training 테스트용 main.py

사용법:
  일반 실행:  python main.py run
  CLI 학습:   crewai train -n 2 my_model.pkl
  코드 학습:  python main.py train
  pkl 확인:   python main.py show
"""
import sys
import pickle
import json
from datetime import datetime


# -------------------------------------------------------
# 공통 inputs
# -------------------------------------------------------
def get_inputs() -> dict:
    topic = input("topic을 입력하세요: ")
    return {
        "topic": topic,
        "current_year": str(datetime.now().year),
    }



# -------------------------------------------------------
# 1. 일반 실행
# -------------------------------------------------------
def run():
    """학습 없이 crew 를 그냥 실행"""
    from .crew import MyTrainingCrew

    try:
        result = MyTrainingCrew().crew().kickoff(inputs=get_inputs())
        print(result)
    except Exception as e:
        raise Exception(f"실행 중 오류 발생: {e}")


# -------------------------------------------------------
# 2-A. Training — CLI 방식에서 호출되는 함수
#       crewai train -n 2 my_model.pkl
#       → 내부적으로 uv run train 2 my_model.pkl 호출
#       → pyproject.toml 의 [scripts] train = "main:train" 로 연결됨
# -------------------------------------------------------
def train():
    """CLI 방식: crewai train -n <n> <filename> 으로 호출됨"""
    from .crew import MyTrainingCrew

    try:
        MyTrainingCrew().crew().train(
            n_iterations=int(sys.argv[1]),  # crewai train -n 2  → sys.argv[1] = "2"
            filename=sys.argv[2],           # crewai train -n 2 my_model.pkl → sys.argv[2]
            inputs=get_inputs() ,
        )
    except Exception as e:
        raise Exception(f"Training 중 오류 발생: {e}")


# -------------------------------------------------------
# 2-B. Training — 코드 방식으로 직접 실행
#       python main.py train_code
# -------------------------------------------------------
def train_code():
    """코드 방식: python main.py train_code 로 직접 실행"""
    from .crew import MyTrainingCrew

    n_iterations = 2          # 반복 횟수
    filename = "trained_agents_data.pkl" # 저장할 파일명 (.pkl 필수)

    try:
        MyTrainingCrew().crew().train(
            n_iterations=n_iterations,
            filename=filename,
            inputs=get_inputs() ,
        )
        print(f"\n✅ Training 완료! → {filename} 저장됨")
    except Exception as e:
        raise Exception(f"Training 중 오류 발생: {e}")


# -------------------------------------------------------
# 3. pkl 파일 내용 확인
#    python main.py show
#    python main.py show my_model.pkl        (최종 결과)
#    python main.py show training_data.pkl   (raw 중간 데이터)
# -------------------------------------------------------
def show():
    """저장된 pkl 파일 내용을 사람이 읽기 쉽게 출력"""
    filename = sys.argv[2] if len(sys.argv) > 2 else "my_model.pkl"

    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)

        if not data:
            print(f"📭 {filename} 이 비어있습니다.")
            return

        print(f"\n📦 [{filename}] 내용\n{'=' * 50}")
        print(json.dumps(data, ensure_ascii=False, indent=2))

    except FileNotFoundError:
        print(f"❌ {filename} 파일이 없습니다. 먼저 training 을 실행하세요.")
    except Exception as e:
        print(f"❌ 파일 읽기 오류: {e}")


# -------------------------------------------------------
# 진입점
# -------------------------------------------------------
COMMANDS = {
    "run":        run,
    "train":      train,        # CLI 방식 (crewai train 에서 호출)
    "train_code": train_code,   # 코드 방식 (python main.py train_code)
    "show":       show,         # pkl 내용 확인
}

if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "run"

    if command not in COMMANDS:
        print(f"사용법: python main.py [{' | '.join(COMMANDS.keys())}]")
        sys.exit(1)

    COMMANDS[command]()