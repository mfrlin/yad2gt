import csv
import datetime
import enum
import os
import pathlib
import uuid
from dataclasses import dataclass
from pathlib import Path


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

# position in list is 'category' number
CATEGORIES = [
    'Angelic Raiment',  # 0
    'Arcanna\'s Tricks',  # 1
    'Arctic Gear',  # 2
    'Berserker\'s Arsenal',  # 3
    'Cathan\'s Traps',  # 4
    'Civerb\'s Vestments',  # 5
    'Cleglaw\'s Brace',  # 6
    'Death\'s Disguise',  # 7
    'Hsaru\'s Defense',  # 8
    'Infernal Tools',  # 9
    'Iratha\'s Finery',  # 10
    'Isenhart\'s Armory',  # 11
    'Milabrega\'s Regalia',  # 12
    'Sigon\'s Complete Steel',  # 13
    'Tancred\'s Battlegear',  # 14
    'Vidala\'s Rig',  # 15
    'Aldur\'s Watchtower',  # 16
    'Bul-Kathos\' Children',  # 17
    'Cow King\'s Leathers',  # 18
    'The Disciple',  # 19
    'Griswold\'s Legacy',  # 20
    'Heaven\'s Brethren',  # 21
    'Hwanin\'s Majesty',  # 22
    'Immortal King',  # 23
    'M\'avina\'s Battle Hymn',  # 24
    'Natalya\'s Odium',  # 25
    'Naj\'s Ancient Vestige',  # 26
    'Orphan\'s Call',  # 27
    'Sander\'s Folly',  # 28
    'Sazabi\'s Grand Tribute',  # 29
    'Tal Rasha\'s Wrappings',  # 30
    'Trang-Oul\'s Avatar',  # 31
    'Runes',  # 32
    'Uncategorized TODO',  # 33 
]
CATEGORY_ITEMS = [set() for _ in range(len(CATEGORIES))]


@dataclass
class Item:
    id: int
    name: str
    base: str
    slot: Slot
    rarity: Rarity
    category: int


def prepare_words(text: str) -> list[str]:
    text = text.replace('-', ' ')
    text = text.replace('\'', '')
    return list(map(str.lower, text.split()))


# {word: set([indices])}
_SEARCH_STRUCTURE: dict[str : set[int]] = {}
_ITEMS: list[Item] = []

def _load_items(file_name: str):
    with open(file_name) as items_file:
        reader = csv.DictReader(items_file)
        for row in reader:
            row['id'] = int(row['id'])
            row['slot'] = Slot(int(row['slot']))
            row['rarity'] = Rarity(int(row['rarity']))
            row['category'] = int(row['category'])
            _ITEMS.append(Item(**row))
            CATEGORY_ITEMS[row['category']].add(row['id'])

_load_items(Path(__file__).parent / 'assets' / 'items.csv')

# future proofing if new items are added
_ITEMS.sort(key=lambda i: i.id)  # sort so that item.id == index

for i, item in enumerate(_ITEMS):
    if i != item.id:
        raise AssertionError(
            f'Item id={item.id} is different than it\'s index={i} in _ITEMS'
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


_FOUND_ITEMS_IDS: set[int] = set()

def mark_found(item_id: int):
    dt = datetime.datetime.now()
    _FOUND_ITEMS_IDS.add(item_id)
    with open('found.db', 'a') as f:
        f.write(f'A,{item_id},{dt.isoformat()}\n')

def mark_missing(item_id: int):
    _FOUND_ITEMS_IDS.remove(item_id)
    with open('found.db', 'a') as f:
        f.write(f'R,{item_id}\n')


# def deduplicate_todo(item_id: int):
#     _FOUND_ITEMS_IDS.remove(item_id)
    
#     temp_file = 'found_temp.db'
#     with open('found.db', 'r') as original, open(temp_file, 'w') as temp:
#         for line in original:
#             if not line.startswith(f'{item_id},'):
#                 temp.write(line)
    
#     os.replace(temp_file, 'found.db')

CURRENT_FOUND_DB_VERSION = '1'
def load_found():
    with open('found.db') as f:
        header_line = f.readline()
        prefix, version, _ = header_line.split(',')
        # _ is UUID. identifier for a future feature that would be awkward to add later.
        # version is also just future proofing the file format 
        if prefix != 'H' or version != CURRENT_FOUND_DB_VERSION:
            raise AssertionError('found.db file corrupted')
        for line in f.readlines():
            action, item_id_str, *_ = line.strip().split(',')
            if action == 'A':
                _FOUND_ITEMS_IDS.add(int(item_id_str))
            else:
                _FOUND_ITEMS_IDS.remove(int(item_id_str))


def ensure_found_file():
    found_file = pathlib.Path('found.db')
    if not found_file.is_file():
        with open('found.db', 'w') as f:
            f.write(f'H,{CURRENT_FOUND_DB_VERSION},{uuid.uuid4()}')
            pass


ensure_found_file()
load_found()
