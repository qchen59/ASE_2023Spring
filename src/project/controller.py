from pathlib import Path
import numerics
import config
import traceback
from tests import projectTest


dataset_paths = [f for f in Path(
    '../../etc/data/project/').iterdir() if f.is_file()]
output_path = Path('../../etc/out/project/')
# print(dataset_paths)

success = []
failed = []
# for dataset_path in dataset_paths:
#     if not dataset_path.name == 'auto93.csv':
#         continue
#     print(f'-----------------------------------------------------------')
#     print(f'\nDataset name = {dataset_path.name}')
#     out_file = f'{dataset_path.name.split(".")[0]}.out'
#     out_path = output_path/out_file
#     # dataset_path = '../../etc/data/project/auto93.csv'
#     try:
#         os.system(
#             f'python main.py -g all -f {str(dataset_path)} > {str(out_path)}')
#         success.append(dataset_path.name)
#     except Exception as e:
#         failed.append(dataset_path.name)

results = {}
for dataset_path in dataset_paths:
    if not dataset_path.name == 'coc10000.csv':
        continue
    print(f'-----------------------------------------------------------')
    print(f'\nDataset name = {dataset_path.name}')
    try:
        numerics.Seed = config.the['seed']
        config.the['file'] = str(dataset_path)
        results[dataset_path.name] = projectTest()
        success.append(dataset_path.name)
    except Exception as e:
        print(traceback.format_exc())
        failed.append(dataset_path.name)

print(f'Results: \n{results}')
print(f'{success=}')
print(f'{failed=}')
