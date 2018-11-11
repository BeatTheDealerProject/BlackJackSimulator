"""
ディーラーを定義するクラス
ディーラーがデッキを管理しているイメージなのでディーラークラスの中にデッキを作成している
カードを配る処理はこのクラスに記述していく
"""

from .GamePlayer import GamePlayer
from .Deck import Deck


class Dealer(GamePlayer):
    # ディーラーの初期化
    def __init__(self, deckNum):
        self.deck = Deck(deckNum)
        self.totaldealerhandlist = [0] * 6
        # ディーラーがシャッフルする回数。今回は10000回シャッフルする。
        self.shufflenum = 10000
        self.deck.shuffle(deckNum * self.shufflenum)
        super().__init__()

    # カードを配る関数
    def dealcard(self):
        card = self.deck.Cards[self.deck.current]
        self.deck.current += 1
        if self.deck.current == len(self.deck.Cards):
            self.deck.current = 0
        return card

    # 一番最初にカードを配る際の関数
    def firstdeal(self, player):
        super().__init__()
        for x in player:
            x.initialize()
        firstdeal = 2
        while firstdeal > 0:
            self.cards.append(self.dealcard())
            for x in player:
                x.cards.append(self.dealcard())
            firstdeal -= 1

    # 合計が17を超えるまで続ける処理
    def continuehit(self):
        self.totalvalue()
        while (self.total < 17):
            self.cards.append(self.dealcard())
            self.totalvalue()


