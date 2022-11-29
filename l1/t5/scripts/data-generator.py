"""Script for generation of artificial datasets."""
import os
import argparse
import json
import sys
sys.path.insert(1, os.getcwd())
from typing import List
from typing import Tuple

from sklearn.datasets import make_regression


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num-samples',
        required=True,
        help='Number of samples to generate',
        type=int,
    )
    parser.add_argument(
        '--out-dir',
        required=False,
        help='Name of directory to save generated data',
        type=str,
        default='/data',
    )

    return parser.parse_args()


def generate_data(num_samples: int) -> Tuple[List[float], List[float]]:
    """Generated X, y with given number of data samples."""
    X, y = make_regression(n_samples=num_samples, n_features=1, noise=0.1)
    return {'input': list(X.flatten()), 'output': list(y)}


def main() -> None:
    """Runs script."""
    args = get_args()

    out_dir = os.getcwd()+args.out_dir
    num_samples = args.num_samples
    data = generate_data(args.num_samples)

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    print(f'{out_dir}/dataset_{num_samples}')
    
    with open(f'{out_dir}/dataset_{num_samples}.json', 'w') as outfile:
        json.dump(data, outfile, indent=1)


if __name__ == '__main__':
    main()
