#!/usr/bin/env python3.5
"""Script to read the color values"""

import abc
import argparse
import sys
import os
import statistics
import cv2


class MouseRectDrawer():
  def __init__(self, window, image, color):
    self.__is_drawing = False
    self.__start_pos = [0, 0]
    self.__color = color
    self.__window = window
    self.__img = image
    self.__img_mark = self.__img.copy()

  def mouse_down_event(self, pos):
    self.__is_drawing = True
    self.__start_pos = pos

  def mouse_move_event(self, pos):
    if self.__is_drawing:
      self.__img = self.__img_mark.copy()
      cv2.rectangle(self.__img, self.__start_pos, pos, self.__color, 1)
      cv2.imshow(self.__window, self.__img)

  def mouse_up_event(self, pos):
    self.__is_drawing = False
    cv2.rectangle(self.__img, self.__start_pos, pos, self.__color, 1)
    cv2.imshow(self.__window, self.__img)


class ColorReader(metaclass = abc.ABCMeta):
  def __init__(self, filename):
    rect_color = (0, 0, 255)
    self.__filename = filename
    self.__window = self.__filename
    self._img = cv2.imread(self.__filename)
    self._img_mark = self._img.copy()
    self.__mouse_drawer = MouseRectDrawer(self.__window, self._img, rect_color)
    self.__rect = [[0, 0], [0, 0]]

  @abc.abstractmethod
  def _get_color_format(self, img_roi):
    pass

  def __calc_roi_color(self, img_roi):
    h, w, num_channels = img_roi.shape
    channel_data = [[], [], []]
    for y in range(0, h):
      for x in range(0, w):
        channel = img_roi[y, x, :]
        channel_data[0].append(int(channel[0]))
        channel_data[1].append(int(channel[1]))
        channel_data[2].append(int(channel[2]))

    channel_val = [0, 0, 0]
    channel_val[0] = statistics.median(channel_data[0])
    channel_val[1] = statistics.median(channel_data[1])
    channel_val[2] = statistics.median(channel_data[2])
    return channel_val
  
  def __read_rect_color(self, rect):
    p1_x, p1_y = [rect[0][0], rect[0][1]]
    p2_x, p2_y = [rect[1][0], rect[1][1]]

    min_x, min_y = [min(p1_x, p2_x), min(p1_y, p2_y)] 
    max_x, max_y = [max(p1_x, p2_x), max(p1_y, p2_y)] 

    roi = self._img[min_y:max_y, min_x:max_x]
    return self.__calc_roi_color(self._get_color_format(roi))

  def __on_mouse_event(self, event, x, y, flags, param):
    del flags, param
    if event == cv2.EVENT_LBUTTONDOWN:
      self.__mouse_drawer.mouse_down_event((x, y))
      self.__rect[0] = [x, y]

    elif event == cv2.EVENT_MOUSEMOVE:
      self.__mouse_drawer.mouse_move_event((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
      self.__mouse_drawer.mouse_up_event((x, y))
      self.__rect[1] = [x, y]
  
      color = self.__read_rect_color(self.__rect)
      print(color[0], '\t', color[1], '\t', color[2])
      

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

  def _get_color_format(self, img_roi):
    return cv2.cvtColor(img_roi, cv2.COLOR_BGR2RGB)

class ColorReaderYUV(ColorReader):
  def __init__(self, filename):
    super().__init__(filename)
    print('Y\tU\tV')

  def _get_color_format(self, img_roi):
    return cv2.cvtColor(img_roi, cv2.COLOR_BGR2YUV)


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
