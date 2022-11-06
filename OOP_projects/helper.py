# When to use class methods and when to use static methods?

class Item:
    pass

    @staticmethod
    def check_if_integer(num):
        '''
        This should do something that has a relationship
        with the class, but not something that must be unique
        per instance!
        '''
        ...

    @classmethod
    def instantiate_from_something(cls):
        '''
        This should also do something that has a relationship
        with the class, but usually, those are used to
        manipulate different structures of data to instantiate
        objects, like we have done with CSV.
        '''
        ...