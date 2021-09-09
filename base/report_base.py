#!/usr/bin/env python
# coding: utf-8
import os
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from mimetypes import guess_type
from email.encoders import encode_base64
from email.header import Header


class MailBase:

    def __init__(self, serverlist):
        # server list [server, username, password, port]
        if ':' in serverlist[0]:
            data = serverlist[0].split(':')
            self.server = data[0]
            self.port = int(data[1])
        else:
            self.server = serverlist[0]
            self.port = 587
        self.username = serverlist[1]
        self.password = serverlist[2]
        if len(serverlist)>3:
            self.port = serverlist[3]
        self.connection = False
        

    def get_email(self, email):
        if '<' in email:
            data = email.split('<')
            email = data[1].split('>')[0].strip()
        return email.strip()

    def connect(self):
        self.connection = smtplib.SMTP(self.server, self.port)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        result = self.connection.login(self.username, self.password)
#         print ("connection = ", result)
        return result
         
    def test_connect_open(self):
        if not self.connection:
            self.connect()
        try:
            status = self.connection.noop()[0]
#             print ("connect status = ", status)
        except:  # smtplib.SMTPServerDisconnected
            status = -1
        return True if status == 250 else self.connect()



    def list_to_string(self, cc):
        if isinstance(cc, str):
            return cc
        elif isinstance(cc, list):
            return ', '.join(cc)
        else:
            return cc

    def clean_list_string(self, lst):
        result = []
        for itm in lst:
            if not itm in ['', ' ', '  ']:
                result.append(itm)
        return result
        
    def get_file_attachment(self, filename):

        try:
            mimetype, encoding = guess_type(filename)
#                 if mimetype == None:
#                     mimetype = "text/plain"
            mimetype = mimetype.split('/', 1)
            fp = open(filename, 'rb')
            attachment = MIMEBase(mimetype[0], mimetype[1])
            attachment.set_payload(fp.read())
            fp.close()
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment',
                                  filename=os.path.basename(filename))
            return attachment
        except:
            print("Could not attachment file-  ", filename)
            pass


    def get_txt_attachment(self, txt, fname, tye='plain'):
        attach_file = MIMEText(txt,tye)
#         plain=MIMEText('plain_body','plain')
#         html=MIMEText('html_body','html') 
        attach_file.add_header('Content-Disposition', 'attachment', filename=fname)
        return attach_file

    def get_zip_attachment(self, fname):
        attach_file = MIMEBase('application', 'zip')
        attach_file.set_payload(fname.read())
        encode_base64(attach_file)
#         encoders.encode_base64(msg)
        attach_file.add_header('Content-Disposition', 'attachment', 
                       filename=fname)
        return attach_file
    
    def sendmail(self, from_, to_, subject, message, attachments=None, 
                cc_=None, message_type='plain', encoding='utf-8'):

        self.email = MIMEMultipart()
        self.email['Subject'] = Header(subject, encoding)
        # from_, to_ cc_ must be string
        self.email['From'] = self.list_to_string(from_)
        self.email['To'] = self.list_to_string(to_)
        self.email['Cc'] = self.list_to_string(cc_)
#         self.email['X-Priority'] = '1'  # X-Priority: 1 (Highest priority)
        msg = MIMEText(message, message_type, encoding)
        self.email.attach(msg)
        
        if attachments is not None:
            for att in attachments:
                self.email.attach(att)   
        
        sendr_esult = self.send(self.email)
        if sendr_esult:
            errstr = ""
            for recip in sendr_esult.keys():
                errstr = """
        Could not deliver mail to: %s
        
        Server said: %s
        %s
        
        %s""" % (recip, sendr_esult[recip][0], sendr_esult[recip][1], errstr)
            self.message_command(self, 'Error', errstr)

        self.connection.close()
        
    def send(self, message, from_=None, to_=None):
        if type(message) == str:
            if from_ is None or to_ is None:
                raise ValueError('You need to specify `from_` and `to`')
            else:
                fr = self.get_email(from_)
                to = self.get_email(to_)
        else:
            fr = message['From']
            if isinstance(message['To'], str):
                to_emails = message['To'].split(', ')
            elif isinstance(message['To'], list):
                to_emails = message['To']
            else:
                errstr = "MailBase.Send - did not get to email = %s" % str(message['To'])
                self.message_command(self, 'Error', errstr)

