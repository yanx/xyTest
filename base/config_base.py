
import os
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.base.base_object import OBase


class ConfigBase(OBase):

    """
    An abstract class
    """

    __instance = None

    def __init__(self,
                 name="ConfigBase",
                 *args, **kwargs):
        """     """

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)

#         self.run_debug = True
        self.set_basetest_constant()
        self.set_configbase_constant()
        
        # ALERT - 
        self.alarm_period = 1500
        self.alarm_re_try = 3
        self.set_alarm_constant()
        
    # ------------------------------------------------
    # function setup root ---
    # ------------------------------------------------

    def set_basetest_constant(self):
        # setupf for root_test directory structure
        #  - _test/config
        self.name_config_env = "env" + OPERATION_FILE.format_config
        self.name_config_user = "user" + OPERATION_FILE.format_config
        self.name_config_appium = "appium" + OPERATION_FILE.format_config
        # _test/
        self.name_dir_log = "log"
        self.name_dir_tmp = "tmp"
        self.name_dir_suites = 'suites'
        # _test/suites/
        self.path_test_suites = None
        # _test/suites/suite_mytest/
        self.name_suite_config = "suite"  + OPERATION_FILE.format_config
        self.pre_case_config = "case_"
        
    def set_configbase_constant(self):
        # setup for case/category/session dic
        self.lst_base_dir = ['base', 'db', 'util', 'log']
        self.lst_category_dir = ['command', 'jmsingle']
        self.lst_env_status = []
        self.dic_root_lib = {} # dic of root location : lib/vicuna
        self.dic_cmd = {}  # dic_from controller
        self.dic_all_session = {}  # {session_name: suite_dic
        self.dic_all_case = {}  # {session_name: {category_name:{case_name:case_dic
        self.dic_object_case = {} # {session_name: {category_name:{case_name:case_object

        # setup for error filter
        self.dic_session_check = {}
        self.lst_session_check = ['check_error', 'check_warning', 'check_pass']
        self.dic_const = { 'list_error'   : True, 
                          'list_warning' : True, 
                          'list_pass'    : True }
        self.info['log'] = []

    def set_alarm_constant(self):
        self.alarm_start = 0
        self.alarm_end = 0
        self.count_alarm = 0
        self.try_alarm = 0

        
#     def check_alarm_count(self):
#         print ("Now try_alarm = ", self.try_alarm)
#         print ("Now count_alarm = ", self.count_alarm)
#         if self.try_alarm < self.alarm_re_try:
#             self.try_alarm += 1
#             return False
#         else:
#             return True
    
    def set_dic_cmd(self, dic_cmd): self.dic_cmd = dic_cmd
    
    def set_root_lib(self, na, pa):
        self.dic_root_lib['name'] = na
        self.dic_root_lib['path'] = pa
        self.dic_root_lib['readme'] = OPERATION_FILE.file_read_readme(pa)
        self.dic_root_lib['root_readme'] = OPERATION_FILE.file_read_readme(self.path_base_root)
      
    def set_ini(self, root_config):
        try:
            # _test/config
            self.path_config_location = root_config
            self.path_config_env = OPERATION_FILE.path_join(self.path_config_location, self.name_config_env)
            self.set_env_config(self.path_config_env )
            self.path_config_user = OPERATION_FILE.path_join(self.path_config_location, self.name_config_user)
            self.set_user_config(self.path_config_user )
            self.path_config_appium = OPERATION_FILE.path_join(self.path_config_location, self.name_config_appium)
            self.set_appium_config(self.path_config_appium )
            # _root
            self.debug("Done - ConfigBase.set_ini() - env, user")
        except Exception as e:
            self.message_command(self, "Exception", "def:set_ini", e)

        # check if in docker
        try:
            with open('/proc/self/cgroup', 'r') as procfile:
                for line in procfile:
                    fields = line.strip().split('/')
                    if 'docker' in fields:
                        self.lst_env_status.append('docker')
                        return
        except:
            pass
            
    def set_root_test(self, dir_root, dir_test):
        try:
            ### _test/ - suites, log, tmp
            self.path_base_test = dir_test
            self.path_test_suites = OPERATION_FILE.path_join(dir_test, self.name_dir_suites)
            self.path_test_log = OPERATION_FILE.path_join(dir_test, self.name_dir_log)
            OPERATION_FILE.set_log_location(self.path_test_log)
