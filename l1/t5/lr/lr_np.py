from typing import List
import numpy as np

from lr import base


class LinearRegressionNumpy(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        self._coef = [0, 0]
        
        x = np.array(X)
        y = np.array(y)

        mean_x, mean_y = np.mean(x), np.mean(y)

        slope = np.sum((x-mean_x)*(y-mean_y)) / np.sum(x-mean_x)**2
        intercept = mean_y - slope * mean_x

        self._coef[0] = intercept
        self._coef[1] = slope