#             if message['Cc'] is not None:
            if message['Cc']:
                to_emails += message['Cc'].split(',')
#             to = [self.get_email(complete_email) for complete_email in to_emails]

            message = message.as_string()
#             to = ", ".join(to_emails)
            to = self.clean_list_string(to_emails)
#             print ("to = ", to )

#         if not self.connection:
#             self.connect()
        self.test_connect_open()
        return self.connection.sendmail(fr, to, message)

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


from xyTest.base.base_object import OBase
from xyTest.base.config_base import CONFIG_BASE
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.sys_operation import OPERATION_SYSTEM
from xyTest.util.format_operation import OPERATION_FORMAT

class ReportBase(OBase):
    """ 
    An abstract class 
    """
    __instance = None

    def __init__(self, 
                 name="Report", 
                 *args, **kwargs):
        
        OBase.__init__(self, 
                       name=name, 
                       *args, **kwargs)


        self.dic_name_general_tmp_file = {'detail': 'summary_report.html',
                                          'summary':  'summary_report.html',
                                          }

        self.setup_email()
        self.set_reportbase_constant()
        self.set_html_constant()
    
    # ------------------------------------------------
    # set ---
    # ------------------------------------------------
    def set_reportbase_constant(self):
        self.set_empty_constant()

        # report template
        self.in_report_type = ''
        self.current_browser =''
        self.in_report_browser =''

    def set_empty_constant(self):
        self.run_detail_email_msg = {}  # {'detail: ,}
        self.current_attachment = []
        self.current_timeout_images = []
        self.lst_att_report = []
        self.lst_zip_report = []
        self.in_report_error = False


    def setup_email(self, slist=None):
        if not slist == None:
            self.new_email = MailBase(slist)
        elif not CONFIG_BASE.ip_smtp ==[]:
            self.new_email = MailBase(CONFIG_BASE.ip_smtp)
#             print ("CONFIG_BASE.ip_smtp =  ", CONFIG_BASE.ip_smtp)
        else:
            self.new_email = None
            
        # after create new report object, set current suite
    def set_current_suite(self, suite):
        self.current_time_date = OPERATION_FORMAT.get_name_date_all()
        self.current_suite = suite
        self.set_empty_constant()
        
#         self.lst_unit += ['current_time_date', 'current_suite']
#         self.unitest()

    # ------------------------------------------------
    # HTML Report   ---
    # ------------------------------------------------
    def set_html_constant(self):
        # constant
        self.report_split = "----"
        self.color_in_report = {"Locked" : "#FF00FF",
                                "Fail" : "#990000",
                                "Success" : "#000066"
                                }
        self.empty_cell = "<td>&nbsp;</td>"
        self.len_max_message = 1000
        
        
    def insert_split(self, num=1):
        return self.report_split*num
#         result = ""
#         for i in range(0, num):
#             result += self.report_split
#         return result

    def add_line_br(self, msg):
        return "<br> %s </br>" % (msg)
    
    def add_line_tr(self, msg):
        return "<tr> %s </tr>" % (msg)

    def add_line_link(self, msg, href=None, target="_blank"):
        result = "<a "
        if href:
            result += (" href=\"%s\" " % href)
        if target:
            result += (" target=\"%s\" " % target)
        result += ("> %s </a>" % msg)
        return result
    
    def add_line_td(self, msg, bgcolor=None, color=None, size=None):
        
        result = "<td"
        if bgcolor:
            result += (" bgcolor=\"%s\" " % bgcolor)
        result += ">"
        
        if color or size:
            result += "<font "
            if color:
                result += (" color=\"%s\" " % color)
            if size:
                result += (" size=\"%s\" " % size)
            result += ("> %s </font></td>" % msg)
        else:
            result += (" %s </td>" % msg)

        return result

    
    def add_line_font(self, msg, color=None, size=None):
        result = "<font "
        if color:
            result += (" color=\"%s\" " % color)
        if size:
            result += (" size=\"%s\" " % size)
        result += ("> %s </font>" % msg)
        return result


    def get_html_next_line(self, ms):
        result = str(ms)
        if '\\n' in result:
            lt_new = result.split('\\n')
            new_r = ''
            for itm in lt_new:
                new_r += "<br>%s</br>" % itm
            return new_r
        return "<br>%s</br>" % result



    # ------------------------------------------------
    # get email attachment    ---
    # ------------------------------------------------
    
    def get_email_attachment(self):
        # self.current_attachment - list of html report - detail report, error report, category report 
        # self.current_timeout_images - list of images - timeout image, performance_image
        # self.lst_zip_report - list of zip file
        this_att =  self.current_attachment + self.current_timeout_images
