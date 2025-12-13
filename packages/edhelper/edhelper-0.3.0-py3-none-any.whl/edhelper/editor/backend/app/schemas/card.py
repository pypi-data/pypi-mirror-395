from typing import List, Optional
from pydantic import BaseModel, field_validator


class Card(BaseModel):
    id: str
    name: str
    colors: str
    color_identity: str
    cmc: int
    mana_cost: Optional[str] = ""
    image: Optional[str] = ""
    art: Optional[str] = ""
    legal_commanders: bool
    is_commander: bool
    price: str
    edhrec_rank: Optional[int] = None
    type_line: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator("price", mode="before")
    def fix_price(cls, v):
        if v is None:
            return "R$0,00"
        return str(v)


class CardList(BaseModel):
    cards: List[Card]


class Commander(Card):
    commander_rank: int

    @field_validator("commander_rank", mode="before")
    def fix_rank(cls, v):
        return v + 1


class CommanderList(BaseModel):
    cards: List[Commander]


class SetCommander(BaseModel):
    card_id: str

    class config:
        from_attributes = True
