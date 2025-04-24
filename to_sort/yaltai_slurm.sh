#! /bin/sh

#SBATCH --constraint=EPYC-7742
#SBATCH --job-name=ocr
#SBATCH --output=output_ladas-1280-l.o%j
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --partition=shared-cpu
#SBATCH --time=10:00:00
#SBATCH --array=5

echo $SLURM_NODELIST
source /home/users/k/kuenzlip/virtualenvs/rtk/bin/activate

srun hostname

srun time python rtk-yaltai-cpu.py books/batch_  ${SLURM_ARRAY_TASK_ID} models/ladas-960-l.pt
