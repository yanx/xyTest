# import os
import time
from xyTest.base.base_object import OBase
from xyTest.base.config_base import CONFIG_BASE
from xyTest.util.sys_operation import OPERATION_SYSTEM
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.format_operation import OPERATION_FORMAT

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
except:
    print ('PageBase could not find Selenium.  Please install Selenium before web browser test')
    pass


class PageBase(OBase):
    def __init__(self,
                 name=None,
                 *args, **kwargs):

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)

#         self.run_debug = True

        self.testing_mode = False
        self.headless_mode = False
        try:
            self.testing_mode = (CONFIG_BASE.session_type in ['api', 'dev'])
            self.headless_mode = (not CONFIG_BASE.dic_cmd['view'])
        except:
            pass
        self.default_browser = CONFIG_BASE.session_browser
        
        self.driver = None
        self.set_pagebase_constant()
        self.set_default_constant()

        self.sleep_second = 2
    # ------------------------------------------------
    # function for __init__ ---
    # ------------------------------------------------

    def set_pagebase_constant(self):
        self.use_inside_driver = False
        self.dic_social = {
            'facebook' : '//www.facebook.',
            'instagram' : '//www.instagram.',
            'twitter' : '//twitter.',
            'pinterest' : '//www.pinterest.',
            'ello' : '//ello.',
            }

    # ------------------------------------------------
    # driver function ---
    # ------------------------------------------------
        
    def check_selenium_driver(self, driver):
        type_driver = str(type(driver)).lower()
        if 'selenium.webdriver.' in type_driver:
            time.sleep(1)
            driver.implicitly_wait(10)
            return True
        return False

                
    def setup_driver(self, driver=None, browser=None):
        time.sleep(1)
        self.runing_name = OPERATION_FORMAT.test_running_name()
        if self.check_selenium_driver(driver):
            self.driver = driver
            return self.driver
        else:
            if not browser:
                browser = self.default_browser
            self.current_browser = str(browser).lower()
#             from selenium import webdriver
            # https://www.seleniumhq.org/download/
            br = str(browser).lower()
            opts = False
            
            re_try = 9
            for i in range (0, re_try):
                try:
                    
                    if self.headless_mode:
                        opts = self.get_browser_options(br)
                    ext = ''
                    # try to build web driver

                    if self.use_inside_driver:
                        path_req = OPERATION_FILE.path_join(CONFIG_BASE.path_lib_xyTest, ['base', 'requirement', OPERATION_SYSTEM.platform])
                        if OPERATION_SYSTEM.platform == 'WINDOWS':
                            ext = '.exe'
                        if br in ['chrome']:
                            name_app = 'chromedriver' + ext
                            path_app = OPERATION_FILE.path_join(path_req, name_app)
    #                         print("executable_path=path_app) = ", path_app)
                            if opts:
                                self.driver = webdriver.Chrome(executable_path=path_app, chrome_options=opts)
                            else:
                                self.driver = webdriver.Chrome(executable_path=path_app)
      
                        elif br in ['firefox']:
                            # https://github.com/mozilla/geckodriver/releases
                            name_app = 'geckodriver' + ext
                            path_app = OPERATION_FILE.path_join(path_req, name_app)
    #                         print("executable_path=path_app) = ", path_app)
                            if opts:
                                self.driver = webdriver.Firefox(firefox_options=opts, executable_path=path_app)
                            else:
                                self.driver = webdriver.Firefox(executable_path=path_app)  
    #                     elif br in ['ie']:
    #                         name_app = 'IEDriverServer.exe'
    #                         path_app = OPERATION_FILE.path_join(path_req, name_app)
    #                         print("executable_path=path_app) = ", path_app)
    #                         self.driver = webdriver.Ie(path_app)
                        else:
                            self.driver = webdriver.Chrome(executable_path=path_app)
    
                    else:
                        if br in ['chrome']:
                            if opts:
                                self.driver = webdriver.Chrome(chrome_options=opts)
                            else:
                                self.driver = webdriver.Chrome()
    
                        elif br in ['firefox']:
                            if opts:
                                self.driver = webdriver.Firefox(firefox_options=opts)
                            else:
                                self.driver = webdriver.Firefox()
                        elif br in ['safari']:
                            if opts:
                                self.driver = webdriver.Safari()
                            else:
                                self.driver = webdriver.Safari()
                        else:
                            self.driver = webdriver.Chrome()

                except Exception as e:
                    self.message_command(self, "Report", "Retry - Not able to setup_driver - " + str(i), e)
                    pass
                
                if self.check_selenium_driver(self.driver):
                    return self.driver
                time.sleep(1)
            # end for
            self.message_command(self, "Error", "not able to set web driver re-try " + str(re_try))
            return False
        
        
    def get_browser_options(self, br):
        opts = None
