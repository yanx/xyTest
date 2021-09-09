import time
from xyTest.base.base_object import OBase
from xyTest.base.config_base import CONFIG_BASE
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.format_operation import OPERATION_FORMAT


class TestBase(OBase):
    
    """
    """
                            
    def __init__(self, 
                 name=None, 
                 typ=None,
                 suite=None,
                 *args, **kwargs):

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)

        if typ:
            self.type = typ
        else:
            self.type ='qa'

        self.running_device = None
        self.waiting_time = None  # After current case, waiting before next case
        self.suite = suite
        self.clenaup_variable()
        self.clenaup_test()
        self.set_default_variable()
        
    # ------------------------------------------------
    # get and set ---
    # ------------------------------------------------

    def before_test_run(self): pass
    def after_test_run(self): pass
    def create_case(self, name, dic): pass
    def set_selected_case(self, value): pass
        
    def get_case_all(self): return self.case_all
    def set_case_all(self, value): 
        self.clenaup_variable()
        
        if (not isinstance(value, dict)) or (not OPERATION_FILE.is_true(value)):
            self.message_command(self, "Error", "Wrong value in set_case_all - value= " + str(value))
            return

        case_dic = {}
        for k, v in value.items():
            case = self.create_case(k, v)
            case_dic[k] = case
            self.list_all_case.append(case)
        self.case_all = case_dic
        CONFIG_BASE.dic_object_case[self.suite]=case_dic
        self.list_all_case.sort(key=lambda x: x.name.lower(), reverse=False)
        self.list_selected_case = self.list_all_case
#         print ("self.case_all = ", self.case_all)
#         print ("self.list_all_case = ", self.list_all_case)
        

    def set_test_running(self):
        self.name_running  = OPERATION_FORMAT.test_running_name(self.name)
        self.name_log_folder = "%s_%s" % (self.suite, self.name_running)
        self.path_category_log = OPERATION_FILE.set_test_log_folder(self.name_log_folder)
#         print ("self.name_log_folder = ", self.name_log_folder)  #  =  suite_and_2018-09-26-15-00-23_onawhim
        
    def clenaup_variable(self):
        # re start test
        self.case_all = {}
        self.list_all_case = []
        self.list_selected_case = []
        
    def clenaup_test(self):
        # this test
        self.name_running = None
        self.time_this_run = None
        self.is_run = False # this test does not run so far
        self.is_submitted = False   # the test result does not submit so far
        
        # add report info
        self.report_list_locked_case = []
        self.report_list_good_case = []
        self.report_list_bad_case = []
        self.lst_att_zip = []

        
    def set_default_variable(self):
#         print ("CONFIG_BASE.dic_lib_category = ", CONFIG_BASE.dic_lib_category)
#         print ("self.name = ", self.name)
        self.category_config = CONFIG_BASE.dic_lib_category[self.name]['config']
#         print ("tesrt Section = ", self.category_config.sections())  #  ['api', 'qa', 'dev']
        self.dic_config = {}
        
#         print ("self.category_config  =", self.category_config)
        if self.category_config:
            for se in self.category_config.options(self.type):
                self.dic_config[se] = OPERATION_FILE.try_one_option(self.category_config, self.type, se)
        #
        this_version = OPERATION_FILE.get_key_value(self.dic_config, 'version')
        if this_version:
            self.version = this_version
        else:
            self.version = 'unknown_version'
        self.default_pre_name = self.type + "_" + self.version 
        
        
    # ------------------------------------------------
    # run test ---
    # ------------------------------------------------


    def before_next_case(self):
        if self.waiting_time:
            wt = self.waiting_time
            self.waiting_time = None
            print ("waiting for %s seconds, - " % (str(wt))) # then call - before_test_run
            time.sleep(wt)
            self.before_test_run()
        

    def run_test(self):
        self.debug(["Start Test - ", self.name])
        self.set_test_running()

        try:
            self.before_test_run()
            print ("\n--------------------------------------------------------------------")
            msg= "--- Begin %s - test %s. --- in test.run_test() ---" % (self.suite, self.name_running)
            self.add_log_message('test', msg)
            print ("--------------------------------------------------------------------\n")
            self.time_start = time.time()
            
            for case in self.list_selected_case:
                self.before_next_case()
                if case.locked:
                    self.report_list_locked_case.append(case)
                else:
                    case.start_test()
                    self.check_run_case(case)
                    
            OPERATION_FILE.set_suite_log_file(CONFIG_BASE)
            self.time_end = time.time()
            self.time_this_run = self.get_time_run() #<class 'float'>
            print ("\n--------------------------------------------------------------------")
            msg= "--- End %s - test %s in %s Seconds. ---" % (self.suite, self.name_running, str((self.time_this_run)))
            self.is_run = True
            self.add_log_message('test', msg)
            print ("--------------------------------------------------------------------\n")
            self.after_test_run()
            
        except Exception as e:
            self.message_command(self, "Exception", "Running test "+self.name, e)
            pass
        
        
        
    def check_run_case(self, case):
        case.analysis_record()
        if case.locked:
            self.report_list_locked_case.append(case)
        elif case.status:
            self.report_list_good_case.append(case)
        else:
            self.report_list_bad_case.append(case)
            
#         print ("self.report_list_bad_case = ", self.report_list_bad_case)


    # ------------------------------------------------
    # before test, setup variables ---
    # ------------------------------------------------

    def get_jmeter_server_option(self, sec='jmeter'):
        in_suite = CONFIG_BASE.session_config
        try:
            opts = []
            if in_suite.has_section(sec):
                for key in in_suite[sec]:  
                    if 'jmeter_H' in key:
                        tt = '-H ' + in_suite[sec][key]
                    elif 'jmeter_P' in key:
                        tt = '-P ' + in_suite[sec][key]
                    else:
                        tt = '-J%s=%s' % (key, in_suite[sec][key])
                    opts.append(tt)
            if opts:
                return ' '.join(opts)
            else:
                return False
        except:
            return False

    def get_rest_server_option(self):
        in_suite = CONFIG_BASE.session_config
        try:
            lst_sec = ['rest', 'db']
            for sec in lst_sec:
                if in_suite.has_section(sec):
                    for key in in_suite[sec]:  
                        OPERATION_FILE.pass_one_config_option(in_suite, sec, key, self, sec+key)
                else:
                    self.message_command(self, "Error", "No REST -%s- Info in suite config file" % sec)
                    return False
        except Exception as e:
            self.message_command(self, "Exception", "in REST Test - def get_rest_server_option-", e)
            return False
        

    def check_appium_config(self, opt, sec='constant'):
        in_suite = CONFIG_BASE.session_config
        in_config = CONFIG_BASE.config_appium
        result = False
        try:
            if opt:
                result = OPERATION_FILE.try_one_option(in_suite, sec, opt)
                if not result:
                    result = OPERATION_FILE.try_one_option(in_config, sec, opt)
                return  result

            else:
                config = False
                if in_suite.has_section(sec):
                    config = in_suite
                else:
                    if in_config.has_section(sec):
                        config = in_config
                if config:
                    dic_option = dict(config.items(sec))
                    return dic_option
                
                return False
        except:
            return False


    def check_appium_driver(self, driver):
        type_driver = str(type(driver)).lower()
        if 'appium.webdriver.' in type_driver:
            return True
        return False
    
    # ------------------------------------------------
    # info and report ---
    # ------------------------------------------------
    
    def add_log_message(self, level, ms='No-Message'):
        self.message_command(self, level, ms)
#         if self.has_log:
#             from xyTest.log.constant import post_log_message, TEST_LOG
#             post_log_message(TEST_LOG, level, ms)

        
