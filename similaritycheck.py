"""Script to measure images similarites """
import cv2
import abc
import ip.imgloader
import abc
import numpy as np
#from skimage.measure import structural_similarity as ssim
from skimage.measure import compare_ssim as ssim

class  QualityMeasurement(metaclass=abc.ABCMeta):
  def create(img_loader_1, img_loader_2, measurementMethod=''):
    if measurementMethod == 'psnr':
      return QualityMeasurementPSNR(img_loader_1,img_loader_2)
    elif measurementMethod == 'ssim':
      return QualityMeasurementSSIM(img_loader_1,img_loader_2)
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

class QualityMeasurementPSNR(QualityMeasurementBase):
  def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementPSNR,self).__init__(img_loader_1, img_loader_2)
  def process(self):
     print(self._image1.shape)
     I = super().convertToGrey(self._image1).astype(float)
     K = super().convertToGrey(self._image2).astype(float)

     MSE = (np.square(I-K)).mean()
     MAXvalue = 255 #for 8 bits
     if(MSE == 0):
         print('MSE is zero, images are same')
         return np.inf

     PSNR = 10 * np.log10((np.square(MAXvalue))/MSE)
     return PSNR

class QualityMeasurementSSIM(QualityMeasurementBase):
    def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementSSIM,self).__init__(img_loader_1, img_loader_2)
    def process(self):
     I = super().convertToGrey(self._image1).astype(float)
     K = super().convertToGrey(self._image2).astype(float)
     return ssim(I,K)

def main():
  print("similaritycheck: ")

 # parser = argparse.ArgumentParser()
 # parser.add_argument('-sc','simcheck')
#imageloader values
  pixel_format  = ''
  video_size = ''

  img_file_1 = 'base.png'
  img_file_2 = 'q90.jpg'

  image_loader_1 = ip.imgloader.create(img_file_1, pixel_format, video_size)
  image_loader_2 = ip.imgloader.create(img_file_2, pixel_format, video_size)

  print('PSNR value is: {}'.format(
  QualityMeasurement.create(image_loader_1,image_loader_2,'psnr').process())
  )

  print('SSIM value is: {}'.format(
  QualityMeasurement.create(image_loader_1,image_loader_2,'ssim').process())
  )





if __name__ == '__main__':
  main()
