from pathlib import Path
import numerics
import config
import traceback
import time
from tests import projectTest
from collections import defaultdict
import pandas as pd
from stats import bootstrap, cliffsDelta
import pickle
from collections import Counter

RUNS = 2
RE_RUNS = 5


def getAllDatasets():
    return [f for f in Path(
        '../../etc/data/project/').iterdir() if f.is_file()]


def clusterDataset(dataset_path: Path):
    clustered_results = []
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
        clustered_results.append(result)
    return clustered_results


def getTable1(clustered_result):
    table1 = pd.concat(clustered_result).groupby(level=0).mean().round(2)
    return table1


def createRanges(clustered_result):
    rxs = {}
    for output in clustered_result:
        d = output.T.to_dict('dict')
        # we add everything to rx
        for row, row_value in d.items():
            for col, col_value in row_value.items():
                if row not in rxs:
                    rxs[row] = {}
                if col not in rxs[row]:
                    rxs[row][col] = []
                rxs[row][col].append(col_value)
    return rxs


def getTable2(range_result):
    table2 = pd.DataFrame(columns=range_result['all'].keys(),
                          index=['all to all', 'all to sway1', 'all to sway2', 'sway1 to sway2', 'sway1 to xpln1', 'sway2 to xpln2', 'sway1 to top', 'sway2 to top'])

    sway1_equals_sway2 = [False]*len(range_result['all'])

    for i, col in enumerate(range_result['all']):
        # For all to all
        table2.loc['all to all', col] = "=" if bootstrap(range_result['all'][col], range_result['all'][col]) and cliffsDelta(
            range_result['all'][col], range_result['all'][col]) else "≠"
        # For all to sway1
        table2.loc['all to sway1', col] = "=" if bootstrap(range_result['all'][col], range_result['sway1'][col]) and cliffsDelta(
            range_result['all'][col], range_result['sway1'][col]) else "≠"
        # For all to sway2
        table2.loc['all to sway2', col] = "=" if bootstrap(range_result['all'][col], range_result['sway2'][col]) and cliffsDelta(
            range_result['all'][col], range_result['sway2'][col]) else "≠"
        # For sway1 to sway2
        table2.loc['sway1 to sway2', col] = "=" if bootstrap(range_result['sway1'][col], range_result['sway2'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['sway2'][col]) else "≠"
        # check if sway1 equals sway2
        sway1_equals_sway2[i] = True if table2.loc['sway1 to sway2',
                                                   col] == '=' else False
        # For sway1 to xpln1
        table2.loc['sway1 to xpln1', col] = "=" if bootstrap(range_result['sway1'][col], range_result['xpln1'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['xpln1'][col]) else "≠"
        # For sway2 to xpln2
        table2.loc['sway2 to xpln2', col] = "=" if bootstrap(range_result['sway2'][col], range_result['xpln2'][col]) and cliffsDelta(
            range_result['sway2'][col], range_result['xpln2'][col]) else "≠"
        # For sway1 to top
        table2.loc['sway1 to top', col] = "=" if bootstrap(range_result['sway1'][col], range_result['top'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['top'][col]) else "≠"
        # For sway2 to top
        table2.loc['sway2 to top', col] = "=" if bootstrap(range_result['sway2'][col], range_result['top'][col]) and cliffsDelta(
            range_result['sway2'][col], range_result['top'][col]) else "≠"

    return table2


def generateBothTablesForDataset(dataset_path: Path, retry_attempt: int = 0):
    clustered_results = clusterDataset(dataset_path)
    # print(f'{clustered_results=}')
    table1 = getTable1(clustered_results)
    # print(f'{table1=}')
    range_result = createRanges(clustered_results)
    table2 = getTable2(range_result)

    # check if sway1=sway2
    counts = Counter(table2.loc['sway1 to sway2'].to_list())
    print(f'{counts=}')
    different = True if counts['≠'] == len(
        table2.loc['sway1 to sway2'].to_list()) else False
    print(different, retry_attempt)

    if retry_attempt == RE_RUNS or different:
        return [table1, table2]

    # recursive call
    return generateBothTablesForDataset(dataset_path, retry_attempt+1)


def writeOutputsForDatasets(dataset_tables: dict[list], text_filename: str = 'project.out', latex_filename: str = 'project_latex.out', terminal_output: bool = True):
    text_file = Path('../../etc/out') / text_filename
    latex_file = Path('../../etc/out') / latex_filename
    with text_file.open('w') as f1, latex_file.open('w') as f2:
        for dataset, tables in dataset_tables.items():
            table1, table2 = tables[0], tables[1]
            # Write to terminal out
            if terminal_output:
                print(f'\nX{dataset:-^40}X\n')
                print(table1)
                print("\n")
                print(table2)

            # Write to text file
            f1.write(f'\n\nX{dataset:-^50}X\n\n')
            f1.write(table1.to_string())
            f1.write("\n\n")
            f1.write(table2.to_string())

            # Write to latex file
            f2.write(f'\n\nX{dataset:-^50}X\n\n')
            f2.write(table1.to_latex(float_format="%.2f"))
            f2.write("\n\n")
            f2.write(table2.to_latex())


def serializeObjectToFile(object, filename: str = 'objs.pkl'):
    text_file = Path('../../etc/out') / filename
    with text_file.open('wb') as f:
        pickle.dump(object, f)
    return text_file.absolute()


def deserializeFileToObject(filename: str = 'objs.pkl') -> list:
    text_file = Path('../../etc/out') / filename
    with text_file.open('rb') as f:
        objects = pickle.load(f)
    return objects


def main():
    datasets = getAllDatasets()

    dataset_tables = {}
    for dataset in datasets[2:4]:
        tables = generateBothTablesForDataset(dataset)
        dataset_tables[dataset.name] = tables

    writeOutputsForDatasets(dataset_tables)
    serializeObjectToFile(dataset_tables)


# def clusterAllDatasets(dataset_name=None):
#     dataset_paths = [f for f in Path(
#         '../../etc/data/project/').iterdir() if f.is_file()]
#     results = defaultdict(list)

#     # filter and cluster only those datasets that have been asked for
#     if dataset_name:
#         print("XXXXXXXXXX", dataset_name)
#         updated_dataset_paths = []
#         for dataset_path in dataset_paths:
#             if dataset_name in dataset_path.name:
#                 updated_dataset_paths.append(dataset_path)
#         dataset_paths = updated_dataset_paths
#     else:
#         dataset_paths = dataset_paths[2:4]
#     for dataset_path in dataset_paths:  # outermost loop
#         # if dataset_path.name != 'auto93.csv':
#         #     continue
#         print(f'-----------------------------------------------------------')
#         for i in range(RUNS):
#             numerics.Seed = time.time()
#             print(
#                 f'Dataset={dataset_path.name}\tRun={i}/{RUNS}\tSeed={numerics.Seed}')
#             config.the['file'] = str(dataset_path)
#             result = None
#             while result is None:
#                 try:
#                     result = projectTest()
#                 except Exception as e:
#                     result = None
#                     numerics.Seed = time.time()
#             results[dataset_path.name].append(result)
#     return results


# def displayMeanResults(results: dict[str, list]):
#     print('------------ MEAN RESULTS -------------')
#     meantable = {}
#     for dataset, outputs in results.items():
#         print(f'Dataset={dataset}')
#         print(f'{outputs=}')
#         mean = pd.concat(outputs).groupby(level=0).mean().round(2)
#         print(mean)
#         meantable[dataset] = mean
#         print()
#     return meantable


# def displayResults(results: dict[str, list]):
#     print('------------ RESULTS -------------')
#     for dataset, outputs in results.items():
#         for i, output in enumerate(outputs, 1):
#             print(f'Dataset={dataset}\tRun={i}/{RUNS}')
#             print(output)
#             print()


# def createRanges2(results: dict[str, list]):
#     data_rxs = {}
#     for dataset, outputs in results.items():
#         rxs = {}
#         for output in outputs:
#             d = output.T.to_dict('dict')
#             # we add everything to rx
#             for row, row_value in d.items():
#                 for col, col_value in row_value.items():
#                     if row not in rxs:
#                         rxs[row] = {}
#                     if col not in rxs[row]:
#                         rxs[row][col] = []
#                     rxs[row][col].append(col_value)
#         data_rxs[dataset] = rxs
#     return data_rxs


# def generateTable2(all_results):
#     all_table2s = {}
#     for dataset, dataset_values in all_results.items():
#         table2 = pd.DataFrame(columns=dataset_values['all'].keys(),
#                               index=['all to all', 'all to sway1', 'all to sway2', 'sway1 to sway2', 'sway1 to xpln1', 'sway2 to xpln2', 'sway1 to top'])

#         sway1_equals_sway2 = [False]*len(dataset_values['all'])
#         for i, col in enumerate(dataset_values['all']):
#             # For all to all
#             table2.loc['all to all', col] = "=" if bootstrap(dataset_values['all'][col], dataset_values['all'][col]) and cliffsDelta(
#                 dataset_values['all'][col], dataset_values['all'][col]) else "≠"
#             # For all to sway1
#             table2.loc['all to sway1', col] = "=" if bootstrap(dataset_values['all'][col], dataset_values['sway1'][col]) and cliffsDelta(
#                 dataset_values['all'][col], dataset_values['sway1'][col]) else "≠"
#             # For all to sway2
#             table2.loc['all to sway2', col] = "=" if bootstrap(dataset_values['all'][col], dataset_values['sway2'][col]) and cliffsDelta(
#                 dataset_values['all'][col], dataset_values['sway2'][col]) else "≠"
#             # For sway1 to sway2
#             table2.loc['sway1 to sway2', col] = "=" if bootstrap(dataset_values['sway1'][col], dataset_values['sway2'][col]) and cliffsDelta(
#                 dataset_values['sway1'][col], dataset_values['sway2'][col]) else "≠"
#             # check if sway1 equals sway2
#             sway1_equals_sway2[i] = True if table2.loc['sway1 to sway2',
#                                                        col] == '=' else False
#             # For sway1 to xpln1
#             table2.loc['sway1 to xpln1', col] = "=" if bootstrap(dataset_values['sway1'][col], dataset_values['xpln1'][col]) and cliffsDelta(
#                 dataset_values['sway1'][col], dataset_values['xpln1'][col]) else "≠"
#             # For sway2 to xpln2
#             table2.loc['sway2 to xpln2', col] = "=" if bootstrap(dataset_values['sway2'][col], dataset_values['xpln2'][col]) and cliffsDelta(
#                 dataset_values['sway2'][col], dataset_values['xpln2'][col]) else "≠"
#             # For sway1 to top
#             table2.loc['sway1 to top', col] = "=" if bootstrap(dataset_values['sway1'][col], dataset_values['top'][col]) and cliffsDelta(
#                 dataset_values['sway1'][col], dataset_values['top'][col]) else "≠"
#             # For sway2 to top
#             table2.loc['sway2 to top', col] = "=" if bootstrap(dataset_values['sway2'][col], dataset_values['top'][col]) and cliffsDelta(
#                 dataset_values['sway2'][col], dataset_values['top'][col]) else "≠"

#         # rerun for dataset if sway1=sway2
#         if any(sway1_equals_sway2) == True:
#             results = clusterAllDatasets(dataset)
#             print(results)
#             # # displayResults(results)
#             # # meantable = displayMeanResults(results)
#             # all_results = createRanges(results)
#             # # print(all_results)
#             # all_table2s = generateTable2(all_results)
#             # # displayTable2s(all_table2s)
#             # print(all_table2s.keys())
#             # table2 = all_table2s[dataset]

#             # set table2 for dataset
#         all_table2s[dataset] = table2

#     return all_table2s


# def serializeObjectsToFile(objects: list, filename: str = 'objs.pkl'):
#     # Saving the objects:
#     with open(filename, 'wb') as f:
#         pickle.dump(objects, f)


# def deserializeFileToObjects(filename: str = 'objs.pkl') -> list:
#     # Saving the objects:
#     with open(filename, 'rb') as f:
#         objects = pickle.load(f)
#     return objects


# def dataframeToLatexTables(table1s: list, table2s: list, filename: str = 'project.txt'):
#     path = Path('../../etc/out') / filename
#     with path.open('w') as f:
#         for file in table1s:
#             f.write(
#                 f"-------------------------{file}-------------------------\n")
#             f.write(table1s[file].to_latex(float_format="%.2f"))
#             f.write("\n\n")
#             f.write(table2s[file].to_latex())
#             f.write("\n\n")


# def displayTable2s(all_table2s):
#     print(f'------------- TABLE 2s --------------')
#     for dataset, dataset_values in all_table2s.items():
#         print(f'Dataset = {dataset}')
#         print(dataset_values)
#         print()


if __name__ == "__main__":
    # results = clusterAllDatasets()
    # # displayResults(results)
    # meantable = displayMeanResults(results)
    # print(f'YYYY{meantable=}')
    # all_results = createRanges(results)
    # # print(all_results)
    # all_table2s = generateTable2(all_results)
    # displayTable2s(all_table2s)
    # serializeObjectsToFile([all_results, all_table2s])
    # print('~~~~~~~~~~~~~~~~~')
    # a, b = deserializeFileToObjects()
    # displayTable2s(b)
    # dataframeToLatexTables(meantable, all_table2s)
    main()
