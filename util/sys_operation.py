
import sys
import os
import subprocess
#import shutil
import time
import socket

class OperationSystem(object):

    """ 
    An abstract class 
    """
    
    __instance = None

    def __init__(self, 
                 name="System Operation", 
                 info = {},
                 *args, **kwargs):
        """     """
    
        self.name = name
        self.info = info
        
        self.lst_sys_error = [" error", 'Failed', ' fatal', 
                              'Errno' , 'Traceback', 'Exception',# python exception track
                              'An error occurred']
        self.clean_attr()
        self.set_system_info()
        
# === === === === === === === === === === === ===
# init-get-set ---
# === === === === === === === === === === === ===
    def clean_attr(self):
        self.current_process = None
        self.current_output = None
        self.current_err = None
        self.current_running = None
        self.current_memory = None
        
    def get_platform_info(self):
        import platform
#         platform.machine()  # 'x86'
#         platform.version()  #'5.1.2600'
        return str(platform.platform()) # 'Windows-XP-5.1.2600-SP2'
        
    def set_system_info(self):
        self.exe_python = sys.executable.replace("\\", "/")
        #PYTHON_PATH = "C:/Python27/python.exe/"
        self.platform = 'NO_TYPE'
        # system info
        if sys.platform == 'win32':
            self.platform = 'WINDOWS'
        elif sys.platform == 'darwin':
            self.platform = 'MAC'
        elif 'linux' in sys.platform:
            self.platform = 'LINUX'
            
        # machine name
        self.name_machine = self.get_host_name()
        # platform name
        self.dic_name_platform = {
                                  'WINDOWS': ['windows', 'win32', 'win'],
                                  'MAC': ['mac', 'darwin'],
                                  'LINUX': ['linux', 'lnx'],
                                  }
        self.lst_name_platform = self.dic_name_platform[self.platform]
        
        
    def get_host_name(self):
#        import socket
#        print(socket.gethostname())
        return socket.gethostname()
#    
##        import platform
##        import socket
##        import os
##        print ( platform.node())
##        print ( socket.gethostname())
##        print ( os.environ['COMPUTERNAME'])
        
# === === === === === === === === === === === ===
# cmd and process ---
# === === === === === === === === === === === ===
    
    def run_cmd(self, cmd, wait=True):
        self.clean_attr()
        try:
#            print ( "in file.run_cmd cmd = ", cmd)
            if self.platform == 'MAC' or self.platform == 'LINUX':
                self.current_process = subprocess.Popen (cmd , shell=True)
            else:
                self.current_process = subprocess.Popen (cmd , shell=False)
            if wait:
                self.current_process.wait()
            self.current_process = None
            time.sleep(1)
            return True
        
        except Exception as e:
            msg = "Failed to run cmd : \" %s \"\n error = %s" % (cmd, str(e))
            self.sys_error_message (msg)
            self.kill_process(self.current_process)
            return False
                


    def shell_cmd(self, cmd, wait=True):
        self.clean_attr()
        try:
            self.current_process = None
            time_start = time.time()
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate() # there are string
            self.current_process = process
            if wait:
                process.wait()
            # running time
            time_end = time.time()
            self.current_running = time_end - time_start
            time.sleep(1)
            # system log
            
            self.current_output = "%s\n\n%s" % (out, err)
            self.current_err = ''

            lst_ouput = self.current_output.split ('\n')
            lst_err = []
            if lst_ouput:
                for this_out in lst_ouput:
                    for this_eror in self.lst_sys_error:
                        if this_eror.lower() in str(this_out).lower() :
                            lst_err.append(this_out)
                            break
                if lst_err:
                    self.current_err = lst_err

            return True
        except Exception as e:
            msg = "FAILED to run cmd : \" %s \"\n error = %s" % (cmd, str(e))
            self.sys_error_message (msg)
            self.kill_process(self.current_process)
            return False
                
                
    def interrupt_process(self):
        print ("start time.sleep(100)")
        import signal
        self.current_process.send_signal(signal.SIGINT)
#         os.kill(self.current_process.pid, signal.SIGINT)
        print ("time.sleep(100)")
    
    def kill_process(self, process=None):  # Kill a process
        try:
            if not process:
                process = self.current_process
            if process:
                if process.poll() is None: 
                    pid = process.pid
                                            
                    if self.platform == 'MAC':
                        cmd = "kill -9 %s" % str(pid)
                        self.run_cmd(cmd)

                    elif self.platform == 'WINDOWS':
                        cmd = "taskkill /PID %s" % str(pid)
                        self.run_cmd(cmd)
                        
                    elif self.platform == 'LINUX':
                        cmd = "kill -9 %s" % str(pid)
                        self.run_cmd(cmd)
                    else:
                        msg = "Failed to kill process.  Unknown platform %s" % (str(sys.platform))
                        self.sys_error_message (msg)
                        
        except os.error as e:                
            msg = "Failed to kill process \n error = %s" % (str(e))
            self.sys_error_message (msg)

    
    def kill_browser(self):
    # Kill all apps
        self.dic_kill_browser = {'chrome': {
                                  'WINDOWS': 'taskkill /F /IM chrome.exe',
                                  'MAC': 'killall -9 "Google Chrome"',
                                  'LINUX': 'pkill chrome',
                                  },
                                  'firefox': {
                                  'WINDOWS': 'taskkill /F /IM firefox.exe',
                                  'MAC': 'killall -9 "Mozilla Firefox"',
                                  'LINUX': 'pkill firefox',
                                  }
                                }

        try:
            for k, v in self.dic_kill_browser.items():
                print ("clean browser process - "+k)
                cmd = v[self.platform]
                self.run_cmd(cmd)

        except os.error as e:                
            msg = "Failed to kill chrome \n error = %s" % (str(e))
            self.sys_error_message (msg)

