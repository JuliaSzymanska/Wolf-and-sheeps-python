# my_pi = 1
# for j in range(1, 10):
#     my_pi *= (2 * j) ** 2 / (((2 * j) - 1) * ((2 * j) + 1))
#     print(my_pi * 2)
#
# a = 84
# b = 18
# while b != 0:
#     c = a%b
#     a = b
#     b = c
# print(a)
# val = list(range(2, 100+1))
# for i in range(2, 100+1):
#     val

def gdc(a, b):
    if b == 0:
        return a
    return gdc(b, a % b)


def lcm(a, b) -> int:
    return (a / gdc(a, b)) * b


def main() -> None:
    # print(lcm(12, 36))
    print(36%12)

if __name__ == '__main__':
    main()
