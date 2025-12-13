from typing import Union
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from io import BytesIO, StringIO
from edhelper.domain import card_service
from edhelper.editor.backend.app.schemas.card import SetCommander
from edhelper.domain.deck import Deck
from edhelper.domain.deck_card import DeckCard
import edhelper.domain.deck_service as deck_service
import edhelper.domain.deck_card_service as deck_card_service
from edhelper.commom.excptions import (
    CardNotFound,
    DeckNotFound,
    DeckAlreadyExists,
    CardNotOnDeck,
    CardIsCommander,
    ShortPartial,
    InvalidQuantity,
)
from edhelper.external.api import get_many_cards_from_api
import csv
import json
import zipfile
import re

from edhelper.editor.backend.app.schemas.deck import (
    CompleteDeckRead,
    DeckCreate,
    DeckInDB,
    DeckList,
    DeckUpdate,
)
from edhelper.editor.backend.app.schemas.deck_cards import DeckQuantity, FullDeckCards

router = APIRouter(prefix="/api/decks", tags=["deck"])


def convert_exception_to_http(e: Exception) -> HTTPException:
    if isinstance(e, CardNotFound):
        return HTTPException(status_code=404, detail=e.message)
    elif isinstance(e, DeckNotFound):
        return HTTPException(status_code=404, detail=e.message)
    elif isinstance(e, DeckAlreadyExists):
        return HTTPException(status_code=400, detail=e.message)
    elif isinstance(e, CardNotOnDeck):
        return HTTPException(status_code=404, detail=e.message)
    elif isinstance(e, CardIsCommander):
        return HTTPException(status_code=400, detail=e.message)
    elif isinstance(e, ShortPartial):
        return HTTPException(status_code=400, detail=e.message)
    elif isinstance(e, InvalidQuantity):
        return HTTPException(status_code=400, detail=e.message)
    return None


@router.get("/", response_model=DeckList)
def list_decks():
    try:
        decks = deck_service.get_decks()
        return DeckList(decks=decks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}", response_model=CompleteDeckRead)
def get_deck(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        assert deck.name is not None, "Deck should have a name"
        deck, deck_cards = deck_card_service.get_deck_data_by_name(deck.name)

        return {
            "name": deck.name,
            "id": deck.id,
            "last_update": deck.last_update,
            "cards": deck_cards,
        }
    except HTTPException:
        raise
    except (CardNotFound, DeckNotFound) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=DeckInDB, status_code=201)
def create_deck(new_deck: DeckCreate):
    try:
        deck = deck_service.get_deck_by_name(new_deck.name)
        if deck:
            raise DeckAlreadyExists(new_deck.name)

        deck = Deck(name=new_deck.name)
        deck.update()
        if new_deck.commander:
            card = card_service.get_card_by_name(new_deck.commander)
            deck = deck_service.create_deck_with_cards(
                new_deck.name, [{"card": card, "quantidade": 1}]
            )
        else:
            deck = deck_service.create_deck(deck)
        return deck
    except HTTPException:
        raise
    except (DeckAlreadyExists, CardNotFound) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id}", response_model=DeckInDB)
def rename_deck(id: int, data: DeckUpdate):
    try:
        deck = deck_service.get_deck_by_id(id)
        dest = deck_service.get_deck_by_name(data.name)
        if dest:
            raise DeckAlreadyExists(data.name)
        assert deck.name is not None, "Deck should have a name"
        deck_service.rename_deck(deck.name, data.name)
        return deck_service.get_deck_by_name(data.name)
    except HTTPException:
        raise
    except (DeckNotFound, DeckAlreadyExists) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}", status_code=204)
