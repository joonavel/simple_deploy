from typing import Annotated, TypedDict
from task import create_target_number, check_answer, calculate_diff


class GraphState(TypedDict):
    user_question: int  # 사용자의 질문
    ask_user: int # 사용자에게 추가 질문을 할지 여부
    leading_question: str # 사용자의 대답을 이끌어 내기 위한 모델의 질문
    user_answer: int # leading_question에 대한 사용자의 답
    target: int # 사용자가 맞추어야 하는 값
    
    
def target_number_creation(state: GraphState):
    state["target"] = create_target_number()
    return state

def answer_checking(state: GraphState):
    user_answer = state.get("user_answer", state["user_question"])
    state["ask_user"] = 0 if check_answer(user_answer, state["target"]) else 1
    return state

def diff_calculation(state: GraphState):
    user_answer = state.get("user_answer", state["user_question"])
    state["leading_question"] = str(calculate_diff(user_answer, state["target"])) + "의 차이가 납니다. 어떤 수일까요?"
    return state

def human_interaction(state: GraphState):
    return state

def router(state: GraphState):
    if state["ask_user"]:
        return "HUMAN"
    else:
        print("정답입니다.")
        return "KEEP"