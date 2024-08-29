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
        # print(f"cumul value: {self.cumul_value}")
        # print(f"cumul n: {self.cumul_n}")
    
    # ------- Calculate f (variance within image) -------
    def calc_w(self, i, n):
        if self.cumul_n[i][-1] != 0:
            w = n / self.cumul_n[i][-1]
            #print(f"weight: {w}")
            return w
        else: return 0
    
    def calc_v(self, i, n, t1, t2, m_arr):
        #print(f"in calc v function: {i}, {n}, {t1}, {t2}, {m_arr}")
        sqd = 0
        v = 0
        for j in range(t1, t2+1):
            if self.px_count[i][j] != 0:
                sqd += ( (j - m_arr[i])**2 ) * self.px_count[i][j] 
                #print(f"sqd: {sqd}")
        if n != 0:
            v = sqd / n
        #print(f"variance: {v}------")
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

    def calc_f(self, t1, t2):
        m_arr = self.mean_array(t1, t2)
        f = 0
        for i in range(0, len(m_arr)):
            if t1 == 0:
                n = self.cumul_n[i][t2]
                #print(f"n: {self.cumul_n[i][t2]}")
            else:
                n = self.cumul_n[i][t2] - self.cumul_n[i][t1-1]
                #print(f"n: {self.cumul_n[i][t2]} - {self.cumul_n[i][t1-1]} = {n}")

            w = self.calc_w(i, n)
            v = self.calc_v(i, n, t1, t2, m_arr)
            f += w*v
        return f
    
    # ------- Find best threshold -------
    def find_thresh_f_only(self): # two thresholds with f without g
        for t1 in range(0, len(self.px_count[0])):
            for t2 in range(t1+1, len(self.px_count[0])): 
                #print(f"t1: {t1}, t2: {t2} ----------------------")
                f = 0

                if self.min_g == None:
                    f = self.calc_f(0, t1) + self.calc_f(t1+1, t2) + self.calc_f(t2+1, len(self.px_count[0])-1)
                    self.min_g = f
                    self.t = [t1, t2]

                else:
                    #print("~~~ 1 ~~~")
                    #print(self.px_count[0][0:t1])
                    x = self.calc_f(0, t1)
                    #print(f"f1: {x}")
                    f += x
                    if f < self.min_g:
                        #print("~~~ 2 ~~~")
                        #print(self.px_count[0][t1+1:t2])
                        x = self.calc_f(t1+1, t2)
                        #print(f"f2: {x}")
                        f += x 

                        if f < self.min_g:
                            #print("~~~ 3 ~~~")
                            #print(self.px_count[0][t2+1:len(self.px_count[0])-1])
                            x = self.calc_f(t2+1, len(self.px_count[0])-1)
                            #print(f"f3: {x}")
                            f += x

                            if f < self.min_g:
                                self.min_g = f
                                self.t = [t1, t2]
                                #print(f"f: {f}")

        print("min f:" + str(self.min_g))
        print("t1: " + str(self.t[0]))
        print("t2: " + str(self.t[1]))
        return self.t

from read_imgs import ReadImages, Linearize, Hist
from segment import Segment

folder_path = "imgs"
reader = ReadImages(folder_path)
images_array = reader.read_folder()

lin_arr = Linearize(images_array).linearize_multi()

multi = M_Gotsu(lin_arr)
thresholds = multi.find_thresh_f_only()

print(thresholds)

# show threshold on histogram
histogram = Hist(images_array)
histogram.histogram(thresholds)

# show segmented image
Segment(thresholds, images_array, 1)