#         print ("this_att  = ", this_att )  #  [<email.mime.text.MIMEText object at 0x10c13af60>]
        if self.lst_att_report:
#             print ("self.lst_att_report = ", self.lst_att_report)  # [<email.mime.base.MIMEBase object at 0x10c13ae48>, 
            this_att += self.lst_att_report
        if self.lst_zip_report:
#             print ("self.lst_zip_report = ", self.lst_zip_report)  # [<email.mime.base.MIMEBase object at 0x10c13ae48>, 
            this_att += self.lst_zip_report

        return this_att
    # ------------------------------------------------
    # Create HTML Report   ---
    # ------------------------------------------------
    def add_test_running_info(self, tst):
            test_runing = ""
            case_num = len(tst.list_selected_case)
            test_time_start = OPERATION_FORMAT.get_mysql_datetime(tst.time_start)
            test_time_end = OPERATION_FORMAT.get_mysql_datetime(tst.time_end)
            use_time = int(tst.get_time_run())
            total_time = OPERATION_FORMAT.second_to_str(use_time)

            test_runing += "<div class=\"\"> <br> %s (Used: %s. - %s Cases)</br></div>  " % (tst.name.upper(), total_time, case_num)
            test_runing += "<div class=\"\"> <font size=\"-1\"><br> %s Start At: %s </br>  " % (self.report_split, test_time_start)
            test_runing += "<br> %s End At: %s </br> </font> </div> " % (self.report_split, test_time_end)
            tst.report_category_info = test_runing
