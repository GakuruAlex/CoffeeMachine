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
class TestEspressoResourcesAvailability:
    espresso_drink = CoffeeMachine()
    def test_check_espresso_resources_availability(self, resources, chosen_drink, result):
        assert self.espresso_drink.check_resources_availability(resources, chosen_drink) == result

#Test with latte
@pytest.mark.parametrize("resources, chosen_drink, result", [
    ({"water": 300, "milk": 200, "coffee": 100, "money": 0}, "latte", ("Let's make latte", True)),
    ({"water": 100, "milk": 200, "coffee": 100, "money": 2.5}, "latte", ("Sorry! There's not enough Water!", False)),
    ({"water": 200, "milk": 100, "coffee": 100, "money": 2.5}, "latte", ("Sorry! There's not enough Milk!", False)),
    ({"water": 300, "milk": 200, "coffee": 20, "money": 2.5}, "latte", ("Sorry! There's not enough Coffee!", False)),
    ({"water": 100, "milk": 100, "coffee": 100, "money": 2.5}, "latte", ("Sorry! There's not enough Water and Milk!", False)),
    ({"water": 100, "milk": 200, "coffee": 20, "money": 2.5}, "latte", ("Sorry! There's not enough Water and Coffee!", False)),
    ({"water": 300, "milk": 100, "coffee": 20, "money": 2.5}, "latte", ("Sorry! There's not enough Milk and Coffee!", False)),
    ({"water": 100, "milk": 100, "coffee": 20, "money": 2.5}, "latte", ("Sorry! There's not enough Water, Milk and Coffee!", False)),
])
class TestLatteResourcesAvailability:
    latte_drink = CoffeeMachine()
    def test_check_latte_resources_availability(self, resources, chosen_drink, result):
        assert self.latte_drink.check_resources_availability(resources, chosen_drink) == result

#Test with cappuccino
@pytest.mark.parametrize("resources, chosen_drink, result", [
    ({"water": 300, "milk": 200, "coffee": 100, "money": 0}, "cappuccino", ("Let's make cappuccino", True)),
    ({"water": 100, "milk": 200, "coffee": 100, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Water!", False)),
    ({"water": 250, "milk": 90, "coffee": 100, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Milk!", False)),
    ({"water": 300, "milk": 200, "coffee": 20, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Coffee!", False)),
    ({"water": 100, "milk": 90, "coffee": 100, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Water and Milk!", False)),
    ({"water": 100, "milk": 200, "coffee": 20, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Water and Coffee!", False)),
    ({"water": 300, "milk": 90, "coffee": 20, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Milk and Coffee!", False)),
    ({"water": 100, "milk": 90, "coffee": 20, "money": 2.5}, "cappuccino", ("Sorry! There's not enough Water, Milk and Coffee!", False)),
])
class TestCappuccinoResourcesAvailability:
    cappuccino_drink = CoffeeMachine()
    def test_check_cappuccino_resources_availability(self, resources, chosen_drink, result):
        assert self.cappuccino_drink.check_resources_availability(resources, chosen_drink) == result


#Test process coins
@pytest.mark.parametrize("no_quarters, no_dimes, no_nickles, no_pennies, total_value", [
    (1, 1, 1, 1, 0.41),
    (4, 5, 6, 8, 1.88),
    (10, 10, 10, 10, 4.10),
    (3, 3, 3, 3, 1.23),
])
class TestProcessCoins:
    coins = CoffeeMachine()
    def test_process_coins(self, no_quarters, no_dimes, no_nickles, no_pennies, total_value):
        assert self.coins.process_coins(no_quarters, no_dimes, no_nickles, no_pennies) == total_value

#Test check whether the coins are enough for specified drink
#Check enough money for espresso
@pytest.mark.parametrize("total_coins, chosen_drink, result",[
    (4.0, "espresso", ("Here is $2.50 in change.", True)),
    (1.5, "espresso", ("No change.", True)),
    (1.4, "espresso", ("Sorry! That's not enough money. Money refunded.", False)),
])
class TestEnoughCoinsForEspresso:
    enough_coins_espresso = CoffeeMachine()
    def test_process_coins_for_espresso(self, total_coins, chosen_drink, result):
        assert self.enough_coins_espresso.check_enough_coins(total_coins, chosen_drink) == result

#Check enough money for latte
@pytest.mark.parametrize("total_coins, chosen_drink, result",[
    (4.0, "latte", ("Here is $1.50 in change.", True)),
    (2.5, "latte", ("No change.", True)),
    (1.4, "latte", ("Sorry! That's not enough money. Money refunded.", False)),
])
class TestEnoughCoinsForEspresso:
    enough_coins_latte = CoffeeMachine()
    def test_process_coins_for_espresso(self, total_coins, chosen_drink, result):
        assert self.enough_coins_latte.check_enough_coins(total_coins, chosen_drink) == result