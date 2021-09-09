import os
import time
from xyTest.base.base_object import OBase
from xyTest.util.file_operation import OPERATION_FILE
from xyTest.util.format_operation import OPERATION_FORMAT

try:
    from appium.webdriver.common.touch_action import TouchAction
except:
    print ('PageBase could not find Appium.  Please install Appium before mobile app test')
    pass


class MobileBase(OBase):
    def __init__(self,
                 name=None,
                 *args, **kwargs):

        OBase.__init__(self,
                       name=name,
                       *args, **kwargs)

        self.driver = None
        self.set_mobilebase_constant()
        self.set_default_constant()
        
        self.sleep_second = 2

    # ------------------------------------------------
    # function for __init__ ---
    # ------------------------------------------------

    def set_mobilebase_constant(self):
        self.default_platform = 'iOS'
        
        self.dic_ele_type = {
            'bt' : 'XCUIElementTypeButton',
            'txt' : 'XCUIElementTypeStaticText',
            'img' : 'XCUIElementTypeImage',
            'lk' : 'XCUIElementTypeLink',

            'tf' : 'XCUIElementTypeTextField',
            'sf' : 'XCUIElementTypeSecureTextField',
            'tv' : 'XCUIElementTypeTextView',
            
            'cell' : 'XCUIElementTypeCell',
            'sv' : 'XCUIElementTypeScrollView',
            'cv' : 'XCUIElementTypeCollectionView',
            'tb' : 'XCUIElementTypeTable',
            
            'tab' : 'XCUIElementTypeTabBar',
            'bottom' : 'BottomBrowserToolbar',
            'navigation' : 'XCUIElementTypeNavigationBar',
            
            'other' : 'XCUIElementTypeOther',
            'window' : 'XCUIElementTypeWindow',
            }
        
    # ------------------------------------------------
    # driver function ---
    # ------------------------------------------------

    def setup_driver(self, driver):
        self.driver = driver

    # click many times
    def appium_touch_action(self, obj, x=5, y=5, mul=1):  # mul - how many times, default click once
#         from appium.webdriver.common.touch_action import TouchAction
        act = TouchAction(self.driver)
        act.tap(obj, x, y, mul)
#         act.tap(None, 150, 300, 4)  # click 4 times

#         x = obj.location['x'] + 5
#         y = obj.location['y'] + 5
        act.perform()
        time.sleep(1)


    def appium_touch_point(self, x=100, y=100, mul=1):  # mul - how many times, default click once
#         from appium.webdriver.common.touch_action import TouchAction
        act = TouchAction(self.driver)
#         act.tap(obj, x, y, mul)
        act.tap(None, x, y, mul)
        act.perform()
        time.sleep(1)
        
    def appium_touch_side(self, side='bottom',  x=5, y=5, mul=1):
        size = self.driver.get_window_size() 
        str_go = str(side).lower()
        startx = mid_x = int(size["width"]/2)
        starty = mid_y = int(size["height"]/2)
        
        if str_go in ['top']:
            startx = mid_x +x
            starty = y
        elif str_go in ['right']:
            startx = size["width"] -x
            starty = mid_y +y
        elif str_go in ['left']:
            startx = x
            starty = mid_y +y
        elif str_go in ['bottom']:
            startx = mid_x +x
            starty = size["height"] -y
        else: # elif str_go in ['center']:
            startx = mid_x +x
            starty = mid_y +y
        time.sleep(1)
        act = TouchAction(self.driver)
        act.tap(None, startx, starty, mul)
#         print ("appium_touch_side"*20)
        time.sleep(2)
        act.perform()

    
    # press and drop
    # example TouchAction().press(el0).moveTo(el1).release()
    def appium_drop(self, e1, e2):
        act = TouchAction(self.driver)
        act.press(e1).moveTo(e2).release()
        time.sleep(1)

    # press and wait 
    def appium_long_press(self, obj, duration=3000):
#         from appium.webdriver.common.touch_action import TouchAction
        act = TouchAction(self.driver)
        if obj==None:
            act.press(x=300, y=300).wait(duration).release().perform()
        else:
        #act.press(x=x, y=y).release().perform()
        #act.press(some_web_obj).wait(duration_in_millisec).release().perform()          # some_web_obj = driver.find...
            act.press(obj).wait(duration).release().perform()
        time.sleep(3)
        
        
    def appium_cross(self, startx, starty, endx, endy, due=1000):
        self.driver.swipe(startx, starty, endx, endy, due)
        time.sleep(1)
        
        
