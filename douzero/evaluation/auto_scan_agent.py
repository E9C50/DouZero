from time import sleep

import my_cards_scan as mcs

RealCard2EnvCard = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 17, 'X': 20, 'D': 30
}


class AutoScanAgent(object):

    def __init__(self, position, player_position):
        self.name = 'AutoScan'
        self.position = position
        self.player_position = player_position

    def act(self, info_set):
        while (not mcs.check_pass(self.player_position, self.position)) and \
                (not mcs.check_white(self.player_position, self.position)):
            # print("等待{}出牌".format(self.position))
            pass

        sleep(2)

        pass_flag = mcs.check_pass(self.player_position, self.position)
        if pass_flag:
            self.other_played_cards_real = ""
        else:
            self.other_played_cards_real = mcs.find_cards_by_role(self.player_position, self.position)

        return [RealCard2EnvCard[c] for c in list(self.other_played_cards_real)]
