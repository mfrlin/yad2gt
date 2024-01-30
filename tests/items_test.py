import items


def test_items_count():
    assert len(items._ITEMS) == 545
    assert (
        len([item for item in items._ITEMS if item.rarity == items.Rarity.SET]) == 127
    )
    assert len([item for item in items._ITEMS if item.slot == items.Slot.RUNE]) == 33
    assert (
        len([item for item in items._ITEMS if item.rarity == items.Rarity.UNIQUE])
        == 545 - 127 - 33
    )


def test_search_by_set_name():
    result = [item.id for item in items.search("orphans")]
    assert sorted(result) == [524, 525, 526, 527]

    result = [item.id for item in items.search("heavens brethren")]
    assert sorted(result) == [498, 499, 500, 501]
