# Functional dependency miner - fd_miner 
The following code allows mining functional dependencies using partition pattern structures

## Installation:
- git clone https://github.com/anonexp/fd_miner.git
- virtualenv venv
- sourve venv/bin/activate
- python -m pip install -r requirements.txt
- python mine_fds.py [dataset]
    - Example: python mine_fds.py diagnostics.csv

## Datasets provided (folder data)
- abalone.csv
- adult.data.csv
- caulkins.csv
- cmc.data.csv
- credit.data.csv
- diagnostics.csv
- forestfires_2xtuples.csv
- forestfires.csv
- hughes.original.csv
- mushroom.csv
- ncvoter_1001r_19c.csv
- pglw00_2xattributes.csv
- pglw00.original.csv
- servo.original.csv

## Observations
Mining some datasets may take several minutes or even hours.
