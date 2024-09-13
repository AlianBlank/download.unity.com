import json
import time
import demjson3
import ssl
import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# 指定Edge WebDriver的路径
edge_driver_path = 'msedgedriver.exe'
service = Service(executable_path=edge_driver_path)

# 设置Selenium浏览器选项
options = webdriver.EdgeOptions()
options.use_chromium = True  # 指定使用Chromium内核的Edge
# options.headless = True  # 无头模式，不显示浏览器窗口
driver = webdriver.Edge(service=service, options=options)


def get_web_page(url):
    driver.get(url)
    time.sleep(3)
    return driver.page_source


def download_web():
    # url = 'https://unity.com/releases/editor/archive'
    url = 'https://unity.com/de/releases/editor/archive'
    text = get_web_page(url)
    return text


# generate md file
def generate(_dict):
    result = []
    line = ['', "\n# Unity Version: " + _dict['version_code'] + "", "\tPublish Date: " + _dict['version_build_date'],
            "\n> Unity Hub: [" + _dict['unity_hub_url'] + "](" + _dict['unity_hub_url'] + ")", '\n\n']
    keys = ['Operating systems', 'Other installs', 'Windows', 'Windows ARM64', 'macOS', 'macOS ARM64', 'Linux', 'macOS']
    for key in keys:
        if _dict.get(key) is not None:
            kvs = _dict[key]
            line.append(f'## {key} \n\n')
            for item in kvs:
                line.append("- " + item['key'] + ' :[' + item['value'] + '](' + item['value'] + ')\n\n')

    result.append(''.join(line))
    result.append(f'releases_notes_link: [{_dict["releases_link"]}]({_dict["releases_link"]})\n')
    return '\n\n'.join(result)


def decode():
    version_list = []
    main_version_list_div = driver.find_element(By.CSS_SELECTOR, ".relative.flex.flex-wrap.justify-center.gap-2.p-2")

    main_version_list_button = main_version_list_div.find_elements(By.TAG_NAME, "button")
    for button_row in main_version_list_button:
        # 主版本列表
        main_version_list = []
        main_version_object = {"main": button_row.text, "version_list": main_version_list}
        version_list.append(main_version_object)
        button_row.click()
        time.sleep(1)
        # 下方的分类按钮列表
        main_version_list_class = driver.find_element(By.CSS_SELECTOR, ".flex.items-center.gap-2.rounded-3xl.bg-gray-200.p-2")
        all_button = main_version_list_class.find_elements(By.TAG_NAME, "button")[0]
        all_button.click()
        time.sleep(1)

        main_content = driver.find_element(By.CSS_SELECTOR, ".relative.flex-1")
        main_section = main_content.find_element(By.TAG_NAME, 'section')
        main_section_div = main_section.find_element(By.CSS_SELECTOR, '.hidden.min-w-full.rounded-md.bg-gray-100.align-middle')
        main_section_tbody = main_section_div.find_element(By.TAG_NAME, "tbody")
        main_section_tr = main_section_tbody.find_elements(By.TAG_NAME, "tr")
        for tr in main_section_tr:
            td_list = tr.find_elements(By.TAG_NAME, "td")
            version_object = {}
            main_version_list.append(version_object)
            index = 0
            for td in td_list:
                if index == 0:
                    # 版本号
                    version_object['version_code'] = td.text
                elif index == 1:
                    # 发布时间
                    version_object['version_build_date'] = td.text
                elif index == 2:
                    # 发布日志
                    version_object['releases_link'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                elif index == 3:
                    # unityHub 安装链接
                    version_object['unity_hub_url'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                elif index == 4:
                    # 扩展 安装链接
                    version_object['install_link'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                index += 1

    print(version_list)

    fo = open('version' + ".json", "w+", encoding="utf-8")
    fo.write(json.dumps(version_list, indent=2))
    # close file
    fo.close()
    return version_list


def run_extension(version, main_version):
    install_link = version['install_link']
    get_web_page(install_link)
    container = driver.find_element(By.CSS_SELECTOR, ".container.py-16")
    container_div = container.find_element(By.CSS_SELECTOR, ".top-16.col-span-12")
    section_list = container_div.find_elements(By.TAG_NAME, 'section')
    # 把当前页面的页签全部打开
    for section in section_list:
        section_div = section.find_element(By.CSS_SELECTOR, '.border-b.border-gray-200')
        section_button_div = section.find_element(By.CSS_SELECTOR, '.cursor-pointer.py-6')
        try:
            # 检查内容是否展开
            section_div.find_element(By.CSS_SELECTOR, '.accordion-content.ease-in-out')
        except NoSuchElementException as e:
            # 没有展开,需要调用展开
            try:
                # 滚动到目标位置
                scroll_to_view(section_button_div)
                # 模拟点击展开
                section_button_div.click()
            except Exception as ee:
                print(section_button_div.text)
                print(ee)
            else:
                time.sleep(4)
    # 抓取详细界面的内容
    for section in section_list:
        section_div = section.find_element(By.CSS_SELECTOR, '.border-b.border-gray-200')
        section_button_div = section.find_element(By.CSS_SELECTOR, '.cursor-pointer.py-6')
        # 执行抓取数据
        data_list = []
        version[section_button_div.text.replace('\n', '').strip('-')] = data_list
        # 展开的内容
        accordion_content = section_div.find_element(By.CSS_SELECTOR, '.accordion-content.ease-in-out')
        try:
            note_list = accordion_content.find_element(By.TAG_NAME, 'ul')
            # 找到了note 说明是版本说明
        except Exception as notes_e:
            # 没有找到notes,说明是下载链接
            link_list = accordion_content.find_elements(By.TAG_NAME, 'a')
            for link in link_list:
                data_list.append({'key': link.text, "value": link.get_attribute('href')})

    # 写入完整的版本信息到文件
    fo = open(main_version + ".json", "a", encoding="utf-8")
    fo.write(json.dumps(version, indent=2))
    fo.close()
    return version


def scroll_to_view(element):
    # 获取页面高度
    page_height = driver.execute_script("return document.body.scrollHeight")
    offset = -400  # 你希望的垂直偏移量
    target_y = element.location['y'] + offset
    driver.execute_script(f"window.scrollTo(0, {target_y});")
    time.sleep(2)


def run():
    fo = open("version.json", "r", encoding="utf-8")
    all_version_list = json.loads(fo.read())
    for main_version in all_version_list:
        main_version_list = main_version['version_list']
        main_version = main_version['main']
        for version in main_version_list:
            json_result = generate(run_extension(version, main_version))
            file_md = open('download-' + main_version + '.md', 'a', encoding="utf-8")
            file_md.write(json_result)
            file_md.close()

    print('ok')