#         from selenium import webdriver
        if br in ['chrome']:
            opts = webdriver.ChromeOptions()
        elif br in ['firefox']:
            from selenium.webdriver.firefox.options import Options
            opts = Options()
        else:
            self.message_command(self, "Warning", "Browser %s has no options." % str(br))
            return False
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")
        
        opts.add_argument('--disable-impl-side-painting')
        opts.add_argument('--disable-gpu-sandbox')
        opts.add_argument('--disable-dev-shm-usage')  # for docker
        
#         opts.add_argument('--window-size=1280x1696')
#         opts.add_argument('--hide-scrollbars')
#         opts.add_argument('--enable-logging')
#         opts.add_argument('--log-level=0')
#         opts.add_argument('--v=99')
#         opts.add_argument('--single-process')
#         opts.add_argument('--data-path=/tmp/data-path')
        opts.add_argument('--ignore-certificate-errors')
        
        return opts


    def get_home_page(self, url, nam=None):
        self.message_command(self, "Info", "Accessing " + url)
        try:
            if not self.headless_mode:
                self.driver.maximize_window()
        except:
            pass
        self.driver.get(url)
        time.sleep(5)
        
        if nam==None:
            self.message_command(self, "Report", "trying to open url="+url)
            return True
        else:
            return self.confirm(nam, "connect to %s " % (url), False)

    # start - home page
    def browser_open(self, url, nam='front'):
        if 'docker' in CONFIG_BASE.lst_env_status:
            # docker fix - retry browser
            for i in range (0,3):
                try:
                    if self.get_home_page(url, nam):
                        return True
                except Exception as e:
                    self.message_command(self, "Report", "try -%s- when open browser url %s" % (str(i), url), e)
                    pass
                self.driver = None
                OPERATION_SYSTEM.kill_browser()
                time.sleep(3)
                self.setup_driver(browser=self.current_browser)
        else:
            try:
                if self.get_home_page(url, nam):
                    return True
            except Exception as e:
                self.message_command(self, "Exception", "Error when open browser", e)
                pass

        self.message_command(self, "Error", "def browser_open - Failed to open url="+url)
        self.browser_close()
        return False
        
    def browser_close(self):
        if self.run_debug:
            return
        time.sleep(1)
        self.driver.quit()


    def go_back(self):
        self.driver.execute_script("window.history.go(-1)")
        # This is the best solution. The back() and forward() methods aren't guaranteed to work.


    # window.scrollBy(xnum, ynum)
    # self.driver.execute_script("window.scrollBy(0,500)")
    def mouse_scroll(self, xnum=0, ynum=500):
        cod = "window.scrollBy(%s,%s)" % (str(xnum), str(ynum))
        print ("code = ", cod)
        self.driver.execute_script(cod)
        time.sleep(2)


    # ------------------------------------------------
    # key action ---
    # ------------------------------------------------
    def act_list_key(self, lst_k):
        dic_key = {
            'space' : Keys.SPACE,
            'ad' : Keys.ARROW_DOWN,
            'enter' : Keys.ENTER,
            }
        actions = ActionChains(self.driver)
        if type(lst_k) == type([]):
            for e in lst_k:
                actions.send_keys(dic_key[e]).perform()
                time.sleep(1)
        else:
            actions.send_keys(dic_key[lst_k]).perform()
            time.sleep(1)


    #  CTRL + HOME keys.
    def page_top(self):
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(1)
        
    # ------------------------------------------------
    # element action ---
    # ------------------------------------------------

    def click_this_element(self, ele):
        if self.headless_mode:
            print ('Headless mode.  No element perform')
        else:
