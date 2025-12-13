import httpx
from edhelper.infra.config import settings
from edhelper.domain.card import Card


def get_headers():
    """Get headers with current API credentials."""
    return {
        "x-api-key": settings.API_KEY,
        "x-client-id": settings.CLIENT_ID,
    }


def create_client() -> dict:
    """Create a new client by calling /api/auth/create-client endpoint."""
    if not settings.API_URL:
        raise Exception("API_URL not configured. Please set it in your environment.")

    url = f"{settings.API_URL}/api/auth/create-client"
    try:
        with httpx.Client() as client:
            resp = client.post(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise Exception(
            f"HTTP error creating client: {e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        raise Exception(f"Error connecting to API: {str(e)}")


def get_card_from_api(name: str) -> Card:
    url = f"{settings.API_URL}/api/cards/named/{name}"
    try:
        with httpx.Client() as client:
            resp = client.get(url, headers=get_headers())
            resp.raise_for_status()
            return Card.from_dict(resp.json())
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error fetching card: {e.response.status_code}")
    except httpx.RequestError as e:
        raise Exception(f"Error connecting to API: {str(e)}")


def get_autocomplete_from_api(partial: str) -> list[Card]:
    url = f"{settings.API_URL}/api/cards/autocomplete/{partial}"
    try:
        with httpx.Client() as client:
            resp = client.get(url, headers=get_headers())
            resp.raise_for_status()
            cards = [Card.from_dict(card) for card in resp.json()["cards"]]
            return cards
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error fetching autocomplete: {e.response.status_code}")
    except httpx.RequestError as e:
        raise Exception(f"Error connecting to API: {str(e)}")


def get_many_cards_from_api(cards: list[str]) -> list[Card]:
    url = f"{settings.API_URL}/api/cards/"
    payload = {"cards": cards}

    try:
        with httpx.Client() as client:
            resp = client.post(url, json=payload, headers=get_headers())
            resp.raise_for_status()
            resp = resp.json()
            card_list: list[dict] = resp["cards"]
            cards_final = [Card.from_dict(card) for card in card_list]
            return cards_final
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error fetching multiple cards: {e.response.status_code}")
    except httpx.RequestError as e:
        raise Exception(f"Error connecting to API: {str(e)}")


def get_commanders_from_api() -> list[Card]:
    url = f"{settings.API_URL}/api/cards/topcommanders"
    try:
        with httpx.Client() as client:
            resp = client.get(url, headers=get_headers())
            resp.raise_for_status()
            cards_final = [Card.from_dict(card) for card in resp.json()["cards"]]
            return cards_final
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP error fetching multiple cards: {e.response.status_code}")
    except httpx.RequestError as e:
        raise Exception(f"Error connecting to API: {str(e)}")
