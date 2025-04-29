# Dependencies

- python uv : https://github.com/astral-sh/uv?tab=readme-ov-file#installation

# Run

## 1. Download the books

```
uv run 0-download-books.py metadata_sample.tsv books 1
```

## 2. Segmentation + OCR

### Local

```
uv run 2-rtk-cpu.py batch/batch_ 1 models/catmus-print-fondue-tiny-2024-01-31.mlmodel models/LADaS.pt models/blla.mlmodel
```

### Batch

change 2-rtk-cpu-batch.sh array according to the number of batch made in step 1

value higher than 10 for cpus-per-task could lead to instability

```
uv run 1-batch.py books batch 3

sbatch 2-rtk-cpu-batch.sh
```

## 3. Generate TEI

```
uv run 3-create-ladas2tei-metadata.py metadata_sample.tsv l2t_metadata.tsv

uv run 4-ladas2tei.py batch l2t_metadata.tsv
```
