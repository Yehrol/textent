```
curl -LsSf https://astral.sh/uv/install.sh | sh

uv run 0-download-books.py metadata_sample.tsv books 1

uv run 1-batch.py books batch 3

uv run 2-rtk-cpu.py batch/batch_ 1 models/catmus-print-fondue-tiny-2024-01-31.mlmodel models/LADaS.pt models/blla.mlmodel

uv run 3-create-ladas2tei-metadata.py metadata_sample.tsv l2t_metadata.tsv

uv run 4-ladas2tei.py l2t_metadata.tsv
```
