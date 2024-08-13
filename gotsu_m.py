# group otsu (mean)
class M_Gotsu:
    def __init__(self, px_count):
        self.px_count = px_count # array containing arrays of number of pixels of each value of each picture
        self.t = None
        self.min_g = None
        self.cumul_value = None # cumulative value of individual images
        self.cumul_n = None
        self.calc_cumul()

    def calc_cumul(self):
        cumul_value_all_images = []
        cumul_n_all_images = []
        for i in self.px_count:
            cumul_value = []
            cumul_n = []
            value = 0
            n = 0
            for j in range(len(i)):
                value += i[j] * j
                n += i[j]
                cumul_value.append(value)
                cumul_n.append(n)
            cumul_value_all_images.append(cumul_value)
            cumul_n_all_images.append(cumul_n)
        self.cumul_value = cumul_value_all_images
        self.cumul_n = cumul_n_all_images
        print(f"cumul_value length: {len(self.cumul_value[0])}, {len(self.cumul_value[1])}")
        print(f"cumul_n length: {len(self.cumul_n[0])}, {len(self.cumul_n[1])}")

    def calc_f(self, m_arr, t1, t2): # calc f of all images in the group
        f = 0
        w = 0
        v = 0
        for i in range(len(m_arr)):
            n = self.cumul_n[i][t2] - self.cumul_n[i][t1]
            if self.cumul_n[i][255] != 0:
                w = n / self.cumul_n[i][255]
            sqd = 0
            for j in range(t1, t2):
                sqd += (self.px_count[i][j] - m_arr[i])**2 
            if n-1 != 0:
                v = sqd / (n-1)
            f += w*v
        return f
            
    def calc_g(self, t1, t2): # calculate square diff and f of group between t1 and t2
        v_tot = 0
        n_tot = 0 
        m_global = 0
        m_arr = [] # array of mean of indv images
        sq_diff = 0
        for i, j in zip(self.cumul_value, self.cumul_n):
            v = i[t2] - i[t1]
            n = j[t2] - j[t1]
            if n != 0:
                m_arr.append(v/n)
                v_tot += v
                n_tot += n
        if n_tot != 0:
            m_global = v_tot/n_tot

        for i in m_arr:
            sq_diff += (i - m_global)**2
        f = self.calc_f(m_arr, t1, t2)
        g = sq_diff + f
        return g

    def find_thresh(self):
        for t1 in range(0, 256):
            for t2 in range(t1+1, 256): 
                g = 0
                if self.min_g == None:
                    g = self.calc_g(0, t1) + self.calc_g(t1, t2) + self.calc_g(t2, 255)
                    self.min_g = g
                else:
                    g += self.calc_g(0, t1)
                if g < self.min_g:
                    g += self.calc_g(t1, t2) 
                    if g < self.min_g: 
                        g += self.calc_g(t2, 255)
                        if g < self.min_g:
                            self.min_g = g
                            self.t = [t1, t2]
        
        print("min g:" + str(self.min_g))
        print("t1: " + str(self.t[0]))
        print("t2: " + str(self.t[1]))
        return self.t
