#!/usr/bin/env python3.5
"""Script to read the color data of each pixel"""

import abc
import argparse
import sys
import os
import cv2

DRAWING = False # true if mouse is pressed
MODE = True # if True, draw rectangle. Press 'm' to toggle to curve

ix = 0
iy = 0

class ColorReader(metaclass=abc.ABCMeta):
  def __init__(self, filename):
    self.__filename = filename
    self.__window = self.__filename
    self._img = cv2.imread(self.__filename)
    self._img_mark = self._img.copy()


  @abc.abstractmethod
  def _read_colors(self, pos):
    pass

  def __mouse_event_processing(self, pos):
    color = self._read_colors(pos)
    print(color[0], '\t', color[1], '\t', color[2])

  def __on_mouse_event(self, event, x, y, flags, param):
    del flags, param
    global ix, iy, DRAWING, MODE

    if event == cv2.EVENT_LBUTTONDOWN:
      DRAWING = True
      ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
      if DRAWING == True:
        if MODE == True:
          self._img = self._img_mark.copy()
          cv2.rectangle(self._img, (ix, iy), (x, y), (0, 0, 255), 1)
          cv2.imshow(self.__window, self._img)

    elif event == cv2.EVENT_LBUTTONUP:
      DRAWING = False
      if MODE == True:
        cv2.rectangle(self._img, (ix, iy), (x, y), (0, 0, 255), 1)
        cv2.imshow(self.__window, self._img)

  def processing(self):
    cv2.imshow(self.__window, self._img)
    cv2.setMouseCallback(self.__window, self.__on_mouse_event)
    while True:
      pressedkey = cv2.waitKey(100)
      if pressedkey == 27:
        cv2.destroyAllWindows()
        break
      if cv2.getWindowProperty(self.__window, cv2.WND_PROP_VISIBLE) < 1:
        break
    cv2.destroyAllWindows()


class ColorReaderRGB(ColorReader):
  def __init__(self, filename):
    super().__init__(filename)
    print('R\tG\tB')

  def _read_colors(self, pos):
    super()._read_colors(pos)
    pos_x, pos_y = pos
    b, g, r = self._img[pos_y, pos_x, :]
    return r, g, b


class ColorReaderYUV(ColorReader):
  def __init__(self, filename):
    super().__init__(filename)
    print('Y\tU\tV')

  def _read_colors(self, pos):
    super()._read_colors(pos)
    pos_x, pos_y = pos
    img_yuv = cv2.cvtColor(self._img, cv2.COLOR_BGR2YUV)
    return img_yuv[pos_y, pos_x, :]


def make_color_reader(color_format, img_file):
  if color_format == 'rgb':
    return ColorReaderRGB(img_file)
  if color_format == 'yuv':
    return ColorReaderYUV(img_file)
  raise AttributeError('Color format: ' + color_format + ' not found')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--imgfile', type=str, help='Image file', default='')
  parser.add_argument('-f', '--format', type=str, help='RGB, YUV (Default: RGB)', default='RGB')

  args = parser.parse_args()
  img_format = args.format.lower()
  img_file = args.imgfile

  if not os.path.exists(img_file):
    sys.exit('File not found')

  try:
    color_reader = make_color_reader(img_format, img_file)
    color_reader.processing()
  except AttributeError:
    err = sys.exc_info()[1]
    sys.exit('Cannot read color: ' + str(err))

if __name__ == '__main__':
  main()
