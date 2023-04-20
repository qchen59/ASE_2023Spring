from pathlib import Path
import numerics
import config
from tests import projectTest
import pandas as pd
from stats import bootstrap, cliffsDelta
import pickle
from collections import Counter
import random

RUNS = 20
RE_RUNS = 1


def getAllDatasets():
    return [f for f in Path(
        '../../etc/data/project/').iterdir() if f.is_file()]


def clusterDataset(dataset_path: Path):
    clustered_results = []
    times = {
        'sway1_time': 0,
        'sway2_time': 0,
        'sway3_time': 0,
    }
    for i in range(RUNS):
        numerics.Seed = random.randint(1, 100000)
        print(
            f'Dataset={dataset_path.name}\tRun={i}/{RUNS}\tSeed={numerics.Seed}')
        config.the['file'] = str(dataset_path)
        result = None
        while result is None:
            try:
                result, sway1_time, sway2_time, sway3_time = projectTest()
                times['sway1_time'] += sway1_time
                times['sway2_time'] += sway2_time
                times['sway3_time'] += sway3_time
            except Exception as e:
                result = None
                numerics.Seed = random.randint(1, 100000)
        clustered_results.append(result)
    return clustered_results, times


def getTable1(clustered_result):
    table1 = pd.concat(clustered_result).groupby(level=0).mean().round(2)
    return table1


def getAverageRuntime(times: dict):
    for sway_type, sway_time in times.items():
        times[sway_type] = [sway_time/RUNS]
    return pd.DataFrame.from_dict(times)


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
                          index=['all to all', 'all to sway1', 'all to sway2', 'all to sway3', 'sway1 to sway2', 'sway1 to sway3', 'sway1 to xpln1', 'sway2 to xpln2', 'sway3 to xpln3', 'sway1 to top', 'sway2 to top', 'sway3 to top'])

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
        # For all to sway3
        table2.loc['all to sway3', col] = "=" if bootstrap(range_result['all'][col], range_result['sway3'][col]) and cliffsDelta(
            range_result['all'][col], range_result['sway3'][col]) else "≠"
        # For sway1 to sway2
        table2.loc['sway1 to sway2', col] = "=" if bootstrap(range_result['sway1'][col], range_result['sway2'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['sway2'][col]) else "≠"
        # For sway1 to sway3
        table2.loc['sway1 to sway3', col] = "=" if bootstrap(range_result['sway1'][col], range_result['sway3'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['sway3'][col]) else "≠"
        # check if sway1 equals sway2
        sway1_equals_sway2[i] = True if table2.loc['sway1 to sway2',
                                                   col] == '=' else False
        # For sway1 to xpln1
        table2.loc['sway1 to xpln1', col] = "=" if bootstrap(range_result['sway1'][col], range_result['xpln1'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['xpln1'][col]) else "≠"
        # For sway2 to xpln2
        table2.loc['sway2 to xpln2', col] = "=" if bootstrap(range_result['sway2'][col], range_result['xpln2'][col]) and cliffsDelta(
            range_result['sway2'][col], range_result['xpln2'][col]) else "≠"
        # For sway3 to xpln3
        table2.loc['sway3 to xpln3', col] = "=" if bootstrap(range_result['sway3'][col], range_result['xpln3'][col]) and cliffsDelta(
            range_result['sway3'][col], range_result['xpln3'][col]) else "≠"
        # For sway1 to top
        table2.loc['sway1 to top', col] = "=" if bootstrap(range_result['sway1'][col], range_result['top'][col]) and cliffsDelta(
            range_result['sway1'][col], range_result['top'][col]) else "≠"
        # For sway2 to top
        table2.loc['sway2 to top', col] = "=" if bootstrap(range_result['sway2'][col], range_result['top'][col]) and cliffsDelta(
            range_result['sway2'][col], range_result['top'][col]) else "≠"
        # For sway3 to top
        table2.loc['sway3 to top', col] = "=" if bootstrap(range_result['sway3'][col], range_result['top'][col]) and cliffsDelta(
            range_result['sway3'][col], range_result['top'][col]) else "≠"

    return table2


# def generateBothTablesForDataset(dataset_path: Path, retry_attempt: int = 0):
def generateBothTablesForDataset(dataset_path: Path):
    bestScore, bestRun = 0, None
    for i in range(RE_RUNS):
        clustered_results, times = clusterDataset(dataset_path)
        table_time = getAverageRuntime(times)
        table1 = getTable1(clustered_results)
        range_result = createRanges(clustered_results)
        table2 = getTable2(range_result)
        # check if sway1=sway2
        counts = Counter(table2.loc['sway1 to sway2'].to_list())
        print(f'{counts=}')
        different = True if counts['≠'] == len(
            table2.loc['sway1 to sway2'].to_list()) else False
        if counts['≠'] >= bestScore:
            print("BEST: ", counts['≠'], bestScore)
            bestScore = counts['≠']
            bestRun = [table1, table2, table_time]
        if different:
            break
    return bestRun


def writeOutputsForDatasets(dataset_tables: dict[list], text_filename: str = 'project.out', latex_filename: str = 'project_latex.out', terminal_output: bool = True):
    text_file = Path('../../etc/out') / text_filename
    latex_file = Path('../../etc/out') / latex_filename
    with text_file.open('w') as f1, latex_file.open('w') as f2:
        for dataset, tables in dataset_tables.items():
            table1, table2, table_times = tables[0], tables[1], tables[2]
            # Write to terminal out
            if terminal_output:
                print(f'\nX{dataset:-^40}X\n')
                print(table1)
                print("\n")
                print(table2)
                print("\n")
                print(table_times)

            # Write to text file
            f1.write(f'\n\nX{dataset:-^50}X\n\n')
            f1.write(table1.to_string())
            f1.write("\n\n")
            f1.write(table2.to_string())
            f1.write("\n\n")
            f1.write(table_times.to_string())

            # Write to latex file
            f2.write(f'\n\nX{dataset:-^50}X\n\n')
            f2.write(table1.to_latex(float_format="%.2f"))
            f2.write("\n\n")
            f2.write(table2.to_latex())
            f2.write("\n\n")
            f2.write(table_times.to_latex())


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
    for dataset in datasets:
        tables = generateBothTablesForDataset(dataset)
        dataset_tables[dataset.name] = tables

    writeOutputsForDatasets(dataset_tables)
    serializeObjectToFile(dataset_tables)


if __name__ == "__main__":
    main()