def delete_deck(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        assert deck.name is not None, "Deck should have a name"
        deck_service.delete_deck(deck.name)
        return
    except HTTPException:
        raise
    except DeckNotFound as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/copy", response_model=DeckInDB, status_code=201)
def copy_deck(id: int, dest: DeckUpdate):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        assert deck.name is not None, "Deck should have a name"
        dest_deck = deck_service.get_deck_by_name(dest.name)
        if dest_deck:
            raise HTTPException(status_code=400, detail="Deck already exists")
        deck_service.copy_deck(deck, dest.name)
        resp = deck_service.get_deck_by_name(dest.name)
        return resp
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/txt")
def export_txt(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        assert deck.name is not None, "Deck should have a name"
        _, cards = deck_card_service.get_deck_data_by_name(deck.name)
        txt = []
        for card in cards:
            if card.is_commander:
                txt.insert(0, f"{card.quantidade} {card.card.name}")
            else:
                txt.append(f"{card.quantidade} {card.card.name}")
        path = deck.name + ".txt"
        buffer = StringIO("\n".join(txt))
        return StreamingResponse(
            buffer,
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="{path}"'},
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/csv")
def export_csv(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        assert deck.name is not None, "Deck should have a name"
        _, cards = deck_card_service.get_deck_data_by_name(deck.name)

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["Quantity", "Card"])
        rows = []

        for card in cards:
            if card.is_commander:
                writer.writerow([card.quantidade, card.card.name])
            else:
                rows.append([card.quantidade, card.card.name])
        writer.writerows(rows)
        buffer.seek(0)
        path = deck.name + ".csv"
        return StreamingResponse(
            buffer,
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{path}"'},
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{id}/json",
)
def export_json(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        assert deck.name is not None, "Deck should have a name"
        _, cards = deck_card_service.get_deck_data_by_name(deck.name)

        data = []
        for card in cards:
            if card.is_commander:
                data.insert(0, {"card": card.card.name, "quantity": card.quantidade})
            else:
                data.append({"card": card.card.name, "quantity": card.quantidade})
        json_bytes = json.dumps(data, indent=4).encode("utf-8")
        buffer = BytesIO(json_bytes)
        path = deck.name + ".json"
        return StreamingResponse(
            buffer,
            media_type="application/json",
            headers={"Content-Disposition": f'attachment; filename="{path}"'},
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all/export")
def export_all():
    try:
        decks = deck_service.get_decks()

        # Create zip file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for deck in decks:
                assert deck.name is not None
                _, cards = deck_card_service.get_deck_data_by_name(deck.name)

                # Create txt content
                txt_lines = []
                for card in cards:
                    if card.is_commander:
                        txt_lines.insert(0, f"{card.quantidade} {card.card.name}")
                    else:
                        txt_lines.append(f"{card.quantidade} {card.card.name}")

                # Add to zip
                zip_file.writestr(f"{deck.name}.txt", "\n".join(txt_lines))

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="all_decks.zip"'},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import-txt", response_model=CompleteDeckRead, status_code=201)
def import_txt(deck_name: str = Form(...), file: UploadFile = File(...)):
    try:
        # Check if deck already exists (following CLI pattern)
        existing_deck = deck_service.get_deck_by_name(deck_name)
        if existing_deck:
            raise DeckAlreadyExists(deck_name)

        # Read file content
        content = file.file.read().decode("utf-8")
        lines = content.splitlines()

        # Parse cards from txt
        cards = []
        pattern = re.compile(r"^(\d+) (.+)$")
        errors = []

        for line in lines:
            line = line.strip()
            if line.startswith("//"):
                continue
            if not line:
                continue
            match = pattern.match(line)
            if not match:
                errors.append(line)
                continue
            cards.append(match.groups())

        if errors:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid lines in file: {', '.join(errors[:5])}",
            )

        # Get card names
        card_names = [card[1] for card in cards]

        # Get cards from database
        card_data = card_service.get_cards_by_name(card_names)

        # Fetch missing cards from API
        if len(card_data) != len(card_names):
            card_data_names = [card.name for card in card_data]
            extra_cards = [card for card in card_names if card not in card_data_names]
            extra_card_data = get_many_cards_from_api(extra_cards)
            card_service.insert_or_update_cards(extra_card_data)
            card_data.extend(extra_card_data)

        # Create deck cards list (following CLI pattern)
        card_list = []
        for card in card_data:
            for qty, name in cards:
                if card.name == name:
                    card_list.append({"card": card, "quantidade": int(qty)})
                    break

        # Create deck with cards (following CLI pattern)
        deck = deck_service.create_deck_with_cards(deck_name, card_list)

        # Return created deck
        deck, deck_cards = deck_card_service.get_deck_data_by_name(deck.name)
        return {
            "name": deck.name,
            "id": deck.id,
            "last_update": deck.last_update,
            "cards": deck_cards,
        }
    except HTTPException:
        raise
    except DeckAlreadyExists as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/analyze", response_model=dict)
def analyze_deck(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        assert deck.name is not None, "Deck should have a name"
        deck, deck_cards = deck_card_service.get_deck_data_by_name(deck.name)

        from edhelper.commom.deck_analyzer import analyze_commander_rules

        result = analyze_commander_rules(deck_cards)

        commander_data = None
        if result["commander"]:
            commander = result["commander"]
            commander_data = {
                "id": commander.id,
                "name": commander.name,
                "color_identity": commander.color_identity,
            }

        return {
            "deck_id": deck.id,
            "deck_name": deck.name,
            "valid": result["valid"],
            "total_cards": result["total_cards"],
            "commander": commander_data,
            "commander_color_identity": result.get("commander_color_identity"),
            "errors": result["errors"],
            "warnings": result["warnings"],
        }
    except HTTPException:
        raise
    except DeckNotFound as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/add", response_model=FullDeckCards)
def add_card(id: int, body: DeckQuantity):
    try:
        if body.quantidade <= 0:
            raise InvalidQuantity(body.quantidade)
        deck = deck_service.get_deck_by_id(id)
        card = card_service.get_card_by_id(body.card_id)
        assert card.name is not None, "Card should have a name"
        dc = deck_card_service.get_deck_commanders_name(card.name)
        if not dc:
            dc = DeckCard(
                deck_id=deck.id,
                card=card,
                quantidade=body.quantidade,
                is_commander=False,
            )
        else:
            dc.quantidade = body.quantidade
        deck_card_service.update_or_insert_deck_card(dc)
        assert deck.id is not None, "Deck should have an id"
        assert card.id is not None, "Card should have an id"
        dc = deck_card_service.get_deck_card(deck.id, card.id)
        if not dc:
            raise HTTPException(status_code=404, detail="Deck card not found")
        return dc
    except HTTPException:
        raise
    except (InvalidQuantity, DeckNotFound, CardNotFound) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/remove", response_model=FullDeckCards)
def remove_card(id: int, body: DeckQuantity):
    try:
        if body.quantidade <= 0:
            raise InvalidQuantity(body.quantidade)
        deck = deck_service.get_deck_by_id(id)
        card = card_service.get_card_by_id(body.card_id)
        assert card.name is not None, "Card should have a name"
        assert deck.id is not None, "Deck should have an id"
        assert card.id is not None, "Card should have an id"
        dc = deck_card_service.get_deck_card(deck.id, card.id)
        if not dc:
            assert deck.name is not None
            raise CardNotOnDeck(card.name, deck.name)
        assert dc.quantidade is not None, "Deck card should have a qty"
        if dc.quantidade <= body.quantidade:
            deck_card_service.delete_deck_card(dc)
            return DeckCard(card=card, quantidade=0, is_commander=False)
        dc.quantidade -= body.quantidade
        deck_card_service.update_deck_card_quantity(dc)
        return dc
    except HTTPException:
        raise
    except (InvalidQuantity, DeckNotFound, CardNotFound, CardNotOnDeck) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id}/commander", status_code=204)
def reset_commander(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        assert deck.id is not None, "Deck should have a id"
        deck_card_service.reset_deck_commander(deck.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id}/commander", response_model=FullDeckCards)
def set_commander(id: int, card: SetCommander):
    try:
        card_id = card.card_id
        deck = deck_service.get_deck_by_id(id)
        assert deck.id is not None, "Deck should have a id"
        card = card_service.get_card_by_id(card_id)
        dc = deck_card_service.get_deck_card(deck.id, card_id)
        if not dc:
            assert deck.name is not None
            raise CardNotOnDeck(card.name, deck.name)
        dc.is_commander = True
        dc.quantidade = 1
        deck_card_service.set_deck_commander(dc)
        return dc
    except HTTPException:
        raise
    except (DeckNotFound, CardNotFound, CardNotOnDeck) as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id}/commander", response_model=FullDeckCards)
def get_commander(id: int):
    try:
        deck = deck_service.get_deck_by_id(id)
        if not deck:
            raise HTTPException(status_code=404, detail="Deck not found")
        commander = deck_card_service.get_deck_commanders_name(id)
        if not commander:
            raise HTTPException(status_code=404, detail="Commander not found")
        card = card_service.get_card_by_name(commander)
        assert deck.id is not None, "Deck should have an id"
        assert card.id is not None, "Card should have an id"
        deck_card = deck_card_service.get_deck_card(deck.id, card.id)
        return deck_card
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