#             from selenium.webdriver.common.action_chains import ActionChains
            action_chains = ActionChains(self.driver).move_to_element_with_offset(ele, 5, 5)
            
#             action_chains = ActionChains(self.driver)
#             action_chains.move_to_element(ele).move_by_offset(5,5)
#             
            action_chains.click()
            action_chains.perform()


    def view_this_element(self, ele):
        if self.headless_mode:
            print ('Headless mode.  No scrollIntoView')
        else:
            self.driver.execute_script("return arguments[0].scrollIntoView();", ele)
#             self.driver.execute_script("return arguments[0].scrollIntoView(true);", ele)

    def moveto_this_element(self, ele):
        if self.headless_mode:
            print ('Headless mode.  No element perform')
        else:
#             from selenium.webdriver.common.action_chains import ActionChains
            fel = ActionChains(self.driver).move_to_element(ele)
            fel.perform()

    # find element and move on it
    def moveto_this_xpath(self, xpath):
        if xpath:
#             print ('xpath = ', xpath)
            eles = self.driver.find_elements_by_xpath(xpath)
            element = self.check_list_element(eles)
            if element:
                self.moveto_this_element(element)
                return element
        return False

    def get_parent_element(self, et):
        par = et.find_element_by_xpath('..')
        #  ../ syntax doesn't work,
        #  ./.. and ./../.. work as expected. 
        return par

    # ------------------------------------------------
    # Pass and View function ---
    # ------------------------------------------------

    # find max num element in the page and show in view
    # random elements in a page
    def navigation_list(self, lst, num=5):
        if len(lst) < num:
            num = len(lst)
#         for i in range (0, num-1):
        for i in range (0, num):
            self.view_this_element(lst[i])
            time.sleep(1)
        return True


    # check list title element, h2, h3
    # usually a list of title elements
    def along_detail(self, lst, tit="Detail"):
        time.sleep(2)
        len_title = len(lst)
        if len_title > 0:
            self.message_command(self, 'Report', "Find %d items in %s" % (len_title, tit))
            try:
                for itm in lst:
                    self.moveto_this_element(itm)
                    self.check_an_element(itm, 'Topic - '+ itm.text)
                    time.sleep(2)
            except:
                pass
        else:
            self.message_command(self, 'Report', "No items in " + tit)

    # ------------------------------------------------
    # general element function ---
    # ------------------------------------------------
    # element and activity - [get_key_element, get_key_field]
    # check list if not empty, return first element - [check_list_element]
    # ------------------------------------------------

    def confirm_an_element(self, ele):
#         print ("confirm_an_element = ", ele)
        try:
            e_e = self.get_element(ele, False)
#             print ("e_e = ", e_e)
            return e_e
        except:
            return False

    # get element by find_elements instead find_element  - to avoid exception
    # then return the first in list
    def check_list_element(self, lst):
        if type(lst) == type([]):
            le = len(lst)
            if le >0:
#                 if len(lst) > 1:
#                     self.message_command(self, "Info", "get %s elements" % str(le))
                return lst[0]
            else:
                self.message_command(self, "Error", "No element in list = %s" % str(lst))
                return False
        else:
            self.message_command(self, "Error", "get unknown elements = %s" % str(lst))
            return False


    def get_key_element(self, element, name='noname', click=True, w=None, rev=False, force=True):
#         print ("get element  = ", name)
        try:
            if not element:
                self.message_command(self, "Error", "Failed to get element = %s" % name)
                return False
            else:
#                 print ("%s.is_enabled() = " % name, element.is_enabled())
                if click:
                    if force:
                        if not element.is_enabled():
                            self.message_command(self, "Error", "element is not enable = %s" % name)
                            return False
                        else:     
                            if rev:
                                self.view_this_element(element)
                                self.get_time_sleep(w)
                            element.click()
