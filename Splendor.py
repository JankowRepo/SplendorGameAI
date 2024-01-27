from enum import Enum
import random

import pandas as pd


class Colors(Enum):
    Green = 0
    Black = 1
    Red = 2
    Blue = 3
    White = 4


class CardRarity(Enum):
    Common = 0
    Rare = 1
    Epic = 2
    Special = 3


class Board:
    deck_common_cards = []
    deck_rare_cards = []
    deck_epic_cards = []
    deck_special_cards = []

    available_common_cards = []
    available_rare_cards = []
    available_epic_cards = []
    available_special_cards = []

    coins = []

    players = []

    def __init__(self, number_of_players, deck: pd.DataFrame):
        self.deck_common_cards = self.DrawDeck(CardRarity.Common, deck)
        self.deck_rare_cards = self.DrawDeck(CardRarity.Rare, deck)
        self.deck_epic_cards = self.DrawDeck(CardRarity.Epic, deck)
        self.deck_special_cards = self.DrawDeck(CardRarity.Special, deck)
        self.available_common_cards = self.DrawCards(self.deck_common_cards, 3)
        self.available_rare_cards = self.DrawCards(self.deck_rare_cards, 3)
        self.available_epic_cards = self.DrawCards(self.deck_epic_cards, 3)
        self.available_special_cards = self.DrawCards(self.deck_special_cards, 3)
        self.coins = self.GetCoins(5)
        self.players = self.CreatePlayers(number_of_players)

    def DrawDeck(self, rarity: CardRarity, deck: pd.DataFrame):
        deck_part = deck[deck["Rarity"] == rarity.name]
        cards = [Card(deck_part[i]) for i in range(len(deck_part))]
        return cards

    def DrawCards(self, deck: list, quantity: int):
        cards = random.sample(deck, quantity)
        return cards

    def GetCoins(self, quantity: int):
        lists_of_coins = [[Coin(color) for color in Colors] for i in range(quantity)]
        coins = [coin for coins in lists_of_coins for coin in coins]
        return coins

    def CreatePlayers(self, number_of_players: int):
        players = [Player(self) for i in range(number_of_players)]
        return players


class Coin:
    color: Colors = None

    def __init__(self, color):
        self.color = color


class Card:
    green_coin_cost = 0
    black_coin_cost = 0
    red_coin_cost = 0
    blue_coin_cost = 0
    white_coin_cost = 0
    value: int = 0
    rarity: CardRarity = None
    color: Colors = None

    def __init__(self, card_info: pd.DataFrame):
        self.green_coin_cost = card_info[0].green_coin_cost
        self.black_coin_cost = card_info[0].black_coin_cost
        self.red_coin_cost = card_info[0].red_coin_cost
        self.blue_coin_cost = card_info[0].blue_coin_cost
        self.white_coin_cost = card_info[0].white_coin_cost
        self.value = card_info[0].value
        self.rarity = card_info[0].rarity
        self.color = card_info[0].color


class Player:
    board: Board = None
    cards = []
    coins = []
    points: int = 0

    def __init__(self, board: Board):
        self.board = board

    def DrawTwoSameCoins(self, coin_color: Colors):
        # Add code to prevent having more than 9 coins
        try:
            typed_coins = list((coin for coin in self.board.coins if coin.color == coin_color))[:2]
            self.coins = self.coins + typed_coins
            self.board.coins = [coins for coins in self.board.coins if coins not in typed_coins]
        except Exception as e:
            print("Error", e)

    def DrawThreeOtherCoins(self, coin_color1: Colors, coin_color2: Colors, coin_color3: Colors):
        # Add code to prevent having more than 9 coins
        try:
            typed_coin_1 = list((coin for coin in self.board.coins if coin.color == coin_color1))[0]
            typed_coin_2 = list((coin for coin in self.board.coins if coin.color == coin_color2))[0]
            typed_coin_3 = list((coin for coin in self.board.coins if coin.color == coin_color3))[0]
            typed_coins = [typed_coin_1, typed_coin_2, typed_coin_3]
            self.coins = self.coins + typed_coins
            self.board.coins = [coins for coins in self.board.coins if coins not in typed_coins]
        except Exception as e:
            print("Error", e)

    def BuyCard(self, card: Card):
        try:
            if self.IsWealthEnough():
                self.ReturnCoinsToBoard(card)
                self.DrawCard(card)
            else:
                print("Brak zasobów")
        except Exception as e:
            print("Error", e)

    def DrawCard(self, card: Card):
        try:
            self.cards.append(card)
            self.CountPoints()
        except Exception as e:
            print("Error", e)

    def CountPoints(self):
        points = [card.value for card in self.cards]
        self.points = sum(points)

    def ReturnCoinsToBoard(self, card: Card):
        self.SendChoosenColorCoinsToBoard(card.green_coin_cost, Colors.Green)
        self.SendChoosenColorCoinsToBoard(card.black_coin_cost, Colors.Black)
        self.SendChoosenColorCoinsToBoard(card.red_coin_cost, Colors.Red)
        self.SendChoosenColorCoinsToBoard(card.blue_coin_cost, Colors.Blue)
        self.SendChoosenColorCoinsToBoard(card.white_coin_cost, Colors.White)

    def SendChoosenColorCoinsToBoard(self, cost: int, color: Colors):
        for i in range(cost):
            typed_coin = list((coin for coin in self.coins if coin.color == color))[0]
            self.board.coins.append(typed_coin)
            self.coins.remove(typed_coin)

    def IsWealthEnough(self):
        return True
