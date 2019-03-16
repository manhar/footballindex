#!/usr/bin/python

"""

This class represents a football player

"""

class Player():


    def __init__(self, name, team, position="", sprice=0.0, bprice =0.0 ):
        self.name = name
        self.team = team
        self.position = position
        self.selling_price = sprice
        self.buying_rice = bprice

    def BuyingPrice(self):
        """

        Returns the buying price of a player

        :param name: the name of the player
        :return: double number

        """
        return self.buying_rice

    def SellingPrice(self):
        """

        Returns the selling price of a player

        :param name: the name of the player
        :return: double number

        """
        return self.selling_price

    def Team(self):

        """
        Returns the players team
        :return: String
        """

        return self.team

    def Position(self):
        """
        Returns the player's position
        :return: String
        """

        return self.position



def main():
    ash = Player("Ashish", "manchester", "Forward" )
    print(ash.name, ash.team )

if __name__ == "__main__":
    main()