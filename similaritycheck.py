"""Script to measure images similarites """
import cv2
import abc
import ip.imgloader
import abc
import numpy as np
from skimage.measure import compare_ssim as ssim

class  QualityMeasurement(metaclass=abc.ABCMeta):
  def create(img_loader_1, img_loader_2, measurementMethod=''):
    if measurementMethod == 'ssim-gr':
      return QualityMeasurementSSIMGreyscale(img_loader_1,img_loader_2)
    elif measurementMethod == 'ssim':
      return QualityMeasurementSSIM(img_loader_1,img_loader_2)
    elif measurementMethod == 'psnr':
      return QualityMeasurementPSNR(img_loader_1,img_loader_2)
    elif measurementMethod == 'psnr-gr':
      return QualityMeasurementPSNRGreyscale(img_loader_1,img_loader_2)
    raise AttribiteError('quality_measure_factory method {} not found'.format(measurmentMethod))

class QualityMeasurementBase(QualityMeasurement):
  def __init__(self, img_loader_1, img_loader_2):
    self._image1 = img_loader_1.imread()
    self._image2 = img_loader_2.imread()
    #do some checks
    if self._image1 is None or self._image2 is None:
      raise AttributeError('Incorrect input data files')
    if self._image1.shape != self._image2.shape:
      raise AttributeError('Unmatching images size')

  def convertToGrey(self, inputImage):
     return cv2.cvtColor(inputImage,cv2.COLOR_BGR2GRAY)

  def process():
      pass

class QualityMeasurementPSNRGreyscale(QualityMeasurementBase):
  def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementPSNR,self).__init__(img_loader_1, img_loader_2)
  def process(self):
     print("Standard PSNR")
     I = super().convertToGrey(self._image1).astype(float)
     K = super().convertToGrey(self._image2).astype(float)

     MSE = (np.square(I-K)).mean()
     MAXvalue = 255 #for 8 bits
     if(MSE == 0):
         print('MSE is zero, images are same')
         return np.inf
     PSNR = 10 * np.log10((np.square(MAXvalue))/MSE)
     return PSNR

class QualityMeasurementSSIMGreyscale(QualityMeasurementBase):
    def __init__(self, img_loader_1, img_loader_2):
      super().__init__(img_loader_1, img_loader_2)
    def process(self):
     I = super().convertToGrey(self._image1).astype(float)
     K = super().convertToGrey(self._image2).astype(float)
     print(I.shape)
     return ssim(I,K)

class QualityMeasurementSSIM(QualityMeasurementBase):
    def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementSSIM,self).__init__(img_loader_1, img_loader_2)
    def process(self):
     I = self._image1
     K = self._image2
     print(I.shape)
     return ssim(I,K,multichannel=True, Full=True)
class QualityMeasurementPSNR(QualityMeasurementBase):
  def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementPSNR,self).__init__(img_loader_1, img_loader_2)
  def process(self):
     I = self._image1.astype(float)
     K = self._image2.astype(float)
     MSE = np.sum(np.square(I - K))/(I.shape[0]*I.shape[1])/3
     if(MSE == 0):
         print('MSE is zero, images are same')
         return np.inf
     MAXvalue = 255#for 8 bits
     return 10 * np.log10((np.square(MAXvalue))/MSE)
def main():
#imageloader values
  pixel_format  = ''
  video_size = ''

  img_file_1 = 'base.png'
  img_file_2 = 'q10.jpg'

  image_loader_1 = ip.imgloader.create(img_file_1, pixel_format, video_size)
  image_loader_2 = ip.imgloader.create(img_file_2, pixel_format, video_size)

  print('SSIM grey color value is: {}'.format(
  QualityMeasurement.create(image_loader_1,image_loader_2,'ssim-gr').process())
  )
  print('SSIM value is: {}'.format(
  QualityMeasurement.create(image_loader_1,image_loader_2,'ssim').process())
  )






if __name__ == '__main__':
  main()
