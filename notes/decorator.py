"""
Attach additional responsibilities to an object dynamically. Decorators
provide a flexible alternative to subclassing for extending
functionality.
"""

import abc


class Component(metaclass=abc.ABCMeta):
    """
    Define the interface for objects that can have responsibilities
    added to them dynamically.
    """

    @abc.abstractmethod
    def operation(self):
        pass


class Decorator(Component, metaclass=abc.ABCMeta):
    """
    Maintain a reference to a Component object and define an interface
    that conforms to Component's interface.
    """

    def __init__(self, component):
        self._component = component

    @abc.abstractmethod
    def operation(self):
        self._component.operation()


class ConcreteDecoratorA(Decorator):
    """
    Add responsibilities to the component.
    """

    def operation(self):
        # ...
        print("decorated by A")
        super().operation()
        # ...

class ConcreteDecoratorB(Decorator):
    """
    Add responsibilities to the component.
    """

    def operation(self):
        # ...
        print("decorated by B")
        super().operation()
        # ...

class ConcreteComponent(Component):
    """
    Define an object to which additional responsibilities can be
    attached.
    """

    def operation(self):
        print("calling operation on the base component")


def main():
    concrete_component = ConcreteComponent()
    component_stack = ConcreteDecoratorA(ConcreteDecoratorB(concrete_component))
    component_stack.operation()
    

    


if __name__ == "__main__":
    main()