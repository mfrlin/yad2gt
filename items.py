import csv
import datetime
import enum
import pathlib
from dataclasses import dataclass


class Rarity(enum.Enum):
    NORMAL = 1
    MAGIC = 2
    RARE = 3
    SET = 4
    UNIQUE = 5


class Slot(enum.Enum):
    HELM = 1
    ARMOR = 2
    BELT = 3
    GLOVES = 4
    BOOTS = 5
    WEAPON = 6
    SHIELD = 7
    AMULET = 8
    RING = 9
    CHARM = 10
    JEWEL = 11
    RUNE = 12


CATEGORIES = [
    "Angelic Raiment",  # 0
    "Arcanna's Tricks",  # 1
    "Arctic Gear",  # 2
    "Berserker's Arsenal",  # 3
    "Cathan's Traps",  # 4
    "Civerb's Vestments",  # 5
    "Cleglaw's Brace",  # 6
    "Death's Disguise",  # 7
    "Hsaru's Defense",  # 8
    "Infernal Tools",  # 9
    "Iratha's Finery",  # 10
    "Isenhart's Armory",  # 11
    "Milabrega's Regalia",  # 12
    "Sigon's Complete Steel",  # 13
    "Tancred's Battlegear",  # 14
    "Vidala's Rig",  # 15
    "Aldur's Watchtower",  # 16
    "Bul-Kathos' Children",  # 17
    "Cow King's Leathers",  # 18
    "The Disciple",  # 19
    "Griswold's Legacy",  # 20
    "Heaven's Brethren",  # 21
    "Hwanin's Majesty",  # 22
    "Immortal King",  # 23
    "M'avina's Battle Hymn",  # 24
    "Natalya's Odium",  # 25
    "Naj's Ancient Vestige",  # 26
    "Orphan's Call",  # 27
    "Sander's Folly",  # 28
    "Sazabi's Grand Tribute",  # 29
    "Tal Rasha's Wrappings",  # 30
    "Trang-Oul's Avatar",  # 31
    "Runes",  # 32
    "",  # 33
    "",  # 34
    "",  # 35
    "",  # 36
    "",  # 37
    "",  # 38
    "",  # 39
    "",  # 40
    "",  # 41
    "",  # 42
    "",  # 43
    "",  # 44
    "",  # 45
    "",  # 46
    "",  # 47
    "",  # 48
    "",  # 49
    "",  # 5
]


# CATEGORIES = {
#     'Unique Items': {
#         'Rings': _RINGS,
#         'Amulets': _AMULETS,
#         'Charms': _CHARMS,
#         'Jewels': _JEWELS,
#         'Class-Specific Items': {
#             'Amazon': _AMAZON_SPECIFIC,
#             'Assassin': _ASSASSIN_SPECIFIC,
#             'Necromancer': _NECROMANCER_SPECIFIC,
#             'Barbarian': _BARBARIAN_SPECIFIC,
#             'Sorceress': _SORCERESS_SPECIFIC,
#             'Druid': _DRUID_SPECIFIC,
#             'Paladin': _PALADIN_SPECIFIC,
#         },
#         'Normal Unique Armor': {
#             'Helms': _NORMAL_UNIQUE_HELMS,
#             'Armor': _NORMAL_UNIQUE_ARMOR,
#             'Shields': _NORMAL_UNIQUE_SHIELDS,
#             'Gloves': _NORMAL_UNIQUE_GLOVES,
#             'Boots': _NORMAL_UNIQUE_BOOTS,
#             'Belts': _NORMAL_UNIQUE_BELTS,
#         },
#         'Exceptional Unique Armor': {
#             'Helms': _EXCEPTIONAL_UNIQUE_HELMS,
#             'Armor': _EXCEPTIONAL_UNIQUE_ARMOR,
#             'Shields': _EXCEPTIONAL_UNIQUE_SHIELDS,
#             'Gloves': _EXCEPTIONAL_UNIQUE_GLOVES,
#             'Boots': _EXCEPTIONAL_UNIQUE_BOOTS,
#             'Belts': _EXCEPTIONAL_UNIQUE_BELTS,
#         },
#         'Elite Unique Armor': {
#             'Helms': _ELITE_UNIQUE_HELMS,
#             'Armor': _ELITE_UNIQUE_ARMOR,
#             'Shields': _ELITE_UNIQUE_SHIELDS,
#             'Gloves': _ELITE_UNIQUE_GLOVES,
#             'Boots': _ELITE_UNIQUE_BOOTS,
#             'Belts': _ELITE_UNIQUE_BELTS,
#         },
#         'Normal Unique Weapons': {
#             'Axes': _NORMAL_UNIQUE_AXES,
#             'Bows': _NORMAL_UNIQUE_BOWS,
#             'Crossbows': _NORMAL_UNIQUE_CROSSBOWS,
#             'Daggers': _NORMAL_UNIQUE_DAGGERS,
#             'Maces': _NORMAL_UNIQUE_MACES,
#             'Polearms': _NORMAL_UNIQUE_POLEARMS,
#             'Scepters': _NORMAL_UNIQUE_SCEPTERS,
#             'Spears': _NORMAL_UNIQUE_SPEARS,
#             'Staves': _NORMAL_UNIQUE_STAVES,
#             'Swords': _NORMAL_UNIQUE_SWORDS,
#             'Wands': _NORMAL_UNIQUE_WANDS,
#         },
#         'Exceptional Unique Weapons': {
#             'Axes': _EXCEPTIONAL_UNIQUE_AXES,
#             'Bows': _EXCEPTIONAL_UNIQUE_BOWS,
#             'Crossbows': _EXCEPTIONAL_UNIQUE_CROSSBOWS,
#             'Daggers': _EXCEPTIONAL_UNIQUE_DAGGERS,
#             'Maces': _EXCEPTIONAL_UNIQUE_MACES,
#             'Polearms': _EXCEPTIONAL_UNIQUE_POLEARMS,
#             'Scepters': _EXCEPTIONAL_UNIQUE_SCEPTERS,
#             'Spears': _EXCEPTIONAL_UNIQUE_SPEARS,
#             'Staves': _EXCEPTIONAL_UNIQUE_STAVES,
#             'Swords': _EXCEPTIONAL_UNIQUE_SWORDS,
#             'Throwing Weapons': _EXCEPTIONAL_UNIQUE_THROWING_WEAPONS,
#             'Wands': _EXCEPTIONAL_UNIQUE_WANDS,
#         },
#         'Elite Unique Weapons': {
#             'Axes': _ELITE_UNIQUE_AXES,
#             'Bows': _ELITE_UNIQUE_BOWS,
#             'Crossbows': _ELITE_UNIQUE_CROSSBOWS,
#             'Daggers': _ELITE_UNIQUE_DAGGERS,
#             'Javelins': _ELITE_UNIQUE_JAVELINS,
#             'Maces': _ELITE_UNIQUE_MACES,
#             'Polearms': _ELITE_UNIQUE_POLEARMS,
#             'Scepters': _ELITE_UNIQUE_SCEPTERS,
#             'Spears': _ELITE_UNIQUE_SPEARS,
#             'Staves': _ELITE_UNIQUE_STAVES,
#             'Swords': _ELITE_UNIQUE_SWORDS,
#             'Throwing Weapons': _ELITE_UNIQUE_THROWING_WEAPONS,
#             'Wands': _ELITE_UNIQUE_WANDS,
#         },
#     },
#     'Sets': {
#         'Angelic Raiment': _ANGELIC_RAIMENT,
#     }
# }


