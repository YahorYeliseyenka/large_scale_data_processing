from typing import List

from lr import base


class LinearRegressionSequential(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        self._coef = [0, 0]

        mean_x = sum(X)/len(X)
        mean_y = sum(y)/len(y)

        slope_dividend, slope_divisor = 0, 0

        for x_val, y_val in zip(X, y):
            slope_dividend += (x_val - mean_x) * (y_val - mean_y)
            slope_divisor += (x_val - mean_x) ** 2
        
        slope = slope_dividend / slope_divisor
        intercept = mean_y - slope * mean_x

        self._coef[0] = intercept
        self._coef[1] = slope
