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


### Create an inventory list functionality

We basically want to list out all items in our store

We can store inventory as a class attr

`__repr__`: object representation - use this to display object

-- see main.py to see use of a class attr


#### Using Class method for Separating out our data


__Using a Class Method__:

When we want to load in the data, we want to create objects from the loaded data using that function 

We cannot do `item.instantiate_from_csv()` as we want `instantiate_from_csv` to take care of initializing the objs


1. Setup fpath as a class var

`fpath = os.path.join(os.getcwd(), 'OOP_projects', 'data', 'items.csv')`

2. Create a class method to load in the csv and instantiate an item object for each record

Note that the `cls` is like `self` but signifies the class. 

```
@classmethod
    def instantiate_from_csv(cls):
        """
        Read a csv file and create instances for each record
        """
        fpath = cls.fpath
        try:
            df = pd.read_csv(fpath, index_col=False)
        except FileNotFoundError as e:
            print (f'Not found file at {fpath}')
            raise

        records = df.to_dict(orient='list')

        for item_ in  (list(zip(records['name'], records['price'], records['quantity']))):
            Item(name=item_[0], price=item_[1], quantity=item_[2])
```

> It can modify a class state that would apply across all the instances of the class. For example, it can modify a class variable that will be applicable to all the instances.

For example if u want to instantiate hundreds of objects from a file - use a class method


#### Static method

 This method can’t access or modify the class state. It is present in a class because it makes sense for the method to be present in class.

 > https://www.geeksforgeeks.org/class-method-vs-static-method-python/

 - We generally use static methods to create utility functions.


Static methods do not receive the obj/class as the first arg - just like a regular function

The validation of input function and a function to check if an arg is an int seem like good candidates for static methods


```
@staticmethod
    def validate_input(name: str, price: float, quantity: float) -> Union[bool, AssertionError]:
        assert price >=0 and quantity>=0, 'Price and quantity should be >= 0'

    @staticmethod
    def is_integer(num):
        
        # if float
        if isinstance(num, float):
            # if 7.0 it will return True, False if has fractional part
            return num.is_integer()
        # if int like 7
        elif isinstance(num, int):
            return True
        return False

```

Ok, so what is the diff bw writing static methods and independent functions outside the class? - not much, but if the function is related to the class then its good practice to use static methods

Also note - do not call a static or class method from an instance level - you will not receive error but its not good practice


### Inheritence

Now we might have phones of class `Item` but these phones might be broken

```
phone1 = Item(name='nokia10', price=1000, quantity=5)
phone1.broken_phones = 1
phone2 = Item(name='nokia11', price=2500, quantity=5)
phone2.broken_phones = 2
```

Now if we were to calculate broken phones

```
@classmethod
    def calculate_broken_phones(cls):
        for item_ in Item.inventory:
            print (item_.broken_phones)

```

Not all items might have this `broken_phones` attr - so we can get error:

```
AttributeError: 'Item' object has no attribute 'broken_phones'
```

We can modify this by:

```
@classmethod
    def calculate_broken_phones(cls):
        num_broken_phones = 0
        for item_ in Item.inventory:
            if 'broken_phones' in item_.__dict__:
                num_broken_phones += item_.broken_phones

        return num_broken_phones
```

But we can build this better using inheitence as this `broken_phones` is an attr only phone type instances of class Item should have. So Phone should have its own class and inherit from Item


How we want to design this is have a parent class - Item

We want to have multiple child classes - Phone, Laptop etc.

In `__init__` class of Phone - we want the `__init__` functionality of Item class but we want to also store an addnl attr like `broken_phones`

`super()` allows us to do this. `super()` basically returns a proxy object which represents the parent’s class. In an inherited subclass, a parent class can be referred with the use of the super() function. The super function returns a temporary object of the superclass that allows access to all of its methods to its child class. - https://www.geeksforgeeks.org/python-super/

```
class Phone(Item):

    def __init__(self, name: str, price: float, quantity=0, broken_phones=0) -> None:
        super().__init__(name, price, quantity)
        self.broken_phones = broken_phones

Item.instantiate_from_csv()
phone1 = Phone(name='nokia10', price=1000, quantity=5, broken_phones=2)
Item.display_inventory()
```

```
>>>
Item('Phone',100.0,1)
Item('Laptop',1000.0,3)
Item('Cable',10.5,5)
Item('Mouse',50.0,5)
Item('Keyboard',75.0,5)
Item('nokia10',1000,5)
```

Note that the Phone class is still printed as Item in `display_inventory()`

This is because in `__repr__` method we had

`return f"Item('{self.name}',{self.price},{self.quantity})"`

