"""
メイン関数
ゲーム全体の流れをここに記述する
プレイヤーの追加はここで手動で行ってください
"""

from BlackJack.Player import *
from BlackJack.Dealer import *
from BlackJack.GameManager import *


def main(strategy):
    # プレイヤーを作成
    p1 = Player("player1")
    #    p2 = Player("player2")
    #    players = [p1, p2]

    # ゲームに参加するプレイヤーを表現
    players = [p1]

    # ディーラーの作成
    # 引数はゲームに使用するデッキの数を表現
    dealer = Dealer(1)

    # カットカードを表現
    # 今回はデッキの1/2の位置にカットカードを固定している
    cutcard = len(dealer.deck.Cards) / 2

    # txtデータとして出力するものをstring形式で初期化
    text = ""
    debagText = ""

    # ゲーム全体のループ回数
    totalGameNum = remainingGameNum = 1000

    split_strategy = [["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 2,2
                      ["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 3,3
                      ["H", "H", "H", "P", "P", "H", "H", "H", "H", "H"],  # 4,4
                      ["D", "D", "D", "D", "D", "D", "D", "D", "H", "H"],  # 5,5
                      ["P", "P", "P", "P", "P", "H", "H", "H", "H", "H"],  # 6,6
                      ["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 7,7
                      ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"],  # 8,8
                      ["P", "P", "P", "P", "P", "S", "P", "P", "S", "S"],  # 9,9
                      ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 10,10
                      ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"],  # A,A
                      ]

    # メインループ
    while True:
        # ゲームを始める前にデッキの中からカットカードが出てきているかを確認し、出てきていれば、デッキをシャッフルする
        if dealer.deck.current > cutcard:
            dealer.deck.shuffle(dealer.shufflenum)

        # ディーラーが各プレイヤー（自身含む）に初期カードを配る
        dealer.firstdeal(players)

        # 各プレイヤーの点数を更新
        for player in players:
            player.totalvalue()

        # スプリットするかどうかを先に確認する
        for i, player in enumerate(players):
            if player.cards[0].rank == player.cards[1].rank:
                usermessage = split_strategy[player.cards[0].value - 2][dealer.cards[0].value - 2]
                if usermessage == 'P' or usermessage == 'p':

                    # プレイヤーのクローンを作成し、ゲームに参加するプレイヤーとして追加登録する
                    playerClone = Player(player.name, "clone")
                    players.insert(i+1, playerClone)

                    # クローンにプレイヤーが所持しているカードを一枚渡す
                    playerClone.dealedcard(player.cards[1])
                    del player.cards[1]

                    # 使用済みAの数を初期化する
                    player.usedace = 0
                    playerClone.usedace = 0

                    # プレイヤーとクローンにカードを配り直す
                    player.dealedcard(dealer.dealcard())
                    playerClone.dealedcard(dealer.dealcard())

        # 各プレイヤーに対して選択肢を提示する
        for i, player in enumerate(players):
            while remainingGameNum > 0:
                # プレイヤーの選択はベーシックストラテジーに沿って行われるものとする
                # プレイヤーの手札にA(11)が残っている場合
                if player.acetotal - player.usedace > 0:
                    usermessage = strategy[player.total + 6][dealer.cards[0].value - 2]
                # プレイヤーの手札にA(11)が残っていない場合
                else:
                    usermessage = strategy[player.total - 4][dealer.cards[0].value - 2]

                # プレイヤーの選択による行動の分岐を記述
                # プレイヤーがヒットを選択した場合
                if usermessage == 'H' or usermessage == 'h':
                    # print("hit\n")
                    player.hit(dealer)
                    if (player.burst == True):
                        break
                # プレイヤーがスタンドを選択した場合
                elif usermessage == 'S' or usermessage == 's':
                    # print("stand\n")
                    player.stand()
                    break
                # プレイヤーがダブルダウンを選択した場合
                elif usermessage == 'D' or usermessage == 'd':
                    player.doubledown(dealer)
                    break

        # ディーラーは17を超えるまでヒットを続ける
        dealer.continuehit()

        # GameManagerの初期化
        gamemanager: GameManager = GameManager(players, dealer)

        # 勝敗を判定する
        gamemanager.judge()

        # デバッグ
        for player in players:
            debagText += "\n" + str(remainingGameNum) +  "\n" + player.name +"-" + player.tag + "\n"
            for card in player.cards:
                debagText += str(card.value) + "-"
            debagText += "player total = " + str(player.total) + "\n"

        debagText += "\ndealer\n"
        for card in dealer.cards:
            debagText += str(card.value) + "-"
        debagText += "dealer total = " + str(dealer.total)
        debagText += "\n\n-----------------------\n\n"

        # クローンを削除する
        for i, player in enumerate(players):
            if player.tag == "clone":
                del players[i]

        if remainingGameNum % 100 == 0:
            print(remainingGameNum)

        # ループの処理
        remainingGameNum -= 1
        if remainingGameNum == 0:
            for player in players:
                file = open('result.txt', 'w')
                text += "win : " + str(player.totalwin) + "\nlose : " + str(player.totallose) + \
                        "\ndraw : " + str(player.totaldraw)
                file.writelines(text)

                debagfile = open('debag.txt', 'w')
                debagfile.writelines(debagText)
                break
            break


# デッキ確認用関数
def showdeck():
    dealer = Dealer(2)
    i = 0
    for x in dealer.deck.Cards:
        print(i + 1, x.suit, x.rank)
        i += 1


if __name__ == "__main__":
    main([['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 4
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 5
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 6
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 7
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 8
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 9
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 10
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 11
          ['h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 12
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 13
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 14
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 15
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 16
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 17
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 18
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 19
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 20
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 21
          # ここからはAがある場合のストラテジー表
          ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # AA
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # A2
          ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # A3
          ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # A4
          ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # A5
          ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # A6
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'H', 'H', 'S'],  # A7
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A8
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A9
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']  # A10
          ])
    # デッキ確認用のデバッグ関数
    # showdeck()
