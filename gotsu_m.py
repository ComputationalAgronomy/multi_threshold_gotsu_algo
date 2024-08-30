class M_Gotsu:
    def __init__(self, px_count):
        self.px_count = px_count # array containing arrays of number of pixels of each value of each picture
        self.t = None
        self.min_g = None
        self.cumul_value = None # cumulative value of individual images
        self.cumul_n = None
        self.calc_cumul()

    # ------- Calculate cumulative values and px count -------
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

    # ------- Calculate g (variance between images) ------- 
    def calc_w(self, i, n):
        if self.cumul_n[i][-1] != 0:
            w = n / self.cumul_n[i][-1]
            return w
        else: return 0
    
    def calc_v(self, i, n, t1, t2, m_arr):
        sqd = 0
        v = 0
        for j in range(t1, t2+1):
            if self.px_count[i][j] != 0:
                sqd += ( (j - m_arr[i])**2 ) * self.px_count[i][j] 
        if n != 0:
            v = sqd / n
        return v

    def mean_array(self, t1, t2):
        m_arr = [] # array of mean of indv images
        for i, j in zip(self.cumul_value, self.cumul_n):
            if t1 == 0 and t2 == 0:
                v = 0
                n = 0
            elif t1 == 0 and t2 != 0:
                v = i[t2]
                n = j[t2]
                #print(f"mean array: {v}/{n}")
            else:
                v = i[t2] - i[t1-1]
                n = j[t2] - j[t1-1]
                #print(f"mean array: ({i[t2]}-{i[t1-1]})/{n}")

            if n != 0:
                m_arr.append(v/n)
                #print(v/n)
            else:
                m_arr.append(0)
            
        return m_arr

    def calc_f_for_g(self, m_arr, t1, t2): # calc f of all images in the group
        f = 0
        for i in range(len(m_arr)):
            if t1 == 0:
                n = self.cumul_n[i][t2]
            else:
                n = self.cumul_n[i][t2] - self.cumul_n[i][t1-1]
            w = self.calc_w(i, n)
            v = self.calc_v(i, n, t1, t2, m_arr)
            f += w*v
        return f
    
    def calc_glob_m(self, t1, t2):
        v_tot = 0
        n_tot = 0
        glob_m = 0
        
        if t1 == 0 and t2 != 0:
            for i, j in zip(self.cumul_value, self.cumul_n):
                v_tot += i[t2]
                n_tot += j[t2]
        else:
            for i, j in zip(self.cumul_value, self.cumul_n):
                v_tot += i[t2] - i[t1]
                n_tot += j[t2] - j[t1]
        if n_tot != 0: 
            glob_m = v_tot/n_tot
        return glob_m

    def calc_g(self, t1, t2): # calculate square diff and f of group between t1 and t2
        m_arr = self.mean_array(t1, t2) 
        glob_mean = self.calc_glob_m(t1, t2)

        sq_diff = 0
        for i in m_arr:
            sq_diff += (i - glob_mean)**2
        f = self.calc_f_for_g(m_arr, t1, t2)
        g = sq_diff + f
        return g
    
    # ------- Find best threshold -------
    def find_thresh_g(self): # two thresholds
        for t1 in range(0, len(self.px_count[0])):
            for t2 in range(t1+1, len(self.px_count[0])): 
                g = 0
                if self.min_g == None:
                    g = self.calc_g(0, t1) + self.calc_g(t1+1, t2) + self.calc_g(t2+1, len(self.px_count[0])-1)
                    self.min_g = g
                    self.t = [t1, t2]
                else:
                    g += self.calc_g(0, t1)
                    if g < self.min_g:
                        g += self.calc_g(t1+1, t2) 
                        if g < self.min_g: 
                            g += self.calc_g(t2+1, len(self.px_count[0])-1)
                            if g < self.min_g:
                                self.min_g = g
                                self.t = [t1, t2]
        print("min g:" + str(self.min_g))
        print("t1: " + str(self.t[0]))
        print("t2: " + str(self.t[1]))
        return self.t
