# group otsu (mean)
class M_Gotsu:
    def __init__(self, px_count):
        self.px_count = px_count # array containing arrays of number of pixels of each value of each picture
        self.t1 = None
        self.t2 = None
        self.min_var = None
        self.min_g = None

    def calc_mean(self, arr):
        total = 0
        n = sum(arr)
        if n == 0:
            return 0
        else:
            for x in range(len(arr)):
                total += arr[x]*x
            m = total / n
            return m
    
    def calc_sum_mean_group(self, t1, t2):
        total_value = 0 # total value of all images in group i
        n = 0 # total number of pixels of all images in group i
        m = [] # array of mean of group i of each image
        for i in range(len(self.px_count)):
            value_single = 0
            n_single = 0

            for j in range(t1, t2):
                total_value += self.px_count[i][j] * j
                n += self.px_count[i][j]
                value_single += self.px_count[i][j] * j
                n_single += self.px_count[i][j]

            if n_single == 0:
                m.append(0)
            else:
                m.append(value_single / n_single)

        if n == 0:
            return 0
        else: 
            m_tot = total_value / n
            x = 0  # sum( (Mi_0 - Mi)**2 ) <- of all images
            for i in m:
                x += (i - m_tot)**2
            return x
    
    def calc_g_single(self, t1, t2):
        sum_m1 = self.calc_sum_mean_group(0, t1)
        sum_m2 = self.calc_sum_mean_group(t1, t2)
        sum_m3 = self.calc_sum_mean_group(t2, 256)

        g = sum_m1 + sum_m2 + sum_m3 + f
        return g

    def calc_G(self, t1, t2):
        g_tot = 0
        for x in self.px_count:
            m1 = 
            g_tot += self.calc_g_single(x, t1, t2)
        
            
    
    def find_thresh(self):
        for t1 in range(0, 255):
            for t2 in range(1, 256):
                g_tot = self.calc_G(t1, t2)
                if self.min_g == None or g_tot < self.min_g :
                    self.min_g = g_tot
                    self.t1 = t1
                    self.t2 = t2
        print("min var:" + str(self.min_g))
        print("t1: " + str(self.t1))
        print("t2: " + str(self.t2))
        return [self.t1, self.t2] 

    def calc_var(self, m, arr):
        sq_diff = 0
        for x in range(len(arr)):
            sq_diff += ((x-m)**2) * arr[x]
        if sum(arr)-1 != 0:
            var = sq_diff / (sum(arr)-1)
        else:
            return 0
        return var

    def calc_wv(self, arr, n_total): # weight multiplied by variance
        if len(arr) != 0:
            m = self.calc_mean(arr)
            v = self.calc_var(m, arr)
            w = sum(arr) / n_total
        else:
            return 0
        return w*v
    
    def calc_intragroup_var(self, t1, t2):
        arr1 = self.px_count[0:t1+1]
        arr2 = self.px_count[t1+1:t2+1]
        arr3 = self.px_count[t2+1:]
        n_total = sum(self.px_count)

        wv1 = self.calc_wv(arr1, n_total)
        wv2 = self.calc_wv(arr2, n_total)
        wv3 = self.calc_wv(arr3, n_total)

        intra_g_var = wv1 + wv2 + wv3
        return intra_g_var
        
    def find_threshold(self):
        for t1 in range(0, 255):
            for t2 in range(1, 256):
                v = self.calc_intragroup_var(t1, t2)
                if self.min_var == None or self.min_var > v :
                    self.min_var = v
                    self.t1 = t1
                    self.t2 = t2
        print("final")
        print("min var:" + str(self.min_var))
        print("t1: " + str(self.t1))
        print("t2: " + str(self.t2))
        return [self.t1, self.t2]
