import os

import pyautogui

MY_CARD_FILTER = 50  # 我的牌检测结果过滤参数
OTHER_CARD_FILTER = 25  # 我的牌检测结果过滤参数

AllCards = [
    'rD', 'bX', 'b2', 'r2', 'bA', 'rA', 'bK', 'rK', 'bQ', 'rQ', 'bJ', 'rJ', 'bT', 'rT',
    'b9', 'r9', 'b8', 'r8', 'b7', 'r7', 'b6', 'r6', 'b5', 'r5', 'b4', 'r4', 'b3', 'r3'
]

capture_pos = {
    'player': (690, 680, 1200, 250),  # 玩家出牌区域
    'player_up': (550, 400, 600, 200),  # 玩家上家区域
    'player_down': (1400, 400, 600, 200)  # 玩家下家区域
}


def get_file_list(base_dir):
    for root, ds, fs in os.walk(base_dir):
        for f in fs:
            yield f


def cards_filter(location, distance):  # 牌检测结果滤波
    if len(location) == 0:
        return 0
    loc_list = [location[0][0]]
    count = 1
    for e in location:
        flag = 1
        for have in loc_list:
            if abs(e[0] - have) <= distance:
                flag = 0
                break
        if flag:
            count += 1
            loc_list.append(e[0])
    return count


def find_my_cards():
    return find_cards_in_pos((10, 937, 2500, 300), True)


def find_cards_by_role(player_role, check_role):
    pos = get_player_pos(player_role, check_role)
    return find_cards_in_pos(pos, False)


def find_cards_in_pos(pos, is_mine):
    user_hand_cards_real = ""
    base_img_path = 'imgs/mycards/' if is_mine else 'imgs/othercards/'
    img = pyautogui.screenshot(region=pos)
    for card in AllCards:
        result = pyautogui.locateAll(needleImage=base_img_path + card + '.png', haystackImage=img, confidence=0.93)
        user_hand_cards_real += card[1] * cards_filter(list(result), MY_CARD_FILTER if is_mine else OTHER_CARD_FILTER)
    return user_hand_cards_real


def get_player_pos(player_role, check_role):
    if player_role == check_role:
        return capture_pos['player']
    elif player_role == 'landlord':
        return capture_pos['player_up'] if check_role == 'landlord_up' else capture_pos['player_down']
    elif player_role == 'landlord_up':
        return capture_pos['player_up'] if check_role == 'landlord_down' else capture_pos['player_down']
    elif player_role == 'landlord_down':
        return capture_pos['player_up'] if check_role == 'landlord' else capture_pos['player_down']


def check_pass(player_role, check_role):
    pos = get_player_pos(player_role, check_role)
    img = pyautogui.screenshot(region=pos)
    pass_result = pyautogui.locate(needleImage='imgs/pass.png', haystackImage=img, confidence=0.95)
    return pass_result is not None


def check_white(player_role, check_role):
    pos = get_player_pos(player_role, check_role)
    img = pyautogui.screenshot(region=pos)
    white_result = pyautogui.locate(needleImage='imgs/white.png', haystackImage=img, confidence=0.95)
    return white_result is not None