#     def appium_cross(self, startx, starty, endx, endy):
#         
#         from appium.webdriver.common.touch_action import TouchAction
#         act = TouchAction(self.driver)
#         act.press(startx, starty).moveTo(endx, endy).release()
#         
# #         act.press(el0).moveTo(el1).release()
#         act.perform()
#         time.sleep(1)
        
        
    def appium_scroll(self, el):
        self.driver.execute_script('mobile: scroll', {"element": el, "toVisible": True})
#         self.driver.execute_script("mobile: scroll", {"direction": 'down', 'element': el})

    def appium_swipe(self, going='down', duration=1000, few=False):
        size = self.driver.get_window_size() 
        str_go = str(going).lower()
        mid_x = int(size["width"]/2)
        up_y = int(size["height"] * 0.30)
        down_y = int(size["height"] *0.70) 
        
        left_x = int(size["width"]*0.15)
        right_x = int(size["width"]*0.85)
        mid_y = int(size["height"]/2)

        if few:
            up_y = int(size["height"] * 0.40)
            down_y = int(size["height"] *0.60) 
            
            left_x = int(size["width"]*0.35)
            right_x = int(size["width"]*0.65)
        
        if str_go in ['down']:
            starty = up_y
            startx = endx = mid_x
            endy = down_y
        elif str_go in ['right']:
            startx = left_x
            starty = endy = mid_y
            endx = right_x
        elif str_go in ['left']:
            startx = right_x
            starty = endy = mid_y
            endx = left_x
        else: # elif str_go in ['up']:
            starty = down_y
            startx = endx = mid_x
            endy = up_y
        time.sleep(1)
        self.driver.swipe(startx, starty, endx, endy, duration)
        time.sleep(2)


        
    def test_swipe(self):
        x = []
        while x == []: #Perform below till i get the desired item which i am looking for. In this case the item is in second page 
            x = self.driver.find_elements_by_name("Grid")
            if x == []: #Perform the scroll only if not able to locate the desired item in current screen
                size = self.driver.get_window_size() 
                starty = int(size["height"] * 0.80)
                endy = int(size["height"]*0.20) 
                startx = int(size["width"]/2)
                time.sleep(2)
                self.driver.swipe(startx, starty, startx, endy, 2000) #Swipe from bottom to top
                time.sleep(2)
            else:
                pass
            time.sleep(1)
            x[0].click()

    def appium_screenshot(self, pth=None):
        right_pth = str(pth)
        try:
            if pth==None:
                fn = "%s_%s_%s" % ('screenshot', OPERATION_FORMAT.get_name_date_all(), '.png')
                right_pth = OPERATION_FILE.path_join(OPERATION_FILE.path_user_documents, [fn])
#             print ("right_pth = ", right_pth)
            self.driver.save_screenshot(right_pth)
            self.message_command(self, "Report", "Save appium_screenshot to - " + right_pth)
        except Exception as e:
            self.message_command(self, "Report", "Not able to Save appium_screenshot to - " + right_pth, e)
            pass   



    def app_reset(self):
        try:
            self.driver.reset()
            time.sleep(3)
        except Exception as e:
            self.message_command(self, "Report", "def app_reset-", e)
            pass

    def app_close(self):
        try:
            self.driver.close_app()
            time.sleep(3)
        except Exception as e:
            self.message_command(self, "Report", "def app_quit-", e)
            pass   
        
        
    def app_quit(self):
        try:
            self.driver.quit()
            time.sleep(3)
        except Exception as e:
            self.message_command(self, "Report", "def app_quit-", e)
            pass
        
    # ------------------------------------------------
    # general element function ---
    # ------------------------------------------------
    # element and activity - [get_key_element, get_key_field]
    # get element with xpath then activity - [get_xpath_element, get_xpath_field] - usually with for loop
    # ------------------------------------------------
    
    def get_key_element(self, element, name='noname', click=True, w=None):
#         print ("get element  = ", name)
        try:
            if not element:
                self.message_command(self, "Error", "get_key_element - Not able to get element = %s" % name)
                return False
            else:
                if click:
                    element.click()
                    self.get_time_sleep(w)
#                     time.sleep(w)
                return element
        except Exception as e:
            self.message_command(self, "Exception", "When get element = %s" % name , e)
            return False

    def get_key_field(self, element, name, key=None, w=None):
