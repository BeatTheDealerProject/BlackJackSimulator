
'''
ゲームを管理するクラス
主にゲームの勝敗に関連する事柄を管理するのでデッキ自体の操作などは行わない
'''


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
            if player.burst == True:
                player.addtotallose()
                # print(player.name, "lose (player burst)")
                return "lose"
            elif player.burst == False and self.dealer.burst == True:
                player.addtotalwin()
                # print(player.name, "win (dealer burst)")
                return "win"
            elif player.total > self.dealer.total:
                player.addtotalwin()
                # print(player.name, "win (player>dealer)")
                return "win"
            elif player.total < self.dealer.total:
                player.addtotallose()
                # print(player.name, "lose (player<dealer)")
                return "lose"
            elif player.total == self.dealer.total:
                if player.naturalbj and self.dealer.naturalbj:
                    # print(player.name, "draw (natural vs natural)")
                    return "draw"
                elif player.naturalbj and self.dealer.normalbj:
                    player.addtotalwin()
                    # print(player.name, "win (natural vs normal)")
                    return "win"
                elif player.normalbj and self.dealer.naturalbj:
                    player.addtotallose()
                    # print(player.name, "lose (normal vs natural)")
                    return "lose"
                elif player.normalbj and self.dealer.normalbj:
                    # print(player.name, "draw (normal vs normal)")
                    return "draw"
                else:
                    # print(player.name, " draw (player==dealer)")
                    return "draw"

    # ナチュラルブラックジャックとノーマルブラックジャックを判別する関数
    # 入力にプレイヤー個人またはディーラ－個人を与える
    def checkblackjack(self, player):
        if (player.total == 21):
            if (len(player.cards) == 2):
                player.naturalbj = True
            else:
                player.normalbj = True

