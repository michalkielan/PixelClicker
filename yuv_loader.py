import cv2
import numpy as np
import abc

class ImageLoader(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def imread(self):
    pass


class ImageDefaultLoader(ImageLoader):
  def __init__(self, filename):
    self.__filename = filename

  def imread(self):
    return cv.imread(self.__filename)


class ImageLoaderRawNV21(ImageLoader):
  def __init__(self, filename, size):
    height, width = size
    self.__frame_len = width * height * 3 / 2
    self.__img_file = open(filename, 'rb')
    self.__shape = (int(height * 1.5), width)

  def __read_raw(self):
    raw = self.__img_file.read(int(self.__frame_len))
    buf = np.frombuffer(raw, dtype=np.uint8)
    nv21 = buf.reshape(self.__shape)
    return nv21

  def imread(self):
    nv21 = self.__read_raw()
    return cv2.cvtColor(nv21, cv2.COLOR_YUV2BGR_NV21)


def image_loader_factory(filename, pixel_format, size):
  if pixel_format is 'nv21':
    return ImageLoaderRawNV21(filename, size)
  else:
    return ImageDefaultLoader(filename)

if __name__ == "__main__":
  filename = ""
  size = (480, 640)
  img = image_loader_factory(filename, 'nv21', size)

  frame = img.imread()
  cv2.imshow(filename, frame)
  cv2.waitKey(0)