#         print ("get field  = ", name)
        try:
            if not element:
                self.message_command(self, "Error", "Failed get_key_field = %s" % name)
                return False
            else:
                if key:
                    try:
                        element.clear()
#                         element.getAttribute("value")
                    except:
                        pass
                    element.send_keys(key)
                    self.get_time_sleep(w)
#                     time.sleep(w)
                return element
        except Exception as e:
            self.message_command(self, "Exception", "When get_key_field = %s" % name , e)
            return False
        
    def try_xpath(self, xpath, par=None):
        element = False
        try:
            if xpath:
    #             print ('xpath = ', xpath)
                if par:
                    element = par.find_element_by_xpath(xpath)
                else:
                    element = self.driver.find_element_by_xpath(xpath)
            else:
                self.message_command(self, "Report", "Unknow xpath = " + str(xpath))
            return element
        except:
            pass
            self.message_command(self, "Report", "except - xpath = " + str(xpath))
            return False
        

    def check_list_elements(self, lst, msg, name, click=True, w=None):
        if len(lst) > 0:
            doele = self.get_key_element(lst[0], name, click, w)
            return doele
        else:
            self.message_command(self, "Report", msg)
            return False
        
    def check_list_fields(self, lst, msg, name, key=None, w=None):
        if len(lst) > 0:
            doele = self.get_key_field(lst[0], name, key, w)
            return doele
        else:
            self.message_command(self, "Report", msg)
            return False


    def get_xpath_element(self, xpath, click=True, w=None, par=None):
        elements = []
        if xpath:
#             print ('xpath = ', xpath)
            if par:
                elements = par.find_elements_by_xpath(xpath)
            else:
                elements = self.driver.find_elements_by_xpath(xpath)
#         print ("get_xpath_element = ", elements)
        msg = "not able to find element When get_xpath_element = %s" % str(xpath)
        return self.check_list_elements(elements, msg, str(xpath), click, w)

##################################################################
#         ele = self.try_xpath(xpath, par)
#         if ele:
#             doele = self.get_key_element(ele, str(xpath), click, w)
#             return doele
#         else:
#             msg = "not able to find element When get_xpath_element = %s" % str(xpath)
#             self.message_command(self, "Report", msg)
#             return False
##################################################################

    def get_xpath_field(self, xpath, key=None, w=None, par=None):
        elements = []
        if xpath:
#             print ('xpath = ', xpath)
            if par:
                elements = par.find_elements_by_xpath(xpath)
            else:
                elements = self.driver.find_elements_by_xpath(xpath)
#         print ("get_xpath_element = ", elements)
        msg = "not able to find field When get_xpath_element = %s" % str(xpath)
        return self.check_list_fields(elements, msg, str(xpath), key, w)
    
##################################################################
#         ele = self.try_xpath(xpath, par)
#         if ele:
#             doele = self.get_key_field(ele, str(xpath), key, w)
#             return doele
#         else:
#             msg = "not able to find field When get_xpath_element = %s" % str(xpath)
#             self.message_command(self, "Report", msg)
#             return False
##################################################################

    def get_name_of_element(self, el):
        txt = None
        txt_new = el.text
        if OPERATION_FILE.is_true(txt_new):
            txt = str(txt_new)
        else:
            txt = el.get_attribute('name')
        return txt
    
    def get_parent_element(self, et, deep=1):
        # get parent of an element
#         print ("et = ", et) 
        nam = et.get_attribute("name")
#         print ("name = ", nam)
        xph = '//*[@name= "' + nam + '"]' + '/..'*deep  #  level deep 
#         print ('xph = ', xph)
        par = self.driver.find_elements_by_xpath(xph)
#         print ("par = ", par)
        return par
#         par = self.driver.find_element_by_xpath('//*[@name= "' + nam + '"]/..')
#         grand_par = self.driver.find_element_by_xpath('//*[@name= "' + nam + '"]/../..')


    def get_navigation_name(self):
        lst_bar = self.driver.find_elements_by_class_name(self.dic_ele_type['navigation'])
        if lst_bar:
