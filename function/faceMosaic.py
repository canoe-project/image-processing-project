import cv2

def profile_moszic(src):

    face_classifier = cv2.CascadeClassifier('./xml/haarcascade_frontface.xml')
    eye_classifier = cv2.CascadeClassifier('./xml/haarcascade_eye.xml')

    size = 25
    gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)                     
    faces = face_classifier.detectMultiScale(gray,1.1,2)
    
    for (x,y,w,h) in faces:
        roi_faces = src[y:y+h, x:x+w]
        
        eyes = eye_classifier.detectMultiScale(roi_faces,1.1,3)
        for (ex,ey,ew,eh) in eyes:
            roi_eyes = roi_faces[ey:ey+eh, ex:ex+ew]

                    #---------모자이크----------
            roi = cv2.resize(roi_faces, (w//size, h//size))     #축소
            roi = cv2.resize(roi, (w, h),interpolation=cv2.INTER_AREA)  #확대
            src[y:y+h, x:x+w] = roi
    
    return src

