import pytest
from coffee_machine import CoffeeMachine
from unittest.mock import patch


#Test resources str
@pytest.mark.parametrize("resources, result", [
    ({"water": 300, "milk": 200, "coffee": 100, "money": 0}, "Water: 300\nMilk: 200\nCoffee: 100\nMoney: $0"),
    ({"water": 200, "milk": 150, "coffee": 90, "money": 2.5}, "Water: 200\nMilk: 150\nCoffee: 90\nMoney: $2.5"),
    ({"water": 100, "milk": 100, "coffee": 78, "money": 4.0}, "Water: 100\nMilk: 100\nCoffee: 78\nMoney: $4.0"), 
])
class TestResourcesStr:
    resource_str = CoffeeMachine()
    def test_resource_str(self, resources, result):
        assert self.resource_str.resources_str(resources) == result

#Test checking resource availability function
# Test with espresso as drink
@pytest.mark.parametrize("resources, chosen_drink, result", [
    ({"water": 300, "milk": 200, "coffee": 100, "money": 0}, "espresso", ("Let's make espresso", True)),
    ({"water": 40, "milk": 200, "coffee": 20, "money": 0}, "espresso", ("Sorry! There's not enough Water!", False)),
    ({"water": 300, "milk": 200, "coffee": 10, "money": 0}, "espresso", ("Sorry! There's not enough Coffee!", False)),
    ({"water": 45, "milk": 200, "coffee": 10, "money": 0}, "espresso", ("Sorry! There's not enough Water and Coffee!", False)),
    
])
class TestCheckResourcesAvailability:
    espresso_drink = CoffeeMachine()
    def test_check_resources_availability(self, resources, chosen_drink, result):
        assert self.espresso_drink.check_resources_availability(resources, chosen_drink) == result