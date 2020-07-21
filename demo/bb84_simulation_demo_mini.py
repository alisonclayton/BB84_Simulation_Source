import random
import numpy as np


class SimulationDemoMini:
    """
    Mini demo of BB84 protocol simulation
    """

    def __init__(self, gamma=0):
        self.gamma = gamma
        pass

    def wheter_eavesdropp(self):
        p = random.random()
        if p <= self.gamma:
            return True
        else:
            return False

    def algorithm_1(self, input_c_0, input_c_1):
        output_c_0 = random.randint(0, 1)
        if output_c_0 == input_c_0:
            output_c_1 = input_c_1
        else:
            output_c_1 = random.randint(0, 1)
        return output_c_0, output_c_1

    def algorithm_2(self, times):
        a = []
        b = []
        for i in range(times):
            a_c_0 = random.randint(0, 1)
            a_c_1 = random.randint(0, 1)
            if self.wheter_eavesdropp():
                e_c_0, e_c_1 = self.algorithm_1(a_c_0, a_c_1)
                b_c_0, b_c_1 = self.algorithm_1(e_c_0, e_c_1)
            else:
                b_c_0, b_c_1 = self.algorithm_1(a_c_0, a_c_1)
            a.append([a_c_0, a_c_1])
            b.append([b_c_0, b_c_1])
        return a, b

    def show_episode(self, length):
        a, b = self.algorithm_2(times=length)
        print(a)
        print(b)
        # a and b should be saved into a file

    def cal_ber(self, length):
        """
        calculate bit error rate of the classical bit between Alice and Bob
        cber means the bit error rate contains the part that Alice and Bob choose different basis
        qber means the bit error rate ignores the part that Alice and Bob choose different basis
        According to the manuscript, cber should be 0.375 and qber should be 0.25
        :return:
        """
        print('\nusing algorithm_2!!\n')
        a, b = self.algorithm_2(length)
        cber_count = 0
        qber_count = 0
        remain_bits = 0
        c_00 = 0
        c_01 = 0
        c_10 = 0
        c_11 = 0
        for i in range(len(a)):
            a_c_1 = a[i][0]
            a_c_2 = a[i][1]
            b_b_1 = b[i][0]
            b_b_2 = b[i][1]
            # calculate cber
            if a_c_2 != b_b_2:
                cber_count += 1
            # calculate qber
            if a_c_1 == b_b_1:
                remain_bits += 1
                if a_c_2 != b_b_2:
                    qber_count += 1
            if a_c_2 == 0 and b_b_2 == 0:
                c_00 += 1
            if a_c_2 == 0 and b_b_2 == 1:
                c_01 += 1
            if a_c_2 == 1 and b_b_2 == 0:
                c_10 += 1
            if a_c_2 == 1 and b_b_2 == 1:
                c_11 += 1
        print('gamma=', self.gamma)
        print('\ntheoretical value:')
        print('p_00:', 3 / 8 - self.gamma / 16, 'p_01:', 1 / 8 + self.gamma / 16, 'p_10:', 1 / 8 + self.gamma / 16,
              'p_11:', 3 / 8 - self.gamma / 16)
        print('cber:', 0.25 + 0.125 * self.gamma)
        print('qber:', 0.25 * self.gamma)

        print('\nsimulation data:')
        print('p_00:', c_00 / length, 'p_01:', c_01 / length, 'p_10:', c_10 / length, 'p_11:', c_11 / length)
        print('cber:', cber_count / len(a))
        print('qber:', qber_count / remain_bits)
        print('remain bits num:', remain_bits)


if __name__ == '__main__':
    # this demo only shows the results when Alice and Bob using algorithm_2
    s = SimulationDemoMini(gamma=1)
    # using different data to show episode and calculate ber
    s.show_episode(length=20)
    s.cal_ber(length=5000)

"""
/Users/lileilei/Documents/IdeaProject/py3.6/bin/python /Users/lileilei/Documents/IdeaProject/bishe/bb84_simulation_demo_mini.py
[[0, 1], [0, 0], [1, 0], [1, 1], [0, 0], [1, 0], [1, 0], [0, 1], [0, 1], [1, 0], [0, 0], [1, 0], [0, 0], [1, 0], [1, 0], [1, 0], [0, 0], [0, 1], [1, 1], [1, 0]]
[[0, 1], [0, 0], [1, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 1], [0, 1], [0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [0, 1], [0, 1], [0, 0], [1, 1], [1, 1], [1, 0]]

using algorithm_2!!

gamma= 0

theoretical value:
p_00: 0.375 p_01: 0.125 p_10: 0.125 p_11: 0.375
cber: 0.25
qber: 0.0

simulation data:
p_00: 0.3728 p_01: 0.1238 p_10: 0.1258 p_11: 0.3776
cber: 0.2496
qber: 0.0
remain bits num: 2533

Process finished with exit code 0

"""
"""
[[0, 1], [1, 0], [0, 0], [1, 1], [0, 1], [0, 0], [0, 0], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [1, 0], [0, 1], [0, 0], [1, 0], [1, 1], [1, 1], [1, 0]]
[[0, 1], [1, 0], [1, 1], [1, 1], [1, 1], [0, 1], [0, 0], [1, 1], [1, 0], [1, 0], [0, 0], [1, 0], [0, 1], [1, 0], [0, 1], [0, 0], [0, 1], [0, 1], [1, 1], [0, 1]]

using algorithm_2!!

gamma= 0.5

theoretical value:
p_00: 0.34375 p_01: 0.15625 p_10: 0.15625 p_11: 0.34375
cber: 0.3125
qber: 0.125

simulation data:
p_00: 0.3446 p_01: 0.1576 p_10: 0.1542 p_11: 0.3436
cber: 0.3118
qber: 0.1250989707046714
remain bits num: 2526

Process finished with exit code 0

"""
"""
[[0, 0], [0, 1], [1, 0], [1, 1], [0, 0], [0, 0], [0, 0], [1, 0], [0, 0], [0, 1], [0, 0], [1, 1], [1, 0], [0, 0], [0, 1], [1, 1], [0, 0], [1, 1], [0, 1], [0, 1]]
[[1, 0], [1, 1], [1, 0], [1, 1], [1, 0], [1, 0], [0, 0], [0, 1], [0, 0], [1, 0], [0, 1], [0, 1], [1, 0], [1, 1], [0, 0], [0, 1], [1, 0], [0, 1], [0, 1], [1, 1]]

using algorithm_2!!

gamma= 1

theoretical value:
p_00: 0.3125 p_01: 0.1875 p_10: 0.1875 p_11: 0.3125
cber: 0.375
qber: 0.25

simulation data:
p_00: 0.308 p_01: 0.1822 p_10: 0.1912 p_11: 0.3186
cber: 0.3734
qber: 0.24859887910328263
remain bits num: 2498

Process finished with exit code 0

"""
