### Object Oriented Programming with Python

> Based on tutorial by JimShapedCoding on freecodecamp: https://www.youtube.com/watch?v=Ej_02ICOIgs&list=WL

---

### Basics

#### instance attr vs class attr

class attr belongs to the class but we can access from instance level as well as class level

```
class Item:
    pay_rate = 0.8 # discount
    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity
```

```
print (Item.pay_rate)
>>> 0.8
```

We can also access these class attrs from instance level as well

```
item1 = Item('Phone', 100, 5)
print (item1.pay_rate)
>>> 0.8
```

How this works is first the object will try and fetch the attr from instance level - if not found, it will fetch from class level

If we have this attr defined at both class and instance levels:

```
class Item:
    # NOTE: these are class attrs
    pay_rate = 0.8 # discount
    def __init__(self, name: str, price: float, quantity=0) -> None:

        validate_input(name, price, quantity)

        self.name = name
        self.price = price
        self.quantity = quantity
        self.pay_rate = 1

item1 = Item('Phone', 100, 5)

print (Item.pay_rate)

print (item1.pay_rate)

>>> 0.8
>>> 1
```

Using `__dict__` - gets all attrs belonging to this object

```
print (Item.__dict__)
>>>
{'__module__': '__main__', 'pay_rate': 0.8, '__init__': <function Item.__init__ at 0x100b8eb80>, 'calculate_total_price': <function Item.calculate_total_price at 0x100b8ec10>, '__dict__': <attribute '__dict__' of 'Item' objects>, '__weakref__': <attribute '__weakref__' of 'Item' objects>, '__doc__': None}

print (item1.__dict__)
>>>
{'name': 'Phone', 'price': 100, 'quantity': 5}
```

Note that `pay_rate` is not there in the attrs of the item1 instance

