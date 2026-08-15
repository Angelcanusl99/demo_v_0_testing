from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str


class config:
    from_attributes = True


class PrototypeBase(BaseModel):
    model_name: str
    engine_type: str
    horsepower: int
    weight: float


class PrototypeCreate(PrototypeBase):
    pass


class PrototypeResponse(PrototypeBase):
    id: int

    class config:
        from_attributes = True
