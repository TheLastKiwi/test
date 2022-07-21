from pydantic import BaseModel


class SomePostRequest(BaseModel):
    id: int