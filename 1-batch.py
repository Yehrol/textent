import argparse
import os
import shutil
from math import ceil
from glob import glob

def split_dir_into_batches(input_dir, output_dir, nb_batches):
	if nb_batches <= 0:
		raise ValueError(f"Number of batches must be greater than 0, got {nb_batches}")
	
	if not os.path.isdir(input_dir):
		raise ValueError(f"{input_dir} isn't a directory")

	subdir = glob(os.path.join(input_dir, '*'))

	batch_size = ceil(len(subdir) / nb_batches)

	for i in range(nb_batches):
		batch_dir = f'{output_dir}/batch_{i+1}'
		os.makedirs(batch_dir, exist_ok=True)

		for j in range(batch_size):
			if i * batch_size + j >= len(subdir):
				break
			src = subdir[i * batch_size + j]
			dst = os.path.join(batch_dir, os.path.basename(src))
			shutil.copytree(src, dst, dirs_exist_ok=True)
			print(f"Copied {src} to {dst}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('input', metavar='IN', type=str, help='')
	parser.add_argument('output', metavar='OUT', type=str, help='')
	parser.add_argument('nb_batchs', metavar='NB', type=int, help='')
	args = parser.parse_args()

	split_dir_into_batches(args.input, args.output, args.nb_batchs)