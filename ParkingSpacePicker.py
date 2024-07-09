import cv2
import pickle

#we need to store the data in pickle object so that we need not edit the same thing again and again
#to keep the edtting one stored



width,height =107,48 #x2-x1,y2-y1 from the rectamgle coordinate

try:
    with open('CarParkposi', 'rb') as f:
        posList = pickle.load(f)
        
except:
    posList=[]

def mouseClick(events,x,y,flags,params):
    # to set up the parking slots
    if events==cv2.EVENT_LBUTTONDOWN:
        posList.append((x,y))
    
    #TO DELETE THE UNWANTED POSITIONS
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(posList):
            x1,y1= pos
            #x ,y is the point ehre the mouse is pointing to
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)

    with open('CarParkposi', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img =cv2.imread('carParkImg.png')
    #to create a rectangle around the parking spot
    #cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)

    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1]+height),(255,0,255),2)

    
    cv2.imshow("image",img)
    cv2.setMouseCallback("image",mouseClick)
    cv2.waitKey(1)

