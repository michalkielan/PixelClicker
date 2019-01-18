#!/usr/bin/env python3.5
import cv2
import sys


class ImageProcessing:
  def __init__(self, filename):
    self.filename = filename
    self.img = cv2.imread(self.filename)

  def __read_colors__(self, x, y):
    color = self.img[y, x, :]
    b, g, r = color
    print(r, '\t', g, '\t', b)

  def __mouse_event_processing__(self, x, y):
    self.__read_colors__(x, y)

  def on_mouse_event(self, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      self.__mouse_event_processing__(x, y)

  def processing(self):
    cv2.imshow(self.filename, self.img)

    cv2.set_mouse_callback(self.filename, self.on_mouse_event)
    pressedkey = cv2.waitKey(0)

    if pressedkey == 27:
      cv2.destroyAllWindows()


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('Specify image name: ./PixelClicker.py image_file.jpg')
  else:
    filename = sys.argv[1]
    print('Filename: ', filename)
    img = ImageProcessing(filename)
    img.processing()