#             self.path_test_tmp = OPERATION_FILE.path_join(dir_test, self.name_dir_tmp)
#             OPERATION_FILE.set_tmp_location(self.path_test_tmp)

            # check sessions 
            self.get_session_dic()
            ### _root/
            self.path_base_root= dir_root

            self.debug("Done - ConfigBase.set_root_test() - ")
        except Exception as e:
            self.message_command(self, "Exception", "def:set_root_test", e)
        
    def set_new_lib (self, name_lib):
        try:
            ### _root/lib/new_lib/
            self.dic_lib_category = {}
            self.path_lib_xyTest= OPERATION_FILE.path_join(self.path_base_root, ['lib', 'xyTest']) 
            self.path_lib_new = OPERATION_FILE.path_join(self.path_base_root, ['lib', name_lib]) 
            
            self.set_root_lib(name_lib, self.path_lib_new)
            
            dic_sub = OPERATION_FILE.get_dic_of_subfolder(self.path_lib_new)
#             print ("dic_sub = ", dic_sub)
            for k, v in dic_sub.items():
                if (not k in self.lst_base_dir) and (not "__" in k):
                    this_cate = self.check_this_category(k, v)
                    self.dic_lib_category[k] = this_cate
                    
            for itm in self.lst_category_dir:
                path_cate = OPERATION_FILE.path_join(self.path_lib_xyTest, [itm]) 
                this_cate = self.check_this_category(itm, path_cate)
                self.dic_lib_category[itm] = this_cate
#             print ("self.dic_lib_category = ", self.dic_lib_category) 
            self.list_lib_category = list(self.dic_lib_category.keys())

            ### _root/lib/xyTest/template
            self.path_lib_template = OPERATION_FILE.path_join(self.path_lib_xyTest, ['template'])

            self.debug("Done - ConfigBase.set_new_lib() - ")
        except Exception as e:
            self.message_command(self, "Exception", "def:set_new_lib", e)

    def check_this_category(self, k, v):
        this_cate = {}
        this_cate['path'] = v
        this_cate['config'] = None
        this_cate['text'] = None
        path_config = OPERATION_FILE.path_join(v, k+'.ini')
        if os.path.isfile(path_config):
            this_cate['config'] = OPERATION_FILE.read_ini_config(path_config)
            this_cate['text'] = OPERATION_FILE.file_read(path_config)

#         this_cate['readme'] = None
#         path_readme = OPERATION_FILE.path_join(v, 'readme.md')
#         if os.path.isfile(path_readme):
#             this_cate['readme'] = OPERATION_FILE.file_read(path_readme)

        this_cate['readme'] = OPERATION_FILE.file_read_readme(v)
            
            
        return this_cate
    
    
    def get_session_dic(self):
        self.dic_all_session = {}
        dic_of_subfolder = OPERATION_FILE.get_dic_of_subfolder(self.path_test_suites)
#         print ("dic_of_subfolder  = ", dic_of_subfolder )
        for k, v in dic_of_subfolder.items():
            file_config = OPERATION_FILE.path_join(v, self.name_suite_config)
            this_session = {}
            if os.path.isfile(file_config):
                this_session['name'] = k
                this_session['ini'] = file_config

                this_config = OPERATION_FILE.read_ini_config(file_config)
                this_session['config']  = this_config
                
                get_root = OPERATION_FILE.try_one_option(this_config, 'root', 'path')
                if get_root and os.path.isdir(get_root):
                    this_session['path'] = get_root
                else:
                    this_session['path'] = v

                self.dic_all_session[k] = this_session
#         print ("self.dic_all_session = ", self.dic_all_session)

        return self.dic_all_session

    # ------------------------------------------------
    # function set new suite ---
    # ------------------------------------------------

    def clean_obj_attr(self):
        self.time_start = None
        self.time_end = None
        self.bless_string = None
        self.session_email_send_to = None
        self.session_alarm = None
        
    def set_session_config(self, nam, typ='qa', b=None):
        self.debug("Start - set_session_config")
        self.clean_obj_attr()

        try:
            self.session_name = nam.lower()
            self.session_type = typ.lower()
            self.session_browser = b
            self.session_config = self.dic_all_session[nam]['config']
            self.session_path = self.dic_all_session[nam]['path']
            self.session_dic_case = self.get_case_list(nam)
#             print ("self.session_path = ", self.session_path)
#             print ("self.session_dic_case = ", self.session_dic_case)
            
            # suite.ini
            self.session_timeout = OPERATION_FILE.try_one_option(self.session_config, 'constant', 'timeout', 'int')
            if not self.session_timeout:
                self.session_timeout = self.timeout
            self.session_email_send_to = OPERATION_FILE.try_one_option(self.session_config, 'constant', 'email_send_to', 'list')
#             print ("self.session_email_send_to = ", self.session_email_send_to)
            if not self.session_email_send_to:
                self.session_email_send_to = self.email_send_to
