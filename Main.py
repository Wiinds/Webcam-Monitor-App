import cv2
import time
from emailing import send_email
from datetime import datetime
import streamlit as st


st.title("Motion Capture")

start = st.button("Start Camera", key="start")


camera_active = False


if start:
    time.sleep(1)
    camera_active = True
    video = cv2.VideoCapture(0)
    streamlit_image = st.image([])
            
    while camera_active:
        status = 0
        check, frame = video.read()

        first_frame = None
        status_list = []

        now = datetime.now()
        #change frame color and blur image a little
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        
        if first_frame is None:
            first_frame = gray_frame_gau
            
        delta_frame = cv2.absdiff(first_frame ,gray_frame_gau)
        
        thresh_frame = cv2.threshold(delta_frame, 80, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        
        contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < 8000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            if rectangle.any():
                status = 1

        cv2.putText(img=frame, text=now.strftime("%A"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)


        cv2.putText(img=frame, text=now.strftime("%H:%M"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, color=(255, 0, 255),
                    thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)

        status_list.append(status)
        status_list = status_list[-2:]
        
        if status_list[0] == 1 and status_list[1] == 0:
            send_email()
            
        #cv2.imshow("Video", frame)
        
        key = cv2.waitKey(1)
        
        #if key == ord("q"):
        #    break

        #video.release()

end_video = st.button("End Video", key="end")

if end_video: 
    camera_active = False
    video.release()
    st.info(" Video has Ended")


#first_frame = None
#status_list = []
    



