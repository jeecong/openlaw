from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq
import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
db = client['law']
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType

# proxy = Proxy(
#     {
#         'proxyType': ProxyType.MANUAL,
#         'httpProxy': get_proxy_ip_port()
#     }
# )
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
# browser.set_window_size(1400, 900)
from selenium.webdriver.support import expected_conditions as EC


def search(i):
    try:
        if i == 0:
            browser.get("http://openlaw.cn/search/judgement/type")
            button1 = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#judgement-filters > div > div > span > a:nth-child(1)'))
            )
            button1.click()
            button2 = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#judgement-filters > div > div > span > a:nth-child(5)'))
            )
            button2.click()
            for i in range(1, 21):
                st = "#ht-kb > article:nth-child(" + str(i) + ") > h3 > a"
                button7 = browser.find_element_by_css_selector(st)
                button7.click()
                get()
                # 定位到首页
                handles = browser.window_handles
                browser.switch_to_window(handles[0])
            nextpage()
        else:
            s1 = "http://openlaw.cn/search/judgement/type?causeId=d8347b89678645e1887045b4200e822f&page=" + str(i)
            browser.get(s1)
            for i in range(1, 21):
                st = "#ht-kb > article:nth-child(" + str(i) + ") > h3 > a"
                button7 = browser.find_element_by_css_selector(st)
                button7.click()
                get()
                # 定位到首页
                handles = browser.window_handles
                browser.switch_to_window(handles[0])
            nextpage()
    except Exception:
        print("请求分类出错！")


def nextpage():
    handles = browser.window_handles
    browser.switch_to_window(handles[0])
    try:
        wait.until(EC.presence_of_element_located
                   ((By.CSS_SELECTOR,
                     '#ht-kb > nav > ul > nav > ul')))
        button4 = browser.find_element_by_css_selector("#ht-kb > nav > ul > nav > ul").find_elements_by_tag_name("li")[-2]
        button4.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ht-kb')))
        for i in range(1, 21):
            st = "#ht-kb > article:nth-child(" + str(i) + ") > h3 > a"
            button7 = browser.find_element_by_css_selector(st)
            button7.click()
            get()
            handles = browser.window_handles
            browser.switch_to_window(handles[0])
        handles = browser.window_handles
        browser.switch_to_window(handles[0])
        nextpage()


    except Exception:
        print("翻页出错或数据已爬完！")
def get():
    handles = browser.window_handles
    browser.switch_to_window(handles[2])
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#ht-kb > article'))
    )
    html = browser.page_source
    doc = pq(html)
    product = {
        "标题": doc.find(".entry-title").text(),
        "法院": doc.find(".n").text(),
        "案号": doc.find(".ht-kb-em-category").text()[4:],
        "Litigants": doc.find("#Litigants").text(),
        "Explain": doc.find("#Explain").text(),
        "Opinion": doc.find("#Opinion").text(),
        "Facts": doc.find("#Facts").text(),
        "Verdict": doc.find("#Verdict").text(),
        "Inform": doc.find("#Inform").text(),

    }
    save(product)
    time.sleep(20)
    browser.close()


def save(product):
    try:
        if db['law'].insert(product):
            print(product['标题'] + "已存入数据库")
    except Exception:
        print("存入数据库失败！")


def main():
    print("请输入开始的页数（从首页开始请输入0）：")
    i = input()
    search(i)


if __name__ == '__main__':
    main()