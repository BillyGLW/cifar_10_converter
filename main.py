#!/usr/bin/env python3
import argparse

import os

from PIL import Image
import numpy as np

import struct

def parse():
	parser = argparse.ArgumentParser(description='png2cifar10')
	parser.add_argument('--mode', type=int, default=0, help='0 - PNG to CIFER10 (.bin) format, 1 - CIFER10 to PNG format.')
	parser.add_argument('--data', type=str, default=None, help='Input data.')
	parser.add_argument('--out', type=str, default='file_', help='Output data.')
	parser.add_argument('--all', type=str, default=None, help='Input data with png multiple files.')
	return parser.parse_args()


def png_handler(filename=None, destination, new_file, in_folder=None, label=5):
	if in_folder:
		path_folder = os.path.join(os.getcwd(), in_folder)
		im2arr = bytearray()
		for i, x in enumerate(os.listdir(in_folder)):
			image = Image.open(os.path.join(path_folder, x))
			_ = struct.pack('B', label) + np.array(image).transpose().tobytes()
			im2arr = _ + im2arr
	else:
		im = Image.open(filename)
		im2arr = np.array(im).transpose().tobytes()
		im2arr = struct.pack('B', label) + im2arr
	
	with open(os.path.join(os.getcwd(), destination, new_file) , 'wb') as f:
		f.write(im2arr)
	return

def cifer10_handler(filename, out='file_', transpose=0):
	'''
	Transpose argument stands for rotating an image. 
	(choosing from 0-6 ex. 5 means - Image.tranpose)
	'''
	dt = np.dtype('uint8')
	dt = dt.newbyteorder('<')

	with open(filename, 'rb') as f:
		byte_im = f.read()
	file_size = len(np.frombuffer(byte_im, dtype=dt))
	files_number = int(file_size/3073)

	for i in range(1, files_number + 1):
		im2arr = np.frombuffer(byte_im[1:3073], dtype=dt)
		im2arr = np.array(im2arr)
		im2arr = np.reshape(im2arr, [3,32,32])
		im2arr = np.transpose(im2arr, [1,2,0])
		im = Image.fromarray(im2arr).transpose(method=transpose)
		im.save('data/images/%s_%d.png' % (out, i), format='png')
		byte_im = byte_im[3073:]
	return im

if __name__ == "__main__":
	args = parse()
	if args.mode:
		# 3073 size of single image with label
		png_handler(args.data, 'data\\bin', args.out, args.all)
	elif args.mode == 0:
		from_bin_to_png = cifer10_handler(args.data, args.out)
	else:
		print("No mode value")