#                             time.sleep(w)
                            self.get_time_sleep(w)
                    else:
                        try:
                            element.click()
#                             time.sleep(w)
                            self.get_time_sleep(w)
                        except:
                            pass
                return element
        except Exception as e:
            self.message_command(self, "Exception", "When get element = %s" % name , e)
            return False


    def get_key_field(self, element, name, key=None, w=None, rev=False):
#         print ("get field  = ", name)
        try:
            if not element:
                self.message_command(self, "Error", "Failed to get field = %s" % name)
                return False
            else:
#                 print ("%s.is_enabled() = " % nam, element.is_enabled())
                if key:
                    if not element.is_enabled():
                        self.message_command(self, "Error", "element is not enable = %s" % name)
                        return False
                    else:
                        if rev:
                            self.view_this_element(element)
                        element.clear()
                        element.send_keys(key)
        #                 has_value = element.get_attribute('value')
        #                 if not has_value == key:
        #                     element.send_keys(key)
#                         time.sleep(w)
                        self.get_time_sleep(w)
                        
                return element
        except Exception as e:
            self.message_command(self, "Exception", "When get field = %s" % name , e)
            return False


    # ------------------------------------------------
    #  find  element function ---
    # ------------------------------------------------
    #   click element by xpath - [click_this_xpath] - 
    #            sub - [get_maticon_button, get_text_span, get_text_type]
    #   input field  by xpath  - [input_this_xpath]
    #            sub - [get_place_field, get_name_field]
    #   search element by type and text [get_name_element] 
    #            sub-similar - [get_name_button, get_name_li_item, ] 
    # ------------------------------------------------

    # List
    def list_type_elements(self, tp):
        return self.driver.find_elements_by_tag_name(tp)
#         return self.driver.find_elements_by_tag_name('mat-chip')
    def list_xpath_elements(self, xp):
        return self.driver.find_elements_by_xpath(xp)
#         return self.driver.find_elements_by_xpath('//span/mat-icon[contains (text(), "cancel")]')

    def list_text_type(self, typ, txt):
        xp =('//%s[contains(.,"%s")]' % (typ, txt))
        return self.driver.find_elements_by_xpath(xp)
    
    # element 
    # search element by text (all or part)
    def search_element_type_text(self, typ, txt, click=True, w=None, rev=False, force=True):
        try:
            lst = self.driver.find_elements_by_tag_name(typ)
#             print ('len button = ', len(list_button))
            n = len(lst)
            for i in range(0, n):
                el = lst[n-1-i]
#             for el in list_button:
#                 print (el.text, "  len el.text= ", len(el.text) ) # add UPLOAD # add Add new piece
                if txt in el.text:
#                     print (name, "  len name = ", len(name) ) 
                    doele = self.get_key_element(el, txt, click, w, rev, force)
                    return doele
            self.message_command(self, "Error", "search_element_type_text - Could not element = %s - %s." % (typ, txt))
            return None
        except Exception as e:
            self.message_command(self, "Exception", "When get_name_element = %s - %s." % (typ, txt) , e)
            return None


    # element and click
    def click_this_xpath(self, xpath, click=True, w=None, rev=False, force=True):
        if xpath:
#             print ('xpath = ', xpath)
            eles = self.driver.find_elements_by_xpath(xpath)
#             print ("eles = ", len(eles))
            element = self.check_list_element(eles)
#             print ("element = ", element)
            if element:
                doele = self.get_key_element(element, xpath, click, w, rev, force)
