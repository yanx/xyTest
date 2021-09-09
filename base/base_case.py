
import time
import sys
import threading 
from xyTest.base.base_object import OBase
from xyTest.base.config_base import CONFIG_BASE
from xyTest.util.sys_operation import OPERATION_SYSTEM
from xyTest.util.file_operation import OPERATION_FILE


class TestThread(threading.Thread):
    """  """
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
    
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run # Force the Thread to install our trace.
        threading.Thread.start(self)
    
    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    
    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None
    
    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace
    
    def kill(self):
        self.killed = True


class CaseBase(OBase):
    """
    """
    def __init__(self,
                 name=None,
                 test=None,
                 *args, **kwargs):

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)
        # parent
        self.test = test
        # case
        self.name_short = name  # case config file name
        self.name_timeout_screnshot = name + "_timeout.png"
        self.name_performance_image = name + "_performance.png"

        self.default_time= 600  # default time out
        self.timeout = None
        
        self.link = None  # in report, add link
        self.repeat = 1
        self.performance = False  # [speed, ]
        
        # case states
        self.locked = False
        self.str_lock = None   # lower case - locked attribute in case config
        self.score = 'failed' # [pass, locked, failed, error]

        # category special -
        # cmd, jmeter
        self.cmd_run = False  # string - cmd_run = case.config[se]['cmd']
        self.cmd_result = None  # cmd_result = OPERATION_SYSTEM.shell_cmd(cmd)
        
        self.clean_up_case()

    # ------------------------------------------------
    # __init__ Setup ---
    # ------------------------------------------------
    def setup_config_special(self): pass
    def before_run_case(self): pass
    def run_case(self): pass
    def after_run_case(self): pass
    
    def clean_up_case(self):
        # Log variables
        # Log does not work while thread.run().  Store message here and send after run()
        self.case_log_message = {}  # message for log
        self.dic_cmd_report = {}
#         self.info['log'] = []
        self.info = {'log':[]}
        
        
    def set_info(self, dic):
        self.has_log = self.test.has_log
        for dk, dv in dic.items():
            setattr(self, dk, dv)
            
        self.setup_config_general()
        self.setup_config_special()


    def setup_config_general(self):
        self.path_root = CONFIG_BASE.session_path
        # run-able sections
        self.lst_run = []
        for se in self.config.sections():
            new_se = str(se).strip()
            if new_se[:3] == 'run':
                self.lst_run.append(se)
#             print ("run list = ", self.lst_run )
        if self.config.has_section('constant'):
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'description', self, 'description')
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'link', self, 'link')
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'locked', self, 'locked')
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'timeout', self, 'timeout', 'int')

            # Performance Test
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'performance', self, 'performance')
            OPERATION_FILE.pass_one_config_option(self.config, 'constant', 'repeat', self, 'repeat', 'int')
        
            # debug
            this_debug = OPERATION_FILE.try_one_option(self.config, 'constant', 'debug')
            if this_debug:
                self.run_debug = True
                
            this_root = OPERATION_FILE.try_one_option(self.config, 'constant', 'path_root')
            if this_root:
                self.path_root = CONFIG_BASE.get_file_path_in_conf(this_root, True)
#             print ("self.path_root = ", self.path_root)

        self.lst_key_attr = [CONFIG_BASE.session_type, 
                             CONFIG_BASE.session_name, 
                             CONFIG_BASE.session_browser, 
                             OPERATION_SYSTEM.platform
                             ]+['true', 'all', 'yes']+ CONFIG_BASE.lst_env_status
#         print ("self.lst_key_attr  =", self.lst_key_attr)
#         print ("self.str_lock = ", self.str_lock)
        if self.locked:
            self.str_lock = str(self.locked).lower()
            for it in self.lst_key_attr:
                try:
                    if it in self.str_lock:
                        self.locked = True
                        return
                except:
                    pass
            self.locked = False

    # ------------------------------------------------
    #   case run ---    
    # ------------------------------------------------

    # ready to run
    def set_case_running(self):
        self.clean_up_case()

        self.path_case_log = OPERATION_FILE.set_case_log_file(self, self.name)
        self.path_timeout_image = OPERATION_FILE.path_join(self.test.path_category_log, [self.name_timeout_screnshot])
        self.path_performance_image = OPERATION_FILE.path_join(self.test.path_category_log, [self.name_performance_image])
        
    def get_current_timeout(self):
        if not self.timeout:
            if CONFIG_BASE.session_timeout:
                self.timeout = CONFIG_BASE.session_timeout
            else:
                self.timeout = self.default_time
