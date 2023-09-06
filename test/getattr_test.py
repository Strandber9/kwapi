from dataclasses import dataclass


@dataclass
class Person:
    name: str
    age: int
    city: str

    def __getitem__(self, key):
        return getattr(self, key)


# 예제 dict
data = {"name": "John", "age": 30, "city": "New York"}

# 객체 생성
person_obj = Person(**data)

# 객체를 dict처럼 사용
print(person_obj["name"])
