
from xyTest.base.report_base import ReportBase

# example of error report
class JMSingleReport(ReportBase):                   
    def __init__(self, 
                 name=None, 
                 *args, **kwargs):

        ReportBase.__init__(self,
                       name=name,
                       *args, **kwargs)


    def create_jmeter_report(self, tst):
        pass



# ${__P(username, test_account@videri.com)}
# ${__P(password, My0!ssword)}
# 
# ${__P(mysite, dev.whimmade.com)}
# 
# 
# ${__P(users,2)}
# ${__P(rampup,2)}
# ${__P(loops,1)}
