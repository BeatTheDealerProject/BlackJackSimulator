"""
メイン関数
ゲーム全体の流れをここに記述する
プレイヤーの追加はここで手動で行ってください
"""

import argparse
import json
from Player import Player
from Dealer import Dealer
from GameManager import GameManager

def main(strategy, config):
    # プレイヤーを作成
    p1 = Player("player1")

    # ゲームに参加するプレイヤーを表現
    players = [p1]

    # ディーラーの作成
    # 引数はゲームに使用するデッキの数を表現
    dealer = Dealer(config['decknum'])

    # カットカードを表現
    # 今回はデッキの1/2の位置にカットカードを固定している
    cutcard = len(dealer.deck.Cards) / 2

    # txtデータとして出力するものをstring形式で初期化
    text = ""
    debugtext = ""

    # ゲーム全体のループ回数
    totalGameNum = remainingGameNum = config['gamenum']

    # 最小ベットの宣言
    minbet = config['minbet']

    # 最大ベットの宣言
    maxbet = config['maxbet']

    # 初回起動時のみファイルを上書きで開く
    opened_file = False

    split_strategy = [["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 2,2
                      ["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 3,3
                      ["H", "H", "H", "P", "P", "H", "H", "H", "H", "H"],  # 4,4
                      ["D", "D", "D", "D", "D", "D", "D", "D", "H", "H"],  # 5,5
                      ["P", "P", "P", "P", "P", "H", "H", "H", "H", "H"],  # 6,6
                      ["P", "P", "P", "P", "P", "P", "H", "H", "H", "H"],  # 7,7
                      ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"],  # 8,8
                      ["P", "P", "P", "P", "P", "S", "P", "P", "S", "S"],  # 9,9
                      ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"],  # 10,10
                      ["P", "P", "P", "P", "P", "P", "P", "P", "P", "P"]  # A,A
                      ]

    # メインループ
    for gamecount in range(totalGameNum):
        # ゲームを始める前にデッキの中からカットカードが出てきているかを確認し、出てきていれば、デッキをシャッフルする
        if dealer.deck.current > cutcard:
            dealer.deck.shuffle(dealer.shufflenum)

        # 各プレイヤーのベット
        for player in players:
            player.bet(minbet)

        # 参加プレイヤーの初期化を実行後、ディーラーが各プレイヤー（自身含む）に初期カードを配る
        dealer.firstdeal(players)

        # 各プレイヤーの点数を更新
        for player in players:
            player.totalvalue()

        # サレンダーの回数を記録する
        surrenderCounter = 0

        # スプリットするかどうかを確認する
        for i, player in enumerate(players):
            if player.cards[0].rank == player.cards[1].rank:
                usermessage = split_strategy[player.cards[0].value - 2][dealer.cards[0].value - 2]
                if usermessage == 'P' or usermessage == 'p':
                    # プレイヤーのクローンを作成し、ゲームに参加するプレイヤーとして追加登録する
                    playerClone = Player(player.name, betMoney=player.betMoney, tag="clone")
                    players.insert(i + 1, playerClone)

                    # クローンにプレイヤーが所持しているカードを一枚渡す
                    playerClone.dealedcard(player.cards[1])
                    del player.cards[1]

                    # 使用済みAの数を初期化する
                    player.usedace = 0
                    playerClone.usedace = 0

                    # プレイヤーとクローンにカードを配り直す
                    player.dealedcard(dealer.dealcard())
                    playerClone.dealedcard(dealer.dealcard())

        for player in players:
            if player.tag == "clone":
                players[0].totalsplit += 1

        # 各プレイヤーに対して選択肢を提示する
        for player in players:
            while True:
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
                    player.hit(dealer)
                    if player.burst:
                        break

                # プレイヤーがスタンドを選択した場合
                elif usermessage == 'S' or usermessage == 's':
                    player.stand()
                    break

                # プレイヤーがダブルダウンを選択した場合
                elif usermessage == 'D' or usermessage == 'd':
                    # ヒット後にはダブルダウンの選択不可
                    if len(player.cards) == 2:
                        player.doubledown(dealer)
                        break
                    else:
                        player.hit(dealer)
                        if player.burst:
                            break

                # プレイヤーがサレンダーを選択した場合
                elif usermessage == "R" or usermessage == "r":
                    # ヒット後にはサレンダーの選択不可
                    if len(player.cards) == 2:
                        player.surrender()
                        if player.tag == "clone":
                           players[0].totalsurrender += 1
                        surrenderCounter += 1
                        break
                    else:
                        player.hit(dealer)
                        if player.burst:
                            break

        # ディーラーは17を超えるまでヒットを続ける
        dealer.continuehit()

        # GameManagerの初期化
        gamemanager = GameManager(players, dealer)

        # 勝敗を判定する
        gamemanager.judge()

        # プレイヤーハンドの合計値の回数を記録する
        for player in players:
            if player.total > 21:
                player.totalplayerhandlist[len(player.totalplayerhandlist) - 1] += 1
            elif player.total < 10:
                pass
            else:
                player.totalplayerhandlist[player.total - 10] += 1

        if dealer.total > 21:
            dealer.totaldealerhandlist[len(dealer.totaldealerhandlist) - 1] += 1
        else:
            dealer.totaldealerhandlist[dealer.total - 17] += 1


        # クローンを削除する
        while True:
            cloneflg = False
            for i, player in enumerate(players):
                if player.tag == "clone":
                    del player
                    del players[i]
                    cloneflg = True
            if not cloneflg:
                break

        # ファイル入出力
        if gamecount % 10000 == 0:
            debugtext = Debug(dealer, players, gamecount, debugtext)
            if config['exportdebug']:
                if opened_file:
                    debugfile = open('debug.txt', 'a')
                    debugfile.writelines(debugtext)
                    debugtext = ""
                else:
                    opened_file = True
                    debugfile = open('debug.txt', 'w')
                    debugfile.writelines(debugtext)
                    debugtext = ""


    result = []
    for player in players:
        result.append(player.GetPlayerResultData())
        
    if config['exportresult']:
        for player in players:
            file = open('result.txt', 'w')
            text += "win : {0}\nlose : {1}\ndraw : {2}\nsplit : {3}\nsurrender :{4}\nmoney : {5}\ntotal{6}".format(
                str(player.totalwin), str(player.totallose), str(player.totaldraw), str(player.totalsplit),
                str(player.totalsurrender), str(player.money), str(
                    player.totalwin + player.totallose + player.totaldraw + player.totalsurrender - player.totalsplit))
            text += "\n\n--- total player hand --- "
            for i, x in enumerate(player.totalplayerhandlist):
                if i == len(player.totalplayerhandlist) - 1:
                    text += "\nburst : " + str(x)
                else:
                    text += "\n" + str(i+10) + " : " + str(x)
            text += "\n\n--- total dealer hand --- "
            for i, x in enumerate(dealer.totaldealerhandlist):
                if i == len(dealer.totaldealerhandlist) - 1:
                    text += "\nburst : " + str(x)
                else:
                    text += "\n"+ str(i+17) + " : " + str(x)
            file.writelines(text)
            break
    return result

def Debug(dealer, players, gamenum, debugtext):
    # デバッグ
    for player in players:
        debugtext += "\n" + str(gamenum) + "\n" + player.name + "-" + player.tag + "\n"
        debugtext += str(player.betMoney) + "\n"
        debugtext += player.debugtxt + "\n"
        player.debugtxt = ""
        for card in player.cards:
            debugtext += str(card.value) + "-"
        debugtext += "player total = " + str(player.total) + "\n"
    debugtext += "\ndealer\n"
    for card in dealer.cards:
        debugtext += str(card.value) + "-"
    debugtext += "dealer total = " + str(dealer.total)
    if len(players) > 0:
        debugtext += "\ntotal:" + str(players[0].money)
    debugtext += "\n\n-----------------------\n\n"

    return debugtext
    

# デッキ確認用関数
def showdeck():
    dealer = Dealer(2)
    i = 0
    for x in dealer.deck.Cards:
        print(i + 1, x.suit, x.rank)
        i += 1


if __name__ == "__main__":
    #コマンドライン引数についての設定
    parser = argparse.ArgumentParser(
                prog="blackjack",
                usage="python blackjack [simulator config file]",
                description="",
                epilog="",
                add_help=True
              )
    #GAに関する設定ファイルを指定する引数
    parser.add_argument(
        "simulatorconfigfile",
        help="The json file what configures ga simulation."
    )

    args = parser.parse_args()

    configfile = args.simulatorconfigfile
    with open(configfile, "r") as f:
        config = json.load(f)

    # """
    main([['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 4
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 5
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 6
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 7
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 8
          ['h', 'd', 'd', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # 9
          ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h', 'h'],  # 10
          ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'd', 'h'],  # 11
          ['h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 12
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 13
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h'],  # 14
          ['s', 's', 's', 's', 's', 'h', 'h', 'h', 'r', 'h'],  # 15
          ['s', 's', 's', 's', 's', 'h', 'h', 'r', 'r', 'r'],  # 16
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 17
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 18
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 19
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 20
          ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],  # 21
          # ここからはAがある場合のストラテジー表
          ['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # AA
          ['h', 'h', 'h', 'd', 'd', 'h', 'h', 'h', 'h', 'h'],  # A2
          ['H', 'H', 'H', 'd', 'd', 'H', 'H', 'H', 'H', 'H'],  # A3
          ['H', 'H', 'd', 'd', 'd', 'H', 'H', 'H', 'H', 'H'],  # A4
          ['H', 'H', 'd', 'd', 'd', 'H', 'H', 'H', 'H', 'H'],  # A5
          ['H', 'd', 'd', 'd', 'd', 'H', 'H', 'H', 'H', 'H'],  # A6
          ['S', 'd', 'd', 'd', 'd', 'S', 'S', 'H', 'H', 'S'],  # A7
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A8
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A9
          ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']  # A10
          ], config)
    # """
    # デッキ確認用のデバッグ関数
    # showdeck()
