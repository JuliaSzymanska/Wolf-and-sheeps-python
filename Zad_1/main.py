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


# todo, check if val >= 2
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


# todo cleanup
def least_common_multiple(val1: int, val2: int) -> int:
    """

    :param val1:
    :param val2:
    :return:
    """
    def get_value_divisors(val: int) -> list:
        val_divisors: list = []
        while val > 1:
            # todo optimize
            """
            to jest kiepskie, powinno przynajmniej iść do max sqrt(val) + 1, i jakimś mądrym alg powinienme generować wszystrkie dzielniki
            imagine jakiświelki gigantyczny prime xd 
            """
            possible_values = list(range(2, val + 1))
            for i in possible_values:
                if val % i == 0:
                    val = int(val / i)
                    val_divisors.append(i)
                    break
        return val_divisors
    val1_divisors: list = get_value_divisors(val1)
    val2_divisors: list = get_value_divisors(val2)
    val1_divisors_unique = set(val1_divisors)
    val2_divisors_unique = set(val2_divisors)
    least_common_multiple_value: int = 1
    for i in val1_divisors_unique:
        count = max(val1_divisors.count(i), val2_divisors.count(i))
        least_common_multiple_value *= i ** count
        val2_divisors_unique.remove(i)
    for i in val2_divisors_unique:
        least_common_multiple_value *= i ** val2_divisors.count(i)
    return least_common_multiple_value


def main() -> None:
    # wallis
    for i in range(1, 10):
        print(wallis(i))
    # Euclidean_GDC
    print(euclidean_GDC(18, 84))
    # Sieve
    print(sieve_of_erastothenes(64))
    # LCM
    print(least_common_multiple(192, 348))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
