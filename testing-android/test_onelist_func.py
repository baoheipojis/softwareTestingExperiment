import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

capabilities = {
    "platformName": "Android",
    "deviceName": "Android",  # 根据设备名称修改
    "appPackage": "com.lolo.io.onelist",
    "appActivity": ".MainActivity",
    "automationName": "UiAutomator2",
    "language": 'en',
    "locale": 'US'
}


appium_server_url = 'http://localhost:4723'

class TestOneList(unittest.TestCase):
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
        input_box = self.driver.find_element(By.XPATH, "//android.widget.EditText")
        input_box.send_keys(item_name)

        # 点击保存按钮
        save_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.EditText//child::android.widget.Button"))
        )
        save_button.click()
    
    def delete_item(self, item_name: str) -> None:
        """删除todo项"""
        # 定位要删除的todo项
        item = self.driver.find_element(By.XPATH, f"//android.widget.TextView[@text='{item_name}']")
        # 滑动 item 删除
        bounds = item.rect
        start_x = bounds['x'] + bounds['width'] - 50
        start_y = bounds['y'] + bounds['height'] // 2
        end_x = bounds['x'] + 50
        end_y = start_y
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        
    def edit_item(self, item_name: str, new_name: str) -> None:
        """编辑todo项"""
        # TODO: 请补充完整测试代码

        # 点击要编辑的todo项
        item = self.driver.find_element(By.XPATH, f"//android.widget.TextView[@text='{item_name}']")
        # 滑动 item 编辑，从左向右
        bounds = item.rect
        start_x = bounds['x'] + 50
        start_y = bounds['y'] + bounds['height'] // 2
        end_x = bounds['x'] + bounds['width'] - 50
        end_y = start_y
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        # 清除旧名称并输入新名称
        input_box = self.driver.find_element(By.XPATH, "//android.widget.EditText")
        input_box.clear()
        input_box.send_keys(new_name)

        # 点击保存按钮
        save_button = self.driver.find_elements(By.XPATH, "//android.widget.Button")[1]
        save_button.click()



    # def test_switch_lists(self) -> None:
    #     """测试切换列表"""
    #     # 定位并点击"TODO"列表
    #     tutorial_list = self.driver.find_element(By.XPATH, "//*[ends-with(@text, 'TODO')]")
    #     tutorial_list.click()
    #     # 等待"TODO"列表出现
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//android.widget.TextView[starts-with(@text, 'Enjoy')]"))
    #     )
    #     # 定位并点击"Tutorial"列表
    #     tutorial_list = self.driver.find_element(By.XPATH, "//*[ends-with(@text, 'Tutorial')]")
    #     tutorial_list.click()

    #     # 验证是否成功切换
    #     assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='Switch lists by clicking on them']")
        
    # def test_add_list(self) -> None:
    #     """测试添加新列表"""
    #     self.add_list("New List")
    #     # 验证新列表是否创建成功
    #     assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='New List']")
        
    def edit_delete_list(self) -> None:
        """测试编辑和删除列表"""
        # TODO: 请补充完整测试代码
        self.add_list("New List")
        self.edit_item("New List", "Updated List")
        assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='Updated List']")
        self.delete_item("Updated List")
        assert not self.driver.find_elements(By.XPATH, "//android.widget.TextView[@text='Updated List']")
    
    # def test_add_delete_item(self) -> None:
    #     """测试添加todo项"""
    #     self.add_item("New Item")
    #     assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='New Item']")
    #     self.delete_item("New Item")
    #     assert not self.driver.find_elements(By.XPATH, "//android.widget.TextView[@text='New Item']")
        
    
    # def test_edit_item(self) -> None:
    #     """测试编辑todo项"""
    #     # TODO: 请补充完整测试代码
    #     self.add_item("New Item")
    #     self.edit_item("New Item", "Updated Item")
    #     assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='Updated Item']")
    #     self.delete_item("Updated Item")
    #     assert not self.driver.find_elements(By.XPATH, "//android.widget.TextView[@text='Updated Item']")
        
    def test_release_note(self) -> None:
        """测试查看设置中的版本信息"""
        # TODO: 请补充完整测试代码
        # 定位设置按钮
        setting_button = self.driver.find_elements(By.XPATH, "//android.widget.Button")[0]
        setting_button.click()
        # 定位版本信息
        list = self.driver.find_element(By.XPATH, "//*[ends-with(@text, 'note')]")
        list.click()
        # 验证是否成功切换
        assert self.driver.find_element(By.XPATH, "//android.widget.TextView[@text='1List has been updated.']")
        

if __name__ == '__main__':
    unittest.main()

