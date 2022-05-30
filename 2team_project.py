from email.mime import image
import tkinter
import cv2
from PIL import Image
from PIL import ImageTk
from perspective import perspective_img
import tkinter.ttk
import numpy as np
from tkinter import filedialog

from function.textDetection import textDetection
from function.mosaic import imageMosaic

#임시저장 경로

path = './images/white.png'
dictionary = []
tempImage = np.zeros((320,200,3), np.uint8)
#영상 위치
before_src = cv2.imread('./images/white.png')       #공백으로 초기화
after_src = cv2.imread('./images/white.png')
#영상 값
before_img = cv2.cvtColor(before_src, cv2.COLOR_RGB2BGR)
after_img = cv2.cvtColor(after_src, cv2.COLOR_RGB2BGR)
after_img = after_src.copy()

window = tkinter.Tk()

window.title("2팀 신분증 모자이크 프로젝트")
window.geometry("800x400+100+100")
window.resizable(False, False)

#함수
#사진 불러오기
def img_upload(event):
    global path
    global before_src
    global before_img

    filename = filedialog.askopenfilename(initialdir='', title='파일선택', filetypes=(
                                                    ('png files', '*.png'), ('jpg files', '*.jpg'), ('all files', '*.*')))
    path = filename
    before_src = cv2.imread(filename)
    before_img = cv2.cvtColor(before_src, cv2.COLOR_RGB2BGR)
    before_img = cv2.resize(before_img, (320,200))
    trans = Image.fromarray(before_img)
    transTk = ImageTk.PhotoImage(image = trans)
    before_label.config(image=transTk)
    before_label.image = transTk

#사진 편집
def processing(event):
    global path
    global before_src
    global before_img
    print("사진 변환")
    ret_src = perspective_img(before_src)      #numpy 값으로 되돌려 받는다.
    ret_src = cv2.resize(ret_src, (320,200))
    cv2.imwrite("./images/temp.jpg", ret_src)  #임시로 사진 저장
    path = "./images/temp.jpg"
    before_img = cv2.cvtColor(ret_src, cv2.COLOR_RGB2BGR)   #이거 변환하기 전에 무조건 다시 해줘야한다.
    trans = Image.fromarray(before_img)
    transTk = ImageTk.PhotoImage(image = trans)
    before_label.config(image=transTk)
    before_label.image = transTk

#텍스트 검출
def findtext(event):
    global path
    global dictionary
    global tempImage
    #path를 통하여 작업하시면 됩니다.
    tempImage = cv2.imread(path)
    localDict = []
    dictionary = textDetection(path)
    [localDict.append(key) for key in dictionary.keys()]
    setText(localDict)


def setText(dictionary_key):
    global dictionary
    #여기서 받아온 딕션어리 키 값으로 콤보 박스 세팅할 예정
    print('눌림')
    after_text_mosaic_combobox.configure(values = dictionary_key)

def pressMosaic(event):
    global path
    global dictionary
    #콤보 박스에서 모자이클한 텍스트를 클릭한 경우
    mosaicImage = imageMosaic(dictionary[after_text_mosaic_combobox.get()], tempImage)
    after_img = cv2.resize(mosaicImage, (320,200))
    after_img = cv2.cvtColor(after_img, cv2.COLOR_RGB2BGR)
    after_img = Image.fromarray(after_img)
    transTk = ImageTk.PhotoImage(image = after_img)
    after_label.config(image=transTk)
    after_label.image = transTk
    #콤보 박스에서 가져온 텍스트 값이 잘 출력됩니다.
    #여기서 이제 다시 돌아가셔서 작업하면 됩니다.


def saveResult(event):
    global after_src
    cv2.imwrite("./images/result.jpg", after_src)  #사진 결과 저장


#기본 세팅
#사진 불러오기, 사진 저장
img_upload_button = tkinter.Button(window, text= '사진 불러오기')
img_upload_button.place(x = 590, y = 10, width=100, height=30)
img_save_button = tkinter.Button(window, text= '사진 저장')
img_save_button.place(x = 700, y = 10, width=80, height=30)

#이전
#cv2.imshow("d",before_src)
before_img = cv2.resize(before_img, (320,200))
before_img = Image.fromarray(before_img)
before_imgtk = ImageTk.PhotoImage(image = before_img)
before_label = tkinter.Label(window, image=before_imgtk)
before_label.place(x=40, y=50, width=320, height=200)
before_text = tkinter.Label(window, text =  "Before")
before_text.place(x=160, y=250, width=50,height=50) 
#이전 사진 이미지 처리 버튼
before_img_button = tkinter.Button(window, text= '사진 편집')
before_img_button.place(x = 40, y = 300, width=320, height=30)

#이후
after_img = cv2.resize(after_img, (320,200))
after_img = Image.fromarray(after_img)
after_imgtk = ImageTk.PhotoImage(image = after_img)
after_label = tkinter.Label(window, image=after_imgtk)
after_label.place(x=440, y=50, width=320, height=200)
after_text = tkinter.Label(window, text =  "After")
after_text.place(x=580, y=250, width=50,height=40)
#얼굴 모자이크 버튼
after_face_mosaic_button = tkinter.Button(window, text= '얼굴 모자이크')
after_face_mosaic_button.place(x = 440, y = 300, width=320, height=30)
#텍스트 모자이크 콤보 박스
values=[str(i)+"번" for i in range(1, 101)] 
after_text_mosaic_combobox = tkinter.ttk.Combobox(window, height=15, values=values)
after_text_mosaic_combobox.config(state='readonly')
after_text_mosaic_combobox.place(x = 440, y = 340, width=320, height=30)
#텍스트 검출 버튼
text_find_button = tkinter.Button(window, text= '검출')
text_find_button.place(x = 370, y = 150, width=60, height=30)


#리스너
before_img_button.bind("<Button-1>", processing)
img_upload_button.bind("<Button-1>", img_upload)
text_find_button.bind("<Button-1>", findtext)
img_save_button.bind("<Button-1>", saveResult)
after_text_mosaic_combobox.bind("<<ComboboxSelected>>", pressMosaic)


#창 동작
window.mainloop()