#             print ("test_runing  =", test_runing)
            return test_runing


    def add_test_version_info(self, tst):
            test_version = ""
            if not tst.version == 'unknown_version':
                test_version += "<div class=\"\"> <br> %s (%s)</br></div>  " % (tst.name.upper(), str(tst.version))
    #             print ("test_runing  =", test_runing)
            return test_version

    def add_test_device_info(self, tst):
            test_device = ""
            if tst.running_device == 'app':
                try:
                    di = tst.dic_appium['deviceName']
                except:
                    di = "No Value"
                test_device = "<div class=\"\"> <br> %s Device : %s</br></div>  " % (tst.name.upper(), di)
                
            elif tst.running_device == 'browser':
                if len(self.in_report_browser) > 1:
                    pass
                else:
                    self.in_report_browser = self.current_browser.upper()
                    test_device = "<div class=\"\"> <br> Testing Browser : %s</br></div>  " % (self.in_report_browser)
            else:
                pass 
            return test_device
        
    def add_case_info_line(self, old1, old2):
        c1 = self.get_html_next_line(old1)
        c2 = self.get_html_next_line(old2)
        ms = '<td width="80"><font size="-1" >%s</font></td>' % c1
        ms2 = '<td width="680" ><font size="-1" >%s</font></td>' % c2
        return ms + ms2

    def add_one_case_info(self, testCase, lst_k):
        no_info = True
        info_key =  list(testCase.info.keys())
        for k in lst_k:
            if k in info_key:
                if testCase.info[k] != []:
                    no_info = False
                    break
        if no_info:
            return ''
        else:
            result = "<table> "
            for line in testCase.info['log']:
                ls_line = line.split(OPERATION_FILE.ch_split)
                for it in lst_k:
                    it_k = 'Level: ' + it
                    if it_k in ls_line[0]:
                        result += "<tr> "
                        result += self.add_case_info_line(it, ls_line[1])
                        result += "</tr> "
                        break
            result += "</table> <br> </br>"
            return result

        
        # k : self.color_in_report = {"Locked" : , "Fail" :, "Success" : }
    def add_case_info(self, lst_case, k):
        summary = ""
        detail = ''
        num = "<div class=\""+k+"\"><font color=\"%s\" size=\"-1\"><br> %s %s: %s </br></div>" % (self.color_in_report[k], self.insert_split(), k, str(len(lst_case)))
   
        summary += num
        detail += num
        if lst_case != []:
            for testCase in lst_case:
                if testCase.link:
                    a_link = self.add_line_link(testCase.name, href=testCase.link) # (testCase.name_short, href=testCase.link)
                    this_name = "<br>%s %s </br>" % (self.insert_split(3), a_link)
                else:
                    this_name = "<br>%s %s </br>" % (self.insert_split(3), testCase.name) #testCase.name_short)
                summary += this_name
                if testCase.description:
                    this_name += "<br>%s Description: %s </br>" % (self.insert_split(4), str(testCase.description))
                detail += this_name
 
                if k != "Locked":
                    if OPERATION_FILE.admin_mode:
                        if os.path.isfile(testCase.path_timeout_image):
                            img_att = self.new_email.get_file_attachment(testCase.path_timeout_image)
                            self.current_timeout_images.append(img_att)
                        if os.path.isfile(testCase.path_performance_image):
                            img_att = self.new_email.get_file_attachment(testCase.path_performance_image)
                            self.current_timeout_images.append(img_att)

                    lst_k = self.dic_info_key['Success'] + self.dic_info_key['Fail']
                    this_info = self.add_one_case_info(testCase, lst_k)
                    detail  += (this_info)
                    
        summary  += "</font>"
        detail  += "</font>"
        return summary, detail


    # ------------------------------------------------
    # general report function ---
    # ------------------------------------------------
    def get_general_report_title(self, nm="Detail"):

        title = "%s - %s%s%s - %s Report - %s - %s" % (self.current_suite, self.in_report_type, self.in_report_browser, OPERATION_SYSTEM.platform, nm, CONFIG_BASE.user_name, self.current_time_date )
        name = "%s_%s_%s_report_%s.html" % (self.current_time_date , self.current_suite, nm, CONFIG_BASE.user_name.replace(' ', ''))
        return title, name
    
    def set_report_constant_detail(self):
        self.in_report_type = ''
#         this_ty = OPERATION_FILE.get_key_value(CONFIG_BASE.dic_cmd, 'type')
        this_ty = CONFIG_BASE.session_type
        if this_ty:
            self.in_report_type = str(this_ty).upper() + ' env '
    
        self.current_browser =''
        this_browser = CONFIG_BASE.session_browser
        if this_browser:
            self.current_browser = ' %s ' % ( this_browser)

    # ------------------------------------------------
    # summary_report ---
    # ------------------------------------------------
    def create_run_summary_report(self, list_test):
        list_report = []
        this_name = "test_report"
        
        list_report.append( "Total %s Category\n" % str(len(list_test)) )

        total_time = 0
        totol_case = 0
        list_msg = []
        
        list_test.sort(key=lambda x: x.name, reverse=True)
        for obj in list_test:
            msg = "------------------------------------\n"
            msg += "Test Name: %s\n" % (obj.name)
            case_num = len(obj.list_selected_case)
            totol_case += case_num
            msg += "Case Amount: %s\n" % (str(case_num))
            use_time = int(obj.get_time_run())
            total_time += use_time
            msg += "Time Use: %s\n" % (OPERATION_FORMAT.second_to_str(use_time))
            msg += "------------------------------------"
            list_msg.append(msg)
        
        list_report.append( "Total Case Amount: %s\n" % str(totol_case) )
        list_report.append( "Total Using Time: %s\n" % OPERATION_FORMAT.second_to_str(total_time) )
        
        for ms in list_msg:
            list_report.append( ms )
        
        str_report = "\n".join(list_report)
        
        file_name = OPERATION_FORMAT.report_name(this_name)
        path_test_report = OPERATION_FILE.path_join(OPERATION_FILE.path_report, file_name+".txt")
        OPERATION_FILE.file_write(path_test_report, str_report)
        
        return str_report
    

    # ------------------------------------------------
    # detail_report ---
    # ------------------------------------------------
    def create_run_detail_report(self, lst):
        # report name folder
        if lst == []:
            msg= "In create_run_detail_report, Test List is empty."
            self.message_command(self, "Error", msg)
            return False
        else:
            self.build_run_detail_report_email(lst)
            if self.run_detail_email_msg:
                # general report
                ks = self.run_detail_email_msg.keys()
                for k in ks:
                    html_name = self.run_detail_email_msg[k][2]
                    html_msg = self.run_detail_email_msg[k][1]
                    if OPERATION_FILE.admin_mode:
                        html_path = OPERATION_FILE.write_a_report(html_name, html_msg)
                    if not "summary" in k:
