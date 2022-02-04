import time

from selenium import webdriver
from selenium.webdriver.common.by import By

qq_num = input("请输入你的QQ号：")

if qq_num == '':
    qq_num = "1399128236"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://qzone.qq.com/")
input("请先在弹出的浏览器里完成QQ空间的登录，然后回车继续...")

try:
    driver.set_page_load_timeout(3)
    driver.get("https://www.fwder.cn/index.php/cross.html")
except:
    driver.set_page_load_timeout(20)
    print("等到timeout之后就可以get了")
    try:
        driver.get("https://www.fwder.cn/index.php/cross.html")
    except:
        driver.set_page_load_timeout(99999)
        pass

while True:
    try:
        submit = driver.find_element(By.XPATH,
                                     "/html/body/div/div/main/div/div/div/div/div/div/ol/div[1]/div/div/p")  # 定位元素 div[@='']
        text = submit.text  # 获取元素文本信息
        break
    except:
        text = ""
        print("获取元素文本信息失败！准备重试...")
        continue

print("读取到最初文本为：" + text)  # 打印元素文本

while True:

    try:
        driver.set_page_load_timeout(3)
        driver.get("https://www.fwder.cn/index.php/cross.html")
    except:
        driver.set_page_load_timeout(10)
        print("等到timeout之后就可以get了")
        try:
            driver.get("https://www.fwder.cn/index.php/cross.html")
        except:
            driver.set_page_load_timeout(99999)
            pass

    try:
        submit = driver.find_element(By.XPATH,
                                     "/html/body/div/div/main/div/div/div/div/div/div/ol/div[1]/div/div/p")  # 定位元素 div[@='']
        text_new = submit.text  # 获取元素文本信息
    except:
        print("获取元素文本信息失败！准备重试...")
        continue

    print("读取到最新的文本为：" + text_new)  # 打印元素文本

    if text == text_new:
        print("没有发送新的说说...开始延迟")
        # 延时执行
        time.sleep(60)
        continue

    print("最新的说说内容为：" + text_new + "，开始同步QQ空间的说说...")

    try:
        driver.set_page_load_timeout(3)
        driver.get("https://user.qzone.qq.com/" + qq_num)
    except:
        driver.set_page_load_timeout(20)
        print("等到timeout之后就可以get了")
        try:
            driver.get("https://user.qzone.qq.com/" + qq_num)
            time.sleep(3)
        except:
            driver.set_page_load_timeout(99999)
            pass

    try:
        driver.find_element(By.XPATH, "//div[text()='说点儿什么吧']").click()
        time.sleep(2)
    except:
        print("点击输入框失败，准备重试...")
        pass

    try:
        driver.find_element(By.XPATH, "/html/body/div[12]")
        print("有登录层，尝试关闭登录层...")
        try:
            driver.find_element(By.XPATH, "/html/body/div[12]/div/div[3]/button").click()
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, "//div[text()='说点儿什么吧']").click()
                time.sleep(2)
            except:
                print("登录层关闭成功，但是点击输入框失败，准备重试...")
                continue
        except:
            print("登录层关闭失败！准备重试...")
            continue
    except:
        print("没有输入层")
        pass

    try:
        driver.find_element(By.XPATH,
                            "/html[@class='skin-light']/body[@class='os-winxp bg-body date-20220204']/div[@id='layBackground']/div[@class='layout-background']/div[@class='layout-body']/div[@id='pageContent']/div[@id='main_feed_container']/div[@class='col-main-feed']/div[@id='QM_Mood_Poster_Container']/div[@id='QM_Mood_Poster_Inner']/div[@class='qz-poster-inner qz-poster-2022-02-04']/div[@class='qz-poster-bd']/div[@id='qz_poster_v4_editor_container_1']/div[@class='qz-inputer bor2']/div/div[@id='$1_content_content']").send_keys(
            text_new + "\n\n——————————————\n此说说为脚本推送，并与我的博客动态同步 -> https://www.fwder.cn/index.php/cross.html")
        time.sleep(2)
    except:
        print("编辑框输入文字失败！准备重试...")
        continue

    try:
        driver.find_element(By.XPATH,
                            "/html/body/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div/div/div[4]/div[4]").click()
        time.sleep(3)
    except:
        print("点击发送按钮失败！准备重试...")
        pass

    # 更新一下text的内容
    text = text_new
