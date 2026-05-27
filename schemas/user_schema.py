from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class ChangePhoneRequest(BaseModel):
    phone_number: str = Field(min_length=5)
