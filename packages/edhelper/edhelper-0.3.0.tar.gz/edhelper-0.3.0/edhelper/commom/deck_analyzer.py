from edhelper.domain.deck_card import DeckCard
from edhelper.domain.card import Card
from typing import List, Dict, Tuple


def parse_color_identity(color_identity: str) -> set:
    """Parse color identity string (e.g., 'R,B,U') into a set of colors."""
    if not color_identity:
        return set()
    return set(c.strip() for c in color_identity.split(",") if c.strip())


def is_color_identity_subset(card_identity: str, commander_identity: str) -> bool:
    """Check if card's color identity is a subset of commander's color identity."""
    card_colors = parse_color_identity(card_identity)
    commander_colors = parse_color_identity(commander_identity)
    return card_colors.issubset(commander_colors)


def is_basic_land(type_line: str) -> bool:
    """Check if card is a Basic Land based on type_line."""
    if not type_line:
        return False
    return "Basic Land" in type_line


def analyze_commander_rules(deck_cards: List[DeckCard]) -> Dict:
    """
    Analyze if deck follows Commander format rules:
    - Exactly 100 cards (including commander)
    - No duplicate cards (except Basic Lands)
    - All cards' color identity must be subset of commander's color identity

    Returns a dictionary with:
    - valid: bool
    - total_cards: int
    - commander: Card or None
    - errors: List[str]
    - warnings: List[str]
    """
    errors = []
    warnings = []
    commander = None
    commander_card = None

    count = 0

    for deck_card in deck_cards:
        assert deck_card.card is not None
        assert deck_card.quantidade is not None
        count += deck_card.quantidade
        if deck_card.is_commander:
            commander = deck_card.card.name
            commander_card = deck_card.card
        if (
            deck_card.quantidade != 1
            and deck_card.card.type_line
            and "Basic Land" not in deck_card.card.type_line
        ):
            errors.append(f"Illegal amount of card: {deck_card.card.name}")

    if not commander:
        errors.append("No commander set")
    else:
        assert commander_card is not None
        assert commander_card.color_identity is not None
        for card in deck_cards:
            assert card.card is not None
            if card.card.color_identity and not is_color_identity_subset(
                card.card.color_identity, commander_card.color_identity
            ):
                errors.append(
                    f"Card {card.card.name} has color identity {card.card.color_identity} that is not a subset of commander's"
                )

    if count != 100:
        errors.append("Deck must have exactly 100 cards")

    validation = {
        "valid": False,
        "total_cards": count,
        "commander": commander if commander else "No commander set",
        "commander_color_identity": commander_card.color_identity
        if commander
        else "No commander set",
        "errors": errors,
        "warnings": warnings,
    }

    return validation
