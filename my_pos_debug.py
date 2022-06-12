import cv2
import numpy as np
import pyautogui

capture_pos = [
    (690, 680, 1200, 250),  # 玩家出牌区域
    (550, 400, 600, 200),  # 玩家上家区域
    (1400, 400, 600, 200)  # 玩家下家区域
]

if __name__ == '__main__':
    img = pyautogui.screenshot()
    img = np.array(img)

    for pos in capture_pos:
        img = cv2.rectangle(img, pos[0:2], (pos[0] + pos[2], pos[1] + pos[3]), (0, 0, 255), 3)
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