#                             self.current_attachment.append(html_path)
                        self.current_attachment.append(self.new_email.get_txt_attachment(html_msg, html_name, 'html'))

                return True
            else:
                msg= "In reporter.create_run_detail_report, Failed to build report"
                self.message_command(self, "Error", msg)
                return False
            

    def build_run_detail_report_email(self, lst):
        self.set_report_constant_detail()
        newlist = sorted(lst, key=lambda x: x.name, reverse=False)
        test_detail = self.get_report_test_detail(newlist)
        test_category = test_detail["category"]
        report_detail = test_detail["error"]
        test_summary = test_detail["summary"]
        version_category = test_detail["version"]
        test_device = test_detail["device"]
        
#         print ("test_detail = ", test_detail)
        this_report_date = OPERATION_FORMAT.get_current_date()
        sum_title, sum_name = self.get_general_report_title('summary')

        report_info = {'::report_title::': sum_title ,
                       '::test_category::': test_category,
                       '::test_summary::': test_summary,
                       '::report_date::': this_report_date,
                       '::version_category::': version_category,
                       '::test_device::': test_device,
                       }

        msg_summary = self.write_email_content(report_info, self.dic_name_general_tmp_file['summary'])
        self.run_detail_email_msg['summary'] = [sum_title, msg_summary, sum_name]
        
        rep_title, rep_name = self.get_general_report_title()
        report_info = {'::report_title::': rep_title ,
                       '::test_category::': test_category,
                       '::test_summary::': report_detail,
                       '::report_date::': this_report_date,
                       '::version_category::': version_category,
                       '::test_device::': test_device,
                       }
        msg_detail = self.write_email_content(report_info, self.dic_name_general_tmp_file['detail'])
        self.run_detail_email_msg['detail'] = [rep_title, msg_detail, rep_name]
        
        

    def get_report_test_detail(self, lst):
        test_category = ""
        test_summary = ""
        error_summary = ""
        version_category = ""
        self.in_report_browser =''
        test_device = "<div class=\"\"> <br> Testing Machine : %s </br></div>  " % (OPERATION_SYSTEM.get_platform_info())
        for tst in lst:
            error_in_this_test = ""
#             error_in_this_test  += "<br> %s:  </br>" % (str(tst.name.upper()))
            # add running time
            running_info = self.add_test_running_info(tst)
            test_category += running_info
            version_info = self.add_test_version_info(tst)
            version_category += version_info
            device_info = self.add_test_device_info(tst)
            test_device += device_info
            
            # count cases
            num_case = "<div class=\"Total\"><br> %s:  %s cases </br></div>" % (tst.name.upper(), str(len(tst.list_selected_case)))
            test_summary  += num_case
            error_in_this_test  += num_case
            
            # Locked cases
            if tst.report_list_locked_case  != []:
                l_s, l_d = self.add_case_info(tst.report_list_locked_case , "Locked")
                test_summary += l_s
                error_in_this_test  += l_d

            if tst.report_list_bad_case:
                self.in_report_error = True
            b_s, b_d = self.add_case_info(tst.report_list_bad_case, "Fail")
            test_summary += b_s
            error_in_this_test += b_d
            
            g_s, g_d = self.add_case_info(tst.report_list_good_case, "Success")
            test_summary += g_s
            error_in_this_test  += g_d
            
            error_summary += error_in_this_test
            
            if tst.lst_att_zip:
                for z in tst.lst_att_zip:
                    zip_att = self.new_email.get_file_attachment(z)
                    self.lst_zip_report.append(zip_att)
        # end for tst in lst:
        result = {}
        result["category"] = test_category
        result["summary"] = test_summary
        result["error"] = error_summary
        result["version"] = version_category
        result["device"] = test_device

        return result
    
    

    # ------------------------------------------------
    # write_email_content ---
    # ------------------------------------------------

    def write_email_content(self, report_info, tmp):
        try:
            tmp_html = OPERATION_FILE.path_join(CONFIG_BASE.path_lib_template, [tmp])
            list_msg = OPERATION_FILE.file2list(tmp_html)
        except:
            msg = "Could not get report template - %s"% (str(tmp))
            self.message_command(self, "Error", msg)
            return False
        
        msg = ''
        for line in list_msg:
            if "::" in line:
                for k in report_info.keys():
                    if k in line:
                        try:
                            line = str(line).replace(k, str(report_info[k]))
                            break
                        except Exception as e:
                            msg = "failed to write line - %s - " % (line)
                            self.message_command(self, "Exception", msg, e)
                            pass
            msg = msg + line.rstrip() + "\n"
        return msg


    def send_summary_report(self):
