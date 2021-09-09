
import time
from xyTest.base.base_object import OBase
# import requests
from requests import Request, Session
import json

class RequestBase(OBase):
    def __init__(self,
                 name=None,
                 *args, **kwargs):

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)

#         self.run_debug = True
        self.set_requestbase_constant()
        self.set_default_constant()

    # ------------------------------------------------
    # function for __init__ ---
    # ------------------------------------------------
    def set_requestbase_constant(self):
        self.session = Session()
        self.current_resp = None
        self.current_resp_json = None
        self.using_info = {}
        self.default_headers = {"Content-type": "application/json"}
        self.lst_option = ["GET", "POST", "PUT", "PATCH", "DELETE"]
#         self.dic_send = {"GET": self.session.get,   # (url)
#                          "POST": self.session.post,   # (url, data, json)
#                          "PUT": self.session.put,   # (url, data)
#                          "PATCH": self.session.patch,   # (url, data)
#                          "DELETE": self.session.delete,   # (url)
#                          }


    def pre_check_request(self, typ, url):
        rst = True
        if not typ in self.lst_option:
            self.message_command(self, "Error", 'Unknown Request Type - %s' % (str(typ)))
            rst = False
        if not url:
            self.message_command(self, "Error", 'Unknown Request URL - %s' % (str(url)))
            rst = False

        return rst
    
    def base_request(self, typ, url, data=None, pars=None):
        if typ == "POST":
            rep = self.session.post(url=url, data=data, params=pars)
        elif typ == "GET":
            rep = self.session.get(url=url, params=pars)
        elif typ == "DELETE":
            rep = self.session.delete(url=url, params=pars)
        elif typ == "PUT":
            rep = self.session.put(url=url, data=data, params=pars)
        elif typ == "PATCH":
            rep = self.session.patch(url=url, data=data, params=pars)
        else:
            return None
        return rep


    def send_request(self, typ=None, url=None, data=None, pars=None):
        if not self.pre_check_request(typ, url):
            return False
        else:
#             print ("url = ", url)
#             print ("data = ", data)
            json_data = None
            if data:
                json_data=json.dumps(data)
            
            self.current_resp = self.base_request(typ, url, json_data, pars)
            
            if not self.current_resp == None:
                return self.check_response(self.current_resp, typ)
            else:
                self.message_command(self, "Error", 'No Response when - %s - %s' % (typ, url) )
                return False


    def performance_request(self, typ=None, url=None, data=None, pars=None, rp=100, sp=10):
        if not self.pre_check_request(typ, url):
            return False
        else:
            rep = None
            json_data = None
            if data:
                json_data=json.dumps(data)

            each_step = int(rp/sp)

            num = []
            sd = []
#             self.time_start = time.time() # total time used
            for i in range(1, sp+1):
                self.time_start = time.time()
                for _ in range (each_step):
                    rep = self.base_request(typ, url, json_data, pars)
                self.time_end = time.time() # tiem used in each step
                this_run = self.get_time_run() #<class 'float'>
                num.append(i*each_step)
                sd.append(this_run)

            xr = num
            yr = sd
            ti = '%s - Response Time of %d Repeat ' % (self.case.name_short, each_step)
            xl = 'Repeat Times - %s' % (typ)
            yl = 'Response Time (Second) of %d Repeat ' % (each_step)
            
            pa_png = self.case.path_performance_image
#             print ("pa_png = ", pa_png)
#             GRAPH_BASE.simple_line_histo(ti, xl, yl, xr, yr, pa_png)
            self.message_command(self, "Report", 'X-Row = %s' % (str(xr)) )
            self.message_command(self, "Report", 'Y-Row = %s' % (str(yr)) )
            
            self.current_resp = rep
            if not self.current_resp == None:
                return self.check_response(self.current_resp, typ)
            else:
                self.message_command(self, "Error", 'No Response when - %s - %s' % (typ, url) )
                return False
        
    def api_request(self, typ=None, url=None, **kwargs):
#         param = "("
#         for k in kwargs:
#             param += " " + k + "=" + kwargs[k]
#         param += " )"
        rep = None
        
        if typ == "POST":
            rep = self.session.post(url=url, **kwargs)
        elif typ == "GET":
            rep = self.session.get(url=url, **kwargs)
        elif typ == "DELETE":
            rep = self.session.delete(url=url, **kwargs)
        elif typ == "PUT":
            rep = self.session.put(url=url, **kwargs)
        elif typ == "PATCH":
            rep = self.session.patch(url=url, **kwargs)
        else:
            self.message_command(self, "Error", 'Unknown Request Type - %s' % (str(typ)))
            return False
         
        self.current_resp = rep
        if not rep == None:
            return self.check_response(rep, typ)
        else:
            self.message_command(self, "Error", 'No Response when - %s - %s' % (typ, url) )
            return False


    def send_prepare(self, opt, url, data=None, headers=None):
        print ("send_prepare = data = ", data)
        if opt in self.lst_option:
            reqt = Request(opt, url, data=data, headers=headers)
            prepped = reqt.prepare()
            rep = self.session.send(prepped)
            self.current_resp = rep
            if rep:
                return self.check_response(rep, opt)
            else:
                self.message_command(self, "Error", 'No Response def send_prepare - %s - %s' % (opt, url) )
                return False
        else:
            self.message_command(self, "Error", 'unknown option - %s' % (opt) )
            return False


    def get_response(self):
        return self.current_resp

    def check_response(self, rep, typ='None'):
        code = rep.status_code
#         print('rep.headers = ', rep.headers)
#         print('rep.content = ', rep.content)
        self.current_resp_json = None
#         if rep.status_code ==200:
        if code  >= 200 and code < 300:
#             print (" rep.text ====="+rep.text+"===== rep.text ")
#             print ("len rep.text ===== ", len(rep.text))
            if rep.text in ['']:
                self.current_resp_json = rep.text
            else:
                self.current_resp_json = json.loads(rep.text)
#         print ('response - type = ', type(rep))
#         print ('current_resp_json = ', self.current_resp_json)

            msg = 'Request - %s - %s - %s' % (typ, str(rep.url), str(code))
            self.message_command(self, "Report", msg)
            
            pre = "Response Data = "
            if self.run_debug:
                self.message_command(self, "Report", pre+rep.text)
            else:
                self.message_command(self, "Info", pre+rep.text)
#                 self.message_command(self, "Report", pre+OPERATION_FILE.get_limit_string(rep.text))
            return True
        else:
            msg = 'Request - %s - %s - %s - %s' % (typ, str(rep.url), str(code), str(rep.text))
            self.message_command(self, "Error", msg)
            return False


if __name__ == '__main__':
    
    
    pass
