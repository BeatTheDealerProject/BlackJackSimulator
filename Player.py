"""
プレイヤーを定義するクラス
ヒット、スタンドなどのプレイヤーが選択する処理は個々に記述する
name:プレイヤー名, cards:プレイヤー個人の手札, total:プレイヤー個人の手札の合計値,
acetotal:プレイヤーのace所持数でバーストした際などの使用する,burst:Trueでプレイヤーがバーストしていることを示す
"""

from BlackJack.GamePlayer import *


class Player(GamePlayer):
    # プレイヤーの初期化
    def __init__(self, name, money=1000000, betMoney=0, tag="player"):
        # プレイヤー名
        self.name = name
        # 所持金
        self.money = money
        # ベット額(クローンに値を渡す際に使用する)
        self.betMoney = betMoney
        # 累計勝利回数、敗北回数、引き分け回数
        self.totalwin = 0
        self.totallose = 0
        self.totaldraw = 0
        self.totalsplit = 0
        self.totalsurrender = 0
        self.totalplayerhandlist = [0] * 12
        # プレイヤーとクローンを見分ける
        self.tag = tag
        self.debagtxt = ""
        super().__init__()

    # プレイヤーにカードを配るときに使用する関数
    def dealedcard(self, card):
        self.cards.append(card)
        self.totalvalue()

    # プレイヤー側のヒットの処理
    def hit(self, dealer):
        self.dealedcard(dealer.dealcard())
        self.debagtxt += "H"

    # プレイヤー側のスタンドの処理
    def stand(self):
        self.debagtxt += "S"
        pass

    # プレイヤ－側のダブルダウンの処理
    def doubledown(self, dealer):
        self.debagtxt += "D("
        self.betMoney *= 2
        self.hit(dealer)
        self.stand()
        self.debagtxt += ")"

    # サレンダーの処理
    def surrender(self):
        self.debagtxt += "R"
        self.totalsurrender += 1
        self.surrendeflg = True
        self.money -= self.betMoney/2

    # プレイヤー側のベットの処理
    def bet(self, betMoney):
        self.betMoney = betMoney

    # プレイヤーのインシュランスの処理
    def insurance(self, dealer):
        if dealer.cards[0] + dealer.cards[1] == 21:
            self.money += self.betMoney
        else:
            self.money -= self.betMoney/2

    # 自身の手札を表示するUI
    def showhands(self):
        for x in self.cards:
             print('/', x.suit, x.rank)
        print("---total---: ", self.total, "\n")

    # プレイヤーの勝利回数を増やす
    def addtotalwin(self, money):
        self.money += money
        self.totalwin += 1

    # プレイヤーの敗北回数を増やす
    def addtotallose(self, money):
        self.money -= money
        self.totallose += 1

    # プレイヤーの引き分け回数を増やす
    def addtotaldraw(self):
        self.totaldraw += 1