#             print (".get_attribute('wdName') = ", lst_bar[0].get_attribute('wdName'))  # =  Frames
#             print (".get_attribute('name') = ", lst_bar[0].get_attribute('name')) #  =  Frames
#             print (".tag_name = ", lst_bar[0].tag_name) # .tag_name =  XCUIElementTypeNavigationBar
            return lst_bar[0].get_attribute('name')
        else:
            return None
        
    # ------------------------------------------------
    # get element function ---
    # ------------------------------------------------
    # get element by name of its child - [get_parent_type_name]
    #         - similar [get_cell_staticText, get_other_staticText, get_field_staticText]
    # get element by type and name - [get_name_type_element, get_name_type_field] - similar [get_name_button]
    # search - one(first if more) element - by type and att [find_type_element, ]
    # search - one(first if more) element - by type - [typeSearch]  - sub - [textField, secureField, textView]
    # search - one(first if more) element - by text [search_text_in_static, ]
    # list - get type list [list_type_elements] - similar [list_visible_xpath, list_visible_type]
    # index [cell_in_view] 
    # ------------------------------------------------

    # get first parent element, from type list with the name of the last child.  
    def get_parent_type_name(self, name, lst=['cell','txt'], click=True, w=None):
        num = len(lst)
        if num < 1:
            self.message_command(self, 'Error', "No type in list - " + str(lst))
            return False
        elif num == 1:
            typ = self.dic_ele_type[lst[0]]
            xp = '//%s[@name="%s"]' % (typ, name)
        else:
            typ = self.dic_ele_type[lst[0]]
            xp = '//%s[@name="%s"]' % (typ, name)

            xp = '//%s[' % (typ)
            ls = []
            for i in range (1, num):
                ls.append(self.dic_ele_type[lst[i]])
            xp += '/'.join(ls)
            xp += '[@name="%s"]]' % (name)
        
#         print ("get_parent_type_name = ", xp)
        return self.get_xpath_element(xp, click, w)


    def get_cell_staticText(self, name, click=True, w=None):
        xp = '//XCUIElementTypeCell[XCUIElementTypeStaticText[@name="%s"]]' % (name)
        return self.get_xpath_element(xp, click, w)

    def get_field_staticText(self, name, key=None, w=None):
        cel = self.get_cell_staticText(name, False)
        elements = cel.find_elements_by_class_name('XCUIElementTypeTextField')
        msg = "not able to find field With staticText = %s" % str(name)
        return self.check_list_fields(elements, msg, name, key, w)

    def get_other_staticText(self, name, click=True, w=None):
        xp = '//XCUIElementTypeOther[XCUIElementTypeStaticText[@name="%s"]]' % (name)
#         print ('get_other_staticText = ', xp)
        return self.get_xpath_element(xp, click, w)
    
    
    def get_name_type_element(self, name, typ, click=True, w=None, par=None):
        xp = '//%s[@name="%s"]' % (typ, name)
        return self.get_xpath_element(xp, click, w, par)

    
    def get_name_type_field(self, name, typ, key=None, w=None, par=None):
        xp = '//%s[@name="%s"]' % (typ, name)
        return self.get_xpath_field(xp, key, w, par)
    
    
    def get_name_button(self, name, click=True, w=None, par=None):
        xp = '//XCUIElementTypeButton[@name="%s"]' % (name)
#         print ('button xpath = ', xp)
        return self.get_xpath_element(xp, click, w, par)


    def find_type_element(self, typ, name, par=None, att="name"):
        elements = []
        xp = '//%s[@%s="%s"]' % (typ, att, name)
        if par:
            elements = par.find_elements_by_xpath(xp)
        else:
            elements = self.driver.find_elements_by_xpath(xp)
#         print ("get_xpath_element = ", elements)
        msg = "not able to find element When get_xpath_element = %s" % str(xp)
        if len(elements) > 0:
            return elements[0]
        else:
            self.message_command(self, "Report", msg)
            return False
        

    def typeSearch(self, tp, par=False):
        if par:
            ls= par.find_elements_by_class_name(tp)
        else:
            ls= self.driver.find_elements_by_class_name(tp)
        if ls ==[]:
            return False
        else:
            return ls[0]

    def textField(self, par=False):
        return self.typeSearch("XCUIElementTypeTextField", par)

    def secureField(self, par=False):
        return self.typeSearch("XCUIElementTypeSecureTextField", par)

    def textView(self, par=False):
        return self.typeSearch("XCUIElementTypeTextView", par)
    
        
    # search text in XCUIElementTypeStaticText, return first element or list of element
    def search_text_in_static(self, txt, all=False):
        result = []
        try:
            texts = self.driver.find_elements_by_class_name('XCUIElementTypeStaticText')