# === === === === === === === === === === === ===
# OS Operations ---
# === === === === === === === === === === === ===

    def run_script_cmd(self, scr=None):
        if scr:
            if scr.lower().endswith('.py'):
#            if scr.lower().endswith(('.py', '.pyc')):
                cmd = '"%s" "%s"' % (self.exe_python, scr)
            else:
                self.sys_error_message("Error in run_script_python - Unknown script type : %s" % str(scr))
                return False
                
            return self.run_cmd(cmd)
        else:
            self.sys_error_message("Error in run_script_python - No script : %s" % str(scr))
            return False
        
        
    def open_folder_with_path(self, path):
        if self.platform == 'MAC':
            cmd = 'open "%s"' % path
            
        elif self.platform == 'LINUX':
            cmd = 'nautilus "%s"' % path

        elif self.platform == 'WINDOWS':
            cmd = 'explorer "%s"' % path
            cmd = cmd.replace("/", "\\")

        else:
            msg = "OPERATION_SYSTEM - open_folder_with_path - unknown platform "
            self.sys_error_message(msg)
            return
        self.run_cmd(cmd)


    def link_to_path(self, link, dest):
        link = str(link)
        dest = str(dest)
        
        if self.platform == 'MAC': # ln -s <dest> <link>
            cmd = 'ln -s "%s" "%s"' % (dest, link)
            
        elif self.platform == 'LINUX': # ln -s [target directory or file] [symlink shortcut]
            cmd = 'ln -s "%s" "%s"' % (dest, link)

        elif self.platform == 'WINDOWS':
            cmd = '"%s" "%s"' % (link , dest) # windows: MKLINK [[/D] | [/H] | [/J]] Link Target
            cmd = cmd.replace("/", "\\")
            cmd = 'mklink /J ' + cmd  
        else:
            msg = "OPERATION_SYSTEM - link_to_path - unknown platform "
            self.sys_error_message(msg)
            return
        self.shell_cmd(cmd)
        

    
    def lock_computer(self):
        if self.platform == 'WINDOWS':
            cmd = "rundll32.exe user32.dll, LockWorkStation"
            os.popen(cmd)
            

#         if self.platform == 'WINDOWS':
#             cmd = "rundll32.exe user32.dll, LockWorkStation"
#         elif self.platform == 'LINUX':
#             cmd = "gnome-screensaver-command -l"
#         else:
#             return
#         
#         os.popen(cmd)


# === === === === === === === === === === === ===
#  info, message, screenshot ---
# === === === === === === === === === === === ===

    def sys_error_message(self, msg):
#         print >> sys.stderr, msg
        sys.stderr.write( msg )

        
    def open_sys_info(self):
        if self.platform == 'WINDOWS':
            cmd = "dxdiag.exe"
            os.popen(cmd)
        
    
    def get_info_from_line(self, line):
        infos = line.split(':')
        result = infos[1].strip()
        return result
    
    
    def get_sys_info(self):
        sys_info = {}
        
        if self.platform == 'WINDOWS':
            cmd = "systeminfo"
            result = os.popen(cmd).read()
        #    print ( result )
        #    print ( type(result)  ) # <type 'str'>
            cmd_info = str(result).split('\n')
        #    print ( cmd_info )
        
            for line in cmd_info:
                if 'OS Name' in line:
                    sys_info['OS'] = self.get_info_from_line(line)
        #            print ( "sys_info['OS'] = ", sys_info['OS'] )
                elif 'Total Physical Memory' in line:
                    sys_info['Physical Memory'] = self.get_info_from_line(line)
        #            print ( "sys_info['Physical Memory'] = ", sys_info['Physical Memory'] )
                else:
                    continue
                
        return sys_info
           

    def save_screenshot(self, filePath=False):
        try:
            import pyscreenshot as ImageGrab
            if not filePath:
                from xyTest.util.file_operation import OPERATION_FILE
                filePath = os.path.join(OPERATION_FILE.path_user_documents, "timeout_screnshot.png")
            ImageGrab.grab_to_file(filePath)
        except:
            print ('Please install pyscreenshot to get screen shot image')
            pass

    def get_info(self):
        self.info['exe_python'] = self.exe_python
        self.info['platform'] = self.platform
        return self.info
    

    
OPERATION_SYSTEM = OperationSystem()

if __name__ == '__main__':
    #####################################################
    import platform
    import socket
    print ( platform.node()  )
    print ( socket.gethostname() )
    
    ######################################################
#     cmd = 'ls'
#     p = subprocess.Popen(cmd,shell=True, 
#                          stdout=subprocess.PIPE,
#                          stderr=subprocess.PIPE)
#     
#     p.wait()
#     print ( "stdout = ", p.stdout )
#     print ( "stderr = ",p.stderr )
#     for line in p.stdout:
#         print(">>> " , line.rstrip())
    ############################################################################
    

