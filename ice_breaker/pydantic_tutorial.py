from pydantic import BaseModel, Field, EmailStr, field_validator

class User(BaseModel):
    name: str
    email: str
    age: int

    @field_validator('age')
    def check_age(cls, v):
        if v < 0:
            raise ValueError('Age must be non-negative')
        return v

user1 = User(name="John Doe", email="sdile@gmail", age=2)

user_json_str = user1.model_dump_json()

print(user_json_str)