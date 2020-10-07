# todo only positive integers
# todo test with online values
def wallis(loop_range: int) -> float:
    """
    :param loop_range:
    :return:
    """

    def calc_step_wallis(n: int) -> float:
        common_value = (4 * n ** 2)
        return common_value / (common_value - 1)

    pi_over_2: float = 0
    for i in range(1, loop_range + 1):
        val = calc_step_wallis(i)
        if i == 1:
            pi_over_2 = val
        else:
            pi_over_2 *= val
    return pi_over_2 * 2


def euclidean_GDC(val1: int, val2: int) -> int:
    """
    :param val1:
    :param val2:
    :return:
    """
    while val2 != 0:
        val_temp = val2
        val2 = val1 % val2
        val1 = val_temp
    return val1


def sieve_of_erastothenes(max_val: int) -> list:
    """
    :param max_val:
    :return:
    """

    def determine(x, n):
        return x % n == 0

    values: list = list(range(2, max_val + 1))
    for i in values:
        values[:] = [x for x in values if not determine(x, i)]
    return values


def main() -> None:
    # wallis
    for i in range(1, 10):
        print(wallis(i))
    # Euclidean_GDC
    print(euclidean_GDC(18, 84))
    # Sieve
    print(sieve_of_erastothenes(100))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
