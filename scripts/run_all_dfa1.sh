#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_all_dfa1 ### name of the job. replace my_job with your desired job name
#SBATCH --output run_all_dfa1.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=100G ### total amount of RAM // 500
#SBATCH --ntasks=1

### Start you code below ####
module load anaconda ### load anaconda module
source activate lstar ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/l_star_based_bug_description/ || exit

~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m158 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m172 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m183 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m24 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m45 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m76 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m95 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m199 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m27 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m164 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m159 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m55 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m135 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m185 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m181 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m201 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m196 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m173 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m41 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m106 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m22 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m167 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m189 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m182 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m131 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m132 -M rpni -T 1
~/.conda/envs/lstar/bin/python ~/repos/l_star_based_bug_description/main.py  -B m54 -M rpni -T 1
