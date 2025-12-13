# pywebauto
基于selenium的自动化测试框架和Page Object (PO) 模型，内置工具快速进行Python Web UI 自动化测试和web自动化脚本开发以及web测试赛的模板
- 包含内置工具快速构建项目结构
- 对封装selenium进行二次封装
- cookie注入的封装和处理
- requests的简单封装
- web测试赛模板，内置封装的独立方法

# 使用方式
```bash
pip install pywebauto
```
- 依赖的第三方库
```
pytest>=8.3.5
selenium>=4.27.1
```

# 包的架构
`base_actions.py`对应`BaseActions`类，基础行为封装
`base_options.py`对应`BaseOptions`类，基础选项封装
`cookie_manager.py`对应`CookieManager`类，cookies管理封装
`test_template.py`对应`TestTemplate`类，TestTemplate是web测试赛的测试模板

# 无法实现的封装
在selenium中没有鼠标中键的操作，更准确的说是绝大多数现代浏览器都没有这个操作，对于类似于`<a>`标签实行鼠标中建实际上是进行了一次右击罢了。deepseek给的`actions.click(element, button='middle').perform()`这个方法是错的，旧版早就移除了。

# BaseActions 类方法文档

## 概述
BaseActions 类是对 Selenium WebDriver 的二次封装，提供了更便捷的元素定位、等待机制、鼠标键盘操作和窗口控制等方法。

## 类初始化

### `__init__(self, driver: webdriver.Chrome, default_by_strategy: int = 3) -> None`
初始化 BaseActions 类
- **参数**：
  - `driver`: Chrome 浏览器驱动对象
  - `default_by_strategy`: 默认定位策略（1-8）
- **定位策略映射**：
  - 1: CSS_SELECTOR - 性能好，写法灵活，推荐
  - 2: ID - 性能最佳，元素唯一时首选
  - 3: XPATH - 功能强大，可遍历DOM，但性能相对较差
  - 4: NAME - 主要用于表单元素
  - 5: CLASS_NAME - 按CSS类名定位
  - 6: LINK_TEXT - 精确匹配超链接文本
  - 7: PARTIAL_LINK_TEXT - 部分匹配超链接文本
  - 8: TAG_NAME - 按HTML标签名定位

## 属性修改方法

### `set_default_by_strategy(self, mode: int = 3) -> bool`
修改默认定位策略

### `set_implicitly_wait_time(self, time: int = 0) -> bool`
修改隐式等待时间

### `set_explicit_wait_time(self, time: int = 0) -> bool`
修改显式等待时间

## 元素查找与状态检测

### `wait_element_appear(self, by_value: str) -> WebElement | bool`
等待元素出现（使用默认策略）

### `wait_element_appear_ex(self, by_value: str, mode: int = 3, timeout: int = 10) -> WebElement | bool`
等待元素出现（自定义策略）

### `wait_elements_appear(self, by_value: str, mode: int = 1, timeout: int = 10) -> list[WebElement] | bool`
等待所有元素出现

### `wait_class_change(self, by_value: str, class_value: str) -> bool`
检测元素样式是否改变

### `wait_class_change_ex(self, by_value: str, class_value: str, mode: int = 1, timeout: int = 10) -> bool`
检测元素样式是否改变（自定义策略）

### `get_text(self, by_value: str, mode: int = 1, timeout: int = 10) -> str | bool`
安全获取元素的文本内容

## 行为链控制

### `release_actions(self) -> bool`
释放所有行为（鼠标按住、键盘按住等）

## 鼠标操作

### 点击操作
- `click(self, by_value: str) -> WebElement | bool` - 点击元素
- `click_ex(self, by_value: str, mode: int = 3) -> WebElement | bool` - 点击元素（自定义策略）
- `js_click(self, by_value: str) -> WebElement | bool` - JS点击（绕过遮罩）
- `js_click_ex(self, by_value: str, mode: int = 3) -> WebElement | bool` - JS点击（自定义策略）

### 等待点击
- `wait_click(self, by_value: str) -> WebElement | bool` - 等待元素出现并点击
- `wait_click_ex(self, by_value: str, mode: int = 1, timeout: int = 10) -> WebElement | bool` - 等待点击（自定义策略）
- `js_wait_click(self, by_value: str) -> WebElement | bool` - 等待元素出现并JS点击
- `js_wait_click_ex(self, by_value: str, mode: int = 1, timeout: int = 10) -> WebElement | bool` - 等待JS点击（自定义策略）

