# coding=utf-8
# coding=utf-8
import platform
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, InvalidSessionIdException


class WebEntity:

    def __init__(self, driver=None):
        self.driver = driver if driver else self.get_driver()
        self.actions = ActionChains(self.driver)

    def get_driver(self):
        sys_name = platform.system().lower()
        is_win = sys_name == 'windows'
        print(f"当前系统:{sys_name}")

        if is_win:
            t_driver = self.__get_driver_win()
        else:
            t_driver = self.__get_driver_linux()
        return t_driver

    def __get_driver_win(self):
        # 1. 配置 Chrome 选项（可选）
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # 最大化窗口
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)
        return driver

    def __get_driver_linux(self):
        service = Service(executable_path="/usr/lib/chromium-browser/chromedriver")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # 最大化窗口
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(service=service, options=options)  # 传递service参数
        return driver

    def get_xpath_data(self, xpath):

        rst = self.driver.find_element(By.XPATH, xpath).text
        print(f"xpath规则:[{xpath}]. xpath获取的数据:{rst}")
        return rst

    def get_page_center_coordinates(self):
        """获取页面正中心的坐标"""
        # 获取页面尺寸
        page_width = self.driver.execute_script("return document.documentElement.scrollWidth")
        page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        # 获取视口尺寸
        viewport_width = self.driver.execute_script("return window.innerWidth")
        viewport_height = self.driver.execute_script("return window.innerHeight")

        # 计算页面中心坐标（考虑滚动位置）
        scroll_x = self.driver.execute_script("return window.pageXOffset")
        scroll_y = self.driver.execute_script("return window.pageYOffset")

        # 计算视口中心坐标
        center_x = scroll_x + (viewport_width // 2)
        center_y = scroll_y + (viewport_height // 2)

        # 确保坐标在页面范围内
        center_x = min(center_x, page_width - 1)
        center_y = min(center_y, page_height - 1)

        return center_x, center_y

    def get_web_fps(self, driver=None):
        """
            返回网页平均fps值: {'fps_avg': '4.11', 'fps_count': 9, 'fps_list': [5, 4, 4, 4, 4, 4, 4, 4, 4]}
        """
        # 注入 JavaScript 来监控 FPS
        if driver is None:
            driver = self.driver
        js_code = """
        // function sleep(ms, callback) {
        //     setTimeout(callback, ms);
        // }
        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }
        class FPSMonitor {
            constructor() {
                this.frameCount = 0;
                this.lastTime = performance.now();
                this.fps = 0;
                this.running = false;
                this.fps_count = 0;
                this.fps_sum = 0;
                this.fps_list = [];
            }

            async start() {
                this.running = true;
                this.update();
            }

            stop() {
                this.running = false;
            }

            update() {
                if (!this.running) return;

                this.frameCount++;

                const currentTime = performance.now();
                const delta = currentTime - this.lastTime;

                if (delta >= 1000) {
                    this.fps = Math.round((this.frameCount * 1000) / delta);
                    this.frameCount = 0;
                    this.lastTime = currentTime;

                    // 更新显示或存储数据
                    this.onFPSUpdate(this.fps);
                }

                requestAnimationFrame(() => this.update());
            }

            onFPSUpdate(fps) {
                // 在这里处理 FPS 数据
                this.fps_count++;
                this.fps_sum += fps;
                this.fps_list.push(fps)
                console.log(`当前[${this.fps_count}] FPS: ${fps}`);

                // 可以更新页面显示
                if (!this.displayElement) {
                    this.displayElement = document.createElement('div');
                    this.displayElement.style.cssText = `
                        position: fixed;
                        top: 10px;
                        right: 10px;
                        background: rgba(0,0,0,0.8);
                        color: white;
                        padding: 5px 10px;
                        font-family: monospace;
                        z-index: 9999;
                    `;
                    document.body.appendChild(this.displayElement);
                }
                this.displayElement.textContent = `FPS: ${fps}`;
            }
            getData(){
                return {
                    fps_avg: (this.fps_sum/this.fps_count).toFixed(2) ,
                    fps_count: this.fps_count,
                    fps_list: this.fps_list
                }
            }
        }

        // start test
        const fpsMonitor = new FPSMonitor();
        fpsMonitor.start().then(r => console.log('get', r));
        // run 10s test
        await sleep(10000);
        // stop test
        fpsMonitor.stop();
        return fpsMonitor.getData()
        """
        fps_value = driver.execute_script(js_code)
        print(f"当前 FPS数据: {fps_value}")
        return fps_value

    def is_driver_healthy(self, driver=None):
        """
        更全面的 WebDriver 健康检查

        参数:
        driver: WebDriver 实例

        返回:
        bool: True 表示健康可用，False 表示不可用
        """
        if driver is None:
            driver = self.driver
        try:
            # 1. 检查 session_id
            if not hasattr(driver, 'session_id') or not driver.session_id:
                return False

            # 2. 执行一个简单的命令
            driver.execute_script("return 1;")

            # 3. 检查浏览器窗口是否打开
            if not driver.window_handles:
                return False

            # 4. 检查浏览器进程是否运行（仅适用于本地驱动）
            if hasattr(driver, 'service') and driver.service and driver.service.process:
                if driver.service.process.poll() is not None:
                    return False  # 进程已退出

            return True
        except (WebDriverException, InvalidSessionIdException):
            return False
        except Exception as e:
            print(f"WebDriver 健康检查失败: {e}")
            return False

    def get_available_driver(self, driver):
        if not self.is_driver_healthy(driver):
            print("当前driver异常,需要重新获取driver")
            run_driver = self.get_driver()
            self.driver = run_driver
            return run_driver
        else:
            print("当前driver正常")
            return driver