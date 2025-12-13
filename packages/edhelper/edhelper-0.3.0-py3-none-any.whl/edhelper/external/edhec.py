import requests
import re


def format_commander_name(commander_name: str):
    non_alphas_regex = r"[^\w\s-]"
    formatted_name = commander_name.replace(" ", "-")
    formatted_name = re.sub(non_alphas_regex, "", formatted_name)
    formatted_name = formatted_name.lower()
    formatted_name = formatted_name.replace(" ", "-")
    return formatted_name


def request_json(commander_name: str):
    formatted_name = format_commander_name(commander_name)
    json_url = f"https://json.edhrec.com/pages/commanders/{formatted_name}.json"
    response = requests.get(json_url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return None


def get_edhrec_cardlists(name):
    name = format_commander_name(name)
    json_data = request_json(name)
    if json_data is None:
        return {}
    card_lists = {}
    cardlist_json = json_data["container"]["json_dict"]
    specific_card_lists_data = cardlist_json["cardlists"]
    for cardlist in specific_card_lists_data:
        current_cardlist_name = cardlist["header"]
        current_cardlist_cards = []
        for card_view in cardlist["cardviews"]:
            current_cardlist_cards.append(card_view.get("name"))
        card_lists[current_cardlist_name] = current_cardlist_cards
    return card_lists
