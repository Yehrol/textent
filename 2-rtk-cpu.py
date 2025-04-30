"""
This is a sample script for using RTK (Release the krakens)

It takes a file with a list of manifests to download from IIIF (See manifests.txt) and passes it in a suit of commands:

0. It downloads manifests and transform them into CSV files
1. It downloads images from the manifests
2. It applies YALTAi segmentation with line segmentation
3. It fixes up the image PATH of XML files
4. It processes the text as well through Kraken
5. It removes the image files (from the one hunder object that were meant to be done in group)

The batch file should be lower if you want to keep the space used low, specifically if you use DownloadIIIFManifest.
"""
from rtk.task import KrakenAltoCleanUpCommand, YALTAiCommand, KrakenRecognizerCommand
import glob
import time
import argparse

start = time.time()

parser = argparse.ArgumentParser(description='Applies RTK to a set of images')
parser.add_argument('base', metavar='BASE', type=str, help='base folder name')
parser.add_argument('batch', metavar='BATCH', type=str, help='batch index')
parser.add_argument('kraken_model', metavar='KMDL', type=str, help='kraken model')
parser.add_argument('yolo_model', metavar='YMDL', type=str, help='yolo model')
parser.add_argument('line_model', metavar='LMDL', type=str, help='line model')
args = parser.parse_args()

nb_process = 10
books_per_batch = 4 # value set by simon
device = "cpu"

print("base folder name : "  + args.base)
print("processing batch : "  + args.batch)
print("kraken model : "      + args.kraken_model)
print("yolo model : "        + args.yolo_model)
print("line model : "        + args.line_model)
print("number of process : " + str(nb_process))
folders = glob.glob(args.base + args.batch + "/*")


for i in range(0, len(folders), books_per_batch):
    #print("processing folders ", folders[i], folders[i+1], folders[i+2], folders[i+3])
    batch = [
        file
        for folder in folders[i:i+books_per_batch]
        for file in glob.glob(f"{folder}/*.jpg")
    ]
    startYalt = time.time()
    # Apply YALTAi
    print("[Task] Segment, size of batch ", len(batch))
    yaltai = YALTAiCommand(
        batch,
        binary=".venv/bin/yaltai",
        device=device,
        yolo_model=args.yolo_model,
        verbose=True,
        raise_on_error=False,
        allow_failure=False,
        multiprocess=nb_process,
        check_content=False,
        line_model=args.line_model
    )
    yaltai.process()
    endYalt = time.time()
    print("[Time] Yaltai: ", endYalt - startYalt)
    print("Yaltai output files len ", len(yaltai.output_files)) 
    
    # Clean-up the relative filepath of Kraken Serialization
    print("[Task] Clean-Up Serialization")
    cleanup = KrakenAltoCleanUpCommand(yaltai.output_files)
    cleanup.process()
    
    startKrak = time.time()
    # Apply Kraken
    print("[Task] OCR")
    kraken = KrakenRecognizerCommand(
        yaltai.output_files,
        binary=".venv/bin/kraken",
        device=device,
        model=args.kraken_model,
        multiprocess=nb_process,
        check_content=True  # TODO: was written "Required ?", but I see False in the example-manifest.py
    )
    kraken.process()
    endKrak = time.time()
    print("[Time] Kraken: ", endKrak - startKrak)
    

end = time.time()
print("[Time] total: ", end - start)