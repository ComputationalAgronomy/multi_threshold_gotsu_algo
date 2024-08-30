import pytest

class TestCalcF:
    @pytest.fixture
    def setup(self):
        class MockClass:
            def __init__(self):
                self.px_count = [[0, 1, 2, 3]]
                self.cumul_value = None # cumulative value of individual images
                self.cumul_n = None
                self.calc_cumul()
                # self.cumul_value = [[0, 1, 5, 14]]
                # self.cumul_n = [[0, 1, 3, 6]]
            
            def calc_cumul_single(self, i):
                cumul_value = []
                cumul_n = []
                value = 0
                n = 0
                for j in range(len(i)):
                    value += i[j] * j
                    n += i[j]
                    cumul_value.append(value)
                    cumul_n.append(n)
                return cumul_value, cumul_n

            def calc_cumul(self):
                cumul_value_all_images = []
                cumul_n_all_images = []
                for i in self.px_count:
                    cumul_value, cumul_n = self.calc_cumul_single(i)
                    cumul_value_all_images.append(cumul_value)
                    cumul_n_all_images.append(cumul_n)
                self.cumul_value = cumul_value_all_images
                self.cumul_n = cumul_n_all_images
                # print(f"cumul value: {self.cumul_value}")
                # print(f"cumul n: {self.cumul_n}")
    
            def mean_array(self, t1, t2):
                m_arr = [] # array of mean of indv images
                for i, j in zip(self.cumul_value, self.cumul_n):
                    if t1 == 0 and t2 == 0:
                        v = 0
                        n = 0
                    elif t1 == 0 and t2 != 0:
                        v = i[t2]
                        n = j[t2]
                    else:
                        v = i[t2] - i[t1]
                        n = j[t2] - j[t1]

                    if n != 0:
                        m = v/n
                    else:
                        m = 0
                    
                    m_arr.append(m)
                    print(f"m: {v}/{n} = {m}")
                return m_arr

            def calc_w(self, i, n):
                if self.cumul_n[i][-1] != 0:
                    w = n / self.cumul_n[i][-1]
                    print(f"w: {w}")
                    return w
                else: return 0

            def calc_v(self, i, n, t1, t2, m_arr):
                print(f"in calc v function: {i}, {n}, {t1}, {t2}, {m_arr}")
                sqd_tot = 0
                v = 0
                lb = t1
                if t1!=0:
                    lb+=1
                for j in range(lb, t2+1):
                    if self.px_count[i][j] != 0:
                        sqd = ( (j - m_arr[i])**2 ) * self.px_count[i][j] 
                        sqd_tot += sqd
                        print(f"sqd: ({j} - {m_arr[i]})**2) * {self.px_count[i][j]} = {sqd}")
                print(f"sqd total = {sqd_tot}")
                if n != 0:
                    v = sqd_tot / n
                print(f"variance: {v}")
                return v

            def calc_f(self, t1, t2):
                print(f"t1: {t1} t2: {t2}")
                m_arr = self.mean_array(t1, t2)
                f = 0
                for i in range(0, len(m_arr)):
                    if t1 == 0:
                        n = self.cumul_n[i][t2]
                        print(f"n: {self.cumul_n[i][t2]}")
                    else:
                        n = self.cumul_n[i][t2] - self.cumul_n[i][t1]
                        print(f"n: {self.cumul_n[i][t2]} - {self.cumul_n[i][t1]} = {n}")

                    w = self.calc_w(i, n)
                    v = self.calc_v(i, n, t1, t2, m_arr)
                    f += w*v
                return f

        return MockClass()

    def test_calc_f_t1_zero(self, setup):
        result = setup.calc_f(0, 2)
        n = 3
        v = 2/9
        w = 3/6
        assert result == v*w, f"Got {result}"

    def test_calc_f_t1_non_zero(self, setup):
        result = setup.calc_f(1, 2)
        v = 0
        w = 1/3
        assert result == v*w, f"Got {result}"