#         print ("self.timeout = ", self.timeout)
        return self.timeout

    # after run, 
    def get_cmd_report(self, se, cmd_result):
        this_report = {}
        this_report['process'] = OPERATION_SYSTEM.current_process 
        this_report['result'] = cmd_result 
        this_report['time'] = OPERATION_SYSTEM.current_running
        this_report['output'] = OPERATION_SYSTEM.current_output  
        this_report['error'] = OPERATION_SYSTEM.current_err
        self.dic_cmd_report[se] = this_report
        
#         self.message_command(self, "Info", "CMD Time: "+str(OPERATION_SYSTEM.current_running))
        self.message_command(self, "Report", "CMD Time: "+str(OPERATION_SYSTEM.current_running))
#         self.message_command(self, "Info", "CMD Log: \n\n"+str(OPERATION_SYSTEM.current_output))
        if OPERATION_FILE.is_true(OPERATION_SYSTEM.current_err):
            self.message_command(self, "SYS", "CMD Error: "+str(OPERATION_SYSTEM.current_err))
        else:
            self.message_command(self, "OUTPUT", "CMD OUTPUT: "+str(OPERATION_SYSTEM.current_output))

    def start_test(self):
        self.set_case_running()
        time_out = self.get_current_timeout()
        self.current_thread = TestThread(target=self.run)
        self.current_thread.start()
        self.current_thread.join(time_out)
         
#         if self.current_thread.isAlive():
#             # try to save screen shot
#             if OPERATION_FILE.admin_mode:
#                 try:
#                     OPERATION_SYSTEM.save_screenshot(self.path_timeout_image)
#                     print ( " Timeout - Save ScreenShot to =  %s" % str(self.path_timeout_image))
#                 except:
#                     pass
#              
#             self.status = False
#             self.score = 'timeout'
#  
#             msg= "Error: Stop case %s due to timeout %s seconds. --- In test.runcase()" % (str(self.name), str(self.timeout))
#             self.add_message('Error', msg)
# 
#             self.current_thread.kill()
#             OPERATION_SYSTEM.kill_process()
#             time.sleep(10)
             
        self.post_message()
 
    def run(self):
#        self.unitest()
#        return
        mss= "--- Begin --- case %s. --- in case.run() ---" % (self.name)
        self.add_message('case', mss)
        self.before_run_case()
        run_result = self.run_case()
        if run_result:
            self.status = True
        else:
            self.status = False
            self.score = 'failed'
        self.after_run_case()
        mse= "--- End --- case %s. --- in case.run() ---" % (self.name)
        self.add_message('case', mse)
        
    # ------------------------------------------------
    #    info and report ---
    # ------------------------------------------------
 
    def add_message(self, level, ms):
        self.message_command(self, level, ms)
        if self.has_log:
            if self.case_log_message == {}:
                self.message[0] = [level, ms]
            else:
                ind = len(self.case_log_message.keys())
                self.message[ind] = [level, ms]
         
    def post_message(self):
        if self.has_log:
#             ks = self.case_log_message.keys() # ks =  dict_keys([0, 1])
            ks = list(self.case_log_message.keys())
            ks.sort()
            for i in ks:
                self.add_log_message(self.message[i][0], self.message[i][1])
     

    def add_log_message(self, level, ms):
        pass
#         from xyTest.log.constant import post_log_message, CASE_LOG
#         ms = "%s \n %sCase: \nTest: %s" % (ms, self.name, self.test.name)
#         post_log_message(CASE_LOG, level, ms)

    def analysis_record(self):
        lst_fail = self.dic_info_key['Fail']
        list_info = list(self.info.keys())
#         print( 'case info = ' ,self.info)
#         print( 'case info keys = ' ,list_info)
        for fa in lst_fail:
            if fa in list_info:
                if self.info[fa] != []:
                    self.status = False
                    break