#                 print ("doele = ", doele)
                return doele
        self.message_command(self, "Error", "When click_this_xpath = %s" % xpath)
        return False

    def search_text_type(self, typ, txt, click=True, w=None, rev=False, force=True):
        xp =('//%s[contains(.,"%s")]' % (typ, txt))
        return self.click_this_xpath(xp, click, w, rev, force)
    
    
    def get_name_type(self, typ, nam, click=True, w=None, rev=False, force=True):
        xp =('//%s[@name="%s"]' % (typ, nam))
        return self.click_this_xpath(xp, click, w, rev, force)
    
    def get_text_type(self, typ, txt, click=True, w=None, rev=False, force=True):
        xp = '//%s[contains(text(), "%s")]' % (typ, txt)
        return self.click_this_xpath(xp, click, w, rev, force)
    
    def get_maticon_button(self, name, click=True, w=None, rev=False, force=True):
        xp = '//button[span/mat-icon[contains(text(), "%s")]]' % name
        return self.click_this_xpath(xp, click, w, rev, force)

    def get_maticon_div(self, name, click=True, w=None, rev=False, force=True):
        xp = '//div[span[contains(text(), "%s")]]' % name
        return self.click_this_xpath(xp, click, w, rev, force)

    # field and input
    def input_this_xpath(self, xpath, name, key=None, w=None, rev=False):
        if xpath:
#             print ('xpath = ', xpath)
            eles = self.driver.find_elements_by_xpath(xpath)
            el = self.check_list_element(eles)
            if el:
                doele = self.get_key_field(el, name, key=key, w=w, rev=rev)
                return doele
        return False
    
    def get_dataplace_field(self, area, name, key=None, w=None, rev=False):
        xp = '//%s[@data-placeholder="%s"]' % (area, name)  #('//input[@placeholder="New password."]')
        return self.input_this_xpath(xp, name, key, w, rev)
    
    def get_place_field(self, area, name, key=None, w=None, rev=False):
        xp = '//%s[@placeholder="%s"]' % (area, name)  #('//input[@placeholder="New password."]')
        return self.input_this_xpath(xp, name, key, w, rev)

    def get_name_field(self, area, name, key=None, w=None, rev=False):
        xp = '//%s[@name="%s"]' % (area, name)  #('//input[@name="email"]')
        return self.input_this_xpath(xp, name, key, w, rev)


# - ------ will ignore - 
    # will ignore it
    def get_text_span(self, name, click=True, w=None, rev=False, force=True):
#         return self.get_text_type('span', name, click, w, rev, force)
        xp = '//span[contains(text(), "%s")]' % name
        return self.click_this_xpath(xp, click, w, rev, force)

    # search element by text (all or part)
    def get_name_element(self, typ, name, click=True, w=None, rev=False, force=True):
#         print ("typ , name = ", [typ, name])
        try:
            list_button = self.driver.find_elements_by_tag_name(typ)
#             print ('len get_name_element = ', len(list_button))
            n = len(list_button)
            for i in range(0, n):
                el = list_button[n-1-i]
#             for el in list_button:
#                 print (el.text, "  len el.text= ", len(el.text) ) # add UPLOAD # add Add new piece
                if name in el.text:
#                     print (name, "  len name = ", len(name) ) 
                    doele = self.get_key_element(el, name, click, w, rev, force)
                    return doele
            self.message_command(self, "Error", "Could not get_name_element = %s - %s." % (type, name))
        except Exception as e:
            self.message_command(self, "Exception", "When get_name_element = %s - %s." % (type, name) , e)


    def get_name_button(self, name, click=True, w=None, rev=False, force=True):
        return self.get_name_element('button', name, click, w, rev, force)

    def get_name_li_item(self, name, click=True, w=None, rev=False, force=True):
        return self.get_name_element('li', name, click, w, rev, force)
# - ------ will ignore - 



    # ------------------------------------------------
    # Monkey test function ---
    # ------------------------------------------------
    def get_random_xpath(self, xp, ind='all'):
        # get all link in the page
        elems = self.list_xpath_elements(xp)
        return OPERATION_FORMAT.index_random_in_list(elems, ind)

    def get_random_link(self, ind='all'):
        return self.get_random_xpath("//a[@href]", ind)

    def get_random_type(self, tp, ind='all'): 
        elems = self.list_type_elements(tp)
        return OPERATION_FORMAT.index_random_in_list(elems, ind)
    
    def get_visible_list(self, eles):
        lst = []
#         print ('list_all_eles = ', len(eles))
        for el in eles:
