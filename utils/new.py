import concurrent.futures
import math
from utils.decorator import timeit

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        print("false")
    if n == 2:
        print("true")
    if n % 2 == 0:
        print("false")

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            print("false")
    print("true")


@timeit
def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))



@timeit
def main3():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
        #     print('%d is prime: %s' % (number, prime))
        for prime in PRIMES:
            executor.submit(is_prime,prime)

@timeit
def main2():
    for number in PRIMES:
        print('%d is prime: %s' % (number, is_prime(number)))
        
if __name__ == '__main__':
    main()
    main2()
    main3()