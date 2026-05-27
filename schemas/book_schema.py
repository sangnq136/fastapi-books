from typing import Optional
from pydantic import BaseModel, Field, model_validator


class BooksRequest(BaseModel):
    title: str = Field(min_length=3)

    author_id: Optional[int] = None
    author_name: Optional[str] = None
    author_born_year: Optional[int] = None

    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_year: int = Field(gt=1999, lt=2030)

    @model_validator(mode="after")
    def validate_author_fields(self):
        if self.author_id and self.author_name:
            raise ValueError("Provide either author_id or author_name")

        if not self.author_id and not self.author_name:
            raise ValueError("author_id or author_name required")

        if self.author_name and not self.author_born_year:
            raise ValueError("author_born_year required")

        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book Title 1",
                # "author_id": 1,
                "author_name": "Shelby",
                "author_born_year": 1890,
                "description": "Description 1",
                "rating": 5,
                "published_year": 2000
            }
        }
    }