# group otsu (mean)
class M_Gotsu:
    def __init__(self, px_count):
        self.px_count = px_count # array containing arrays of number of pixels of each value of each picture
        self.t1 = None
        self.t2 = None
        self.min_g = None

    def calc_var(self, i, n_single, m, t1, t2):
        sq_diff = 0
        for j in range(t1, t2):
            sq_diff += (self.px_count[i][j] - m)**2
        if n_single-1 == 0:
            return 0
        else:
            v = float(sq_diff / (n_single-1))
            return v
            
    def calc_sum_mean_group(self, t1, t2):
        total_value = 0 # total value of all images in group i
        n = 0 # total number of pixels of all images in group i
        m = [] # array of mean of group i of each image
        n_arr = [] # array of number of pixels of group i of each image
        v_arr = []
        for i in range(len(self.px_count)):
            value_single = 0
            n_single = 0
            for j in range(t1, t2):
                if self.px_count[i][j] != 0:
                    total_value += self.px_count[i][j] * j
                    n += self.px_count[i][j]
                    value_single += self.px_count[i][j] * j
                    n_single += self.px_count[i][j]

            if n_single == 0:
                m.append(0)
                n_arr.append(0)
                v_arr.append(0)
            else:
                mean = value_single / n_single
                m.append(mean)
                n_arr.append(n_single)
                v = self.calc_var(i, n_single, mean, t1, t2)
                v_arr.append(v)
                
        if n == 0:
            return 0
        else: 
            m_tot = total_value / n
            x = 0  # sum( (Mi_0 - Mi)**2 ) + f <- of all images
            for i in range(len(m)):
                w = n_arr[i] / n
                x += ((m[i] - m_tot)**2 + (w*v_arr[i]))
            return x
    
    def calc_G(self, t1, t2): # output value of g given t1, t2
        sum_m1 = self.calc_sum_mean_group(0, t1)
        sum_m2 = self.calc_sum_mean_group(t1, t2)
        sum_m3 = self.calc_sum_mean_group(t2, 256)

        g = sum_m1 + sum_m2 + sum_m3
        return g
    
    def find_thresh(self):
        for t1 in range(0, 255):
            for t2 in range(1, 256):
                g_tot = self.calc_G(t1, t2)
                if self.min_g == None or g_tot < self.min_g :
                    self.min_g = g_tot
                    self.t1 = t1
                    self.t2 = t2
        print("min g:" + str(self.min_g))
        print("t1: " + str(self.t1))
        print("t2: " + str(self.t2))
        return [self.t1, self.t2] 
