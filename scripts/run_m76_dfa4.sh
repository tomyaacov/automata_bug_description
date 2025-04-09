#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_m76_dfa4 ### name of the job. replace my_job with your desired job name
#SBATCH --output run_m76_dfa4.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=128G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate lstar ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/l_star_based_bug_description/ || exit

#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M solver -D FE
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M solver -D FE -E
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M solver -D RC
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M solver -D RC -E

#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -D FE
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -D FE -E
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -D RC
#~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -D RC -E




~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -D FE -T 4

