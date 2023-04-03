import os
from pathlib import Path

dataset_paths = [f for f in Path(
    '../../etc/data/project/').iterdir() if f.is_file()]
output_path = Path('../../etc/out/project/')

for dataset_path in dataset_paths[:1]:
    out_file = f'{dataset_path.name.split(".")[0]}.out'
    out_path = output_path/out_file
    # dataset_path = '../../etc/data/project/auto93.csv'
    os.system(
        f'python main.py -g all -f {str(dataset_path)} > {str(out_path)}')
