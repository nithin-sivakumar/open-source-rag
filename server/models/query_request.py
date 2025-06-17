from pydantic import BaseModel


class QueryRequest(BaseModel):
    user_input: str
    session: str
