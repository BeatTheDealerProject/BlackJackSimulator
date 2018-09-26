'''
プレイヤーを定義するクラス
ヒット、スタンドなどのプレイヤーが選択する処理は個々に記述する
name:プレイヤー名, cards:プレイヤー個人の手札, total:プレイヤー個人の手札の合計値,
acetotal:プレイヤーのace所持数でバーストした際などの使用する,burst:Trueでプレイヤーがバーストしていることを示す
'''


from BlackJack.GamePlayer import *

class Player(GamePlayer):
    # プレイヤーの初期化
    def __init__(self, name):
        self.name = name
        self.totalwin = 0
        self.totallose = 0
        super().__init__()

    # プレイヤーにカードを配るときに使用する関数
    def dealedcard(self, card):
        self.cards.append(card)

    # プレイヤー側のヒットの処理
    def hit(self, dealer):
        self.dealedcard(dealer.dealcard())
        self.showhands()

    # プレイヤー側のスタンドの処理
    def stand(self):
        # self.showhands()
        pass

    # プレイヤ－側のダブルダウンの処理
    def doubledown(self, dealer):
        self.hit(dealer)

    # プレイヤー側のスプリットの処理
    def split(self):
        pass

    # 自身の手札を表示するUI
    def showhands(self):
        self.totalvalue()
        # print("---hands---")
        for x in self.cards:
            pass
            # print('/', x.suit, x.rank)
        # print("---total---: ", self.total, "\n")

    # プレイヤーの勝利回数を増やす
    def addtotalwin(self):
        self.totalwin += 1

    # プレイヤーの敗北回数を増やす
    def addtotallose(self):
        self.totallose += 1

