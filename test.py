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
        print(f"cumul value: {self.cumul_value}")
        print(f"cumul n: {self.cumul_n}")
    
    # ------- Calculate f (variance within image) -------
    def calc_w(self, i, n):
        if self.cumul_n[i][-1] != 0:
            w = n / self.cumul_n[i][-1]
            print(f"weight: {w}")
            return w
        else: return 0
    
    def calc_v(self, i, n, t1, t2, m_arr):
        print(f"in calc v function: {i}, {n}, {t1}, {t2}, {m_arr}")
        sqd = 0
        v = 0
        for j in range(t1, t2+1):
            print(f"px count: {self.px_count[i][j]}")
            if self.px_count[i][j] != 0:
                sqd += ( (j - m_arr[i])**2 ) * self.px_count[i][j] 
                print(f"sqd: {sqd}")
        if n != 0:
            v = sqd / n
        print(f"variance: {v}")
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
            else:
                v = i[t2] - i[t1-1]
                n = j[t2] - j[t1-1]
            if n != 0:
                m_arr.append(v/n)
            print(f"mean array: ({i[t2]}-{i[t1-1]})/{n} = {m_arr}")
        return m_arr

    def calc_f(self, t1, t2):
        m_arr = self.mean_array(t1, t2)
        f = 0
        for i in range(0, len(m_arr)):
            n = self.cumul_n[i][t2] - self.cumul_n[i][t1-1]
            w = self.calc_w(i, n)
            v = self.calc_v(i, n, t1, t2, m_arr)
            f += w*v
        return f

    # ------- Calculate g (variance between images) ------- 
    def calc_f_for_g(self, m_arr, t1, t2): # calc f of all images in the group
        f = 0
        for i in range(len(m_arr)):
            n = self.cumul_n[i][t2] - self.cumul_n[i][t1]
            w = self.calc_w(i, n)
            v = self.calc_v(i, n, t1, t2, m_arr)
            f += w*v
        return f
           
    def calc_g(self, t1, t2): # calculate square diff and f of group between t1 and t2
        m_arr = self.mean_array(t1, t2) 
        v_tot = sum( self.cumul_value[i][-1] for i in self.cumul_value )
        n_tot = sum( self.cumul_n[i][-1] for i in self.cumul_n )
        glob_mean = 0
        if n_tot != 0:
            glob_mean = v_tot/n_tot

        sq_diff = 0
        for i in m_arr:
            sq_diff += (i - glob_mean)**2
        f = self.calc_f_for_g(m_arr, t1, t2)
        g = sq_diff + f
        return g
    
    # ------- Find best threshold -------
    def find_thresh_f_only(self): # two thresholds with f without g
        for t1 in range(0, len(self.px_count[0])):
            for t2 in range(t1+1, len(self.px_count[0])): 
                print(f"t1: {t1}, t2: {t2} ----------------------")
                f = 0
                if self.min_g == None:
                    f = self.calc_f(0, t1) + self.calc_f(t1+1, t2) + self.calc_f(t2+1, len(self.px_count[0])-1)
                    self.min_g = f
                    self.t = [t1, t2]
                else:
                    f += self.calc_f(0, t1)
                    if f < self.min_g:
                        f += self.calc_f(t1+1, t2) 
                        if f < self.min_g: 
                            f += self.calc_f(t2+1, len(self.px_count[0])-1)
                            if f < self.min_g:
                                self.min_g = f
                                self.t = [t1, t2]
        print("min f:" + str(self.min_g))
        print("t1: " + str(self.t[0]))
        print("t2: " + str(self.t[1]))
        return self.t
    
    def find_thresh_g(self): # two thresholds
        for t1 in range(0, len(self.px_count[0]) + 1):
            for t2 in range(t1+1, len(self.px_count[0]) + 1): 
                g = 0
                if self.min_g == None:
                    g = self.calc_g(0, t1) + self.calc_g(t1, t2) + self.calc_g(t2, len(self.px_count[0]))
                    self.min_g = g
                    self.t = [t1, t2]
                else:
                    g += self.calc_g(0, t1)
                    if g < self.min_g:
                        g += self.calc_g(t1, t2) 
                        if g < self.min_g: 
                            g += self.calc_g(t2, len(self.px_count[0]))
                            if g < self.min_g:
                                self.min_g = g
                                self.t = [t1, t2]
        print("min g:" + str(self.min_g))
        print("t1: " + str(self.t[0]))
        print("t2: " + str(self.t[1]))
        return self.t
            
    def find_thresh_single_g(self): # single threshold
        for t in range(0, 256):
            g = 0
            if self.min_g == None:
                g = self.calc_g(0, t) + self.calc_g(t, -1)
                self.min_g = g
                self.t = t
            else:
                g += self.calc_g(0, t)
                if g < self.min_g:
                    g += self.calc_g(t, -1) 
                    if g < self.min_g:
                        self.min_g = g
                        self.t = t
        
        print("min g:" + str(self.min_g))
        print("t: " + str(self.t))
        return self.t


def calc_v(i, n, t1, t2, m_arr, px_count):
        sqd = 0
        v = 0
        for j in range(t1, t2):
            if px_count[i][j] != 0:
                sqd += ( (j - m_arr[i])**2 ) * px_count[i][j]
            print(f"sqd: {sqd}")
        if n != 0:
            v = sqd / n
        return v

px_count = [[0, 1, 2, 1]]
multi = M_Gotsu(px_count)
thresholds = multi.find_thresh_f_only()
