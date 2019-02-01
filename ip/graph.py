#!/usr/bin/env python3
"""Plot generator"""

import abc
import numpy as np
import cv2
import ip.colorjson
import ip.colormeter
import matplotlib.pyplot as plt

class Const:
  class Symbols:
    @staticmethod
    def delta():
      return '\u0394'

  @staticmethod
  def get_max_hue():
    return 180

  @staticmethod
  def get_max_saturation():
    return 255

  @staticmethod
  def get_max_lightness():
     return 255


def show_window(window_name):
  while True:
    pressed_key = cv2.waitKey(100)
    if pressed_key == 27 or pressed_key == ord('q'):
      cv2.destroyAllWindows()
      break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
      break
  cv2.destroyAllWindows()


class Graph(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def show():
    pass


class GraphHS:
  def __init__(self, ref_json_filename, cap_json_filename):
    self.__ref_color = ip.colorjson.ColorJsonParser(ref_json_filename)
    self.__cap_color = ip.colorjson.ColorJsonParser(cap_json_filename)
    if self.__ref_color.get()['format'] != 'hls' or self.__cap_color.get()['format'] != 'hls':
      raise ValueError('Wrong format, HSL only supported (so far)')

  @staticmethod
  def __get_max_hue():
    return Const.get_max_hue()

  @staticmethod
  def __get_max_saturation():
    return Const.get_max_saturation()

  @staticmethod
  def __get_max_lightness():
    return Const.get_max_lightness()

  def __generate_hs(self):
    img = np.zeros((self.__get_max_hue(), self.__get_max_saturation(), 3), np.uint8)
    height, width, channels = img.shape
    del channels
    img_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    lightness = int(self.__get_max_lightness()/2)
    for y in range(0, height):
      for x in range(0, width):
        s_channel, h_channel = x, y
        img_hls[y, x] = [h_channel, lightness, s_channel]
    return img_hls

  def show(self):
    window_name = 'HS error graph'

    color_meter = ip.colormeter.ColorMeter(self.__ref_color, self.__cap_color)
    h_perc, l_perc, s_perc = color_meter.get_hls_delta_perc()

    print(Const.Symbols.delta() + 'H [average] : ', round(h_perc, 2), '%', sep='')
    print(Const.Symbols.delta() + 'L [average] : ', round(l_perc, 2), '%', sep='')
    print(Const.Symbols.delta() + 'S [average] : ', round(s_perc, 2), '%', sep='')

    img = self.__generate_hs()
    
    img_graph = img

    plt.ylim((0, self.__get_max_hue() - 1))
    plt.xlim(0, self.__get_max_saturation())
    plt.xlabel('Saturation')
    plt.ylabel('Hue')

    plt.imshow(cv2.cvtColor(img_graph, cv2.COLOR_BGR2RGB))
    x = np.arange(30)
    plt.gca().invert_yaxis()

    size = len(self.__ref_color.get()['channels']['h'])

    ref_ax, cap_ax = None, None
    for i in range(0, size):
      ref_channels = self.__ref_color.get()['channels']
      cap_channels = self.__cap_color.get()['channels']

      p1_x = ref_channels['s'][i]
      p1_y = ref_channels['h'][i]

      p2_x = cap_channels['s'][i]
      p2_y = cap_channels['h'][i]

      plt.plot([p1_x, p2_x], [p1_y, p2_y], color='black', linewidth=0.7)
      ref_ax, = plt.plot([p1_x, p1_x], [p1_y, p1_y], 'bs-', label='ref')
      cap_ax, = plt.plot([p2_x, p2_x], [p2_y, p2_y], 'ro-', label='cap')

    plt.legend(handles=[ref_ax, cap_ax])
    plt.show()

  @staticmethod
  def create(ref_json_filename, cap_json_filename):
    graph_hs = GraphHS(ref_json_filename, cap_json_filename)
    graph_hs.show()
