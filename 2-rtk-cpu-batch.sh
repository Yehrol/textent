#!/bin/sh

#SBATCH --job-name=ocr
#SBATCH --output=output.o%j
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=20G
#SBATCH --partition=shared-cpu
#SBATCH --time=10:00:00
#SBATCH --array=1-3

DIR=batch/batch_
KRAKEN_MODEL=models/catmus-print-fondue-tiny-2024-01-31.mlmodel
YOLO_MODEL=models/LADaS.pt
LINE_MODEL=models/blla.mlmodel

echo $SLURM_NODELIST

srun time uv run 2-rtk-cpu.py ${DIR} ${SLURM_ARRAY_TASK_ID} ${KRAKEN_MODEL} ${YOLO_MODEL} ${LINE_MODEL}