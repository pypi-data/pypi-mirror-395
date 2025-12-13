class Card:
    def __init__(
        self,
        id=None,
        name=None,
        colors=None,
        color_identity=None,
        cmc=None,
        mana_cost=None,
        image=None,
        art=None,
        legal_commanders=None,
        is_commander=None,
        price=None,
        edhrec_rank=None,
        commander_rank=None,
        type_line=None,
    ):
        self.id = id
        self.name = name
        self.colors = colors
        self.color_identity = color_identity
        self.cmc = cmc
        self.mana_cost = mana_cost
        self.image = image
        self.art = art
        self.legal_commanders = legal_commanders
        self.is_commander = is_commander
        self.price = price
        self.edhrec_rank = edhrec_rank
        self.commander_rank = commander_rank
        self.type_line = type_line

    def get_values_tuple(
        self,
        id=True,
        name=True,
        colors=True,
        color_identity=True,
        cmc=True,
        mana_cost=True,
        image=True,
        art=True,
        legal_commanders=True,
        is_commander=True,
        price=True,
        edhrec_rank=True,
        commander_rank=False,
        type_line=True,
    ):
        values = []
        if id:
            values.append(self.id)
        if name:
            values.append(self.name)
        if colors:
            values.append(self.colors)
        if color_identity:
            values.append(self.color_identity)
        if cmc:
            values.append(self.cmc)
        if mana_cost:
            values.append(self.mana_cost)
        if image:
            values.append(self.image)
        if art:
            values.append(self.art)
        if legal_commanders:
            values.append(self.legal_commanders)
        if is_commander:
            values.append(self.is_commander)
        if price:
            values.append(self.price)
        if edhrec_rank:
            values.append(self.edhrec_rank)
        if commander_rank:
            values.append(self.commander_rank)
        if type_line:
            values.append(self.type_line)
        return tuple(values)

    def __hash__(self):
        return hash(self.get_values_tuple())

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    @staticmethod
    def from_dict(card_dict: dict):
        card = Card(
            id=card_dict["id"],
            name=card_dict["name"],
            colors=card_dict["colors"],
            color_identity=card_dict["color_identity"],
            cmc=card_dict["cmc"],
            mana_cost=card_dict["mana_cost"],
            image=card_dict["image"],
            art=card_dict["art"],
            legal_commanders=card_dict["legal_commanders"],
            is_commander=card_dict["is_commander"],
            price=card_dict["price"],
            edhrec_rank=card_dict["edhrec_rank"],
            commander_rank=card_dict.get("commander_rank", None),
            type_line=card_dict.get("type_line", None),
        )
        return card

    def show(self):
        if self.name is not None:
            print(f"Name: {self.name}")
        if self.colors is not None:
            print(f"Colors: {self.colors}")
        if self.color_identity is not None:
            print(f"Color Identity: {self.color_identity}")
        if self.cmc is not None:
            print(f"CMC: {self.cmc}")
        if self.mana_cost is not None:
            print(f"Mana Cost: {self.mana_cost}")
        if self.image is not None:
            print(f"Image URL: {self.image}")
        if self.art is not None:
            print(f"Art URL: {self.art}")
        if self.legal_commanders is not None:
            print(f"Legal Commanders: {self.legal_commanders}")
        if self.is_commander is not None:
            print(f"Is Commander: {self.is_commander}")
