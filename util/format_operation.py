import time
import datetime
import random
import string

class OperationFormat(object):

    """ 
    An abstract class 
    """
    
    __instance = None

    def __init__(self, 
                 name="Format Operation", 
                 info = {},
                 *args, **kwargs):
        """     """
    
        self.name = name
        self.info = info
        self.set_date_formate()
        
# === === === === === === === === === === === ===
# init setup ---
# === === === === === === === === === === === ===
    def set_date_formate(self):
        # The date format in MySQL
        self.format_date_mysql = "%Y-%m-%d %H:%M:%S"
        # The date format in excel
        self.format_date_excel = "%d %b %Y"
        # The date format for name
        self.format_date_name = "%Y-%m-%d-%H-%M-%S"
        # between time , datetime and string
        self.format_date_day = "%Y-%m-%d"
        
        self.format_date_log = "%y%m%d_%H%M%S"

        self.format_date_cut = "%Y%m%d"

#         self.dic_special_config_char = {
#             "::SR::" : self.str_random
#             "::IR::" : self.int_random
#             }
#         
# === === === === === === === === === === === ===
# Name Format ---
# === === === === === === === === === === === ===

    def log_name(self, name=None):
        if not name:
            name = "admin"
        date_name = self.get_name_date_log()
        result = "%s_%s.log" % (str(name), date_name)
        return result   # admin_140814_095412.log


    def case_log_name(self, case):
        test = case.test
        test_name = test.name_running
        case_name = case.name_short
        result = "%s_%s.log" % (str(test_name), str(case_name))
        return result
    
    
    def test_running_name(self, name="test"):
        date_name = self.get_name_date_all()
        result = "%s_%s" % (str(date_name), str(name))
        return result   # 2014_08_14_09_54_54_test
    
    
    def report_name(self, name="test_report"):
        date_name = self.get_name_date_all()
        result = "%s_%s" % (str(name), str(date_name))
        return result   # test_report_2014_08_14_09_55_17
    

    def create_an_account(self, pre=''):
        result = {}
        date = datetime.datetime.now().strftime("%m%d%y")
        hour = datetime.datetime.now().strftime("%H%M%S")
#         username = ("auto_" + pre + "_" + date + "_" + hour)
        username = ("test_" + pre + date + "_" + hour)
        result['first'] = self.str_random(6)
        result['last'] = self.str_random(6)
        result['username'] = username
        result['email'] = (username + "@xytest.com")
        result['password']  = "password"
        result['description'] = ("Description of "+ username + ".")
#         result['first_name'] = ''.join(random.choices(string.ascii_letters, 6))
#         result['last_name'] = ''.join(random.choices(string.ascii_letters, 6))
        result['website'] = str("http://"+pre+date+hour+"xytest.com").replace('_', '')
        result['address'] = (date + " " + pre + " Environment")
        result['contact_email'] = (username + "@xytest.com")
        result['contact_number'] = '8666666666'
#         result['contact_number'] = (date + "-" + hour)
#         print ("result = ", result)
        return result

    def create_an_address(self, pre=''):
        result = {}
        date = datetime.datetime.now().strftime("%m%d%y")
        hour = datetime.datetime.now().strftime("%H%M%S")
        username = ("test" + pre + date + "_" + hour)
        result['first'] = self.str_random(6)
        result['last'] = self.str_random(6)
        result['address'] = '8888 Rue Richardson'
        result['company'] = 'xytest'
        result['email'] = (username + "@xytest.com")
        result['phone'] = '8666666666'
        result['post'] = 'H3K 1G6'
        result['status'] = 'Quebec'
        result['city'] = 'Montreal'

#         print ("result = ", result)
        return result
    
# === === === === === === === === === === === ===
# Date Format ---
# === === === === === === === === === === === ===
    def get_mysql_datetime(self, ti):  
        t=time.localtime(ti)    # 1545422813.261864
        result = time.strftime(self.format_date_mysql, t)
        return  result  # 2014-08-14 09:55:56
    
     
    def get_current_date(self):
        t=time.localtime(time.time())
        result = time.strftime(self.format_date_mysql, t)
        return  result  # 2014-08-14 09:55:56

    def get_name_date(self, t=None):
        # get current time
        if t==None:
            t=time.localtime(time.time())
        result = time.strftime(self.format_date_day, t)
        return  result  # 2014-08-14
