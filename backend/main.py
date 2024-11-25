from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)