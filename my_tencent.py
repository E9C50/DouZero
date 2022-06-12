import my_cards_scan as mcs
from douzero.env.game import GameEnv

AllEnvCard = [
    3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10,
    11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 17, 17, 17, 17, 20, 30
]

AllCards = [
    'rD', 'bX', 'b2', 'r2', 'bA', 'rA', 'bK', 'rK', 'bQ', 'rQ', 'bJ', 'rJ', 'bT', 'rT',
    'b9', 'r9', 'b8', 'r8', 'b7', 'r7', 'b6', 'r6', 'b5', 'r5', 'b4', 'r4', 'b3', 'r3'
]

EnvCard2RealCard = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'
}

RealCard2EnvCard = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30
}

PLAYER_MODEL = 'baselines/douzero_WP/{}.ckpt'


def load_card_players(player_position):
    players_result = {}
    for position in ['landlord', 'landlord_up', 'landlord_down']:
        if position == player_position:
            from douzero.evaluation.deep_agent import DeepAgent
            players_result[position] = DeepAgent(position, PLAYER_MODEL.format(position))
        else:
            from douzero.evaluation.auto_scan_agent import AutoScanAgent
            players_result[position] = AutoScanAgent(position, player_position)
    return players_result


if __name__ == '__main__':
    # 玩家手牌
    user_hand_cards_real = mcs.find_my_cards()
    user_hand_cards_env = [RealCard2EnvCard[c] for c in list(user_hand_cards_real)]

    # 三张底牌
    three_landlord_cards_real = input("请输入三张底牌：")
    three_landlord_cards_env = [RealCard2EnvCard[c] for c in list(three_landlord_cards_real)]

    # 玩家角色代码：0-地主上家, 1-地主, 2-地主下家
    user_position_code = int(input("请输入您的角色（0-地主上家, 1-地主, 2-地主下家）："))
    user_position = ['landlord_up', 'landlord', 'landlord_down'][user_position_code]

    other_hand_cards = []  # 其他玩家手牌（整副牌减去玩家手牌，后续再减掉历史出牌）
    card_play_data_list = {}  # 开局时三个玩家的手牌

    # 整副牌减去玩家手上的牌，就是其他人的手牌,再分配给另外两个角色（如何分配对AI判断没有影响）
    for i in set(AllEnvCard):
        other_hand_cards.extend([i] * (AllEnvCard.count(i) - user_hand_cards_env.count(i)))
    card_play_data_list.update({
        'three_landlord_cards': three_landlord_cards_env,
        ['landlord_up', 'landlord', 'landlord_down'][(user_position_code + 0) % 3]: user_hand_cards_env,
        ['landlord_up', 'landlord', 'landlord_down'][(user_position_code + 1) % 3]: other_hand_cards[0:17] if (user_position_code + 1) % 3 != 1 else other_hand_cards[17:],
        ['landlord_up', 'landlord', 'landlord_down'][(user_position_code + 2) % 3]: other_hand_cards[0:17] if (user_position_code + 1) % 3 == 1 else other_hand_cards[17:]
    })
    print(card_play_data_list)

    # # 生成手牌结束，校验手牌数量
    # if len(card_play_data_list["three_landlord_cards"]) != 3:
    #     print("底牌识别出错", "底牌必须是3张！")
    # if len(card_play_data_list["landlord_up"]) != 17 or len(card_play_data_list["landlord_down"]) != 17 or len(card_play_data_list["landlord"]) != 20:
    #     print("手牌识别出错", "初始手牌数目有误")

    # 创建玩家和AI
    players = load_card_players(user_position)

    # 开始游戏
    env = GameEnv(players, user_position)
    env.card_play_init(card_play_data_list)
    while not env.game_over:
        env.step()


    print(env.debug_record)
    env.reset()

    print("获胜次数（地主/农民） [{} : {}] 获胜得分（地主/农民） [{} : {}]".format(
        env.num_wins['landlord'], env.num_wins['farmer'] * 2, env.num_scores['landlord'], env.num_scores['farmer'] * 2
    ))
