from pydantic import BaseModel, Field


class AuthorsRequest(BaseModel):
    name: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    born_year: int = Field(gt=1000, lt=2030)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Author 1",
                "description": "Description 1",
                "born_year": 1890
            }
        }
    }
