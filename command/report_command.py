
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.format_operation import OPERATION_FORMAT
from xyTest.base.config_base import CONFIG_BASE
from xyTest.base.report_base import ReportBase

# example of error report
class CommandReport(ReportBase):                   
    def __init__(self, 
                 name=None, 
                 *args, **kwargs):

        ReportBase.__init__(self,
                       name=name,
                       *args, **kwargs)


    def create_error_report(self, tst):
        # report name folder
        if tst.report_list_bad_case:
            error_report = self.get_error_report_detail(tst)
            error_category = error_report["category"]
            error_detail = error_report["error"]
        
            this_report_date = OPERATION_FORMAT.get_current_date()
            er_title, er_name = self.get_general_report_title('error')
    
            report_info = {'::report_title::': er_title ,
                           '::test_category::': error_category,
                           '::test_summary::': error_detail,
                           '::report_date::': this_report_date,
                           }
    
            
            # save report
            msg_er = self.write_email_content(report_info, self.dic_name_general_tmp_file['detail'])
            html_path = OPERATION_FILE.write_a_report(er_name, msg_er)

            # send email
#             msg_er = msg_er.replace('<br>', '')
            self.new_email.sendmail(from_ = CONFIG_BASE.email_from,
                                    to_ = CONFIG_BASE.session_email_send_to,
                                    subject = er_title,
                                    message = msg_er, 
#                                     attachments = this_att, 
                                    message_type = 'html') 
            
            lst_sending_summary=[]
            lst_sending_summary.append("Sent Report %s to : " % er_title)
            lst_sending_summary.append(CONFIG_BASE.session_email_send_to)
            self.message_command(self, 'INFO', OPERATION_FILE.list_to_string(lst_sending_summary))


            
    def get_error_report_detail(self, tst):
            
        test_category = ""
        test_summary = ""
        error_in_this_test = ""
#             error_in_this_test  += "<br> %s:  </br>" % (str(tst.name.upper()))
        
        # add running time
        running_info = self.add_test_running_info(tst)
        test_category += running_info
        
        # count cases
        num_case = "<div class=\"Total\"><br> %s:  %s cases </br></div>" % (tst.name.upper(), str(len(tst.list_selected_case)))
        test_summary  += num_case
        error_in_this_test  += num_case
        
        # Locked cases
        if tst.report_list_locked_case  != []:
            l_s, l_d = self.add_case_info(tst.report_list_locked_case , "Locked")
            test_summary += l_s
            error_in_this_test  += l_d

        b_s, b_d = self.add_case_info(tst.report_list_bad_case, "Fail")
        test_summary += b_s
        error_in_this_test += b_d

            
        result = {}
        result["category"] = test_category
        result["summary"] = test_summary
        result["error"] = error_in_this_test

        return result

