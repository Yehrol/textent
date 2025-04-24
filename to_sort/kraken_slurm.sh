#! /bin/sh

#SBATCH --constraint=EPYC-7742
#SBATCH --job-name=ocr
#SBATCH --output=output_fondue-tiny.o%j
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=shared-cpu
#SBATCH --time=10:00:00
#SBATCH --array=1

echo $SLURM_NODELIST
source /home/users/k/kuenzlip/virtualenvs/rtk/bin/activate

srun hostname

srun time python rtk-cpu.py benchmarks/ladas-960-l/fondue-tiny/books/batch_  ${SLURM_ARRAY_TASK_ID} models/catmus-print-fondue-tiny-2024-01-31.mlmodel
