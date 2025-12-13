# RAISE
## RBP Activity Inference from Splicing Events
RAISE is a computational pipeline for identifying the activity of RNA-binding proteins (RBPs). It integrates CLIP-seq peaks, motifs, and alternative splicing (AS) data to construct a splicing regulatory network, and infers RBP activities using regression modeling.
<img width="1069" height="1252" alt="image" src="https://github.com/user-attachments/assets/5e26d81a-fa07-4f7e-bd9d-556d5479ed43" />







### Installation

#### Option 1. Install RAISE through pip [recommended]
```bash
conda create -n RAISE python=3.8
pip install RAISE
```

#### Option 2. Local installation
```bash
conda create -n RAISE python=3.7
git clone https://github.com/liuyilei8969/RAISE.git
cd RAISE
pip install .
```


### Usage
#### 1. Identify targets of an RBP
```bash
usage: find_target.py [-h] --rmats RMATS --clip_peaks CLIP_PEAKS --ref_genome REF_GENOME --rbp_motif RBP_MOTIF --cell_line CELL_LINE --rbp RBP --output
                      OUTPUT [--max_iter MAX_ITER] [--tol TOL]

EM algorithm for inferring RBP targets using motif, CLIP peaks, and PSI changes.

options:
  -h, --help                             show this help message and exit
  --rmats RMATS                          Input rMATS SE.MATS.JC.txt file.
  --clip_peaks CLIP_PEAKS                Input CLIP peaks BED file.
  --ref_genome REF_GENOME                Reference genome in FASTA format.
  --rbp_motif RBP_MOTIF                  RBP motif file with two columns: RBP and motif.
  --cell_line CELL_LINE                  Cell line name, used to label the output file.
  --rbp RBP                              Target RBP name.
  --output OUTPUT                        Output directory.
  --max_iter MAX_ITER                    Maximum number of EM iterations.
  --tol TOL                              Convergence threshold for EM.
```
#### 2. Construct RBP-AS network
```bash
usage: construct_network.py [-h] --Target_dir TARGET_DIR [--threshold THRESHOLD] --DE_dir DE_DIR --output OUTPUT

Build a splicing regulatory network from target predictions and RBP expression changes.

options:
  -h, --help                             show this help message and exit
  --Target_dir TARGET_DIR                Directory containing RBP target result folders
  --threshold THRESHOLD                  Minimum conditional probability P(T|S,M,C) to include interaction (default: 0.6)
  --DE_dir DE_DIR                        Directory containing RBP expression change files
  --output OUTPUT                        Path to output GEXF file for the constructed network
```
#### 3. Infer RBP activity
```bash
usage: calculate_activity.py [-h] --diffAS DIFFAS --network NETWORK --output OUTPUT

Infer RBP activity from a splicing regulatory network using ridge regression.

options:
  -h, --help                             show this help message and exit
  --diffAS DIFFAS                        Path to the rMATS differential splicing results file
  --network NETWORK                      Path to the splicing regulatory network
  --output OUTPUT                        Output file for inferred RBP activity scores
```


### Example & Test
Examples are provided in the test/ directory: https://github.com/liuyilei8969/RAISE/tree/main/test     
Data are provided in the data/ directory for users' convenience: https://github.com/liuyilei8969/RAISE/tree/main/data   
   
Note: All differential splicing results should be provided in the rMATS format. For users' convenience, we also provide scripts to either convert data into this format or perform a simple differential splicing analysis using a limma test.


### Requirements
Python >= 3.8

Packages: pandas, numpy, networkx, scikit-learn, argparse

