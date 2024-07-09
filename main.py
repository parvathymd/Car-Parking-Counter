import cv2
import pickle
import cvzone
import numpy as np

#video feed
cap =cv2.VideoCapture('carPark.mp4')

with open('CarParkposi', 'rb') as f:
        posList = pickle.load(f)

width,height =107,48

def checkParkingSpace(imgPro):
     spaceCounter =0
     for pos in posList:
          x,y=pos
          
          imgCrop =imgPro[y:y+height, x:x+width]
          #cv2.imshow(str(x*y) ,imgCrop)  # unique name for the cropped part so it does not overwrite

          #to count the white scale
          count =cv2.countNonZero(imgCrop)

          #to write the count number in front of the box
          cvzone.putTextRect(img,str(count),(x,y+height -3), scale =1, thickness =2, offset =0, colorR=(0,0,255))

          if count<900:
               color =(0,255,0) #no car green
               thickness =5
               spaceCounter += 1
          else:
               color =(0,0,255) #there is car so red
               thickness =2
          cv2.rectangle(img, pos, (pos[0] + width, pos[1]+height),color,thickness) 
    
    #to print the number of free spaces
          cvzone.putTextRect(img,str(spaceCounter),(100,50), scale =5, thickness =5,
                              offset =20, colorR=(0,200,0))

          

while True:

#THIS TO MAKE THE VIODEO CONTIUES IN THE LOOP so the frames are set back to zero
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img =cap.read()

    #after we get the image we convert it into greyscale
    imgGray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur =cv2.GaussianBlur(imgGray, (3,3),1)

    #after bluring the image convert it into binary image
    imgThreshold =cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV,25,16)
    #to remove the noise
    imgMedian =cv2.medianBlur(imgThreshold,5)

    #ti differentiate we use dilation
    kernel =np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel, iterations=1)
    
    #we are giving image dilate as image processed to the function
    checkParkingSpace(imgDilate) 

    #for pos in posList:
         
    
    cv2.imshow("image", img)
    #cv2.imshow("imageBlur", imgBlur)
    #cv2.imshow("imageThresh", imgThreshold)
    #cv2.imshow("imageMedian", imgMedian)
    cv2.waitKey(10) #1 ms delay to slow down the video the delay
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()