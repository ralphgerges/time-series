import math


def winters_model(data, nb_seasons, alpha, beta, gamma, steps):
    L, S, T, F = [[None for _ in range(len(data) + steps)] for _ in range(4)]

    def get_trend(i):
        if T[i] is not None:
            result = T[i]
        elif i == 0:
            result = (sum(data[nb_seasons:2 * nb_seasons]) - sum(data[:nb_seasons])) / nb_seasons
        else:
            result = round(beta * (get_level(i) - get_level(i - 1)) + (1 - beta) * get_trend(i - 1), 2)
        # print(f'T[{i}]:{result}')
        T[i] = result
        return result

    def get_level(i):
        if L[i] is not None:
            result = L[i]
        elif i == 0:
            result = math.ceil(data[0] / get_seasonality(0))
        elif i < len(data):
            result = round(alpha * (data[i] / get_seasonality(i)) + (1 - alpha) * (get_level(i - 1) + get_trend(i - 1)), 2)
        else:
            result = round(alpha * (get_forecasted(i) / get_seasonality(i)) + (1 - alpha) * (get_level(i - 1) + get_trend(i - 1)), 2)
        # print(f'L[{i}]:{result}')
        L[i] = result
        return result

    def get_seasonality(i):
        if S[i] is not None:
            result = S[i]
        elif i == 0:
            result = round(data[0] / sum(data[:nb_seasons]), 2)
        elif i < len(data):
            result = round(data[i] / sum(data[i//nb_seasons * nb_seasons:(i//nb_seasons + 1) * nb_seasons]), 2)
        else:
            result = gamma * (get_forecasted(i - nb_seasons) / get_level(i - nb_seasons)) + (1 + gamma) * get_seasonality(i - nb_seasons)
        # print(f'S[{i}]:{result}')
        S[i] = result
        return result

    def get_forecasted(i):
        if F[i] is not None:
            result = F[i]
        elif i == 0:
            result = data[0]
        else:
            result = (get_level(i - 1) + get_trend(i - 1)) * get_seasonality(i)
        # print(f'F[{i}]:{result}')
        F[i] = result
        return result
    
    result = []
    for i in range(steps):
        result.append(get_forecasted(len(data) + i))
    return result


d = [53, 22, 37, 45, 58, 25, 40, 50, 62, 27, 44, 56]
result = winters_model(data=d, nb_seasons=4, alpha=0.2, beta=0.2, gamma=0.002, steps=30)
print(result)
