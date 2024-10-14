import time
import base64
import os

# import ddddocr

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 获取当前系统时间
current_time = datetime.now()

# 获取当前系统日期
current_date = datetime.now().date()



#maybe change
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Referer": "https://elife.fudan.edu.cn/app/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9，,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
}


url = 'https://ehall.fudan.edu.cn/ywtb-portal/fudan/index.html#/hall'

#输入自己的账号和密码
data = {'username': '',
        'password': ''}

# 初始化找到的标志
found = False

week = {   '1':'one1',
           '2':'one2',
           '3':'oen3',
           '4':'one4',
           '5':'one5',
           '6':'one6',
           '7':'one7'}

# 定义一个变量来记录找到的预订项
found_reservations = []

# 指定保存路径
save_directory = os.path.join(os.path.dirname(__file__), 'captCHA_img')

 
# 定义函数来将网页上的日期字符串转换为 datetime 对象
def convert_to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()


# 定义函数来遍历页面元素并查找日期
def find_date_and_click(driver,user_input_date):
    global found

    while not found:
        # 获取当前页面上所有日期元素
        date_elements = driver.find_elements(By.XPATH, '//ul/li[starts-with(@id, "one")]')

        for date_element in date_elements:
            print("date_element: ", date_element)
            date_text = date_element.text.split("\n")[0].strip()  # 提取日期文本
            print(f"网页上的日期文本: {date_text}")

            try:
                element_date = convert_to_date(date_text)
            except ValueError:
                # 如果不是有效日期，跳过该元素
                continue

            # 如果日期与用户输入的日期匹配
            if element_date == user_input_date:
                print(f"找到日期 {user_input_date}，点击该元素")

                # 获取用户输入的日期对应的星期几（1是星期一，7是星期日）
                weekday_number = user_input_date.isoweekday()

                # 根据星期几，获取对应的one ID
                one_id = week.get(str(weekday_number))

                if one_id:
                    # 通过ID找到并点击对应的li元素
                    driver.find_element(By.ID, one_id).click()
                    found = True
                    break

        # 如果未找到，点击“下一页”按钮继续翻页
        if not found:
            print(f"日期 {user_input_date} 不在当前页面，点击 '下一页'")
            try:
                next_button = driver.find_element(By.XPATH, '//li[@class="right" and @onclick="nextWeek(\'next\')"]')
                next_button.click()

                # 等待页面加载完成
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//ul/li[starts-with(@id, "one")]'))
                )
            except Exception as e:
                print(f"无法点击下一页: {e}")
                break

def save_captcha_info(driver, save_dir, start_index=1):
    """
    截取验证码图片并保存，同时获取提示的文字信息并保存。
    
    参数:
    driver: WebDriver 对象
    save_dir: 图片和文本保存的文件夹路径
    start_index: 从哪个编号开始保存文件，默认为 1
    """
    # 确保保存文件的目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 获取目录下的现有文件数，以确定从哪个编号开始命名
    existing_files = sorted([f for f in os.listdir(save_dir) if f.endswith('.jpg')])
    if existing_files:
        # 取最后一个文件编号作为下一个开始的编号
        last_file = existing_files[-1].split('.')[0]  # 获取最后的编号
        next_index = int(last_file) + 1
    else:
        next_index = start_index

    # 截取验证码图片并保存
    try:
        # 找到图片的 src 属性，它是 base64 编码的
        img_element = driver.find_element(By.CLASS_NAME, 'valid_bg-img')
        img_src = img_element.get_attribute('src')

        # 验证码的 src 是 base64 编码的图片
        if img_src.startswith('data:image'):
            # 去掉前缀 'data:image/jpg;base64,'
            img_base64 = img_src.split(',')[1]

            # 将 base64 解码并保存为图片文件
            img_data = base64.b64decode(img_base64)

            # 构造文件路径，按 001, 002 格式递增保存图片
            img_filename = os.path.join(save_dir, f'{next_index:03}.jpg')
            with open(img_filename, 'wb') as f:
                f.write(img_data)

            print(f"验证码图片已保存为 '{img_filename}'")

        else:
            print("未找到 base64 编码的图片")

    except Exception as e:
        print(f"获取验证码图片时发生错误: {e}")

    # 获取 "请依次点击：只争朝夕" 中的提示文字并保存
    try:
        # 定位提示信息元素
        tips_element = driver.find_element(By.CLASS_NAME, 'valid_tips__text')

        # 获取文本内容并提取“只争朝夕”
        tips_text = tips_element.text
        click_sequence = tips_text.split('：')[1].strip()  # 提取冒号后面的文字

        # 构造对应的文本文件名
        text_filename = os.path.join(save_dir, f'{next_index:03}.txt')

        # 保存提示信息
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(click_sequence)

        print(f"验证码提示已保存为 '{text_filename}', 提示内容: {click_sequence}")

    except Exception as e:
        print(f"获取验证码提示时发生错误: {e}")

