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

    for dataset_path in dataset_paths[2:4]:  # outermost loop
        # if dataset_path.name != 'auto93.csv':
        #     continue
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
    all_table2s = {}
    for dataset, dataset_values in all_results.items():
        table2 = pd.DataFrame(columns=dataset_values['all'].keys(),
                              index=['all to all', 'all to sway1', 'all to sway2', 'sway1 to sway2', 'sway1 to xpln1', 'sway2 to xpln2', 'sway1 to top'])
        for col in dataset_values['all']:
            # For all to all
            table2.loc['all to all', col] = bootstrap(
                dataset_values['all'][col], dataset_values['all'][col])
            # For all to sway1
            table2.loc['all to sway1', col] = bootstrap(
                dataset_values['all'][col], dataset_values['sway1'][col])
            # For all to sway2
            table2.loc['all to sway2', col] = bootstrap(
                dataset_values['all'][col], dataset_values['sway2'][col])
            # For sway1 to sway2
            table2.loc['sway1 to sway2', col] = bootstrap(
                dataset_values['sway1'][col], dataset_values['sway2'][col])
            # For sway1 to xpln1
            table2.loc['sway1 to xpln1', col] = bootstrap(
                dataset_values['sway1'][col], dataset_values['xpln1'][col])
            # For sway2 to xpln2
            table2.loc['sway2 to xpln2', col] = bootstrap(
                dataset_values['sway2'][col], dataset_values['xpln2'][col])
            # For sway1 to top
            table2.loc['sway1 to top', col] = bootstrap(
                dataset_values['sway1'][col], dataset_values['top'][col])
        # set table2 for dataset
        all_table2s[dataset] = table2

    return all_table2s


def displayTable2s(all_table2s):
    print(f'------------- TABLE 2s --------------')
    for dataset, dataset_values in all_table2s.items():
        print(f'Dataset = {dataset}')
        print(dataset_values)
        print()


if __name__ == "__main__":
    results = clusterAllDatasets()
    displayResults(results)
    displayMeanResults(results)
    all_results = createRanges(results)
    print(all_results)
    all_table2s = generateTable2(all_results)
    displayTable2s(all_table2s)


# print(f'Results: \n{results}')
# for k,r in results.items():
#     print(k,'\n')
#     print(r,'\n')
# print(f'{success=}, num:{len(success)}')
# print(f'{failed=}')