#             if el.is_enabled():
#             if el.is_selected():
            if el.is_displayed():
                lst.append(el)
#         print ('list_visible = ', len(lst))
        return lst


    def get_base_url_root(self, url):
        url_root = None
        new_url = str(url)
        if '//' in new_url:
            new_url = new_url.split('//')[1]
        
        lst_url = new_url.split('/')
#         print ('lst_url = ', lst_url)
        if len(lst_url[0]) > 9:
            url_root = lst_url[0][-9:]
        else:
            url_root = lst_url[0]
#         print ("url_root = ", url_root)
        return url_root
        
        
    def check_visibal_link(self, t=False):
        lst_link_out = ['print']
        if t:
            msg = None
            txt = str(t).lower()
            if 'mailto:' in txt:
                msg = ("Ignore email link = " + txt)
            else:
                for ch in lst_link_out:
                    if txt == ch:
                        msg = ("Ignore outside link = " + txt)
                        break
            if msg:
                self.message_command(self, "Report", msg)
                return False
        return True
    

    def do_a_go_clcik(self, e):
#         self.view_this_element(e)
        try:
            e.click()
        except:
            self.click_this_element(e)
        time.sleep(2)
        this_url = self.driver.current_url
        return this_url
    
    def do_a_back_clcik(self, e, url):
        this_url = self.do_a_go_clcik(e)
        self.driver.get(url)
        time.sleep(2)
        return this_url
        
    def raise_back_click_check(self, e, txt, msg, new_url, lst_target):
        new_lst = []
        this_url = new_url
        self.message_command(self, "Report", msg)
        if self.check_visibal_link(txt):
            this_url = self.do_a_back_clcik(e, new_url)
        will_add = (this_url != new_url) and (this_url not in lst_target)
        if will_add:
            new_lst.append(this_url)
        return new_lst

        
    def all_link_in_page(self, new_url):
        # get all link in the page
        lst_target = []
        self.driver.get(new_url)
        msg = "Check page = " + new_url
        self.message_command(self, "Report", msg)
        
        # link
        elems = self.get_random_link()
        num = len(elems)
        for i in range (1, num+1):
            e = self.get_random_link(i)
            txt = e.get_attribute("href")
            msg = ("link %d = %s" % (i, txt))
            lst_target += self.raise_back_click_check(e, txt, msg, new_url, lst_target)

        # button
        elems1 = self.get_random_type('button')
        num = len(elems1)
        msg = ("In page Button  = " + str(num))
        self.message_command(self, "Report", msg)
        for i in range (1, num+1):
            e1 = self.get_random_type('button', i)
            txt = e1.text.strip()
            msg = ("button %d = %s" % (i, txt))
            lst_target += self.raise_back_click_check(e1, txt, msg, new_url, lst_target)

        # and mat-icon 
        elems2 = self.get_random_type('mat-icon')
        num = len(elems2)
        msg = ("In page Mat-Icon  = " + str(num))
        self.message_command(self, "Report", msg)
        for i in range (1, num+1):
            e2 = self.get_random_type('mat-icon', i)
            txt = e2.text.strip()
            msg = ("icon %d = %s" % (i, txt))
            lst_target += self.raise_back_click_check(e2, txt, msg, new_url, lst_target)
#         print ('lst_target = ', lst_target)
        return lst_target


    def level_click_in_page(self, new_url, num=None):
        # get all link in the page
        if not num:
            num = 1
        msg = ("Total %d pages from = %s" % (num, new_url))
        self.message_command(self, "Report", msg)
        
        # make sure in this site
        base_url = self.get_base_url_root(new_url)
#         print ('base_url = ', base_url)
        this_url = new_url
        lst_checked = []
        
        for i in range(1, num+1):
            lst_target = self.all_link_in_page(this_url)
