"""Script for time measurement experiments on linear regression models."""
import os
import argparse
import json
import sys
sys.path.insert(1, os.getcwd())
import time
from typing import List
from typing import Tuple
from typing import Type

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lr


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datasets-dir',
        required=False,
        help='Name of directory with generated datasets',
        type=str,
        default='/data'
    )

    return parser.parse_args()


def run_experiments(
    models: List[Type[lr.base.LinearRegression]],
    datasets: List[Tuple[List[float], List[float]]],
) -> pd.DataFrame:
    results = pd.DataFrame({"model": [], "size": [], "time": []})
    for dataset in datasets:
        for model in models:
            regression = model()

            start_time = time.time()
            regression.fit(X=dataset[0], y=dataset[1])
            regression.predict(X=dataset[0])
            end_time = time.time()

            part_res = pd.DataFrame({"model":[model.__name__], 
                    "size":[len(dataset[0])],
                    "time":[end_time-start_time]})
            results = results.append(part_res)
    return results


def make_plot(results: pd.DataFrame) -> None:
    fig, ax = plt.subplots()
    for key, grp in results.sort_values(by=['size']).groupby('model'):
        ax = grp.plot(ax=ax, kind='line', x='size', y='time', label=key,
                      style='.-', title='Linear regression computation time')
    plt.xlabel("number of data points")
    plt.ylabel("execution time")
    plt.savefig(f'../task_5/results/plot-{time.time()}.png')


def read_datasets(datasets_dir):
    data = []
    for file in os.listdir(os.getcwd()+datasets_dir):
        with open(f'{os.getcwd()}/{datasets_dir}/{file}', 'r') as outfile:
            dataset = json.load(outfile)
            data.append((dataset["input"], dataset["output"]))
    return data


def main() -> None:
    """Runs script."""
    args = get_args()

    models = [
        lr.LinearRegressionNumpy,
        lr.LinearRegressionProcess,
        lr.LinearRegressionSequential,
        lr.LinearRegressionThreads,
    ]

    datasets = read_datasets(args.datasets_dir)

    results = run_experiments(models, datasets)

    make_plot(results)


if __name__ == '__main__':
    main()
