import math


class Winters:
    def __init__(self):
        pass

    def train(self, data, m, alpha, beta, gamma):
        if m < 2: raise ValueError('number of seasons must be minimum 2')
        if not isinstance(data, list) or any(not isinstance(value, float | int) for value in data):
            raise ValueError('data must be a list of floats or integers')
        if not all(isinstance(p, int | float) for p in [alpha, beta, gamma]):
            raise ValueError('parameters must be numbers')
        if not (0<=alpha<=1 and 0<=beta<=1 and 0<=gamma<=1):
            raise ValueError('alpha, beta & gamma must be between 0 and 1')
        if len(data) < 2 * m:
            raise ValueError('data must be at least 2 times the number of seasons')

        self.data = data
        self.nb_seasons = m
        self.alpha, self.beta, self.gamma = alpha, beta, gamma
        L, S, T, F = [[0 for _ in range(len(data))] for _ in range(4)]

        i = 0
        S[0] = round(data[0] / sum(data[:m]), 2)
        L[0] = math.ceil(data[0] / S[0])
        T[0] = (sum(data[m:2 * m]) - sum(data[:m])) / m
        F[0] = data[0]

        for i in range(1, len(data)):
            S[i] = round(data[i] / sum(data[i//m * m:(i//m + 1) * m]), 2)
            L[i] = round(alpha * (data[i] / S[i]) + (1 - alpha) * (L[i - 1] + T[i - 1]), 2)
            T[i] = round(beta * (L[i] - L[i - 1]) + (1 - beta) * T[i - 1], 2)
            F[i] = round((L[i - 1] + T[i - 1]) * S[i], 2)

        self.components = {'level': L, 'trend': T, 'seasonality': S}
        self.forecasted = F

    def forcast(self, n: int) -> list[float]:
        if self.forecasted is None:
            raise RuntimeError('Model is not trained yet. use Winters.train() method before forecasting')
        if not isinstance(n, int) or n < 1:
            raise ValueError('n must be a positive integer')

        L, T, S = [nums + [0 for _ in range(n)] for nums in self.components.values()]
        F = self.forecasted
        m = self.nb_seasons
        for i in range(len(self.data), len(self.data) + n):
            S[i] = self.gamma * (F[i - m] / L[i - m]) + (1 + self.gamma) * S[i - m]
            F.append((L[i - 1] + T[i - 1]) * S[i])
            L[i] = self.alpha * (F[i] / S[i - m]) + (1 - self.alpha) * (L[i - 1] + T[i - 1])
            T[i] = self.beta * (L[i] - L[i - 1]) + (1 - self.beta) * T[i - 1]
        result = F[len(self.data):]
        self.forecasted = F[:len(self.data)]
        return result


    def score(self):
        score = {
            'mean_absolute_error': sum([abs(self.data[i] - self.forecasted[i]) for i in range(len(self.data))]),
            'mean_squared_error': sum([(self.data[i] - self.forecasted[i])**2 for i in range(len(self.data))]),
            'mean_absolute_percentage_error': 100 * sum([abs(self.data[i] - self.forecasted[i])/self.data[i] for i in range(len(self.data))])
        }
        return score
    
    

    def displayModelComponents(self):
        print( f"""Trained Model Components
        Level: {self.components['level']}
        Seasonality: {self.components['seasonality']}
        Trend: {self.components['trend']}
        Forecast: {self.forecasted}
        Data:{self.data}
        """)


if __name__ == '__main__':
    d = [53, 22, 37, 45, 58, 25, 40, 50, 62, 27, 44, 56]
    model = Winters()
    model.train(data=d, m=4, alpha=0.2, beta=0.3, gamma=0.002)
    model.displayModelComponents()
    print(f'Forecasted Values: {model.forcast(n=10)}')
    print(f'\n\nModel Evaluation: {model.score()}')
