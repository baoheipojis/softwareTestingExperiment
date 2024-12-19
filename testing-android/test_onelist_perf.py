import time
import unittest
import pandas as pd
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = {
    "platformName": "Android",
    "deviceName": "192.168.3.29:5555",  # 根据设备名称修改
    "appPackage": "com.lolo.io.onelist",
    "appActivity": ".MainActivity",
    "automationName": "UiAutomator2",
    "language": 'en',
    "locale": 'US'
}


appium_server_url = 'http://localhost:4723'

class TestOneListPerformance(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()
    
    def add_list(self, list_name: str) -> None:
        """添加新列表"""
        add_button = self.driver.find_elements(By.XPATH, "//android.widget.Button")[2]
        add_button.click()

        # 输入新列表名称
        input_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText"))
        )
        input_box.send_keys(list_name)

        # 点击保存按钮
        save_button = self.driver.find_elements(By.XPATH, "//android.widget.Button")[1]
        save_button.click()
    
    def add_item(self, item_name: str) -> None:
        """添加todo项"""
        # 输入todo项名称
        input_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText"))
        )
        input_box.send_keys(item_name)

        # 点击保存按钮
        save_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText//child::android.widget.Button"))
        )
        save_button.click()
      
    def test_add_many_items(self):
        self.add_list("My Tasks")
        num_items = 200
        df_perf = pd.DataFrame(columns=['totalPrivateDirty', 'nativePrivateDirty', 'dalvikPrivateDirty', 'eglPrivateDirty', 'glPrivateDirty', 'totalPss', 'nativePss', 'dalvikPss', 'eglPss', 'glPss', 'nativeHeapAllocatedSize', 'nativeHeapSize', 'nativeRss', 'dalvikRss', 'totalRss'])
        for i in range(num_items):
            self.add_item(f"Task {i+1}")
            # 在添加10个、20个任务时追踪性能指标
            if (i + 1) % 10 == 0:
                memoryinfo = self.driver.get_performance_data('com.lolo.io.onelist', 'memoryinfo')
                new_row = {
                    'totalPrivateDirty': memoryinfo[1][0],
                    'nativePrivateDirty': memoryinfo[1][1],
                    'dalvikPrivateDirty': memoryinfo[1][2],
                    'eglPrivateDirty': memoryinfo[1][3],
                    'glPrivateDirty': memoryinfo[1][4],
                    'totalPss': memoryinfo[1][5],
                    'nativePss': memoryinfo[1][6],
                    'dalvikPss': memoryinfo[1][7],
                    'eglPss': memoryinfo[1][8],
                    'glPss': memoryinfo[1][9],
                    'nativeHeapAllocatedSize': memoryinfo[1][10],
                    'nativeHeapSize': memoryinfo[1][11],
                    'nativeRss': memoryinfo[1][12],
                    'dalvikRss': memoryinfo[1][13],
                    'totalRss': memoryinfo[1][14]
                }
                df_perf = pd.concat([df_perf, pd.DataFrame([new_row])], ignore_index=True)
        df_perf.to_csv('onelist_perf.csv', index=False)
                
if __name__ == '__main__':
    unittest.main()