#             print ("self.session_email_send_to =", self.session_email_send_to)

            self.session_alarm = OPERATION_FILE.try_one_option(self.session_config, 'constant', 'alarm') # string - alarm report title

            # json setup - for rest, 
            self.session_json_setup = None
            if self.session_config.has_option('constant', 'env_json'):
                    json_file = self.get_file_path_in_conf(self.session_config['constant']['env_json'])
                    self.session_json_setup = OPERATION_FILE.file_read_json(json_file)
#                     print ('self.session_json_setup = ', self.session_json_setup )
                
            self.debug("Done - session config")
        except Exception as e:
            self.message_command(self, "Exception", "def:set_session_config", e)
            

    def get_file_path_in_conf(self, pa, check=True, root=None):
        this_path = self.session_path
        if root:
            this_path = root
        result = False
        if OPERATION_FILE.is_true(pa):
            str_pa = str(pa).strip()
            specail_option = OPERATION_FILE.get_specail_path_option(str_pa)
#             print ("specail_option = ", specail_option)
            if specail_option :
                result = specail_option
            elif check:
                result = OPERATION_FILE.path_join(this_path, str_pa)
            else:
                result = OPERATION_FILE.format_path(str_pa)
        return result


    def get_case_list(self, ss):
        self.dic_all_case[ss] = {}
        self.dic_object_case[ss] = {}
        loc = self.dic_all_session[ss]['path']
        lst_lib_category = self.dic_lib_category.keys()
#         print ("lst_lib_category = ", lst_lib_category)  # dict_keys(['whimwebmobile', 'onawhim', 'onamobile', 'whimadmin', 'qtest', 'whimapp', 'whimmade', 'command', 'jmsingle'])
        for fn in os.listdir(loc):
            if fn in lst_lib_category:
                dirfile = OPERATION_FILE.path_join(loc, fn)
                lst_of_case = OPERATION_FILE.get_pre_ext_file_list(dirfile, self.pre_case_config, OPERATION_FILE.format_config, True)
#                 print ("lst_of_case = ", lst_of_case) 
                dic_this_category = {}
                for cas in lst_of_case:
                    dic_this_case = {}
#                     name_case = OPERATION_FILE.get_name_subpath(loc, cas)
                    name_case = OPERATION_FILE.get_name_subpath(dirfile, cas)
                    dic_this_case['name_short'] = OPERATION_FILE.get_file_short_name(cas)
                    dic_this_case['ini'] = cas
                    dic_this_case['config'] = OPERATION_FILE.read_ini_config(cas)
                    dic_this_category[name_case] = dic_this_case
                self.dic_all_case[ss][fn] = dic_this_category
#         print ("self.dic_all_case[ss]  = ", self.dic_all_case[ss] )
        return self.dic_all_case[ss]
    
    # ------------------------------------------------
    # function config files ---
    # ------------------------------------------------

    def set_env_config(self, path_config_env):
        self.config_env = OPERATION_FILE.read_ini_config(path_config_env)
        self.ip_smtp = []
        if self.config_env.has_section('smtp'):
            try:
                server = self.config_env.get('smtp', 'server')
                user = self.config_env.get('smtp', 'user')
                password = self.config_env.get('smtp', 'password')
                port = OPERATION_FILE.try_one_option(self.config_env, 'smtp', 'port')
                self.ip_smtp = [server, user, password, port]
                
                self.email_from = self.config_env.get('smtp', 'from')

            except Exception as e:
                self.message_command(self, "Exception", "set_env_config.smtp", e)
                self.ip_smtp = []
                pass


    def set_user_config(self, path_config_user ):
        self.config_user = OPERATION_FILE.read_ini_config(path_config_user)
        self.user_name = str(OPERATION_FILE.try_one_option(self.config_user, 'user', 'name'))
        self.user_email = str(OPERATION_FILE.try_one_option(self.config_user, 'user', 'email'))
        self.email_send_to = OPERATION_FILE.try_one_option(self.config_user, 'constant', 'email_send_to', 'list')
        self.timeout = OPERATION_FILE.try_one_option(self.config_user, 'constant', 'timeout', 'int')
#         self.loop_wait = OPERATION_FILE.try_one_option(self.config_user, 'constant', 'loop_wait', 'int')
        
#         self.lst_unit += ['user_name', 'user_email', 'email_send_to', 'timeout', 'loop_wait']
#         self.unitest()

    def set_appium_config(self, path_config_appium ):
        if os.path.isfile(path_config_appium):
            self.config_appium = OPERATION_FILE.read_ini_config(path_config_appium)
        else:
            self.config_appium  = None


CONFIG_BASE = ConfigBase()

#if __name__ == '__main__':
#    CONFIG_BASE.set_config("config.xml")
#    print CONFIG_BASE.get_info()


