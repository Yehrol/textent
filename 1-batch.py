import argparse
import os
import shutil
from glob import glob

def split_dir_into_batches(input_dir, output_dir, nb_batches):
	if nb_batches <= 0:
		raise ValueError(f"Number of batches must be greater than 0, got {nb_batches}")
	
	if not os.path.isdir(input_dir):
		raise ValueError(f"{input_dir} isn't a directory")

	subdir = glob(os.path.join(input_dir, '*'))

	for i in range(len(subdir)):
		batch = i % nb_batches + 1

		batch_dir = f'{output_dir}/batch_{batch}'
		os.makedirs(batch_dir, exist_ok=True)

		src = subdir[i]
		dst = os.path.join(batch_dir, os.path.basename(src))
		shutil.copytree(src, dst, dirs_exist_ok=True)
		print(f"Copied {src} to {dst}")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Split a directory into batches')
	parser.add_argument('input', metavar='IN', type=str, help='Folder where files are stored')
	parser.add_argument('output', metavar='OUT', type=str, help='Folder where files will be copied')
	parser.add_argument('nb_batchs', metavar='NB', type=int, help='Number of batches to create')
	args = parser.parse_args()

	split_dir_into_batches(args.input, args.output, args.nb_batchs)