# session = requests.session()
# cookie_jar = session.post(url=url, data=data, headers=headers).cookies
# cookie_t = requests.utils.dict_from_cookiejar(cookie_jar)
def login():

        # 让用户输入目标日期，格式为 YYYY-MM-DD
        user_input_date_str = input("请输入目标日期 (格式为 YYYY-MM-DD): ")
        # user_input_date_str = '2024-10-15'

        # 获取用户输入的时间段，支持多选，以逗号分隔
        desired_times = input("请输入您想预订的时间段 (例如 '09:00, 10:00'): ").strip().split(',')
        # desired_times = '08:00'


        # 去掉每个时间段前后的空格
        desired_times = [time.strip() for time in desired_times]
        # 将用户输入的日期字符串转换为 date 对象
        try:
            user_input_date = datetime.strptime(user_input_date_str, "%Y-%m-%d").date()
            # weekday_number = user_input_date.isoweekday()
            # print(weekday_number)
        except ValueError:
            print("日期格式不正确，请输入正确的 YYYY-MM-DD 格式")
            exit()

        print('当前时间： ',current_time)


        driver = webdriver.Edge()
        # driver = webdriver.Chrome()
        driver.get(url)
        # time.sleep(2)
        # driver.find_element(By.CLASS_NAME, 'btnloginbox').click()
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btnloginbox'))).click()
        # cookies = driver.get_cookies()

        time.sleep(1)
        driver.find_element(By.ID, 'username').send_keys(data['username'])
        driver.find_element(By.ID, 'password').send_keys(data['password'])

        driver.find_element(By.ID, 'idcheckloginbtn').click()

        time.sleep(1)
        # driver.find_element(By.ID,'searchbarId').send_keys('体')
        # time.sleep(1)
        # 添加延时或保持打开
        # time.sleep(10)  # 暂停10秒后关闭
        driver.find_element(By.XPATH, '//input[@class="content" and @maxlength="100"]').send_keys('体')
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@class="btn amp-theme" and @type="button"]').click()
        time.sleep(2)
        driver.find_element(By.CLASS_NAME,'ivu-tooltip-rel').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//div[@class="amp-theme app-enter"]').click()
        time.sleep(1)

        # 获取所有的窗口句柄
        all_windows = driver.window_handles
        # for window in all_windows:
            # print(window)
        # 切换到新窗口（假设新窗口是最后一个）
        driver.switch_to.window(all_windows[-1])

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,
                                            '//a[@href="/public/front/toResourceFrame.htm?contentId=8aecc6ce749544fd01749a31a04332c2"]'))).click()

        except Exception as e:
            print(f"发生错误: {e}")
        # 获取所有包含日期的 li 元素
        # date_elements = driver.find_elements(By.XPATH, '//ul/li[starts-with(@id, "one")]')
        # time.sleep(1)



        # driver.find_element(By.XPATH, '//li[@class="right" and @onclick="nextWeek(\'next\')"]').click()
        # time.sleep(1)

        # driver.find_element(By.ID,'one3').click()

        find_date_and_click(driver,user_input_date)

        # 找到页面中所有的预订行（每个 <tr>）
        rows = driver.find_elements(By.XPATH, '//table[@class="site_table"]/tbody/tr')

        # 遍历每一个用户输入的时间段
        for desired_time in desired_times:
            reservation_found = False  # 标记是否找到匹配的时间段

            # 遍历每一行，查找与当前用户输入的时间段匹配的预订项
            for row in rows:
                try:
                    # 获取时间段
                    time_slot = row.find_element(By.XPATH, './td[1]').text.strip()

                    # 如果时间段与用户输入的时间匹配
                    if desired_time in time_slot:
                        print(f"找到匹配的时间段: {time_slot}")

                        # 获取服务项目名称
                        service_item = row.find_element(By.XPATH, './td[2]').text.strip()

                        # 检查是否有预订按钮
                        img_element = row.find_element(By.XPATH, './td[@align="right"]/img')
                        img_src = img_element.get_attribute('src')

                        # 判断是否为可点击的预订按钮
                        if 'reserve.gif' in img_src:
                            # 执行点击操作
                            img_element.click()
                            # 通过 XPath 定位并点击按钮
                            driver.find_element(By.XPATH, '//input[@value="点击按钮进行验证 "]').click()
                            
                            time.sleep(1)
                            save_captcha_info(driver,save_directory,1)

                            # WebDriverWait(driver, 10).until(
                            #     EC.element_to_be_clickable((By.ID, "btn_sub"))
                            # ).click()
                            print(f"已成功预订时间段: {time_slot}，服务项目: {service_item}")
                            found_reservations.append({'time': time_slot, 'service': service_item})
                            reservation_found = True
                            break
                        else:
                            print(f"时间段 {time_slot} 的预订已满，无法点击预订。")

                except Exception as e:
                    # 如果未找到相关元素或者其他错误，跳过该行
                    continue

            if not reservation_found:
                print(f"未找到与输入的时间段 {desired_time} 匹配且可点击的预订项。")

        # 打印所有成功预订的时间段
        if found_reservations:
            print("已成功预订以下时间段：")
            for reservation in found_reservations:
                print(f"时间段: {reservation['time']}, 服务项目: {reservation['service']}")
        else:
            print("没有成功的预订。")


        input("Press Enter to close the browser·...")  # 按回车键后才关闭
        # driver.quit()

# input("Press Enter to close the browser·...")  # 按回车键后才关闭


# def search():
#         # driver = webdriver.Edge()
#         # driver.get(url)
#         pass




# driver.get("https://www.bilibili.com")



# 定义任务
# def task():
#     print("任务在北京时间执行:", datetime.now())
#     login()
#     #task 模拟发送post请求

# exit(0)


# 创建调度器
# scheduler = BlockingScheduler()

# 设置任务为每天12:00在北京时间执行
# beijing_timezone = pytz.timezone('Asia/Shanghai')

# scheduler.add_job(task, CronTrigger(hour=14, minute=34, timezone=beijing_timezone))
# scheduler.add_job(task, 'interval', minutes=1)
# print("定时任务已启动...")
# scheduler.start()

if __name__ == '__main__':
    login()
    # search()
