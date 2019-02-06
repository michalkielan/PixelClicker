#!/usr/bin/env python3
"""Color data filter"""
import cv2
import abc
import ip.imgloader
import abc
import numpy as np
from skimage.measure import compare_ssim as ssim


class  QualityMeasurement(metaclass=abc.ABCMeta):
  def create(img_loader_1, img_loader_2, measurementMethod=''):
    if measurementMethod == 'ssim-sc':
      return QualityMeasurementSSIMsingleChannel(img_loader_1,img_loader_2)
    elif measurementMethod == 'ssim':
      return QualityMeasurementSSIM(img_loader_1,img_loader_2)
    elif measurementMethod == 'psnr':
      return QualityMeasurementPSNR(img_loader_1,img_loader_2)
    elif measurementMethod == 'psnr-sc':
      return QualityMeasurementPSNRsingleChannel(img_loader_1,img_loader_2)
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
  def process():
      pass


class QualityMeasurementPSNRsingleChannel(QualityMeasurementBase):
  def __init__(self, img_loader_1, img_loader_2):
      super().__init__(img_loader_1, img_loader_2)
  def process(self, chNo):
     I = self._image1[:,:,chNo].astype(float)
     K = self._image2[:,:,chNo].astype(float)
     MSE = (np.square(I-K)).mean()
     MAXvalue = 255 #for 8 bits
     if(MSE == 0):
         return np.inf
     PSNR = 10 * np.log10((np.square(MAXvalue))/MSE)
     return PSNR


class QualityMeasurementSSIMsingleChannel(QualityMeasurementBase):
    def __init__(self, img_loader_1, img_loader_2):
      super().__init__(img_loader_1, img_loader_2)
    def process(self,chNo):
     I = self._image1[:,:,chNo]
     K = self._image2[:,:,chNo]
     return ssim(I,K)


class QualityMeasurementSSIM(QualityMeasurementBase):
    def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementSSIM,self).__init__(img_loader_1, img_loader_2)
    def process(self):
     I = self._image1
     K = self._image2
     return ssim(I,K,multichannel=True)


class QualityMeasurementPSNR(QualityMeasurementBase):
  def __init__(self, img_loader_1, img_loader_2):
      super(QualityMeasurementPSNR,self).__init__(img_loader_1, img_loader_2)
  def process(self):
     I = self._image1.astype(float)
     K = self._image2.astype(float)
     MSE = np.sum(np.square(I - K))/(I.shape[0]*I.shape[1])/3
     if(MSE == 0):
         return np.inf
     MAXvalue = 255#for 8 bits
     return 10 * np.log10((np.square(MAXvalue))/MSE)
