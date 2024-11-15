def number_list(n):
    res = [f'{1 * i}' * i for i in range(1, n + 1)]
    return int(''.join(res))


if __name__ == '__main__':
    number_input = int(input())
    result = number_list(number_input)
    print(result)