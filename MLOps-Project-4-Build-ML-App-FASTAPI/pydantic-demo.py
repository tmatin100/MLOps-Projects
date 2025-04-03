# Pydantic is a parsing library.
# It garuantess the types and constraints of the output model.
# Can also be used for custom valiations. 

# In relation to the ML Model Deployment
# - Data received from other clients might not alwasy be in the format that the model expects.
# - Pydantic ensures that data will be in the correct format before we perform prediction. 

# pip install pydantic
from pydantic import BaseModel

# passing the required data 
data = {
    "name": "Murthy",
    "age": "28",
    "course": "MLOps BootCamp",
    "ratings": [4, 4, "4", "5", 4]
}

# creating a class that inherits the base model and passing expected data types
class Instructor(BaseModel):
    name: str
    age: int
    course: str
    ratings: list[int] = []

# passing data in the Instructor class which uses pydantic BaseModel
user = Instructor(**data) 
print(f"Found a Instructor: {user}")


