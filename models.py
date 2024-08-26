from pydantic import BaseModel, Field


class Mushroom(BaseModel):
    mushroom_id: int
    title: str = Field(default=..., description="Название гриба")
    edibility: bool = Field(default=..., description="Съедобность гриба")
    weight: float = Field(default=..., ge=0.0, description="Съедобность гриба")
    freshness: int = Field(default=..., description="Свежесть (в днях с момента сбора) гриба")
    special_notes: str = Field(default=..., max_length=500, description="Особые заметки о грибе в формате до 500 символов")


class Basket(BaseModel):
    basket_id: int
    owner: str = Field(default=..., description="Имя владельца корзинки")
    capacity: int = Field(default=..., description="Вместительность корзинки в граммах")
    mushrooms: list = Field(default=[], description="Список ID грибов из корзинки")


class Basket_for_post(BaseModel):
    owner: str = Field(default=..., description="Имя владельца корзинки")
    capacity: int = Field(default=..., description="Вместительность корзинки в граммах")
    mushrooms: list[int] = Field(default=[], description="Список ID грибов из корзинки")


class Mushroom_to_add(BaseModel):
    mushroom_id: int
    basket_id: int