import os
from xyTest.base.base_object import OBase
GET_LIB = True
try:
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import pandas as pd
except:
    GET_LIB = False
    print ('Please install numpy, matplotlib and pandas before use histogram class')
    pass

        
class GraphBase(OBase):
    def __init__(self, 
                 name="Graph Base", 
                 *args, **kwargs):
        
        OBase.__init__(self, 
                       name=name, 
                       *args, **kwargs)
        
        self.x_label = "Users"
        self.y_label = "Running Time (M Seconds)"
        


    def simple_line_histo(self, ti, xl, yl, xr, yr, pa=None, show=None):
        # title, and label - ti, xl, yl
        # Data for plotting - xr, yr
        #image out path - pa

        fig, ax = plt.subplots()
        ax.plot(xr, yr)

        ax.set(xlabel=xl, ylabel=yl, title= ti)
        ax.grid()
        
        if pa:
            fig.savefig(pa)
        if show:
            plt.show()


if GET_LIB:
    GRAPH_BASE = GraphBase()
else:
    GRAPH_BASE = None

if __name__ == "__main__":
    import datetime
    x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
    print ('x = ', x)
    y = np.random.randint(100, size=x.shape)
    print ('y = ', y)
    plt.plot(x,y)
#     plt.grid()
    plt.show()
    