# Try to implement spec with strawberry

import strawberry

@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self, info) -> User:
        return User(name="Patrick", age=100)


schema = strawberry.Schema(query=Query)
