class M_Gotsu:
    def __init__(self, px_count):
        self.px_count = px_count # array containing arrays of number of pixels of each value of each picture
        self.t = None
        self.min_g = float('inf')
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
        
    def calc_f(self, m_arr, t1, t2): # calc f of all images in the group
        f = 0
        w = 0
        sqd = 0
        for i in range(len(m_arr)):
            n = self.cumul_n[i][t2] - self.cumul_n[i][t1]
            if self.cumul_n[i][255] != 0:
                w = n / self.cumul_n[i][255]

            for j in range(t1, t2):
                sqd += (self.px_count[i][j] - m_arr[i])**2 
            if n != 1:
                v = sqd / (n-1)
            else:
                v = 0
            f += w*v
        return f
            
    def calc_g(self, t1, t2): # calculate square diff and f of group between t1 and t2
        v_tot = 0
        n_tot = 0 
        glob_mean = 0
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
            glob_mean = v_tot/n_tot

        for i in m_arr:
            sq_diff += (i - glob_mean)**2
        f = self.calc_f(m_arr, t1, t2)
        g = sq_diff + f
        return g
    
    def calc_G_total(self, t1, t2):
        g = self.calc_g(0, t1) + self.calc_g(t1, t2) + self.calc_g(t2, 255)
        return g

    def refine_search(self, t1, t2, step=1):
        for delta_t1 in range(-step, step+1):
            for delta_t2 in range(-step, step+1):
                new_t1 = t1 + delta_t1
                new_t2 = t2 + delta_t2
                if 0 <= new_t1 < new_t2 <= 255:
                    g = self.calc_G_total(new_t1, new_t2)
                    if g < self.min_g:
                        self.min_g = g
                        self.best_t1 = new_t1
                        self.best_t2 = new_t2

    def binary_search_thresholds(self, low1, high1, low2, high2, tolerance=1):
        if high1 - low1 <= tolerance and high2 - low2 <= tolerance:
            return

        mid1 = (low1 + high1) // 2
        mid2 = (low2 + high2) // 2

        g_mid = self.calc_G_total(mid1, mid2)

        if g_mid < self.min_g:
            self.min_g = g_mid
            self.best_t1 = mid1
            self.best_t2 = mid2

        # Refine around the current best midpoints
        self.refine_search(mid1, mid2, step=1)

        # narrow down the search space
        self.binary_search_thresholds(low1, mid1, low2, mid2, tolerance)
        self.binary_search_thresholds(mid1 + 1, high1, low2, mid2, tolerance)
        self.binary_search_thresholds(low1, mid1, mid2 + 1, high2, tolerance)
        self.binary_search_thresholds(mid1 + 1, high1, mid2 + 1, high2, tolerance)

    def find_thresh(self, tolerance=1):
        self.binary_search_thresholds(0, 255, 1, 256, tolerance)
        print(f"min G: {self.min_g}")
        print(f"Best t1: {self.best_t1}, Best t2: {self.best_t2}")
        return [self.best_t1, self.best_t2]
