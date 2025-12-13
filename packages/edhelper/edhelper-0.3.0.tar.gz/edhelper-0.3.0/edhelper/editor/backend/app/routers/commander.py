from fastapi import APIRouter, HTTPException
from edhelper.external.edhec import get_edhrec_cardlists
from edhelper.external.api import get_commanders_from_api, get_many_cards_from_api
import edhelper.domain.card_service as card_service
from edhelper.commom.excptions import CardNotFound, DeckNotFound
from edhelper.editor.backend.app.schemas.card import CommanderList

router = APIRouter(prefix="/api/commander", tags=["commander"])

CATEGORIES = [
    "New Cards",
    "Basic Lands",
    "High Synergy Cards",
    "Top Cards",
    "Game Changers",
    "Creatures",
    "Instants",
    "Sorceries",
    "Utility Artifacts",
    "Enchantments",
    "Battles",
    "Planeswalkers",
    "Utility Lands",
    "Mana Artifacts",
]


def convert_exception_to_http(e: Exception) -> HTTPException:
    if isinstance(e, CardNotFound):
        return HTTPException(status_code=404, detail=e.message)
    elif isinstance(e, DeckNotFound):
        return HTTPException(status_code=404, detail=e.message)
    return None


@router.get("/", response_model=CommanderList)
def get_top_commanders():
    try:
        commanders = get_commanders_from_api()
        card_service.insert_or_update_cards(commanders)
        return CommanderList(cards=commanders)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{name}/meta", response_model=dict)
def get_commander_meta(name: str, category: str | None = None):
    try:
        card_list = get_edhrec_cardlists(name)

        if not card_list:
            raise HTTPException(
                status_code=404, detail=f"No meta data found for commander {name}"
            )

        if category != "Basic Lands" and category not in card_list:
            available_categories = [cat for cat in CATEGORIES if cat in card_list]
            available_categories.append("Basic Lands")
            raise HTTPException(
                status_code=400,
                detail=f"Category '{category}' not found. Available categories: {', '.join(available_categories)}",
            )

        if category == "Basic Lands":
            card = card_service.get_card_by_name(name)
            if not card:
                raise CardNotFound(name)
            card_ci = card.color_identity
            card_names = []
            if card_ci is not None:
                if "W" in card_ci:
                    card_names.append("Plains")
                if "U" in card_ci:
                    card_names.append("Island")
                if "B" in card_ci:
                    card_names.append("Swamp")
                if "R" in card_ci:
                    card_names.append("Mountain")
                if "G" in card_ci:
                    card_names.append("Forest")
        else:
            card_names = card_list[category]
        if not card_names:
            return {"commander": name, "category": category, "cards": []}

        cards = get_many_cards_from_api(card_names)

        card_service.insert_or_update_cards(cards)

        cards_dict = []
        for card in cards:
            cards_dict.append(
                {
                    "id": card.id,
                    "name": card.name,
                    "colors": card.colors,
                    "color_identity": card.color_identity,
                    "cmc": card.cmc,
                    "mana_cost": card.mana_cost,
                    "image": card.image,
                    "art": card.art,
                    "legal_commanders": card.legal_commanders,
                    "is_commander": card.is_commander,
                    "price": card.price,
                    "edhrec_rank": card.edhrec_rank,
                    "type_line": card.type_line,
                }
            )

        return {"commander": name, "category": category, "cards": cards_dict}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_basic_lands_for_color_identity(color_identity: str) -> list[str]:
    """Get basic land names based on color identity."""
    card_names = []
    if not color_identity:
        return card_names

    if "W" in color_identity:
        card_names.append("Plains")
    if "U" in color_identity:
        card_names.append("Island")
    if "B" in color_identity:
        card_names.append("Swamp")
    if "R" in color_identity:
        card_names.append("Mountain")
    if "G" in color_identity:
        card_names.append("Forest")

    return card_names


@router.get("/{name}/meta/all", response_model=dict)
def get_commander_meta_all(name: str):
    """Get all meta categories and basic lands for a commander by name."""
    try:
        # Get commander by name
        commander = card_service.get_card_by_name(name)
        if not commander:
            raise CardNotFound(name)

        commander_name = commander.name
        if not commander_name:
            raise HTTPException(
                status_code=400, detail=f"Commander '{name}' has no name"
            )

        # Get all categories from EDHREC
        card_list = get_edhrec_cardlists(commander_name)

        if not card_list:
            raise HTTPException(
                status_code=404,
                detail=f"No meta data found for commander {commander_name}",
            )

        # Prepare result structure
        result = {
            "categories": {},
        }

        # Process each category from EDHREC
        all_card_names = set()
        category_card_names = {}  # Track card names per category

        for category, card_names in card_list.items():
            if card_names:
                all_card_names.update(card_names)
                category_card_names[category] = card_names

        # Add Basic Lands category
        basic_land_names = get_basic_lands_for_color_identity(commander.color_identity)
        if basic_land_names:
            all_card_names.update(basic_land_names)
            category_card_names["Basic Lands"] = basic_land_names

        # Fetch all cards from API in one batch
        if all_card_names:
            all_cards = get_many_cards_from_api(list(all_card_names))
            card_service.insert_or_update_cards(all_cards)

            # Create a map of card name to card object
            cards_by_name = {card.name: card for card in all_cards}

            # Helper function to convert card to dict
            def card_to_dict(card):
                return {
                    "id": card.id,
                    "name": card.name,
                    "colors": card.colors,
                    "color_identity": card.color_identity,
                    "cmc": card.cmc,
                    "mana_cost": card.mana_cost,
                    "image": card.image,
                    "art": card.art,
                    "legal_commanders": card.legal_commanders,
                    "is_commander": card.is_commander,
                    "price": card.price,
                    "edhrec_rank": card.edhrec_rank,
                    "type_line": card.type_line,
                }

            # Organize cards by category - directly as arrays
            for category, card_names in category_card_names.items():
                category_cards = []
                for card_name in card_names:
                    if card_name in cards_by_name:
                        category_cards.append(card_to_dict(cards_by_name[card_name]))
                result["categories"][category] = category_cards

        return result
    except HTTPException:
        raise
    except CardNotFound as e:
        http_exc = convert_exception_to_http(e)
        if http_exc:
            raise http_exc
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
