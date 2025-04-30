# Dependencies

- python uv : https://github.com/astral-sh/uv?tab=readme-ov-file#installation

# Run

## 1. Download the books

### Command

```
uv run 0-download-books.py metadata_sample.tsv books 1
```

### Help

```
usage: 0-download-books.py [-h] IN OUT COL

Download books from a metadata file.

positional arguments:
  IN          source metadata file (tsv)
  OUT         folder where files are stored
  COL         index of column containing URL in metadata file
```

## 2. Segmentation + OCR

### Single batch processing

- even if you are not using multiple batch processing, you must provide a batch index. for example, you can rename your books folder to `batch_1`

#### Command

```
uv run 2-rtk-cpu.py batch_ 1 models/catmus-print-fondue-tiny-2024-01-31.mlmodel models/LADaS.pt models/blla.mlmodel
```

#### Help

```
usage: 2-rtk-cpu.py [-h] BASE BATCH KMDL YMDL LMDL

Applies RTK to a set of images.

positional arguments:
  BASE        base folder name
  BATCH       batch index
  KMDL        kraken model
  YMDL        yolo model
  LMDL        line model
```

### Multiple batch processing (Slurm cluster)

- Modify 2-rtk-cpu-batch.sh
  - array: change according to the number of batch made with 1-batch.py
  - cpus-per-task: value higher than 10 could lead to instability
  - DIR: change according to the batch location

#### Command

- first, create batches

```
uv run 1-batch.py books batch 3
```

- then, process them

```
sbatch 2-rtk-cpu-batch.sh
```

#### Help

```
usage: 1-batch.py [-h] IN OUT NB

Split a directory into batches

positional arguments:
  IN          Folder where files are stored
  OUT         Folder where files will be copied
  NB          Number of batches to create
```

## 3. Generate TEI

### Command

- first, convert original textent metadata to ladas2tei format

```
uv run 3-create-ladas2tei-metadata.py metadata_sample.tsv l2t_metadata.tsv
```

- then, convert alto to TEI

```
uv run 4-ladas2tei.py batch l2t_metadata.tsv
```

### Help

```
usage: 3-create-ladas2tei-metadata.py [-h] IN OUT

Convert original textent metadata to ladas2tei format.

positional arguments:
  IN          source metadata file
  OUT         output metadata file
```

```
usage: 4-ladas2tei.py [-h] DIRECTORY CSV_METADATA [PATTERN_HEADER]

Convert alto to TEI.

positional arguments:
  DIRECTORY          directory containing the xml alto files (can contain subfolder)
  CSV_METADATA       tsv file output from 3-create-ladas2tei-metadata.py
  PATTERN_HEADER
```
