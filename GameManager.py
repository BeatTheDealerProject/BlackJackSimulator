
"""
ゲームを管理するクラス
主にゲームの勝敗に関連する事柄を管理するのでデッキ自体の操作などは行わない
"""


class GameManager:
    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        self.checkdeal = True

    # 各プレイヤーとディーラーとの間で勝敗を決める
    def judge(self):
        for x in self.players:
            self.checkblackjack(x)
        self.checkblackjack(self.dealer)
        for player in self.players:
            # プレイヤーがバーストした場合
            if player.burst == True:
                if player.tag == "clone":
                    for i, x in enumerate(self.players):
                        if x.name == player.name:
                            self.players[i].addtotallose()
                            break
                player.addtotallose()
                # print(player.name, "lose (player burst)")
            # プレイヤーがバーストせずにディーラーがバーストした場合
            elif player.burst == False and self.dealer.burst == True:
                if player.tag == "clone":
                    for i, x in enumerate(self.players):
                        if x.name == player.name:
                            self.players[i].addtotalwin()
                            break
                player.addtotalwin()
                # print(player.name, "win (dealer burst)")
            # プレイヤーのトータルがディーラーのトータルよりも多い場合
            elif player.total > self.dealer.total:
                if player.tag == "clone":
                    for i, x in enumerate(self.players):
                        if x.name == player.name:
                            self.players[i].addtotalwin()
                            break
                player.addtotalwin()
                # print(player.name, "win (player>dealer)")
            # プレイヤーのトータルがディーラーのトータルよりも少ない場合
            elif player.total < self.dealer.total:
                if player.tag == "clone":
                    for i, x in enumerate(self.players):
                        if x.name == player.name:
                            self.players[i].addtotallose()
                            break
                player.addtotallose()
                # print(player.name, "lose (player<dealer)")
            # プレイヤーのトータルとディーラーのトータルが同じ場合
            elif player.total == self.dealer.total:
                # プレイヤーがナチュラルブラックジャックかつディーラーがナチュラルブラックジャック
                if player.naturalbj and self.dealer.naturalbj:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotaldraw()
                                break
                    player.addtotaldraw()
                    # print(player.name, "draw (natural vs natural)")
                # プレイヤーがナチュラルブラックジャックかつディーラーがノーマルブラックジャック
                elif player.naturalbj and self.dealer.normalbj:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotalwin()
                                break
                    player.addtotalwin()
                    # print(player.name, "win (natural vs normal)")
                # プレイヤーがノーマルブラックジャックかつディーラーがナチュラルブラックジャック
                elif player.normalbj and self.dealer.naturalbj:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotallose()
                                break
                    player.addtotallose()
                    # print(player.name, "lose (normal vs natural)")
                # プレイヤーがノーマルブラックジャックかつディーラーがノーマルブラックジャック
                elif player.normalbj and self.dealer.normalbj:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotaldraw()
                                break
                    player.addtotaldraw()
                    # print(player.name, "draw (normal vs normal)")
                else:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotalwin()
                                break
                    player.addtotaldraw()
                    # print(player.name, " draw (player==dealer)")

    # ナチュラルブラックジャックとノーマルブラックジャックを判別する関数
    # 入力にプレイヤー個人またはディーラ－個人を与える
    def checkblackjack(self, player):
        if player.total == 21:
            if len(player.cards) == 2:
                player.naturalbj = True
            else:
                player.normalbj = True

