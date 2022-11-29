import os
from typing import List
from concurrent.futures import ProcessPoolExecutor

from lr import base


class LinearRegressionProcess(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        self._coef = [0, 0]

        N = len(X)
        mean_x = sum(X)/len(X)
        mean_y = sum(y)/len(y)

        cpu_num = os.cpu_count()

        batches = []        
        for i in range(cpu_num):
            batches.append(list(range(N))[i::cpu_num])

        part_slope = []
        with ProcessPoolExecutor(max_workers=cpu_num) as executor:
            for i in range(cpu_num):
                task = executor.submit(self.count_slope, X, y, batches[i],
                                    mean_x, mean_y)
                part_slope.append(task)
        
        dividend, divisor = 0, 0
        for task in part_slope:
            dend, sor = task.result()
            dividend += dend
            divisor += sor
        
        slope = dividend / divisor
        intercept = mean_y - slope * mean_x

        self._coef[0] = intercept
        self._coef[1] = slope

    def count_slope(self, X, y, batch, mean_x, mean_y):
        dividend, divisor = 0, 0
        for index in batch:
            dividend += (X[index] - mean_x) * (y[index] - mean_y)
            divisor += (X[index] - mean_x) ** 2
        return dividend, divisor