@dataclass
class Item:
    id: int
    name: str
    base: str
    slot: Slot
    rarity: Rarity
    category: int


def prepare_words(text: str) -> list[str]:
    text = text.replace("-", " ")
    text = text.replace("'", "")
    return list(map(str.lower, text.split()))


# {word: set([indices])}
_SEARCH_STRUCTURE: dict[str : set[int]] = {}
_ITEMS: list[Item] = []


def _load_items(file_name: str):
    with open(file_name) as items_file:
        reader = csv.DictReader(items_file)
        for row in reader:
            row["id"] = int(row["id"])
            row["slot"] = Slot(int(row["slot"]))
            row["rarity"] = Rarity(int(row["rarity"]))
            row["category"] = int(row["category"])
            _ITEMS.append(Item(**row))


_load_items("items.csv")

# future proofing if new items are added
_ITEMS.sort(key=lambda i: i.id)  # sort so that item.id == index

for i, item in enumerate(_ITEMS):
    if i != item.id:
        raise AssertionError(
            f"Item id={item.id} is different than it's index={i} in _ITEMS"
        )
    words = prepare_words(item.name) + prepare_words(item.base)
    # make set items searchable by set name
    if item.rarity == Rarity.SET:
        words.extend(prepare_words(CATEGORIES[item.category]))
    for word in words:
        if word not in _SEARCH_STRUCTURE:
            _SEARCH_STRUCTURE[word] = set()
        _SEARCH_STRUCTURE[word].add(item.id)


def search(query: str) -> list[Item]:
    words = prepare_words(query)
    result_indices = set()
    for i, word in enumerate(words):
        hits = set()
        for key in _SEARCH_STRUCTURE.keys():
            if word in key:
                hits.update(_SEARCH_STRUCTURE[key])
        if i == 0:
            result_indices.update(hits)
        else:
            result_indices.intersection_update(hits)

    results = []
    for i in result_indices:
        item = _ITEMS[i]
        results.append(item)
    return results


_FOUND_ITEMS: set[Item] = set()
_FOUND_ITEMS_IDS: set[int] = set()


def mark_found(item_id: int):
    dt = datetime.datetime.now()
    _FOUND_ITEMS.add((item_id, dt))
    _FOUND_ITEMS_IDS.add(item_id)
    with open("found.db", "wa") as f:
        f.write(f"{item_id},{dt.isoformat()}")


def mark_missing(item_id: int):
    for_removal = None
    for t in _FOUND_ITEMS:
        if t[0] == item_id:
            for_removal = t
            break
    _FOUND_ITEMS.remove(for_removal)
    _FOUND_ITEMS_IDS.remove(item_id)
    with open("found.db") as f:
        lines = f.readlines()
    with open("found.db", "w") as f:
        for line in lines:
            if line.startswith(f"{item_id},"):
                continue
            f.write(line)


def load_found():
    with open("found.db") as f:
        for line in f.readlines():
            item_id_str, datetime_str = line.strip().split(",")
            _FOUND_ITEMS.add(
                (int(item_id_str), datetime.datetime.fromisoformat(datetime_str))
            )
            _FOUND_ITEMS_IDS.add(int(item_id_str))


def ensure_found_file():
    found_file = pathlib.Path("found.db")
    if not found_file.is_file():
        with open("found.db", "w"):
            pass


ensure_found_file()
load_found()