#         print (' Start summary report ' * 20)
        if not self.in_report_error:
            CONFIG_BASE.set_alarm_constant()
#         return
        sending = 'summary'
        if not self.new_email:
            self.message_command(self, "Error", "No EMAIL Server to send report")
        elif not sending in self.run_detail_email_msg.keys():
            self.message_command(self, "Error", "No EMAIL -%s- to send" % sending)
        elif not CONFIG_BASE.session_email_send_to:
            self.message_command(self, "Error", "No EMAIL Send TO list -%s-" % str(CONFIG_BASE.session_email_send_to))
        else:
            this_email = self.run_detail_email_msg[sending]
            this_att =  self.get_email_attachment()
            msg = this_email[1]
#             msg = msg.replace('<br>', '')
            # [report]
            if CONFIG_BASE.dic_cmd['report']:
                report_title = this_email[0]
                self.new_email.sendmail(from_ = CONFIG_BASE.email_from,
                                        to_ = CONFIG_BASE.session_email_send_to,
                                        subject = report_title,
                                        message = msg, 
                                        attachments = this_att, 
                                        message_type = 'html') 
                
                self.message_command(self, 'INFO', "Sent Report %s to : %s" % (report_title, CONFIG_BASE.session_email_send_to))
               
                
            if (CONFIG_BASE.session_alarm and self.in_report_error):
                print ("Now try_alarm = ", CONFIG_BASE.try_alarm)
                print ("Now count_alarm = ", CONFIG_BASE.count_alarm)
                if CONFIG_BASE.try_alarm < CONFIG_BASE.alarm_re_try:
                    CONFIG_BASE.try_alarm += 1
                else:
                    msg = self.run_detail_email_msg['detail'][1]
                    report_title = "%s - when - %s" % (CONFIG_BASE.session_alarm, str(CONFIG_BASE.time_start))
                    
                    this_att = self.current_timeout_images
                    
                    self.new_email.sendmail(from_ = CONFIG_BASE.email_from,
                                            to_ = CONFIG_BASE.session_email_send_to,
                                            subject = report_title,
                                            message = msg, 
                                            attachments = this_att, 
                                            message_type = 'html') 
                    
                    self.message_command(self, 'INFO', "Sent Report %s to : %s" % (report_title, CONFIG_BASE.session_email_send_to))
                    
                    if CONFIG_BASE.count_alarm  == 0:
                        CONFIG_BASE.alarm_start = time.time() 
#                         print ("CONFIG_BASE.alarm_start = ", CONFIG_BASE.alarm_start)
                    CONFIG_BASE.count_alarm += 1
                    CONFIG_BASE.try_alarm = 0

            self.set_empty_constant()


if __name__ == '__main__':
    
    print ("sending email  - ----------")
    server='email-smtp.us-east-1.amazonaws.com:587'
    username='AKIAJN3IB54YDHGDGJIA'
    password="Agwb0CBlHTlQFS2q81TrPfBZdHZNVhSaU+kEEnUDVM5W"
    sl = [server, username,password ]
    mil = MailBase(sl)
    mil.sendmail(from_ = 'do.not.reply@whimmade.com', 
                 to_="yan.xin@onawhim.com", 
                 subject = "my testing eamil object", 
                 message= "message with attachments")
#     
    


    
