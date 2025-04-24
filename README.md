```
curl -LsSf https://astral.sh/uv/install.sh | sh

uv run 0-download-books.py metadata_sample.tsv books 13

uv run 1-rtk-cpu.py books_ 1 models/catmus-print-fondue-tiny-2024-01-31.mlmodel models/LADaS.pt models/blla.mlmodel

# je ne comprend pour l'instant pas l'interet
uv run tei_conversion/multiprocess.py --config tei_conversion/config.yml --version 1.0 --header --sourcedoc --body

uv run 2-create-ladas2tei-metadata.py Metadata_TextEnt.tsv l2t_metadata_bis.tsv

uv run 3-ladas2tei.py l2t_metadata_bis.tsv
```
