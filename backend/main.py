from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from graph import make_graph
from utils import get_runnable_config

app = FastAPI()

workflow = make_graph()
print("LLM WORKFLOW STARTED.")

class CustomerInfo(BaseModel):
    customer_name: str
    customer_age: int
    customer_gender: str
    customer_address: str

@app.post("/process_customer")
def process_customer(customer: CustomerInfo):
    # 나이에 10을 더함
    processed_info = customer.model_dump()
    processed_info['customer_age'] += 10
    return processed_info

class LLMWorkflowInput(BaseModel):
    user_question: int
    initial_question: int
    thread_id: str
    last_snapshot_values: dict | None


@app.post("/llm_workflow")
def llm_workflow(workflow_input: LLMWorkflowInput):
    processed_input = workflow_input.model_dump()
    config = get_runnable_config(30, processed_input["thread_id"])
    
    inputs = {"user_question": processed_input["user_question"]}
    # 초기 질문이 아닌 경우
    if processed_input["initial_question"] == 0:
        values = processed_input["last_snapshot_values"]
        values.update({"user_answer": processed_input["user_question"]})
        workflow.update_state(
            config,
            values,
            "diff_calculation",
        )
        outputs = workflow.invoke(input=None,
                                  config=config,
                                  interrupt_before=["human_interaction"],
                                  )
    else: # 초기 질문인 경우
        # TODO
        # 첫 번째 초기질문은 잘 작동하나 두번째 초기질문에서 GraphState가 초기화되지 않는 문제 발생
        outputs = workflow.invoke(input=inputs,
                                  config=config,
                                  interrupt_before=["human_interaction"],
                                  )
    return outputs


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)