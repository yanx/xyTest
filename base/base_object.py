#!/usr/bin/python

import time

class OBase(object):

    """
    An abstract class
    """

    __instance = None

    def __init__(self,
                 name=None,
                 *args, **kwargs):
        """     """

        self.name = name
        self.description = None
        self.time_start = None
        self.time_end = None
        
        self.status = False
        self.run_debug = False
        self.has_log = False
        self.set_base_constant()
        
    def set_base_constant(self):
        self.general_constant = {}
        self.lst_unit = ['name']
        self.lst_base_string = ["\n --- Name: %s --- " % str(self.name)]
        
        self.info = {'log':[]}
        self.metadata = {}
        self.dic_info_key = {'Fail': ['ERROR', 'EXCEPTION', 'SYS', 'FAIL'],
                             'Success': ['REPORT', 'SUCCESS', 'OUTPUT']}
        
        # TIME
        self.sleep_second = 1

    def add_log_report(self, lel, log):
        lst_key =  list(self.info.keys())
        if not lel in lst_key:
            self.info[lel] = []
        self.info[lel].append(log)
        self.info['log'].append(log)
        
    # ------------------------------------------------
    # get and set ---
    # ------------------------------------------------

    def get_name(self):         return self.name
    def set_name(self, val):    self.name = val
    
    def get_info(self):         return self.info
    def set_info(self, val):    self.info = val

    def get_metadata(self):     return self.metadata
    def set_metadata(self, val):    self.metadata = val
    
    def get_time_run(self): 
        ts = type(self.time_start)
        te = type(self.time_end)
        if ts == te:
            f_t = self.time_end - self.time_start
            return round(f_t, 3)  #float .123
        else:
            self.lst_unit += ['time_start', 'time_end']
            self.unitest()
            return None
    
    def get_time_sleep(self, w=None):  # oro - on or off
        if not type(w) == type(1):
            w = self.sleep_second
        if w > 0:
            time.sleep(w)
            
    # ------------------------------------------------
    #  General Element Functions ---  for selenium, appium
    # ------------------------------------------------
    def set_default_constant(self): pass
    
    # located an element by key-word
    def get_element(self): pass
    def get_field(self): pass
    
    # ele could by key-word, element object, or a list of 'True' 
    def confirm_an_element(self, ele): pass
    
    #  nam=obj or string, msg=string, err=show error, isF= want 'nam' is false
    def confirm(self, nam, msg, err=True, isF=False):
        ele = self.confirm_an_element(nam)

        isT = False
        if ele:
            isT = True
            if isF:
                isT = False
        elif isF:
                isT = True
            
#         if ele:
        if isT:
            self.message_command(self, "Report", "Successfully - " +msg)
            if ele:
                return ele
            else:
                return isT
        elif err:
            self.message_command(self, "Error", "Failed - " +msg)
        else:
            self.message_command(self, "Report", "Not able to - " +msg)
        return False

    # Yes, want to see this elemnt
    def check_an_element(self, ele, msg, ge_el=None):
        if ele:
            self.message_command(self, "Report", "Check - %s - Done" % msg)
            if ge_el: # string - 
                # after check_an_element, run get_element(ge_el)
                time.sleep(1)
                self.get_element(ge_el)
#                 print ("get element = ", ge_el*20)
            return True
        else:
            self.message_command(self, "Error", "Did not get element - " +msg)
            return False

    # No, don't want to see this element
    def no_this_element(self, ele, msg):
        if ele:
            self.message_command(self, "Error", "This is an incorrect element - " +msg)
            return False
        else:
            self.message_command(self, "Report", "Checked - No this element as designed - " + msg)
            return True

    # ------------------------------------------------
    # message, info and report ---
    # ------------------------------------------------
    def message_command(self, cls, level, msg='No-Message', e=None):
        try:
            from xyTest.util.file_operation import OPERATION_FILE
            OPERATION_FILE.message_command(cls, level, msg, e)
        except:
            ms = "\n[Class: %s - Level: %s] -::- %s\n"  %  (str(cls), str(level).upper(), str(msg))
            print (ms)
            if e:
                print (e)
            pass
        
    def debug(self, msg):

        if self.run_debug:
            try:
                from xyTest.util.file_operation import OPERATION_FILE
                OPERATION_FILE.debug(self, msg)
            except:
                import inspect
                import time
                name_class = self.__class__.__name__
                name_caller = inspect.stack()[2][3]
                mew_msg = str(msg)
                t=time.localtime(time.time())
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
                data = "DEBUG [%s] \t[ Class: %s ] \t[ Function: %s ] \t%s\n" % (current_time, str(name_class), str(name_caller), mew_msg)
                print (data)
        

    def base_string_add(self, ob): 
        if isinstance(ob, list):
            self.lst_base_string += ob
        else:
            self.lst_base_string.append(str(ob))

    def show_detail(self):
        self.base_string_add(" --- show_detail --- \n")
        return "\n".join(self.lst_base_string)

    def unitest(self):
        lst_val = []
        for itm in self.lst_unit:
            va = getattr(self, itm)
            lst_val.append("%s : %s " % (str(itm), str(va)))
        self.base_string_add(lst_val)
        print (self.show_detail())
            
