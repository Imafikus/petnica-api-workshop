from pydantic import BaseModel
from typing import List

class Person(BaseModel):
    id: int 
    name: str 
    surname: str 
    status: str
    
class Course(BaseModel):
    people: List[Person] = []