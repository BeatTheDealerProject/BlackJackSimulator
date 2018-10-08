
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
            if not player.surrendeflg:
                # プレイヤーがバーストした場合
                if player.burst == True:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotallose(player.betMoney)
                                break
                    player.addtotallose(player.betMoney)

                # プレイヤーがバーストせずにディーラーがバーストした場合
                elif player.burst == False and self.dealer.burst == True:
                    # スプリットしているかどうかのフラグ
                    spflg = False
                    for x in self.players:
                        if x.tag == "clone":
                            spflg = True

                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                if player.naturalbj and not spflg:
                                    self.players[i].addtotalwin(player.betMoney*1.5)
                                    break
                                else:
                                    self.players[i].addtotalwin(player.betMoney)
                                    break
                    if player.naturalbj and not spflg:
                        player.addtotalwin(player.betMoney*1.5)
                    else:
                        player.addtotalwin(player.betMoney)

                # プレイヤーのトータルがディーラーのトータルよりも多い場合
                elif player.total > self.dealer.total:
                    spflg = False
                    for x in self.players:
                        if player.tag=="clone":
                            spflg = True

                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                if player.naturalbj and not spflg:
                                    self.players[i].addtotalwin(player.betMoney*1.5)
                                    break
                                else:
                                    self.players[i].addtotalwin(player.betMoney)
                                    break
                    if player.naturalbj and not spflg:
                        player.addtotalwin(player.betMoney*1.5)
                    else:
                        player.addtotalwin(player.betMoney)

                # プレイヤーのトータルがディーラーのトータルよりも少ない場合
                elif player.total < self.dealer.total:
                    if player.tag == "clone":
                        for i, x in enumerate(self.players):
                            if x.name == player.name:
                                self.players[i].addtotallose(player.betMoney)
                                break
                    player.addtotallose(player.betMoney)

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
                    # プレイヤーがナチュラルブラックジャックかつディーラーがノーマルブラックジャック
                    elif player.naturalbj and self.dealer.normalbj:
                        if player.tag == "clone":
                            for i, x in enumerate(self.players):
                                if x.name == player.name:
                                    self.players[i].addtotalwin(player.betMoney * 1.5)
                                    break
                        player.addtotalwin(player.betMoney * 1.5)
                    # プレイヤーがノーマルブラックジャックかつディーラーがナチュラルブラックジャック
                    elif player.normalbj and self.dealer.naturalbj:
                        if player.tag == "clone":
                            for i, x in enumerate(self.players):
                                if x.name == player.name:
                                    self.players[i].addtotallose(player.betMoney)
                                    break
                        player.addtotallose(player.betMoney)
                    # プレイヤーがノーマルブラックジャックかつディーラーがノーマルブラックジャック
                    elif player.normalbj and self.dealer.normalbj:
                        if player.tag == "clone":
                            for i, x in enumerate(self.players):
                                if x.name == player.name:
                                    self.players[i].addtotaldraw()
                                    break
                        player.addtotaldraw()
                    else:
                        if player.tag == "clone":
                            for i, x in enumerate(self.players):
                                if x.name == player.name:
                                    self.players[i].addtotaldraw()
                                    break
                        player.addtotaldraw()

    # ナチュラルブラックジャックとノーマルブラックジャックを判別する関数
    # 入力にプレイヤー個人またはディーラ－個人を与える
    def checkblackjack(self, player):
        if player.total == 21:
            if len(player.cards) == 2:
                player.naturalbj = True
            else:
                player.normalbj = True

