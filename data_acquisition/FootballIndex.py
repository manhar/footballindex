#!/usr/bin/python

"""
Represents football index website

"""

import pandas as pd


class FootballIndex():

    def __init__(self, url, *args, **kwargs):
        """
        Initialize FootballIndex URL

        """
        self.url = url

    def pullData(self):
         """
         This function connects to the API and pull data

         :return : returns dataframe
         """
         try:
             return pd.read_json(self.url)
         except  Exception as e:
             raise e




    def getPlayers(self):
        """

        This function returns the list of players from football index
        :return: list of players

        """

        pass

    def getPrice(self, player):

        """
        This function returns the price of a player

        :param player: Player Name
        :return:
        """
        pass

    def loadToDB(self):
        """
        This funcion load player data to database

        :return: True is data loaded successfully else False
        """

if __name__ == "__main__":
    url = "https://api-prod.footballindex.co.uk/football.all?page=1&per_page=200&sort=asc"
    fi = FootballIndex(url)
    print(fi.pullData())