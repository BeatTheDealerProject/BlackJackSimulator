from blackjacksimulator.BlackJackSimulator import simulate

import argparse
import json


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

strategy =[['h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h'],  # 4
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
          ]

simulate(strategy, config)
