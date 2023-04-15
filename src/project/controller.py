from pathlib import Path
import numerics
import config
import traceback
import time
from tests import projectTest
from collections import defaultdict
import pandas as pd
from stats import bootstrap, cliffsDelta


# output_path = Path('../../etc/out/project/')
# print(dataset_paths)

success = []
failed = []
RUNS = 3
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


def clusterAllDatasets():
    dataset_paths = [f for f in Path(
        '../../etc/data/project/').iterdir() if f.is_file()]
    results = defaultdict(list)

    for dataset_path in dataset_paths:  # outermost loop
        if dataset_path.name != 'auto93.csv':
            continue
        print(f'-----------------------------------------------------------')
        for i in range(RUNS):
            numerics.Seed = time.time()
            print(
                f'Dataset={dataset_path.name}\tRun={i}/{RUNS}\tSeed={numerics.Seed}')
            config.the['file'] = str(dataset_path)
            result = None
            while result is None:
                try:
                    result = projectTest()
                except Exception as e:
                    result = None
                    numerics.Seed = time.time()
            results[dataset_path.name].append(result)
    return results


def displayMeanResults(results: dict[str, list]):
    print('------------ MEAN RESULTS -------------')
    for dataset, outputs in results.items():
        print(f'Dataset={dataset}')
        mean = pd.concat(outputs).groupby(level=0).mean()
        print(mean)
        print()


def displayResults(results: dict[str, list]):
    print('------------ RESULTS -------------')
    for dataset, outputs in results.items():
        for i, output in enumerate(outputs, 1):
            print(f'Dataset={dataset}\tRun={i}/{RUNS}')
            print(output)
            print()


def createRanges(results: dict[str, list]):
    data_rxs = {}
    for dataset, outputs in results.items():
        rxs = {}
        for output in outputs:
            d = output.T.to_dict('dict')
            # we add everything to rx
            for row, row_value in d.items():
                for col, col_value in row_value.items():
                    if row not in rxs:
                        rxs[row] = {}
                    if col not in rxs[row]:
                        rxs[row][col] = []
                    rxs[row][col].append(col_value)
        data_rxs[dataset] = rxs
    return data_rxs


def generateTable2(all_results):
    for dataset, dataset_values in all_results.items():
        print(f'Dataset = {dataset}')
        # For all
        all_to_all = {}
        for col, col_value in dataset_values['all'].items():
            all_to_all[col] = bootstrap(col_value, col_value)
        print(all_to_all)


if __name__ == "__main__":
    results = clusterAllDatasets()
    displayResults(results)
    displayMeanResults(results)
    all_results = createRanges(results)
    print(all_results)
    generateTable2(all_results)


# print(f'Results: \n{results}')
# for k,r in results.items():
#     print(k,'\n')
#     print(r,'\n')
# print(f'{success=}, num:{len(success)}')
# print(f'{failed=}')
