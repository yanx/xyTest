
import os
from xyTest.base.base_test import TestBase
from xyTest.base.base_case import CaseBase
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.sys_operation import OPERATION_SYSTEM
from xyTest.base.config_base import CONFIG_BASE


class JMSingleCase(CaseBase):

    """
    """

    def __init__(self,
                 name=None,
                 test=None,

                 *args, **kwargs):

        CaseBase.__init__(self,
                       name=name,
                       test=test,
                       *args, **kwargs)
        # parent
        

    def setup_config_special(self):
        self.cuurrent_run_dir = OPERATION_FILE.get_parent_dir(self.ini)

    def get_jmeter_cmd(self, dic_cmd, seobj):
        lst_ignor = ['goto', 'jmx', 'jtl', 'jm', 'csv']
        cmd = 'jmeter'
        if dic_cmd['jm']:
            cmd = dic_cmd['jm'] # path of jemter app
        cmd += (' -n -t ' + dic_cmd['jmx']) # path of jemter script file
        cmd += (' -l ' + dic_cmd['jtl']) # path of output log file
        
        if self.test.jmeter_server_option:
            cmd += (' ' + self.test.jmeter_server_option)

        for key in seobj:  
            if not key in lst_ignor:
                cmd += (' -J%s=%s' % (key, seobj[key]))

        cmd += (' -e -o ' + dic_cmd['report'])
#         print ("cmd = ", cmd)
        return cmd

    def run_case(self):
#         return False
        try:
#             self.new_account = self.create()
            for se in self.lst_run:
                if self.config.has_option(se, 'goto'):
                    run_dir = CONFIG_BASE.get_file_path_in_conf(self.config[se]['goto'])
                else:
                    run_dir = self.cuurrent_run_dir
                    
                dic_cmd = {}
                
                # csv if exist
                lst_csv = OPERATION_FILE.try_one_option(self.config, se, 'csv', 'list')
                if lst_csv:
#                     print ("lst_csv = ", lst_csv)
                    for c in lst_csv:
                        sp =  OPERATION_FILE.path_join(run_dir, c.strip())
#                         print ("sp = ", sp)
                        if not os.path.isfile(sp):
                            self.add_message('Error', "No this file= %s" % str(sp))
                            return False
                        dp = OPERATION_FILE.path_join(self.test.path_jmter_report, c)
#                         print ("dp = ", dp)
                        OPERATION_FILE.copy(sp, dp)


                # JMX - MUST
#                 jm = self.config[se]['jm'].strip()
                dic_cmd['jm'] = False
                jm = OPERATION_FILE.try_one_option(self.config, se, 'jm')
                if jm:
                    path_jm =  CONFIG_BASE.get_file_path_in_conf(jm.strip())
                    if os.path.isfile(path_jm):
                        dic_cmd['jm'] = path_jm
      
                jmxstr = self.config[se]['jmx'].strip()
                
                if jmxstr[-4:] == '.jmx':
                    jmxname = jmxstr
#                     jmname = jmxstr[:-4]
                else:
#                     jmname = jmxstr
                    jmxname = jmxstr + '.jmx'
                    
                # check and copy JMX
                os.chdir(self.test.path_jmter_report)
                srcPath = OPERATION_FILE.path_join(run_dir, jmxname)
                if not os.path.isfile(srcPath):
                    self.add_message('Error', "No this jmx file=" % str(srcPath))
                    return False
                
                new_name = self.name_short+'.jmx'
                destPath = OPERATION_FILE.path_join(self.test.path_jmter_report, new_name)
                OPERATION_FILE.copy(srcPath, destPath)
                dic_cmd['jmx']  = new_name
                    
                dic_cmd['jtl'] = self.name_short + '_log.jtl'
                folder_report = self.name_short + '_report'
                path_report = OPERATION_FILE.path_join(self.test.path_jmter_report , folder_report)
                dic_cmd['report'] = OPERATION_FILE.create_dir(path_report)
#                 print ("dic_cmd = ", dic_cmd)
                cmd_run = self.get_jmeter_cmd(dic_cmd, self.config[se])
#                 print ("cmd_run = ", cmd_run)

                if cmd_run:
                    cmd_result = OPERATION_SYSTEM.shell_cmd(cmd_run)
                    self.get_cmd_report(se, cmd_result)
#                     print ("cmd_result = ", cmd_result)
                else:
                    er_ms = "No able to run cmd - %s -  to run in case - %s - section - %s -" % (cmd_run, self.name, se)
                    self.message_command(self, "Error", er_ms)
                    return False
                
                # zip report and attach to test
                output = OPERATION_FILE.path_join(self.test.path_jmter_report, folder_report)
                OPERATION_FILE.zipdir(path_report, output)
                if os.path.isfile(output+'.zip'):
                    self.test.lst_att_zip.append(output+'.zip')
                
            return True
        except Exception as e:
            self.message_command(self, "Exception", "def run_case-", e)
            return False





class Test(TestBase):
    
    """
    """
                            
    def __init__(self, 
                 name='command', 
                 typ=None,
                 suite=None,
                 *args, **kwargs):
            
        TestBase.__init__(self,
                       name=name,
                       typ=typ,
                       suite=suite,
                       *args, **kwargs)
        self.running_device = 'terminal'



    def before_test_run(self):
        try:
            #   self.name_log_folder =  suite_and_2018-09-26-15-00-23_onawhim
            self.path_jmter_report = OPERATION_FILE.path_join(OPERATION_FILE.path_report , self.name_log_folder)
#             print ("path_jmter_report = ", self.path_jmter_report)  # path_jmter_report =  /Users/yanxin/eclipse-workspace/vicuna_base/vicuna_test/log/Report/suite_and_2018-09-26-15-33-55_jmsingle

            OPERATION_FILE.create_dir(self.path_jmter_report)

            if os.path.isdir(self.path_jmter_report):
                os.chdir(self.path_jmter_report)
            else:
                self.add_message('Error', "No run_dir=" % str(self.path_jmter_report))
                return False
                
            # set jemeter variable
            self.jmeter_server_option = self.get_jmeter_server_option()
#             print ('self.jmeter_server_option  = ', self.jmeter_server_option )
                
            return True
        except Exception as e:
            self.message_command(self, "Exception", "def before_test_run-", e)
            return False


#     def after_test_run(self):
#         # example of procedure report
#         from xyTest.jmsingle.report_jmsingle import JMSingleReport
#         current_report = JMSingleReport('report')
#         current_report.set_current_suite(self.suite)
#         current_report.create_jmeter_report(self)

    # ------------------------------------------------
    # case function ---
    # ------------------------------------------------

    def create_case(self, name, dic):
        case = JMSingleCase(name=name, test=self)
        case.set_info(dic)
        return case

