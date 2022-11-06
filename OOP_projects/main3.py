from item import Item
from phone import Phone


Item.instantiate_from_csv()
Item.display_inventory()


item_new = Item(name='Bag', price=700, quantity=20)
item_new.name = "Handbag"
print (item_new.name)

