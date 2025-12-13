from pydantic import BaseModel
from .card import Card


class DeckCards(BaseModel):
    deck_id: int
    card_id: str
    quantidade: int
    is_commander: bool


class FullDeckCards(BaseModel):
    card: Card
    quantidade: int
    is_commander: bool


class DeckQuantity(BaseModel):
    card_id: str
    quantidade: int
