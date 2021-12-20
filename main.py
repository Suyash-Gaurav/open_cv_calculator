import cv2
from cvzone.HandTrackingModule import HandDetector
import time


class Button:

    def __init__(self, pos, width, height, value):
        self.pos= pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        # button
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width, self.pos[1]+self.height), (0, 0, 139), cv2.FILLED)
        # border of button
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0,250,250),3)
        # putting text on button
        cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 54), cv2.FONT_HERSHEY_PLAIN, 3, (0, 250, 250), 2)

    def checkClick(self, x, y, img):
        if self.pos[0] < x < self.pos[0]+self.width and self.pos[1] < y < self.pos[1]+self.height :
            # button
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 225, 0), cv2.FILLED)
            # border of button
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 250, 250), 3)
            # putting text on button
            cv2.putText(img, self.value, (self.pos[0] + 15, self.pos[1] + 67), cv2.FONT_HERSHEY_PLAIN, 4, (0, 250, 250),
                        3)
            return True
        else:
            return False

#webcam
cap = cv2.VideoCapture(1)
cap.set(3, 1380)  #width
cap.set(4, 720)   #height
detector = HandDetector(detectionCon=0.7, maxHands=1)

#Creating button
ButtonListVal = [['7', '8', '9', '*'],
                 ['4', '5', '6', '/'],
                 ['1', '2', '3', '+'],
                 ['.', '0', '=', '-']]
ButtonList =[]
for z in range(4):
    for y in range(4):
        xpos = z*75 + 300
        ypos = y*75 + 50
        button = Button((xpos, ypos), 75, 78, ButtonListVal[y][z])
        ButtonList.append(button)
#variables
myEqs = ''
while True:
    #Getting image form webcam
    sucess, video = cap.read()

    # Flipping the Video
    video = cv2.flip(video, 1)

    #Detection of hand
    hands, video = detector.findHands(video, flipType=False)

    #Drawing Button
    # button
    cv2.rectangle(video, (300, 50), (600, 450), (0, 0, 139), cv2.FILLED)
    # border of button
    cv2.rectangle(video, (300, 50), (600, 450), (0, 250, 250), 3)
    cv2.putText(video, " Press ('c') to clear the results and ('a') to exit", (50, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 250, 250),
                2)
    for button in ButtonList:
        button.draw(video)
    #check for Hand
    if hands:

        lmlist = hands[0]['lmList']
        length, _, video = detector.findDistance(lmlist[4],lmlist[5],video)
        x, y = lmlist[4]
        if length<50:
            for i, button in enumerate(ButtonList):
                if button.checkClick(x, y, video):
                    curVal=ButtonListVal[int(i%4)][int(i/4)]
                    if curVal == '=':
                        myEqs = str(eval(myEqs))
                    else:
                        myEqs += curVal
                time.sleep(0.01)




    #Displaying the result

    cv2.putText(video, myEqs, (310,  420), cv2.FONT_HERSHEY_PLAIN, 3, (0, 250, 250), 2)

    #Clearing the Results


    # Displaying the Video
    cv2.imshow('live cam', video)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEqs = ' '
    elif key == ord('a'):
        break

