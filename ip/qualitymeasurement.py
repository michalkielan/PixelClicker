#!/usr/bin/env python3
"""Quality measurement"""
import cv2
import abc
import ip.imgloader
import abc
import numpy as np
from skimage.measure import compare_ssim as ssim
from enum import IntEnum

class channelsRGB(IntEnum):
   red   = 2
   green = 1
   blue  = 0

class  QualityMeasurement(metaclass=abc.ABCMeta):
  def create(img_loader_ref, img_loader_cap, measurementMethod=''):
    if measurementMethod == 'ssim-sc':
      return QualityMeasurementSSIMsingleChannel(img_loader_ref,img_loader_cap)
    elif measurementMethod == 'ssim':
      return QualityMeasurementSSIM(img_loader_ref,img_loader_cap)
    elif measurementMethod == 'psnr':
      return QualityMeasurementPSNR(img_loader_ref,img_loader_cap)
    elif measurementMethod == 'psnr-sc':
      return QualityMeasurementPSNRsingleChannel(img_loader_ref,img_loader_cap)
    raise AttribiteError('quality_measure_factory method {} not found'.format(measurmentMethod))


class QualityMeasurementBase(QualityMeasurement):
  def __init__(self, img_loader_ref, img_loader_cap):
    self._image_ref = img_loader_ref.imread()
    self._image_cap = img_loader_cap.imread()
    #do some checks
    if self._image_ref is None or self._image_cap is None:
      raise AttributeError('Incorrect input data files')
    if self._image_ref.shape != self._image_cap.shape:
      raise AttributeError('Unmatching images size')
  def process():
      pass


class QualityMeasurementPSNRsingleChannel(QualityMeasurementBase):
  def __init__(self, img_loader_ref, img_loader_cap):
      super().__init__(img_loader_ref, img_loader_cap)
  def process(self, chNo):
     if(self._image_ref.shape[2] <= chNo):
       raise AttributeError("Given image has no channel number: {}. Max channel number: {}".format(chNo, self._image_ref.shape[2]-1))
     I = self._image_ref[:,:,chNo].astype(float)
     K = self._image_cap[:,:,chNo].astype(float)
     MSE = (np.square(I-K)).mean()
     MAXvalue = 255 #for 8 bits
     if(MSE == 0):
         return np.inf
     PSNR = 10 * np.log10((np.square(MAXvalue))/MSE)
     return PSNR


class QualityMeasurementSSIMsingleChannel(QualityMeasurementBase):
    def __init__(self, img_loader_ref, img_loader_cap):
      super().__init__(img_loader_ref, img_loader_cap)
    def process(self,chNo):
     I = self._image_ref[:,:,chNo]
     K = self._image_cap[:,:,chNo]
     return ssim(I,K)


class QualityMeasurementSSIM(QualityMeasurementBase):
    def __init__(self, img_loader_ref, img_loader_cap):
      super(QualityMeasurementSSIM,self).__init__(img_loader_ref, img_loader_cap)
    def process(self):
     I = self._image_ref
     K = self._image_cap
     return ssim(I,K,multichannel=True)


class QualityMeasurementPSNR(QualityMeasurementBase):
  def __init__(self, img_loader_ref, img_loader_cap):
      super(QualityMeasurementPSNR,self).__init__(img_loader_ref, img_loader_cap)
  def process(self):
     I = self._image_ref.astype(float)
     K = self._image_cap.astype(float)
     MSE = np.sum(np.square(I - K))/float(I.shape[0]*I.shape[1])/3.0
     if(MSE == 0):
         return np.inf
     MAXvalue = 255#for 8 bits
     return 10 * np.log10((np.square(MAXvalue))/MSE)
