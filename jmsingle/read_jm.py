
import os
from xyTest.util.file_operation import OPERATION_FILE


class readJM(object):               
    def __init__(self, pa):
        self.dic_report = {}
        self.lst_ext = ['txt', 'csv']
        self.lst_column = ['Label', 'Samples', 'KO', 'Error', 
                        'Average', 'Min', 'Max', '90th', '95th', '99th', 'Throughput', 
                        'Received', 'Sent']
        if os.path.isdir(pa):
            self.path = pa
        else:
            this_report = OPERATION_FILE.path_debug
            self.path = OPERATION_FILE.path_join(this_report, pa)
            
    def read_folder(self):
        dic_rt = {}
        self.dic_report = None
        self.lst_row = None
        self.lst_int_key = []
        
        for fn in os.listdir(self.path):
            if "." in fn:
                na_split = fn.split(".")
                nam = na_split[0]
                ext= na_split[-1]
                if ext in self.lst_ext:
                    dirfile = OPERATION_FILE.path_join(self.path , fn)
                    int_key = int(nam)
                    self.lst_int_key.append(int_key) 
                    dic_rt[int_key] = self.read_txt_report(dirfile)
        self.dic_report = dic_rt
        self.lst_int_key.sort()
        print ("self.lst_int_key = ", self.lst_int_key)
        print ("self.lst_row = ", self.lst_row)
#         print ("self.dic_report = ", self.dic_report)
        return dic_rt

    def read_txt_report(self, fi):
        lst_read = OPERATION_FILE.file2list(fi)
        dic_file = {}
        lst_row = []
        for ln in lst_read:
            this_lst = ln.split('\t')
#             print ('this_lst = ', this_lst)
            dic_file[this_lst[0]] = this_lst
            if self.lst_row == None:
                lst_row.append(this_lst[0])
                
        if not lst_row == []:
            self.lst_row  = lst_row
#             print ("self.lst_row = ", self.lst_row)
#         print ('dic_file = ',dic_file)
        return dic_file
        
    def get_col_list(self, lab, col):
        lst_col = []
        col_ind = OPERATION_FILE.list_item_position(self.lst_column, col)[0]
        for k in self.lst_int_key:
            this_val = self.dic_report[k][lab][col_ind]
            if '%' in this_val:
                this_val = this_val.replace('%', '')
            lst_col.append(float(this_val) )
#         print ('lst_col = ', lst_col)
        return lst_col


if __name__ == '__main__':
    from xyTest.base.graph_base import GRAPH_BASE
#     pa = '/Users/yanxin/eclipse-workspace/vicuna_base/vicuna_test/log/Debug/active_test_report/'
    pa = '/Users/yanxin/eclipse-workspace/vicuna_base/vicuna_test/log/Debug/test_connection/2016-12-26_connection/test_graph'
    a  = readJM(pa)
    a.read_folder()
    
    # total Throughput
    it = 'Total'
    dd = 'Throughput'
    xr = a.lst_int_key
    yr = a.get_col_list(it, dd)
    ti = '%s of \'%s\'' % (dd, it)
    xl = 'Users'
    yl = 'Response Times (ms)'
    yl = dd
    name_png =  '%s_%s.png' % (dd, it)
    pa_png = OPERATION_FILE.path_join(pa, name_png)
    GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)

    # total Error %
    it = 'Total'
    dd = 'Error'
    xr = a.lst_int_key
    yr = a.get_col_list(it, dd)
    ti = '%s of \'%s\'' % (dd, it)
    xl = 'Users'
    yl = 'Error (percentage)'
    yl = dd
    name_png =  '%s_%s.png' % (dd, it)
    pa_png = OPERATION_FILE.path_join(pa, name_png)
    GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)
    
    # all row Average 
    dd = 'Average'
#     dd = '90th'
    for it in a.lst_row:
        xr = a.lst_int_key
        yr = a.get_col_list(it, dd)
        ti = '%s Response time of \'%s\'' % (dd, it)
        xl = 'Users'
        yl = 'Response Times (ms)'
        name_png =  '%s_%s.png' % (dd, it)
        pa_png = OPERATION_FILE.path_join(pa, name_png)
        GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)
    
    
    
    # total Throughput
    it = 'Total'
    dd = 'Error'
#     dd = 'Average'
    xr = a.lst_int_key
    yr = a.get_col_list(it, dd)
    ti = '%s of \'%s\'' % (dd, it)
    xl = 'Users'
    yl = 'Response Times (ms)'
    yl = dd
    name_png =  '%s_%s.png' % (dd, it)
    pa_png = OPERATION_FILE.path_join(pa, name_png)
    GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)
    
    
#     # all row Throughput 
#     dd = 'Throughput'
#     for it in a.lst_row:
#         xr = a.lst_int_key
#         yr = a.get_col_list(it, dd)
#         ti = '%s of \'%s\'' % (dd, it)
#         xl = 'Users'
#         yl = dd
#         name_png =  '%s_%s.png' % (dd, it)
#         pa_png = OPERATION_FILE.path_join(pa, name_png)
#         GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)