#     def get_bar_date(self, t=None):
#         # get current time
#         if t==None:
#             t=datetime.datetime.now()
#         result = t.strftime(self.format_date_day)
#         return  result  # 2014-08-14
    
    def get_name_date_all(self, t=None):
        # get current time
        if t==None:
            t=time.localtime(time.time())
        result = time.strftime(self.format_date_name, t)
        return  result  # 2014_08_14_09_59_07
    
    def get_name_date_log(self, t=None):
        # get current time
        if t==None:
            t=time.localtime(time.time())
        result = time.strftime(self.format_date_log, t)
        return  result  # 140814_095958
    

    def chcek_excel_date(self, stringDate="09 Apr 11"):
        # if the year has only two char, return four char year, for example, from 11 to 2011
        result = stringDate
        if len(stringDate)<11:
            if stringDate[6]==" ":
                result = stringDate[:7]+"20"+stringDate[7:9]
        return result   # 09 Apr 2011
        
        
    def minimalist_xldate_as_datetime(self, xldate, datemode=0):
        # datemode: 0 for 1900-based, 1 for 1904-based
        return (
            datetime.datetime(1899, 12, 30)
            + datetime.timedelta(days=xldate + 1462 * datemode)
            )
    
    # get the day value 
    def date_after_date(self, date=None, days=14):
        if date==None:
            date=time.localtime(time.time())
        dt = datetime.datetime(date[0], date[1],date[2])
        dt_after = dt + datetime.timedelta(days=days)
        
    #    dt_after_time = time.strptime(str(dt_after), self.format_date_mysql)
    #    dt_after_str = time.strftime(self.format_date_excel, dt_after_time)
    #    
    #    print str(dt_after) # 2011-06-09 00:00:00
    #    print dt_after_str    # 09 Jun 2011
    #    
        return str(dt_after)
    

    def second_to_str(self, all_second):
        try:
            result = ""
            h=0
            m=0
            s=0
            if all_second>0:
                if all_second >3600:
                    h = int(all_second / 3600)
                    m = int(all_second % 3600)
                else:
                    m=all_second
                    
                if m>60:
                    s = int(m % 60)
                    m = int(m / 60)
                else:
                    s = m
                    m = 0
                    
                if h!=0:
                    result += " %d hour " % h
                if m !=0:
                    result += " %d minute " % m
                if s !=0:
                    result += " %d second " % s
                    
            return result
        except Exception as e:
            msg = "Failed in util.second_to_str\n error = %s" % (str(e))
            print (msg)

# === === === === === === === === === === === ===
#  random number and string ---
# === === === === === === === === === === === ===

    def name_generator(self, size=9, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
#        name_generator()  - '2CmN6ddbr'
#        name_generator(3, "6793YUIO")  'Y3U'

    def int_random(self, fr=0, to=9):
        return random.randint(fr, to)
    
    def str_random(self, n=9):
        try:
            return ''.join(random.choices(string.ascii_letters, k=n))
            # string.ascii_lowercase + string.ascii_uppercase + string.digits
        except:
            return str(self.int_random(fr=100, to=1000*n))
        
    def str_random_long(self, n=9, m=9):
        st = 'random_string'
        for i in range (0, m):
            st += ' '
            st += self.str_random(n)
        return st
        
    # if not a string, return a random string
    def check_randowm_string(self, pre=None, n=9):
        if pre!=None:
            return str(pre)
        else:
            return self.str_random(n)
        
    # a list with random strings
    def list_random(self, m=6, n=9):
        lst = []
        for i in range (0, m):
            lst.append(self.str_random(n))
        return lst
    
    # pick one from list - n= range
    def random_in_list(self, lst, n=None):
        maxN = len(lst)
        if maxN == 0:
            return None
        elif maxN == 1:
            return lst[0]
        else:
            if n:
                if n<maxN and n>0:
                    maxN = n
            i = random.randint(0, maxN-1)
            return lst[i]
                
    # pick one [ind] or random in range n if no ind
    def index_random_in_list(self, lst, ind=None, n=None):
        # index or random in list
        if ind in ['all']:
            return lst
        
        is_int = (type(1) == type(ind))
        if is_int:
            if len(lst) > ind:
                return lst[ind]
            else:
                return lst[-1]
        else:
            return self.random_in_list(lst, n)
                
                
    # pick some from list - m= how many - n= in range
    def multi_random_in_list(self, lst, m=1,  n=None):
        maxN = len(lst)
        if m > len(lst):
            m = len(lst)
        if n:
            if n< m:
                n = m
            if n < maxN:
                maxN = n
                
        if maxN < 0:
            maxN = 0
#         print ("m, n maxN, = ", m, n, maxN)
        # prepare a sequence
        sequence = [i for i in range(maxN)]
#         print(sequence) # [0, 1, 2]
        # select a subset without replacement
        subset = random.sample(sequence, m)
#         print(subset)  # [2, 1, 0]

        res = []
        for it in subset: 
            res.append(lst[it])
#         print ("multi_random_in_list = ", res)
        return res

# === === === === === === === === === === === ===
# math ---
# === === === === === === === === === === === ===
    # 
    def limit_len_float(self, x, n):
        f = lambda x, n: round(x, n - len(str(int(x))))
        return f(x, n)
    
    
    # if divide 0, return 10000
    def try_divide(self, a, b):
        if self.is_zero(b):
            return a/0.0001
        else:
            return a/b
        
        
    def get_number_digit(self, number):
        count = 0
        num = int(number)   # 1234
        while (num > 0):
            num = int(num/10)
            count = count + 1
#         print ("Total number of digits : ",count)
        return count  # 4
    
    # for graph.  num= long of x, col= how many columns
#     def splite_int(self, num, col=10):
#         int_col = int(num/col)
        
         
         
        
        
# === === === === === === === === === === === ===
# Image ---
# === === === === === === === === === === === ===
    def getMD5(self, path, block_size=256*128, hr=False):
        '''
        Block size directly depends on the block size of your filesystem
        to avoid performances issues
        Here I have blocks of 4096 (Default NTFS)
        '''
        import hashlib
        md5 = hashlib.md5()
        f= open(path,'rb') 
        for chunk in iter(lambda: f.read(block_size), b''): 
            md5.update(chunk)
        f.close()
        if hr:
            return md5.hexdigest()
        return md5.digest()
    
        
        
    
OPERATION_FORMAT = OperationFormat()

if __name__ == '__main__':

    print (OPERATION_FORMAT.chcek_excel_date())
    print ("time.time() = ", str(int(time.time()*100)))  # 154542281326
    print ("time.time() = ", OPERATION_FORMAT.get_mysql_datetime(1545422813))  # 2018-12-21 15:06:53
    print (OPERATION_FORMAT.get_number_digit(1234))

    
