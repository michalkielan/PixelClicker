#!/usr/bin/env python3
"""Script to read the color values"""

import argparse
import sys
import os
import ip.imgloader
import ip.colorjson
import ip.colorreader
import ip.graph
import ip.qualitymeasurement


def parse_video_size_arg(video_size):
  if video_size != '':
    w, h = video_size.split('x', 1)
    return int(w), int(h)
  return None


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-i',
      '--imgfile',
      type=str,
      help='Image file',
      default=''
  )

  parser.add_argument(
      '-o',
      '--out',
      type=str,
      help='Json file',
      default='color_data.json'
  )

  parser.add_argument(
      '-pix_fmt',
      '--pixel_format',
      type=str, help='Raw input pixel format: nv21, nv12',
      default=''
  )

  parser.add_argument(
      '-s',
      '--video_size',
      type=str, help='WxH set the frame size',
      default=''
  )

  parser.add_argument(
      '-out_fmt',
      '--output_format',
      type=str,
      help='Output rgb, yuv, hsv, hls (Default: rgb)',
      default='rgb'
  )

  parser.add_argument(
      '-flt',
      '--filter',
      type=str,
      help='Output med, avg (Default: avg)',
      default='avg'
  )

  parser.add_argument(
      '-gen',
      '--gen_graph',
      type=str,
      help='gen_graph ref.json cap.json Generate graphs',
      nargs=2,
      default=''
  )

  parser.add_argument(
  '-cp',
  '--compare',
  type=str,
  nargs=7,
  help='compare two images using given metrics',
  )

  parser.add_argument(
  '-scp',
  '--compare_singlechannel',
  type=str,
  nargs=8,
  help='compare two images using given metrics for given channel',
  )

  args = parser.parse_args()
  pixel_format = args.pixel_format.lower()
  output_format = args.output_format.lower()
  video_size = parse_video_size_arg(args.video_size)
  filter_type = args.filter.lower()

  img_file = args.imgfile
  out_json_file = args.out
  gen_graph_filenames = args.gen_graph
  compare_multichannel= args.compare
  compare_singlechannel= args.compare_singlechannel

  #colorscope -compare metrics [channelId] refImageDir [ref_pixel_format] [ref_video_size] capImageDir [cap_pixel_format] [cap_video_size]
  if compare_multichannel:
   metric, refImgDir, refPxlFmt, refVSz, capImgDir, capPxlFmt, capVSz  = compare_multichannel
   image_loaderRef = ip.imgloader.create(refImgDir, refPxlFmt, refVSz)
   image_loaderCap = ip.imgloader.create(capImgDir, capPxlFmt, capVSz)
   if(metric != 'ssim' and metric != 'psnr'):
      sys.exit('Unknown metric: {}'.format(metric))
   print(ip.qualitymeasurement.QualityMeasurement.create(image_loaderRef,image_loaderCap,metric).process())
   sys.exit(0)

  if compare_singlechannel:
   metric, channelNo, refImgDir, refPxlFmt, refVSz, capImgDir, capPxlFmt, capVSz  = compare_singlechannel
   image_loaderRef = ip.imgloader.create(refImgDir, refPxlFmt, refVSz)
   image_loaderCap = ip.imgloader.create(capImgDir, capPxlFmt, capVSz)
   if(metric != 'ssim' and metric != 'psnr'):
      sys.exit('Unknown metric: {}'.format(metric))
   print(ip.qualitymeasurement.QualityMeasurement.create(image_loaderRef,image_loaderCap,metric+'-sc').process(int(channelNo)))
   sys.exit(0)

  if gen_graph_filenames != '':
    ref_json, cap_json = gen_graph_filenames
    try:
      ip.graph.GraphHS.create(ref_json, cap_json)
    except (AttributeError, ValueError) as err:
      err = sys.exc_info()[1]
      sys.exit('Cannot generate graph: ' + str(err))
    sys.exit(0)

  if not os.path.exists(img_file):
    sys.exit('File not found')

  image_loader = ip.imgloader.create(img_file, pixel_format, video_size)

  try:
    color_reader = ip.colorreader.create(
        output_format,
        image_loader,
        filter_type,
        out_json_file
    )
    color_reader.processing()
  except (AttributeError, ValueError) as err:
    err = sys.exc_info()[1]
    sys.exit('Cannot read image: ' + str(err))


if __name__ == '__main__':
  main()
