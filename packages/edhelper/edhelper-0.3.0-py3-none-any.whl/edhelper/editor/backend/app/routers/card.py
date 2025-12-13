from fastapi import APIRouter, HTTPException
from edhelper.domain import card_service
from edhelper.external.api import get_commanders_from_api
from edhelper.commom.excptions import CardNotFound, ShortPartial
from edhelper.editor.backend.app.schemas.card import Card, CardList

router = APIRouter(prefix="/api/cards", tags=["card"])


def convert_exception_to_http(e: Exception) -> HTTPException:
    if isinstance(e, CardNotFound):
        return HTTPException(status_code=404, detail=e.message)
    elif isinstance(e, ShortPartial):
        return HTTPException(status_code=400, detail=e.message)
    return None


@router.get("/autocomplete/{partial}", response_model=CardList)
def autocomplete_cards(partial: str):
    try:
        cards = card_service.get_by_autocomplete(partial)
        return CardList(cards=cards)
    except HTTPException:
        raise
    except ShortPartial as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/named/{name}", response_model=Card)
def get_card_by_name(name: str):
    try:
        card = card_service.get_card_by_name(name)
        return card
    except HTTPException:
        raise
    except CardNotFound as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{card_id}", response_model=Card)
def get_card(card_id: str):
    try:
        card = card_service.get_card_by_id(card_id)
        return card
    except HTTPException:
        raise
    except CardNotFound as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
