from coffee_data import MENU, coffee_logo, resources

class CoffeeMachine:
    COINS ={"quarters": 0.25, "dimes": 0.10, "nickles": 0.05, "pennies": 0.01}
    
    def prompt(self) -> str:
        """_Prompt the user for what drink they want_

        Returns:
            str: _choice of drink_
        """
        user_drink =input("What would you like? (espresso/latte/cappuccino): ")
        return user_drink

    def resources_str(self,resources: dict) -> str:
        """_Format given resource for printing_

        Args:
            resources (dict): _current available resources in the coffee machine_

        Returns:
            str: _formatted resources_
        """
        return "Water: {water}\nMilk: {milk}\nCoffee: {coffee}\nMoney: ${money}".format(**resources)

    def display_missing_resources(self, missing_resources: list) -> str:
        """_Given a list of missing resources , title the strs in the list and return a formatted str_

        Args:
            missing_resources (list): _A list of missing resources_

        Returns:
            str: _A formatted string_
        """
        missing_resources = [resource.title() for resource in missing_resources]

        missing = {1: "Sorry! There's not enough {}!",
                   2: "Sorry! There's not enough {} and {}!",
                   3: "Sorry! There's not enough {}, {} and {}!"}

        return missing[len(missing_resources)].format(*missing_resources)

    def check_resources_availability(self,resources: dict, user_drink: str) -> tuple:
        """_Given available resources check if a given drink can be made_

        Args:
            resources (dict): _Current available resources_
            user_drink (str): _Chosen drink_

        Returns:
            tuple: _message to print and True If resources are enough otherwise False_
        """
        missing_ingredient = []
        if user_drink != "espresso":
            for resource  in resources:
                if resource != "money":
                    if resources[resource] < MENU[user_drink]["ingredients"][resource]:
                            missing_ingredient.append(resource)
        else:
            if resources["water"] < MENU["espresso"]["ingredients"]["water"]:
                missing_ingredient.append("water")
            if resources["coffee"] < MENU["espresso"]["ingredients"]["coffee"]:
                missing_ingredient.append("coffee")


        if len(missing_ingredient) == 0:
            return f"Let's make {user_drink}", True
        else:
            return self.display_missing_resources(missing_ingredient), False


    def process_coins(self,no_quarters: int, no_dimes: int, no_nickles: int, no_pennies: int)-> float:
        """_Calculate total value of coins_

        Args:
            no_quarters (int): _Number of quarters_
            no_dimes (int): _Number of dimes_
            no_nickels (int): _Number of nickels_
            no_pennies (int): _Number of pennies_

        Returns:
            float: _Total value of coins_
        """
        return round((self.COINS["quarters"] * no_quarters) + (self.COINS["dimes"] * no_dimes) + (self.COINS["nickles"] * no_nickles) + (self.COINS["pennies"] * no_pennies), 2)


    def check_enough_coins(self, total_coins: float, user_drink: str)-> tuple:
        """_Check if user gave enough coins_

        Args:
            total_coins (float): _total user coins_
            user_drink (str): _the drink the user chose_

        Returns:
            tuple: _Message and True if enough coins else False_
        """
        if MENU[user_drink]["cost"] > total_coins:
            return f"Sorry! That's not enough money. Money refunded.", False
        elif MENU[user_drink]['cost'] == total_coins:
            return f"No change.", True
        else:
            change = total_coins - MENU[user_drink]['cost']
            return "Here is ${:.2f} in change.".format(change), True

    def aks_for_coins(self, user_drink: str)-> tuple:
        """_Ask the user for coins_

        Returns:
            tuple: _Number of quarters, dimes, nickels and pennies_
        """
        print(f"Please insert coins: Cost ${MENU[user_drink]['cost']}")
        quarters = int(input("How many quarters ? "))
        dimes = int(input("How many dimes ? "))
        nickles = int(input("How many nickels ? "))
        pennies = int(input("How many pennies ? "))

        return quarters, dimes, nickles, pennies

    def update_resources(self, resources: dict, user_drink: str)-> dict:
        """_Update available resources after making a drink_

        Args:
            resources (dict): _Current resources_
            user_drink (str): _Chosen drink_

        Returns:
            dict: _Updated resources_
        """
        if user_drink != "espresso":
            for resource in resources:
                if resource != "money":
                    resources[resource] = resources[resource] - MENU[user_drink]["ingredients"][resource]
        else:
            resources["water"] -= MENU[user_drink]["ingredients"]["water"]
            resources["coffee"] -= MENU[user_drink]["ingredients"]["coffee"]

        resources["money"] += MENU[user_drink]["cost"]
        return resources

    def make_coffee(self):

        not_end = True
        while not_end:
            #Ask for which drink
            chosen_drink = self.prompt()
            is_making_coffee = True
            while is_making_coffee:
                if chosen_drink.lower() == "report":
                    #Show report
                    print(f"{self.resources_str(resources)}")
                    is_making_coffee = False
                elif chosen_drink == "end":
                    is_making_coffee = False
                    not_end = False
                else:
                    if self.check_resources_availability(resources= resources, user_drink= chosen_drink)[1]:
                        #Ask for coins
                        no_quarters, no_dimes, no_nickles, no_pennies =  self.aks_for_coins(user_drink= chosen_drink)
                        #Calculate total coins
                        total_coins = self.process_coins(no_quarters, no_dimes, no_nickles, no_pennies)
                        if self.check_enough_coins(total_coins, chosen_drink)[1]:
                            #if user gave enough money
                            print(f"{self.check_enough_coins(total_coins, chosen_drink)[0]}")
                            print(f"Here is your {chosen_drink} {coffee_logo} Enjoy!")
                            self.update_resources(resources, user_drink= chosen_drink)
                            is_making_coffee = False
                        else:
                            #If not enough coins
                            print(f"{self.check_enough_coins(total_coins, chosen_drink)[0]}")
                            is_making_coffee = False

                    else:
                        print(f"{self.check_resources_availability(resources= resources, user_drink= chosen_drink)[0]}")
                        is_making_coffee = False

