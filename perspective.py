import cv2
import sys
import numpy as np
import pyautogui

result = None
pts_cnt = 0    #4개의 점

def perspective_img(src):
    global result
    global pts_cnt
    win_name = "scanning"
    img = src
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img is None:
        print('영상 읽기 실패')
        sys.exit()

    rows, cols = img.shape[:2]
    draw = img.copy()
    pts = np.zeros((4, 2), dtype=np.float32)

    def onMouse(event, x, y, flags, param):     #마우스로 찍은 점 4점
        global pts_cnt
        global result
        if event == cv2.EVENT_LBUTTONDOWN:      #왼쪽 버튼을 누른 이벤트가 맞을 경우
            # 좌표에 초록색 동그라미 표시
            cv2.circle(draw, (x, y), 10, (0, 255, 0), -1)
            cv2.imshow(win_name, draw)

            # 마우스 좌표 저장
            pts[pts_cnt] = [x, y]
            pts_cnt += 1
        
            if pts_cnt == 4:
                # 좌표 4개 중 상하좌우 찾기
                sm = pts.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산    axis는 축에 관한 이야기다.
                diff = np.diff(pts, axis=1)  # 4쌍의 좌표 각각 x-y 계산

                topLeft = pts[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
                bottomRight = pts[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
                topRight = pts[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
                bottomLeft = pts[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

                # 변환 전 4개 좌표 
                pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

                # 변환 후 영상에 사용할 폭과 높이 계산
                w1 = abs(bottomRight[0] - bottomLeft[0])
                w2 = abs(topRight[0] - topLeft[0])
                h1 = abs(topRight[1] - bottomRight[1])
                h2 = abs(topLeft[1] - bottomLeft[1])
                width = int(max([w1, w2]))  # 두 좌우 거리간의 최대값이 서류의 폭
                height = int(max([h1, h2]))  # 두 상하 거리간의 최대값이 서류의 높이

                # 변환 후 4개 좌표
                pts2 = np.float32([[0, 0], [width - 1, 0],
                               [width - 1, height - 1], [0, height - 1]])

                # 변환 행렬 계산 
                M = cv2.getPerspectiveTransform(pts1, pts2)
                # 원근 변환 적용
                result = cv2.warpPerspective(img, M, (width, height))
                cv2.imshow('scanned', result)
                pyautogui.press('enter')   #끝나면 enter를 입력

    cv2.imshow(win_name, img)
    cv2.setMouseCallback(win_name, onMouse)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pts_cnt = 0
    return result