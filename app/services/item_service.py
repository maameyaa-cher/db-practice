from app.models.item import Item

items = [
    Item(id=1, name="Item 1", description="This is the first item"),
    Item(id=2, name="Item 2", description="This is the second item"),
]


def get_all_items() -> list[Item]:
    return items
