from pydantic import BaseModel


class HelloInput(BaseModel):
    name: str


class HelloOutput(BaseModel):
    text: str


def say_hello(input: HelloInput) -> HelloOutput:
    return HelloOutput(text=f"Hello, {input.name}!")


class GoodbyeInput(BaseModel):
    name: str


class GoodbyeOutput(BaseModel):
    text: str


def say_goodbye(input: GoodbyeInput) -> GoodbyeOutput:
    return GoodbyeOutput(text=f"Goodbye, {input.name}!")
