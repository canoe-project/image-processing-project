import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def textDetection(imageFile):
    """
    초기화, initialization
    """
    textDict ={}#텍스트 좌료를 넣을 딕셔너리 선언
    image = cv2.imread(imageFile)# 이미지 로드
    originH = image.shape[0]#이미지 높이 저장

    """
    이미지 전처리
    """

    #그레이 스케일 및 THRESH_OTSU 이진화
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(
        gray, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    clean = thresh.copy()
    # sampleImg = image.copy()

    #오프닝
    open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
    opening = cv2.morphologyEx(clean, cv2.MORPH_OPEN, open_kernel, iterations=2)

    #클로즈
    close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,1))
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=4)

    """
    컨퓨어 검출
    """
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    """
    이미지의 텍스트 좌표를 딕셔너리에 저장
    """
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)#컨퓨어된 이미지의 윤곽선의 경계면을 둘러싸는 사각형을 반환
        #이미지 전체 크기에 1/2가 넘지 않는, 적어도 이미지 전체 크기에 1/30보다는 큰 이미지라면 텍스트를 분석한다.
        if c.shape[0] > originH/30 and c.shape[0] < originH/2:
            #pytesseract로 텍스트 변환
            ROI = image[y:y+h, x:x+w]
            data = pytesseract.image_to_string(ROI, lang='kor',config='--psm 6')
            #변환된 텍스트의 값이 존재할 경우 그 값을 저장한다.
            if(len(data) != 0):          
                textDict[data] = [[x,y], [x + w, y + h]]
                # cv2.rectangle(sampleImg, (x, y), (x + w, y + h), (36,255,12), 2)
                
    # cv2.imshow("sample", sampleImg)
    cv2.imwrite('./result/image.png', image)
    cv2.imwrite('./result/clean.png', clean)
    cv2.imwrite('./result/close.png', close)
    cv2.imwrite('./result/opening.png', opening)
    return(textDict)

