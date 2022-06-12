import numpy as np
import torch

import my_cards_scan as mcs
from douzero.env.env import get_obs

EnvCard2RealCard = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 17: '2', 20: 'X', 30: 'D'
}


def _load_model(position, model_path):
    from douzero.dmc.models import model_dict
    model = model_dict[position]()
    model_state_dict = model.state_dict()
    if torch.cuda.is_available():
        pretrained = torch.load(model_path, map_location='cuda:0')
    else:
        pretrained = torch.load(model_path, map_location='cpu')
    pretrained = {k: v for k, v in pretrained.items() if k in model_state_dict}
    model_state_dict.update(pretrained)
    model.load_state_dict(model_state_dict)
    if torch.cuda.is_available():
        model.cuda()
    model.eval()
    return model


class DeepAgent:

    def __init__(self, position, model_path):
        self.model = _load_model(position, model_path)
        self.position = position

    def act(self, infoset):
        # if len(infoset.legal_actions) == 1:
        #     return infoset.legal_actions[0]

        obs = get_obs(infoset)

        z_batch = torch.from_numpy(obs['z_batch']).float()
        x_batch = torch.from_numpy(obs['x_batch']).float()
        if torch.cuda.is_available():
            z_batch, x_batch = z_batch.cuda(), x_batch.cuda()
        y_pred = self.model.forward(z_batch, x_batch, return_value=True)['values']
        y_pred = y_pred.detach().cpu().numpy()

        best_action_index = np.argmax(y_pred, axis=0)[0]
        best_action = infoset.legal_actions[best_action_index]

        confidence = y_pred[best_action_index]

        real_cards = [EnvCard2RealCard[c] for c in list(best_action)]
        hand_cards = [EnvCard2RealCard[c] for c in list(infoset.player_hand_cards)]
        print("当前胜率：{}% 请玩家出牌：{} 剩余手牌：{}".format(abs(round(confidence[0] * 100)), real_cards, hand_cards))
        print()
        while (not mcs.check_pass(self.position, self.position)) and (not mcs.check_white(self.position, self.position)):
            # print("等待{}出牌".format(self.position))
            pass

        return best_action
