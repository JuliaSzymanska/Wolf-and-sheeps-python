def wallis(loop_range: int) -> float:
    def calc_step_wallis(n: int) -> float:
        common_value = (4 * n ** 2)
        return common_value / (common_value - 1)
    pi_over_2: float = calc_step_wallis(1)
    for i in range(2, loop_range):
        val = calc_step_wallis(i)
        pi_over_2 *= val
    return pi_over_2 * 2


def main() -> None:
    pi_value: float = wallis(100000)
    print(pi_value)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()