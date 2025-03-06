import json
import os
import time
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
options.add_argument('--incognito')
options.use_chromium = True  # 指定使用Chromium内核的Edge
# options.headless = True  # 无头模式，不显示浏览器窗口
driver = webdriver.Edge(service=service, options=options)


def get_web_page(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            driver.get(url)
            time.sleep(5)
            return driver.page_source
        except Exception as e:
            print(f"第 {attempt + 1} 次尝试失败: {str(e)}")
            if attempt < max_retries - 1:  # 如果不是最后一次尝试
                print(f"等待 5 秒后重试...")
                time.sleep(5)
            else:
                print(f"已达到最大重试次数 {max_retries}，获取页面失败")
                raise  # 重新抛出异常


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
    # 检查文件是否存在
    try:
        with open('version.json', 'r', encoding='utf-8') as f:
            version_list = json.loads(f.read())
            print("从缓存文件读取版本信息")
            return version_list
    except FileNotFoundError:
        print("未找到缓存文件，开始从网页获取数据")

    # 获取新的版本列表
    new_version_list = []
    main_version_list_div = driver.find_element(By.CSS_SELECTOR, ".relative.flex.flex-wrap.justify-center.gap-2.p-2")
    main_version_list_button = main_version_list_div.find_elements(By.TAG_NAME, "button")

    # 读取现有的版本数据（如果存在）
    existing_versions = {}
    try:
        with open('version.json', 'r', encoding='utf-8') as f:
            existing_data = json.loads(f.read())
            # 构建版本号映射
            for main_ver in existing_data:
                for ver in main_ver['version_list']:
                    existing_versions[ver['version_code']] = ver
    except FileNotFoundError:
        existing_data = []

    for button_row in main_version_list_button:
        # 主版本列表
        main_version_list = []
        main_version_object = {"main": button_row.text, "version_list": main_version_list}
        new_version_list.append(main_version_object)

        # 检查是否需要获取该版本的详细信息
        button_row.click()
        time.sleep(5)

        # 下方的分类按钮列表
        main_version_list_class = driver.find_element(By.CSS_SELECTOR,
                                                      ".flex.items-center.gap-2.rounded-3xl.bg-gray-200.p-2")
        all_button = main_version_list_class.find_elements(By.TAG_NAME, "button")[0]
        all_button.click()
        time.sleep(1)

        main_content = driver.find_element(By.CSS_SELECTOR, ".relative.flex-1")
        main_section = main_content.find_element(By.TAG_NAME, 'section')
        main_section_div = main_section.find_element(By.CSS_SELECTOR,
                                                     '.hidden.min-w-full.rounded-md.bg-gray-100.align-middle')
        main_section_tbody = main_section_div.find_element(By.TAG_NAME, "tbody")
        main_section_tr = main_section_tbody.find_elements(By.TAG_NAME, "tr")

        for tr in main_section_tr:
            td_list = tr.find_elements(By.TAG_NAME, "td")
            version_code = td_list[0].text

            # 检查版本是否已存在
            if version_code in existing_versions:
                main_version_list.append(existing_versions[version_code])
                print(f"版本 {version_code} 已存在，跳过获取")
                continue

            # 获取新版本信息
            version_object = {}
            main_version_list.append(version_object)
            index = 0
            for td in td_list:
                if index == 0:
                    version_object['version_code'] = td.text
                elif index == 1:
                    version_object['version_build_date'] = td.text
                elif index == 2:
                    version_object['releases_link'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                elif index == 3:
                    version_object['unity_hub_url'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                elif index == 4:
                    version_object['install_link'] = td.find_element(By.TAG_NAME, "a").get_attribute('href')
                index += 1

    print("版本信息获取完成，写入文件")
    # 覆盖写入新的版本信息
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump(new_version_list, f, indent=2)

    return new_version_list


def run_extension(version, main_version):
    # 检查并创建main_version目录
    if not os.path.exists(main_version):
        os.makedirs(main_version)

    install_link = version['install_link']
    version_code = version['version_code']
    version_json_path = os.path.join(main_version, f"{version_code}.json")
    # 检查是否已经存在该版本的JSON文件
    if os.path.exists(version_json_path):
        print(f"版本 {version_code} 的JSON文件已存在，跳过获取")
        with open(version_json_path, "r", encoding="utf-8") as fr:
            return json.loads(fr.read())
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
    with open(version_json_path, "a", encoding="utf-8") as fw:
        json.dump(version, fw, ensure_ascii=False, separators=(',', ':'))
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
