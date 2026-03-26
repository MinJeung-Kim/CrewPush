from .crew import NewsBriefingCrew

n_iterations = 3
filename = "my_model.pkl"
inputs = {"topic": "AWS Security"}   # crew에 넘길 입력값

crew_instance = NewsBriefingCrew()

try:
    crew_instance.crew().train(
        n_iterations=n_iterations,
        filename=filename,
        inputs=inputs
    )
except Exception as e:
    raise Exception(f"Training 실패: {e}")