### 其他鼠标操作
- `wait_double_click(self, by_value: str) -> WebElement | bool` - 双击
- `wait_double_click_ex(self, by_value: str, mode: int = 1, timeout: int = 10) -> WebElement | bool` - 双击（自定义策略）
- `right_click(self, element: WebElement) -> WebElement | bool` - 右击
- `wait_right_click(self, by_value: str) -> bool` - 等待元素出现并右击
- `middle_click(self, element: WebElement) -> bool` - 中击
- `move(self, element: WebElement) -> bool` - 鼠标悬停
- `wait_move(self, by_value: str) -> bool` - 等待元素出现并悬停
- `hold(self, element: WebElement) -> bool` - 鼠标按住元素
- `wait_hold(self, by_value: str) -> bool` - 等待元素出现并按住
- `click_screen(self, x: int, y: int) -> tuple[int, int]` - 点击屏幕指定坐标

## 键盘操作

### `clear_key(self, by_value: str, mode: int = 1, timeout: int = 10) -> WebElement | bool`
等待元素出现并清空内容

### `send_key(self, by_value: str, *keys_to_send: str) -> WebElement | bool`
等待元素出现并输入文本

### `send_key_ex(self, by_value: str, mode: int = 3, timeout: int = 10, *keys_to_send: str) -> WebElement | bool`
等待元素出现并输入文本（自定义策略）

### `rewrite_key(self, keys_to_send: str, by_value: str, mode: int = 1, wait_time: int = 0, timeout: int = 10) -> WebElement | bool`
等待元素出现，清空后重新输入

## 窗口控制

### 窗口大小控制
- `max_win(self) -> bool` - 最大化窗口
- `min_win(self) -> None` - 最小化窗口

### 窗口导航
- `close_win(self, target_window_handle: str) -> bool` - 关闭指定窗口
- `back_win(self) -> None` - 回退上一个网页
- `forward_win(self) -> None` - 前进下一个网页

### 窗口等待
- `wait_win(self, win_num: int, timeout: int = 5) -> bool` - 等待新窗口出现
- `wait_win_ex(self, win_num: int, timeout: int = 5) -> bool` - 等待新窗口出现（自定义时间）
- `wait_win_ready(self, timeout: int = 10) -> bool` - 等待界面元素加载完成

### 窗口切换
- `switch_win(self, target_window_handle: str) -> bool` - 切换到指定句柄窗口
- `switch_different_win(self, win_num: int, timeout: int = 5) -> bool` - 切换到不同窗口
- `switch_win_for_url(self, url: str) -> bool` - 按URL切换到窗口
- `switch_win_for_title(self, window_title: str) -> bool` - 按标题切换到窗口
- `switch_win_for_element(self, by_value: str, mode: int = 3) -> bool` - 按元素切换到窗口
- `switch_win_ex(self, title: str, url: str, by_value: str, mode: int = 3) -> bool` - 多重条件切换窗口

## 设计特点

### 命名规范
1. 基本方法：`method_name`
2. 扩展方法：`method_name_ex`（支持自定义参数）
3. 等待方法：`wait_method_name`（包含等待机制）
4. JavaScript方法：`js_method_name`（使用JavaScript实现）

### 参数设计
1. `by_value`: 元素定位值
2. `mode`: 定位策略（1-8）
3. `timeout`: 等待超时时间
4. 支持可变参数：`*keys_to_send`

### 返回值设计
1. 成功：返回元素对象或True
2. 失败：返回False
3. 多种类型：使用联合类型注解（如 `WebElement | bool`）

### 异常处理
1. 捕获常见Selenium异常
2. 超时返回False而非抛出异常
3. 元素消失或不可交互时返回False

## 使用建议

### 定位策略选择
1. **性能优先**：CSS_SELECTOR > ID > XPATH
2. **稳定性优先**：优先选择ID、NAME等固定属性
3. **灵活性**：XPATH功能最强大，支持DOM遍历

### 等待机制
1. **显式等待**：推荐使用，更精准
2. **隐式等待**：全局设置，影响所有查找
3. **混合使用**：显式等待为主，隐式等待为辅

### 方法选择
1. **常规操作**：使用基本方法
2. **复杂场景**：使用`_ex`扩展方法
3. **特殊需求**：使用JavaScript方法
4. **稳定性要求高**：使用等待方法

这个类库提供了完整的Web自动化操作封装，适合中大型自动化测试项目使用。