instead of Item we can dynamically get the class name from the instance

`return f"{self.__class__.__name__}('{self.name}',{self.price},{self.quantity})"`

Now this will pick the class name from the instance passed in 

Now output will be:

```
Item('Phone',100.0,1)
Item('Laptop',1000.0,3)
Item('Cable',10.5,5)
Item('Mouse',50.0,5)
Item('Keyboard',75.0,5)
Phone('nokia10',1000,5)
```


### Organizing project 

- create 2 files item.py and phone.py
- we will use a new main file main3.py to create instances

main3.py:

```
from item import Item
from phone import Phone


Item.instantiate_from_csv()
Item.display_inventory()
```

- works as expected

### Read only attributes

We can easily overwrite attr of an item

```
item_new = Item(name='Laptop', price=50000, quantity=3)
item_new.price = 10000
print (item_new)
```

```
>>>
Item('Laptop',10000,3)
```

But we might not want this behavior always - we might want critical attrs to be just read-only - like the name

- we can create read-only attrs, we wont be able to overwrite this 


We can create read only __properties__ (not attributes) using `@property`

In class Item:

```
@property
    def read_only_name(self) -> None:
        return "AAA"

```

In main:

```
item_new = Item(name='Laptop', price=50000, quantity=3)
print (item_new.read_only_name)
item_new.read_only_name = "new name"
```

```
>>>
AAA
Traceback (most recent call last):
  File "/Users/shaunaksen/Documents/personal-projects/ML_Deployment/OOP_projects/main3.py", line 10, in <module>
    item_new.read_only_name = "new name"
```


What we want - `name` should be only read-only

We can achieve this using __Encapsulation__

#### Encapsulation

- https://www.geeksforgeeks.org/encapsulation-in-python/


Protected members (in C++ and JAVA) are those members of the class that cannot be accessed outside the class but can be accessed from within the class and its subclasses. To accomplish this in Python, just follow the convention by prefixing the name of the member by a single underscore “_”.

> Although the protected variable can be accessed out of the class as well as in the derived class(modified too in derived class), it is customary(convention not a rule) to not access the protected out the class body.

In Item `__init__`:

`self._name = name`

In main:

```
item_new = Item(name='Bag', price=700, quantity=20)
item_new._name = "Handbag"
print (item_new._name)

```

```
>>>
Handbag
```

This works as normal! What we need to do is register the `_name` as a property:

```
def __init__(self, name: str, price: float, quantity=0) -> None:

        Item.validate_input(name, price, quantity)

        # NOTE: making name a protected class; cant be changed outside this class
        self._name = name
        self.price = price
        self.quantity = quantity

        # add item to inventory now that it is created        
        Item.add_item_to_inventory(self)

    @property
    def name(self):
        return self._name

```

In main:

```
item_new = Item(name='Bag', price=700, quantity=20)
item_new.name = "Handbag"
print (item_new._name)
```

```
>>>
AttributeError: can't set attribute
```

`item_new._name = "Handbag"` will still work - __so the "_" by itself does nothing!__ - we need to declare it as a `@property`

After declaring it as a property, whenever we do `item.name`, python will run the code inside `@property` for that attr 

Even after declaring as a property we can still set it using some special functions:

In class Item

```
# NOTE: property decorator - read only attr
    @property
    def name(self):
        return self._name
```

In main:

```
item_new = Item(name='Bag', price=700, quantity=20)
item_new.name = "Handbag"
print (item_new.name)
```

```
>>>
Handbag
```

This works with `__`(private) attrs as well

We can be restrictive by assigning an attr as a pvt attr

In that case in Item

```
def __init__(self, name: str, price: float, quantity=0) -> None:

        Item.validate_input(name, price, quantity)

        # NOTE: making name a protected class; cant be changed outside this class
        self.__name = name
        self.price = price
        self.quantity = quantity
```

In main:

```
item_new = Item(name='Bag', price=700, quantity=20)
print (item_new.__name)

```

We get:

```
AttributeError: 'Item' object has no attribute '__name'
```

We can use @property on `__` variables as well 


#### Summary

using `@property` we can specify vars as read-only

After declaring it as a property, whenever we do `item.name`, python will run the code inside `@property` for that attr 

Similarly after declaring a setter, python will run the code inside `@name.setter`
wehenever we do `item1.name = 'handbag'` sor similar

Here handbag will be passed as `value` in the setter function:

```
@name.setter
    def name(self, value):
        self._name = value
```

This is how getters and setters work - for example in the setter we can restrict length of name:

```
@name.setter
    def name(self, value):
        if len(value) > 100:
            raise Exception('name is too long')
        else:
            self._name = value
```



### Principles of OOP