#             print ("len - tests = ", len(texts))
            for et in texts:
                this_text = et.text
#                 print (this_text)
                if txt in this_text:
                    if all:
                        result.append(et)
                    else:
                        return et
            if result == []:
                return None
            else:
                return result
        except Exception as e:
            self.message_command(self, "Exception", "When search_text_in_static = %s" % txt , e)
            return False

    def get_visible_list(self, eles):
        if not eles:
            return eles
        lst = []
#         print ('list_all_eles = ', len(eles))
        for el in eles:
#             if el.is_enabled():
#             if el.is_selected():
            if el.is_displayed():
                lst.append(el)
#         print ('list_visible = ', len(lst))
        return lst

    def list_visible_type(self, tp):
        typ = self.dic_ele_type[tp]
        if tp in ['img']:
            als = self.driver.find_elements_by_xpath('//*[@type= "' + typ + '"]/..')
        else:
            als = self.driver.find_elements_by_class_name(typ)
        return self.get_visible_list(als)
    
    def list_visible_xpath(self, xp):
        als = self.driver.find_elements_by_xpath(xp)
        return self.get_visible_list(als)
    
    
    def list_type_elements(self, tp, par=None):
        typ = self.dic_ele_type[tp]
        if par:
            return par.find_elements_by_class_name(typ)
        else:
            return self.driver.find_elements_by_class_name(typ)
        
    # return one cell in a collection view
    def cell_in_view(self, iv=None, ic=None):  # index of view, index of cell
        # find view
        views = self.list_type_elements('cv') #self.listCollectionViews()
#         print ("len - views = ", len(views))
        if views == []:
            self.message_command(self, "Report", "No Views in page.")
            return False
#         elif len(views) == 1:
#             iv = 0
#         print ("iv = ", iv)
        vie = OPERATION_FORMAT.index_random_in_list(views, iv)
        cells = self.list_type_elements('cell', vie) 
#         print ("len - cells = ", len(cells))
        if cells == []:
            self.message_command(self, "Report", "No cells in view.")
            return False
#         print ("ic= ", ic)
        return OPERATION_FORMAT.index_random_in_list(cells, ic)

    # ------------------------------------------------
    # confirm function ---
    # ------------------------------------------------

    def confirm_an_element(self, ele):
        try:
            if type(ele) == type(''):
                result = self.get_element(ele, False)
            elif 'appium.webdriver.webelement' in str(type(ele)):
                result = ele
            elif type(ele) == type([]):
                result = True
                for itm in ele:
                    result = result and self.confirm_an_element(itm)
            else:
                result = False
            return result
        except:
            return False

    # ------------------------------------------------
    # bottom menu function ---
    # ------------------------------------------------

    def menu_browser(self, li='back'):
#         #["back" , "Forward" , "Share" , "Show Bookmarks" , "Tabs"]
        menu = self.driver.find_elements_by_xpath('//BottomBrowserToolbar[@name="BottomBrowserToolbar"]')
        return self.get_name_type_element(name=li, typ='XCUIElementTypeButton', w=None, par=menu)



if __name__ == '__main__':
    new_page = MobileBase('main')
    print ("MobileBase = ", new_page)
    
#     print ("driver.contexts =", self.driver.contexts) 
#     print ("driver.page_source = ",  self.driver.page_source)
#         print ("element ..size = ", element.size)  # ..size =  {'height': 21, 'width': 118}
#         print ("element ..location = ", element.location)  # ..location =  {'x': 128, 'y': 201}

# # You can use below method
# # starts-with()
# # ends-with()
# # contains()
#             for itm in lst_in_items:
#                 xpath = "//XCUIElementTypeSwitch[starts-with(@name, \""+itm+"\")]"
#                 e = self.new_page.get_xpath_element(xpath)
#                 print ("e = ", e)

# element.get_attribute("value")

# (write this in terminal):
# defaults write com.apple.iphonesimulator ConnectHardwareKeyboard -bool false

# Element attribute names are: (
#     UID,
#     accessibilityContainer,
#     accessible,
#     enabled,
#     frame,
#     label,
#     name,
#     rect,
#     type,
#     value,
#     visible,
#     wdAccessibilityContainer,
#     wdAccessible,
#     wdEnabled,
#     wdFrame,
#     wdLabel,
#     wdName,
#     wdRect,
#     wdType,
#     wdUID,
#     wdValue,
#     wdVisible
# )