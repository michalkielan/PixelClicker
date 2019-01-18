#!/usr/bin/env python3.5
import cv2
import sys

drawing=False # true if mouse is pressed
mode=True # if True, draw rectangle. Press 'm' to toggle to curve


class ImageProcessing:
  def __init__(self, filename):
    self.filename = filename

  def __readColors__(self, x, y):
    color = self.img[y, x, :]
    b, g, r = color
    print(r, '\t', g, '\t', b)

  def __mouseEventProcessing__(self, x, y):
    self.__readColors__(x, y)

  def onMouseEvent(self, event, x, y, flags, param):
  #  if event == cv2.EVENT_LBUTTONDOWN:
  #     self.__mouseEventProcessing__(x, y)
    global ix,iy,drawing, mode

    if event==cv2.EVENT_LBUTTONDOWN:
      drawing=True
      ix,iy=x,y

    elif event==cv2.EVENT_MOUSEMOVE:
      if drawing==True:
        if mode==True:
          cv2.rectangle(self.img,(ix,iy),(x,y),(0,0,255),10)
     #     cv2.imshow(self.filename, self.img)

    elif event==cv2.EVENT_LBUTTONUP:
      drawing=False
      if mode==True:
        cv2.rectangle(self.img,(ix,iy),(x,y),(0,0,255),10)
    #    cv2.imshow(self.filename, self.img)

  def processing(self):
    self.img = cv2.imread(self.filename)
    cv2.imshow(self.filename, self.img)

    cv2.setMouseCallback(self.filename, self.onMouseEvent)

    while(1):
      cv2.imshow(self.filename, self.img)
      k = cv2.waitKey(1)&0xFF
      if k == 27:
        break
      cv2.destroyAllWindows()

#    self.pressedkey = cv2.waitKey(0)

#    while True:
#      cv2.imshow(self.filename, self.img)
#    
#    if self.pressedkey == 27:
#      cv2.destroyAllWindows()

if __name__ =='__main__':
  if len(sys.argv) < 2:
    print('Specify image name: ./PixelClicker.py image_file.jpg')
  else:
    filename = sys.argv[1]
    print('Filename: ', filename)
    img = ImageProcessing(filename)
    img.processing()
