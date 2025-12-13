class Helpers:

    # Algorithm to get prime numbers between +- N & +- N
    def get_prime_nums(self, nums_range):
        primes = []
        nums = []
        for num in nums_range:
            nums.append(num)
        nums.sort()
        for num in nums:
            if num <= 1:
                continue
            cont = 0
            for j in range(1, nums[-1]):
                if num % j == 0:
                    cont = cont + 1
            if cont == 2:
                primes.append(num)
        print('Exist ' + str(len(primes)) + ' prime numbers between: ' + str(nums[0]) + ' & ' + str(nums[-1]) + ':')
        print('Prime numbers: ' + str(primes))
        return primes

    # Algorithm to get fibonacci sequence ... of a specific size & with a defined limit
    def get_fibonacci(self, seq_size, limit):
        x, y, fibo_seq = 0, 1, [0, 1]  # As usual on recursion, to initiate base values
        idx = 1
        while len(fibo_seq) < seq_size and (fibo_seq[-1] + fibo_seq[-2]) < limit:
            x, y = y, x + y
            fibo_seq.append(fibo_seq[idx] + fibo_seq[idx - 1])
            idx += 1
        print('Fibonacci sequence with max seq_size of: ' + str(seq_size) + ' and a limit of: ' + str(limit) + ':')
        print('Fibo Seq: ' + str(fibo_seq))
        return fibo_seq