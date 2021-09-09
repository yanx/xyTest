
import os
from xyTest.base.base_test import TestBase
from xyTest.base.base_case import CaseBase
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.sys_operation import OPERATION_SYSTEM
from xyTest.base.config_base import CONFIG_BASE


class CommandCase(CaseBase):
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

    def setup_config_special(self):
        self.cuurrent_run_dir = OPERATION_FILE.get_parent_dir(self.ini)

    def currect_special_char(self, cmd_run):
        dic_special_char = {
            "::TYPE::" : self.test.type,
            "::B::" : '%',
            }
        
        for k, v in dic_special_char.items():
            if k in cmd_run:
                cmd_run = cmd_run.replace(k, v)
            
        return cmd_run

    def run_case(self):
        try:
#             self.new_account = self.create()
            for se in self.lst_run:
                if self.config.has_option(se, 'goto'):
                    run_dir = CONFIG_BASE.get_file_path_in_conf(self.config[se]['goto'])
                else:
                    run_dir = self.cuurrent_run_dir

                if self.config.has_option(se, 'cmd'):
                    cmd_run = self.config[se]['cmd']
                else:
                    self.message_command(self, "Warning", "No cmd line in case %s - section %s " % (self.name, se))
                    cmd_run = False

                if os.path.isdir(run_dir):
                    os.chdir(run_dir)
                else:
                    self.add_message('Error', "No run_dir=" % str(run_dir))
                    return False

                if cmd_run:
                    new_cmd = self.currect_special_char(cmd_run)
                    cmd_result = OPERATION_SYSTEM.shell_cmd(new_cmd)
#                     print ("new_cmd = ", new_cmd)
                    self.get_cmd_report(se, cmd_result)
                else:
                    er_ms = "No able to run cmd - %s -  to run in case - %s - section - %s -" % (cmd_run, self.name, se)
                    self.message_command(self, "Error", er_ms)
                    return False
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

#     def after_test_run(self):
#         # example of procedure report
#         from xyTest.command.report_command import CommandReport
#         current_report = CommandReport('report')
#         current_report.set_current_suite(self.suite)
#         current_report.create_error_report(self)

    # ------------------------------------------------
    # case function ---
    # ------------------------------------------------
    
    def create_case(self, name, dic):
        case = CommandCase(name=name, test=self)
        case.set_info(dic)
        return case



