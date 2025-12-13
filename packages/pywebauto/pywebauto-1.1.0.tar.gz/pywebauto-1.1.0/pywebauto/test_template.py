# python内置库
import os
from datetime import datetime
from time import sleep
from typing import Union    # 额外用到的内置python库，只要是下了python就内置的了
# 官方的的第三方库
import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    ElementNotInteractableException # 添加多了一些异常
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="function")
def driver():
    service = Service(
        executable_path="C:\\Users\\86153\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")
        # executable_path=r"C:\Users\yandifei\.cache\selenium\chromedriver\win64\141.0.7390.122\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("网址")
    driver.maximize_window()
    yield driver
    driver.quit()


class TestTemplate: # 这个名字也得改

    # test-code-start

    # R001需求测试
    @pytest.mark.parametrize("参数1, 参数2, screen_name", [
        # 截图会自动追加上时间戳，截图名严格按照需求文档写
        ("参数1数据", "参数2数据", "Template_R001_001.png"),
        ("参数1数据", "参数2数据", "Template_R001_002.png"),
        ("参数1数据", "参数2数据", "Template_R001_003.png"),
        ("参数1数据", "参数2数据", "Template_R001_004.png"),
    ])
    def test_Template_R001(self, driver, 参数1, 参数2, screen_name):
        # 初始化
        self.driver = driver  # 驱动
        self.actions = ActionChains(driver)  # 动作链

        # 开始业务逻辑
        sleep(2)    # 界面响应需要时间

        # 等待5秒后截图
        sleep(5)
        # 调用截图方法，保存当前页面，并使用参数中指定的文件名
        self.take_screenshot(driver, screen_name)

        # 驱动
        driver: webdriver.Chrome

        # 定位策略
        by_mapping: dict = {
            1: By.CSS_SELECTOR,  # CSS选择器，灵活、性能最佳
            2: By.ID,  # 最快速，但是ID有可能会变（如果确认ID就不管了）
            3: By.XPATH,  # 可能会变位置，
            4: By.NAME,  # 表单元素的名称，除表单外不一定有
            5: By.CLASS_NAME,  # 样式类
            6: By.LINK_TEXT,  # 精确的链接文本
            7: By.PARTIAL_LINK_TEXT,  # 模糊链接文本
            8: By.TAG_NAME,  # 标签名
        }

        # 行为
        actions: ActionChains

        """元素查找、改变（包括元素属性查找）"""

    def wait_element_appear(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """等待元素出现，肉眼可见且存在DOM（有些元素不可见或无法交互不能使用该方法）
        参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value: 需要寻找元素的by方法的值
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 最大等待时间内寻找到元素返回元素否则返回False

        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            return element  # 返回找到的元素
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false

    def wait_elements_appear(self, by_value: str, mode: int = 1, timeout: int = 10):
        """等待所有元素出现，肉眼可见且存在DOM（有些元素不可见或无法交互不能使用该方法）
        参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value: 需要寻找元素的by方法的值
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 最大等待时间内寻找到元素返回该元素的数组否则返回False

        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_all_elements_located((self.by_mapping[mode], by_value))
            )
            return element  # 返回找到的元素数组
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false

    def wait_element_be_click(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """等待元素可以被点击，肉眼可见且存在DOM（有些元素不可见或无法交互不能使用该方法）
        参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value: 需要寻找元素的by方法的值
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 最大等待时间内寻找到元素返回True否则返回False

        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
            return element  # 返回找到的元素
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false

    def wait_class_change(self, by_value: str, class_value: str, mode: int = 1, timeout: int = 10) -> bool:
        """
        检测元素样式是否改变，如果中途元素本身改变也视为css发生了变化。灵活配置定位策略和等待时间
        :param class_value: class改变后属性值（例如："video-like video-toolbar-left-item on"）
        :param by_value: 定位符
        :param mode: 定位策略
        :param timeout: 最大等待时间（秒）
        :return: 样式改变返回 True，否则返回 False
        """
        try:
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 lambda 表达式作为自定义条件
            web_driver_wait.until(
                lambda driver: driver.find_element(self.by_mapping[mode], by_value).get_attribute(
                    "class") != class_value
            )
            return True
        except TimeoutException:
            return False
        except (NoSuchElementException, StaleElementReferenceException):
            # 如果元素在等待过程中消失，也认为状态已改变
            return True

    # 释放所有行为的方法
    def release_actions(self) -> bool:
        """
        释放所有行为，在鼠标按住和键盘按住等场景可以用
        :return:True
        """
        # 创建ActionBuilder对象并释放掉所有行为
        ActionBuilder(self.driver).clear_actions()
        return True

    """鼠标事件"""

    def click(self, by_value: str, mode: int = 1) -> Union[WebElement, bool]:
        """
        二次封装selenium的click方法（捕获错误），自定义捕获策略

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略，默认为3
        :return:执行成功返回被点击元素，没有元素返回false

        """
        try:
            element = self.driver.find_element(self.by_mapping[mode], by_value)  # 找到元素
            element.click()  # 点击元素
            return element
        except NoSuchElementException:
            # 找不到元素异常
            return False

    def wait_click_ex(self, by_value: str, index: int, click_mode: int = 1, mode: int = 1, timeout: int = 10) -> \
            Union[WebElement, bool]:
        """
        搜索所有元素并指定某个元素，等待元素出现并点击（selenium的click），参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param index:元素下标
        :param click_mode:点击方式，默认1，2为js点击
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象，未找到元素（超时）返回false
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 确保至少存在一个元素
            web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
                # expected_conditions.visibility_of_all_elements_located((self.by_mapping[mode], by_value))
            )
            # 确保元素找到
            element = self.driver.find_elements((self.by_mapping[mode], by_value))[index]
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # # 滚动视窗到该元素上()click自带了
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # 如果点击模式为1则默认selenium的点击否则为js点击
        element.click() if click_mode == 1 else self.driver.execute_script("arguments[0].click();", element)  # 点击元素
        return element  # 返回找到的元素

    def js_click(self, by_value: str, mode: int = 1) -> Union[WebElement, bool]:
        """
        点击（js注入的方式实现），出现遮罩无法点击的情况（在B站被ban了）,自定义定位模式

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略，默认3
        :return:执行成功返回被点击元素，没有元素返回false
        """
        try:
            element = self.driver.find_element(self.by_mapping[mode], by_value)  # 找到元素
            self.driver.execute_script("arguments[0].click();", element)  # 点击元素
            return element
        except NoSuchElementException:
            # 找不到元素异常
            return False

    def wait_click(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """
        等待元素出现并点击（selenium的click），参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象，未找到元素（超时）返回false
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            element = web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # # 滚动视窗到该元素上()click自带了
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()  # 点击
        return element  # 返回找到的元素

    def wait_js_click(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """
        等待元素出现并点击（js注入的方式），自定义定位策略和时间，对象额外开销
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象，未找到元素（超时）返回false
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 until() 方法和 EC.presence_of_element_located 条件(元素出现且能被点击)
            element = web_driver_wait.until(
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # 滚动视窗到该元素上
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # 点击
        self.driver.execute_script("arguments[0].click();", element)
        return element  # 返回找到的元素

    def wait_double_click(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """
        等待元素出现并点击（selenium的click）,灵活控制

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象，未找到元素（超时）返回false
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 until() 方法和 EC.presence_of_element_located 条件(元素出现在 DOM 结构中，但不一定可见)
            element = web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))

            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # 滚动视窗到该元素上
        # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        # 双击
        ActionChains(self.driver).double_click(element).perform()
        return element  # 返回找到的元素

    def wait_hold(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """
        等待元素出现并按住（selenium的click），参数直接自定义搜索策略和等待时间更加灵活，但是对象开销也会大

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode:定位策略
        :param timeout: 元素出现最大等待时间（默认10）
        :return:执行成功返回元素对象，未找到元素（超时）返回false
        """
        try:
            # 创建 WebDriverWait 实例，设置最大等待时间
            web_driver_wait = WebDriverWait(self.driver, timeout)
            element = web_driver_wait.until(
                # 确保元素可见且能被点击
                expected_conditions.element_to_be_clickable((self.by_mapping[mode], by_value))
            )
        except TimeoutException:  # 捕获超时异常
            return False  # 直接返回false
        # 按住
        self.actions.click_and_hold(element).perform()
        return element  # 返回找到的元素

    """键盘事件"""

    def clear_key(self, by_value: str, mode: int = 1, timeout: int = 10) -> Union[WebElement, bool]:
        """
        设定时间内等待元素出现点击后清空内容

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param by_value:定位符
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 执行成功返回被点击元素，(没有找到、无法接收输入、状态变化)返回false
        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            element.click()  # 点击元素
            element.clear()
            return element
        except (ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException,
                TimeoutException):
            return False  # 失败异常

    def send_key(self, keys_to_send: str, by_value: str, mode: int = 1, timeout: int = 10) -> Union[
        WebElement, bool]:
        """
        设定时间内等待元素出现点击后输入多个字符(键盘的值或文本)，自定义超时时间和搜索策略

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param keys_to_send:一个或多个字符串
        :param by_value:定位符
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 执行成功返回被点击元素，(没有找到、无法接收输入、状态变化)返回false
        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            element.click()  # 点击元素
            self.actions.send_keys(keys_to_send).perform()  # 执行输入行为
            return element
        except (ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException,
                TimeoutException):
            return False  # 失败异常

    def rewrite_key(self, keys_to_send: str, by_value: str, mode: int = 1, timeout: int = 10) -> Union[
        WebElement, bool]:
        """
        设定时间内等待元素出现点击后清空字符并输入多个字符(键盘的值或文本)，自定义超时时间和搜索策略

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param keys_to_send:一个或多个字符串
        :param by_value:定位符
        :param mode: 搜索模式（by_mapping），默认3
        :param timeout: 最大等待时间（默认10）
        :return: 执行成功返回被点击元素，(没有找到、无法接收输入、状态变化)返回false
        """
        try:
            # 创建显式等待对象
            web_driver_wait = WebDriverWait(self.driver, timeout)  # 使用默认值为10
            # 0.5秒监测元素出现
            element = web_driver_wait.until(
                # 元素可见但不一定能被点击
                expected_conditions.visibility_of_element_located((self.by_mapping[mode], by_value))
            )
            # self.actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform() # 行为链
            element.clear()  # 清除元素文本，这个直接向元素发出的操作和焦点无关
            self.actions.send_keys(keys_to_send).perform()  # 执行输入行为
            return element
        except (ElementNotInteractableException, StaleElementReferenceException, NoSuchElementException,
                TimeoutException):
            return False  # 失败异常

    """窗口控制类型"""

    def wait_win(self, win_num: int, timeout: int = 5) -> bool:
        """
        在指定时间内等待新窗口出现，等待时间自定义
        :param win_num: 原来窗口的数量（新开窗口前保存这个值），len(driver.window_handles)
        :param timeout: 最大等待时间（秒，默认为 5）
        :return: 最大时间内出现新窗口返回 True，超时返回 False
        """
        try:
            # 创建 WebDriverWait 实例
            web_driver_wait = WebDriverWait(self.driver, timeout)
            # 使用 lambda 表达式作为自定义条件：
            web_driver_wait.until(
                lambda driver: len(driver.window_handles) >= win_num
            )
            return True
        except TimeoutException:
            # 如果超过 timeout 时间窗口数量仍不足 2
            return False

    def switch_win(self, title: str, url: str, by_value: str, mode: int = 3) -> bool:
        """
        多重条件判定标签（窗口跳转成功），符合标题、url、存在特定元素才判定为跳转成功。
        须确保网页元素加载完成，因为判定条件是特定元素存在

        1: By.CSS_SELECTOR      - 性能好，写法灵活，推荐
        2: By.ID                - 性能最佳，元素唯一时首选
        3: By.XPATH             - 功能强大，可遍历DOM，但性能相对较差
        4: By.NAME              - 主要用于表单元素
        5: By.CLASS_NAME        - 按CSS类名定位
        6: By.LINK_TEXT         - 精确匹配超链接文本
        7: By.PARTIAL_LINK_TEXT - 部分匹配超链接文本
        8: By.TAG_NAME          - 按HTML标签名定位
        :param title: 目标窗口的标题
        :param url: 目标窗口的url
        :param by_value: 目标窗口独特元素的定位符
        :param mode: 定位模式（by_mapping），默认3
        :return: 没有跳转窗口（标签页）返回False,成功跳转目标窗口（标签页）返回True
        """
        # 记录最开始的窗口句柄
        original_window_handle = self.driver.current_window_handle
        # 遍历句柄并跳转标签页
        for window_handle in self.driver.window_handles:
            # 切换到新的标签页上
            self.driver.switch_to.window(window_handle)
            # 判定跳转网页是否符合给定标题、url、存在的元素
            if (self.driver.title == title and self.driver.current_url == url
                    and self.wait_element_appear(by_value, mode, 0)):
                # 成功跳转指定的标签页
                return True
        # 跳回最开始的标签页
        self.driver.switch_to.window(original_window_handle)
        # 没有新的标签页
        return False

    def switch_different_win(self, win_num: int, timeout: int = 5) -> bool:
        """
        切换到不是当前窗口的窗口（切换后等待1秒，不等待找不到元素）
        :param win_num: 原来窗口的数量（新开窗口前保存这个值），len(driver.window_handles)
        :param timeout: 最大等待时间（秒，默认为 5）
        :return: 最大时间内出现新窗口返回 True，超时返回 False
        """
        # 判断是否有新标签页
        if self.wait_win(win_num, timeout):
            # 遍历所有句柄
            for handle in self.driver.window_handles:
                # 不是当前窗口句柄
                if handle != self.driver.current_window_handle:
                    self.driver.switch_to.window(handle)  # 跳转
                    # sleep(1)
            else:
                # 新标签页突然消失
                return False
        return True

    def wait_win_ready(self, timeout: int = 10) -> bool:
            """
            等待界面元素加载完成（使用显式等待检查 document.readyState 是否为 'complete'）,完成后也会等待1秒
            :param timeout: 最大等待时间（秒，默认为 10）
            :return: 超时返回False，准备好返回True
            """
            try:
                # 创建 WebDriverWait 实例
                web_driver_wait = WebDriverWait(self.driver, timeout)
                # 使用 lambda 表达式作为自定义条件：
                web_driver_wait.until(
                    # 驱动对象是默认传递的第一个参数
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                sleep(1)  # 休眠1秒
                return True
            except TimeoutException:
                return False

    # test-code-start

    @staticmethod
    def take_screenshot(driver, file_name):
        timestamp = datetime.now().strftime( "%H%M%S%d%f" )[:-3]
        timestamped_file_name = f"{timestamp}_{file_name}"
        screenshots_dir = "screenshots"
        if not os.path.exists( screenshots_dir ):
            os.makedirs( screenshots_dir )
        screenshot_file_path = os.path.join( screenshots_dir, timestamped_file_name )
        driver.save_screenshot( screenshot_file_path )
