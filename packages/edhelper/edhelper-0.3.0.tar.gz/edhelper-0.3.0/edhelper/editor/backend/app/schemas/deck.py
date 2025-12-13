from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .deck_cards import FullDeckCards


class Deck(BaseModel):
    name: str

    class Config:
        from_attributes = True


class DeckCreate(Deck):
    commander: Optional[str] = None


class DeckUpdate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class DeckInDB(Deck):
    id: int
    last_update: datetime


class DeckList(BaseModel):
    decks: list[DeckInDB]

    class Config:
        from_attributes = True


class CompleteDeckRead(DeckInDB):
    cards: List[FullDeckCards]
