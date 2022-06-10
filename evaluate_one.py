import pickle

from douzero.env.game import GameEnv


def load_card_play_models(card_play_model_path_dict):
    players = {}

    for position in ['landlord', 'landlord_up', 'landlord_down']:
        if card_play_model_path_dict[position] == 'rlcard':
            from douzero.evaluation.rlcard_agent import RLCardAgent
            players[position] = RLCardAgent(position)
        elif card_play_model_path_dict[position] == 'random':
            from douzero.evaluation.random_agent import RandomAgent
            players[position] = RandomAgent()
        else:
            from douzero.evaluation.deep_agent import DeepAgent
            players[position] = DeepAgent(position, card_play_model_path_dict[position])
    return players


if __name__ == '__main__':
    card_play_model_path_dict = {
        'landlord': 'baselines/douzero_ADP/landlord.ckpt',
        'landlord_up': 'baselines/sl/landlord_up.ckpt',
        'landlord_down': 'baselines/sl/landlord_down.ckpt'
    }
    players = load_card_play_models(card_play_model_path_dict)

    with open('eval_data.pkl', 'rb') as f:
        card_play_data_list = pickle.load(f)

    num_total_wins = 0
    num_landlord_wins = 0
    num_landlord_scores = 0
    num_farmer_wins = 0
    num_farmer_scores = 0

    for i in range(len(card_play_data_list)):
        card_play_data = card_play_data_list[i]

        env = GameEnv(players)
        env.card_play_init(card_play_data)
        while not env.game_over:
            env.step()

        print(env.debug_record)
        env.reset()

        num_landlord_wins += env.num_wins['landlord']
        num_farmer_wins += env.num_wins['farmer']
        num_landlord_scores += env.num_scores['landlord']
        num_farmer_scores += env.num_scores['farmer']

        num_total_wins = num_landlord_wins + num_farmer_wins

        print("获胜次数（地主/农民） [{} : {}] 获胜得分（地主/农民） [{} : {}] 胜率（地主/农民） [{}% : {}%] 总得分（地主/农民） [{} : {}]".format(
            env.num_wins['landlord'], env.num_wins['farmer'] * 2, env.num_scores['landlord'], env.num_scores['farmer'] * 2,
            round(num_landlord_wins / num_total_wins * 100), round(num_farmer_wins / num_total_wins * 100),
            round(num_landlord_scores / num_total_wins * 100), round(2 * num_farmer_scores / num_total_wins * 100)
        ))
