#!/bin/bash

#SBATCH --job-name=update_hmm_job
#SBATCH --chdir=/work/user_name/update_hmm      # <-- insert user name and change working directory if desired
#SBATCH --output=/work/%u/%x-%j.log             # output of stdout
#SBATCH --error=/work/%u/%x-%j.err              # output of stderr
#SBATCH -t 1:00:00
#SBATCH --mem-per-cpu 2G
#SBATCH --cpus-per-task 4

# Before running this script, make sure you have:
# - created a recent mitos2 conda environment
# - installed mitos2
# - all genbank files and HMMs in the correct folder

# ==========================================================
# === configuration: please modify necessary information ===
# ==========================================================

# path to folder containing all genbank-files (*.gb)
GB_DIR="/work/$SLURM_JOB_USER/update_hmm/input_data"

# path to folder containing all HMMs (*.db)
HMM_DIR="/work/$SLURM_JOB_USER/update_hmm/input_hmm"

# path to output folder
OUTPUT_DIR="/work/$SLURM_JOB_USER/update_hmm/output"

# name of mitos2 conda environment
ENV_NAME="mitos2_new"

# ==========================================================

module purge
module load Conda/24.11.2


conda activate $ENV_NAME

update_hmm -gb "$GB_DIR" -hm "$HMM_DIR" -o "$OUTPUT_DIR" --cpu "$SLURM_CPUS_PER_TASK"

conda deactivate
