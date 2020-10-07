def wallis(loop_range: int) -> float:
    """
    :param loop_range:
    :return:
    """
    def calc_step_wallis(n: int) -> float:
        common_value = (4 * n ** 2)
        return common_value / (common_value - 1)
    pi_over_2: float = calc_step_wallis(1)
    for i in range(2, loop_range):
        val = calc_step_wallis(i)
        pi_over_2 *= val
    return pi_over_2 * 2


def euclidean_GDC(val1 : int, val2 :int) -> int:
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



def main() -> None:
    # wallis
    pi_value: float = wallis(100000)
    print(pi_value)
    # Euclidean_GDC
    print(euclidean_GDC(18, 84))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
