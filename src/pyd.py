from pydantic import BaseModel, ValidationError # pup install pydantic

class Address(BaseModel):
    city: str
    country: str = ""

class Person(BaseModel):
    name: str
    age: float
    address: Address
    
# p = MyType(name="nadav", age="20")
# result = p.model_dump() # from MyType into dict
# result = p.model_dump_json() # from MyType into JSON string
p1 = Person.model_validate({"name": "nadav", "age": "20.7", "address": {"city": "haifa"}}) # from dict into MyType object
# p2 = MyType.model_validate_json('{"name": "nadav", "age": "20.7"}') # from string JSON into MyType object

try:
    p1 = Person.model_validate({"name": "nadav", "age": "20.7"}) # from dict into MyType object
    p2 = Person.model_validate_json('{"name": "nadav", "age": "20.7"}') # from string JSON into MyType object
except ValidationError as err:
    print(err.errors())