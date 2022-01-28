import cv2
import time , pandas
from datetime import datetime

video = cv2.VideoCapture(0 , cv2.CAP_DSHOW)                      # This is used to capture the video from laptop's webcam
first_frame = None
df = pandas.DataFrame(columns = ["Start" , "End"])               # From the purpose of getting a data about the time.
status_list = [None, None]
times=[]
while True:
    check, frame = video.read()                                  # This is getting about the first frame to be able to compare with the next frame to detect an moving object
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)                # Used for creating gray image as it will be much easier for processing. Color image has lot's of diff cause it has different colors.
    gray = cv2.GaussianBlur(gray,(21,2w1),0)                     # Blur is used to reduce the image noise.

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame , gray)                # This is used to get the absolute difference between the first_frame and gary 
    thresh_frame = cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]     
    thresh_frame = cv2.dilate(thresh_frame , None , iterations = 2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)   #Used to find the objects that have a specfic area.

    for contour in cnts:
        if cv2.contourArea(contour) <10000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h) , (0,255,0),3)       # Used to box the object which is moving in the frame.  

    status_list.append(status)

    if status_list[-1] ==1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] ==0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow("Gray frame" , gray)
    cv2.imshow("delta_frame" , delta_frame)
    cv2.imshow("threshold frame" , thresh_frame )
    cv2.imshow("Color frame" ,frame)

    key = cv2.waitKey(1)
    if key == ord("q"):                                        # This is used to close all imshow windows.
        if status == 1:
            times.append(datetime.now())
        break
print(times)
for i in range(0,len(times),2):
    df = df.append({"Start":times[i] ,"End":times[i+1]},ignore_index=True)      # The df variable will store the datetime of the oject entering the frame and the object leaving the frame.
df.to_csv("Times.csv")                                                          # Used to convert the data in variable to a csv file .
video.release()
cv2.destroyAllWindows()
