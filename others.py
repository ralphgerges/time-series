mean = lambda x: round(sum(x)/len(x), 2)
mean_absolute_deviation = lambda nums: sum([abs(num - mean(nums)) for num in nums])
mean_squared_deviation = lambda nums: sum([(num - mean(nums)) ** 2 for num in nums])
mean_absolute_percentage_deviation = lambda nums: mean_absolute_deviation(nums) / mean(nums) * 100


def moving_average(data: list[float], n: int):
    result = [mean(data[i-n//2:i+(n-n//2)]) if len(data) - n//2 > i >= n//2 else None for i in range(len(data))]
    return result


def linear_interpolation(data: list[float]) -> list[float]:
    result = []
    for i, n in enumerate(data):
        if isinstance(n, int | float):
            result.append(n)
        else:
            if i == 0 or i == len(data) - 1:
                raise ValueError("first or last value cannot be null")
            prev_index, prev = len(result) - 1, result[-1]
            next_index, next = [(j+i+1, x) for j, x in enumerate(data[i+1:]) if x is not None][0]
            slope = (next - prev) / (next_index - prev_index)
            value = prev + slope * (i - prev_index)
            result.append(value)
    return result

if __name__ == '__main__':
    d = [0, None, 10, None, None, 40]
    print(linear_interpolation(d))
    d = [30, 32, 31, 30]
    print(mean_absolute_deviation(d))
    print(mean_squared_deviation(d))
    print(mean_absolute_percentage_deviation(d))
