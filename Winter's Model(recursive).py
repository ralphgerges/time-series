import math


ALPHA = 0.2
BETA = 0.3
GAMMA = 0.002
DATA = [53, 22, 37, 45, 58, 25, 40, 50, 62, 27, 44, 56]
N = 4

def get_trend(i):
    if i == 0:
        result = (sum(DATA[N:2 * N]) - sum(DATA[:N])) / N
    else:
        result = round(BETA * (get_level(i) - get_level(i - 1)) + (1 - BETA) * get_trend(i - 1), 2)
    # print(f'T[{i}]:{result}')
    return result


def get_level(i):
    if i == 0:
        result = math.ceil(DATA[0] / get_seasonality(0))
    elif i < len(DATA):
        result = round(ALPHA * (DATA[i] / get_seasonality(i)) + (1 - ALPHA) * (get_level(i - 1) + get_trend(i - 1)), 2)
    else:
        result = round(ALPHA * (get_forecasted(i) / get_seasonality(i)) + (1 - ALPHA) * (get_level(i - 1) + get_trend(i - 1)), 2)
    # print(f'L[{i}]:{result}')
    return result


def get_seasonality(i):
    if i == 0:
        result = round(DATA[0] / sum(DATA[:N]), 2)
    elif i < len(DATA):
        result = round(DATA[i] / sum(DATA[i//N * N:(i//N + 1) * N]), 2)
    else:
        result = GAMMA * (get_forecasted(i - N) / get_level(i - N)) + (1 + GAMMA) * get_seasonality(i - N)
    # print(f'S[{i}]:{result}')
    return result


def get_forecasted(i):
    if i == 0:
        result = DATA[0]
    else:
        result = (get_level(i - 1) + get_trend(i - 1)) * get_seasonality(i)
    #  print(f'F[{i}]:{result}')
    return result


for i in range(14):
    print(get_forecasted(i))