#             this_url = (self.driver.current_url)
            if not this_url in lst_checked:
                lst_checked.append(this_url)
            msg = ("Page %d = %s" % (i, this_url))
            self.message_command(self, "Report", msg)
            
            lst_choice = []
            for pg in lst_target:
                next_pg = (base_url in pg) and (not pg in lst_checked)
                if next_pg:
                    lst_choice.append(pg)
            
            if lst_choice == []:
                msg = "No more page to check.  Finish!"
                self.message_command(self, "Report", msg)
                break
            else:
                this_url = OPERATION_FORMAT.random_in_list(lst_choice, None)

        return True


    def random_click_button(self, new_url, num=None):
        # get all link in the page
        if not num:
            num = 10
        msg = ("Total %d click from = %s" % (num, new_url))
        self.message_command(self, "Report", msg)
        
        # make sure in this site
        base_url = self.get_base_url_root(new_url)
#         print ('base_url = ', base_url)
        backup_url = new_url
        self.driver.get(backup_url)
        time.sleep(2)

        for i in range(1, num+1):
            all_link = self.get_random_link('all')
            all_bt = self.get_random_type('button', 'all')
            all_icon = self.get_random_type('mat-icon', 'all')
#             all_span = self.get_random_type('span', 'all')
            
            bt_icon = self.get_visible_list(all_bt+all_icon+all_link)
#             bt_icon = all_bt+all_icon+all_link
            if len(bt_icon) > 1:
                el = OPERATION_FORMAT.index_random_in_list(bt_icon, None)
            else:
                msg = "click %d = %s" % (i, 'Nothing found.  back')
                self.message_command(self, "Report", msg)
                self.driver.get(backup_url)
                time.sleep(2)
                continue
            
            txt = el.text.strip()
            if txt.lower() in ['print', 'map', 'sign out', 'exit_to_appsign out']:
                msg = "ignore %d click  = %s." % (i, txt)
                self.message_command(self, "Report", msg)
                continue
                
            msg = "click %d = %s" % (i, txt)
            self.message_command(self, "Report", msg)
            backup_url = self.driver.current_url
            msg = ("Page %d = %s" % (i, backup_url))
            self.message_command(self, "Report", msg)
            this_url = self.do_a_go_clcik(el)

            if not base_url in this_url:
                msg = "click %d = %s" % (i, 'Seems outside site.  back')
                self.driver.get(backup_url)
                time.sleep(2)

            for ur in ['/#letmeknow']:
                if ur in this_url:
                    self.get_text_span('Cancel')
                    break

        return True




if __name__ == '__main__':
    
    CONFIG_BASE.dic_cmd['view'] = True
    CONFIG_BASE.session_browser = 'firefox'
    new_page = PageBase('main')
    new_page.setup_driver(browser='Firefox')
    env = 'qa'
    url = 'http://www.facebook.com/'
    new_page.browser_open(url)

# driver.forward()

# driver.back()
# driver.execute_script("window.history.go(-1)")

# # wait to make sure there are two windows open
# WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
# 
# # switch windows
# driver.switch_to_window(driver.window_handles[1])


# el = self.driver.find_element_by_xpath("//h1[contains(., 'This is my way')]")


# parent = child_element.find_element_by_xpath('..')
# # Just to add detail:
# # ../ syntax doesn't work, 
# # ./.. and ./../.. work as expected. Don't add the trailing slash.

# Find select option
# selected_option = driver.find_element_by_xpath('//option[@selected="selected"]')


# find buttons by their labels as follows:
#//button[.='OK']
# select only visible elements using XPath?
#//div[not(contains(@style,'display:none'))]//button[.='OK']


# element visiable
# visibility != hidden
# display != none (is also checked against every parent element)
# opacity != 0 (this is not checked for clicking an element)
# height and width are both > 0
# for an input, the attribute type != hidden

# for element in self.driver.find_elements_by_tag_name('img'):
#        print element.text
#        print element.tag_name
#        print element.parent
#        print element.location
#        print element.size

#         driver.find_element_by_xpath("//div[@class='fc-day-content' and text()='15']")

# get attributes
# current_tab_info = driver.find_elements_by_xpath("//div[@class='GMHeadMid']/table[@class='GMSection']/tbody/tr[@class='GMHeaderRow']/td/div/span")
# current_tab_header_list = [x.get_attribute('id') for x in current_tab_info]
