"""
Cardクラスからデッキを作成するクラス
使用するデッキの数と、デッキのシャッフル、使用している山札を担当する
実際のカードが入っているのはDeckの中のCardsなので注意すること
"""

import random
from BlackJack.Card import *


class Deck:
    CARDS = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
    Cards = []
    BaseDeck = []
    for rank in Card.RANKS:
        for suit in Card.SUITS:
            BaseDeck.append(Card(rank, suit))  # オブジェクト共有を回避するための基本となる一デッキ

    # 初期化
    # decNumの数だけデッキを使用する
    def __init__(self, decNum):
        basedec = []
        while (decNum > 0):
            basedec += self.BaseDeck
            decNum -= 1
        self.Cards = basedec
        self.current = 0

    # シャッフルをする関数
    # shuffleNumに入れる数字によりシャッフルの回数を制御
    def shuffle(self, shuffleNum):
        self.current = 0
        while shuffleNum > 0:
            cut1 = random.randrange(0, len(self.Cards) / 2)
            cut2 = random.randrange(len(self.Cards) / 2, len(self.Cards))
            temp = self.Cards[cut1]
            self.Cards[cut1] = self.Cards[cut2]
            self.Cards[cut2] = temp
            shuffleNum -= 1
