from coffee_data import MENU, coffee_logo, resources

class CoffeeMachine:
    COINS ={"quarters": 0.25, "dimes": 0.10, "nickles": 0.05, "pennies": 0.01}
    
    def prompt(self) -> str:
        """_Prompt the user for what drink they want_

        Returns:
            str: _choice of drink_
        """
        user_drink =input("What would you like? (espresso/latte/cappuccino):")
        return user_drink

    def resources_str(self,resources: dict) -> str:
        """_Format given resource for printing_

        Args:
            resources (dict): _current available resources in the coffee machine_

        Returns:
            str: _formatted resources_
        """
        return "Water: {water} \nMilk: {milk} \nCoffee: {coffee} \nMoney: ${money}".format(**resources)


    def check_resources_availability(self,resources: dict, user_drink: str) -> tuple:
        """_Given available resources check if a given drink can be made_

        Args:
            resources (dict): _Current available resources_
            user_drink (str): _Chosen drink_

        Returns:
            tuple: _message to print and True If resources are enough otherwise False_
        """
        if user_drink != "espresso":
            for resource in resources[0:-1]:

                if resources[resource] < MENU[user_drink]["ingredients"][resource]:
                    return f"Sorry! There's not enough {resource.title()}!", False

                else:
                    return f"Let's make {user_drink}", True
        else:
            for resource in resources[0:-1:1]:

                if resources[resource] < MENU[user_drink]["ingredients"][resource]:
                    return f"Sorry! There's not enough {resource.title()}!", False

                else:
                    return f"Let's make {user_drink}", True

    def process_coins(self,no_quarters: int, no_dimes: int, no_nickels: int, no_pennies: int)-> float:
        """_Calculate total value of coins_

        Args:
            no_quarters (int): _Number of quarters_
            no_dimes (int): _Number of dimes_
            no_nickels (int): _Number of nickels_
            no_pennies (int): _Number of pennies_

        Returns:
            float: _Total value of coins_
        """
        return (self.COINS["quarters"] * no_quarters) + (self.COINS["dimes"] * no_dimes) + (self.COINS["nickels"] * no_nickels) + (self.COINS["pennies"] * no_pennies)


    def check_enough_coins(self, total_coins: float, user_drink: str)-> tuple:
        """_Check if user gave enough coins_

        Args:
            total_coins (float): _total user coins_
            user_drink (str): _the drink the user chose_

        Returns:
            tuple: _Message and True if enough coins else False_
        """
        if MENU[user_drink]["cost"] > total_coins:
            return f"Sorry! Thats not enough money. Money refunded.", False
        elif MENU[user_drink]['cost'] == total_coins:
            return f"No change.", True
        else:
            change = total_coins - MENU[user_drink]['cost']
            return "Here is ${:.2f} in change.".format(change), True
    def aks_for_coins(self)-> tuple:
        """_Ask the user for coins_

        Returns:
            tuple: _Number of quarters, dimes, nickels and pennies_
        """
        print("Please insert coins:")
        quarters = input("How many quarters ? ")
        dimes = input("How many dimes ? ")
        nickels = input("How many nickels ? ")
        pennies = input("How many pennies ? ")

        return quarters, dimes, nickels, pennies

    def update_resources(self, resources: dict, user_drink: str)-> dict:
        """_Update available resources after making a drink_

        Args:
            resources (dict): _Current resources_
            user_drink (str): _Chosen drink_

        Returns:
            dict: _Updated resources_
        """
        for resource in resources[:-1]:
            resources[resource] = resources[resource] - MENU[user_drink][resource]
        resources["money"] += MENU[user_drink]["cost"]
        return resources

    def make_coffee(self):
        is_making_coffee = True
        not_end = True
        while not_end:
            #Ask for which drink
            chosen_drink =self.prompt()
            while is_making_coffee:
                if chosen_drink == "report":
                    #Show report
                    print(f"{self.resources_str(resources)}")
                elif chosen_drink == "end":
                    is_making_coffee = False
                    not_end = False
                else:
                    if self.check_resources_availability(resources= resources, user_drink= chosen_drink)[1]:
                        #Ask for coins
                        no_quarters, no_dimes, no_nickels, no_pennies =  self.aks_for_coins()
                        #Calculate total coins
                        total_coins = self.process_coins(no_quarters, no_dimes, no_nickels, no_pennies)
                        if self.check_enough_coins(total_coins, chosen_drink)[1]:
                            #if user gave enough money
                            print(f"{self.check_enough_coins(total_coins, chosen_drink)[0]}")
                            print(f"Here is your {chosen_drink} {coffee_logo} Enjoy!")
                            self.update_resources(resources, user_drink= chosen_drink)

                        else:
                            #If not enough coins
                            print(f"{self.check_enough_coins(total_coins, chosen_drink)[0]}")
                            is_making_coffee = False

                    else:
                        print(f"{self.check_resources_availability(resources= resources, user_drink= chosen_drink)[0]}")
                        is_making_coffee = False

