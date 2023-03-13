from bs4 import BeautifulSoup


# generate md file
def generate(_dict):
    result = []
    line = ['', "\n# Unity Version :" + _dict['version_code'], "\tPublish Date :" + _dict['version_build_date'],
            "\n> Unity Hub :" + _dict['unity_hub_url'], '\n\n']
    # for big_version_key, big_version_value in _dict.items():
    # for version_value in _dict.items():
    win_list = _dict['platform']['win']
    line.append('## Windows \n\n')
    for item in win_list:
        line.append("> " + item['key'] + '   ' + item['value'] + '\n\n')
    mac_list = _dict['platform']['mac']
    line.append('## Mac \n\n')
    for item in mac_list:
        line.append("> " + item['key'] + '   ' + item['value'] + '\n\n')
    mac_list = _dict['platform']['linux']
    line.append('## Linux \n\n')
    for item in mac_list:
        line.append("> " + item['key'] + '   ' + item['value'] + '\n\n')
    result.append(''.join(line))
    return '\n\n'.join(result)


# decode
def decode(text):
    soup = BeautifulSoup(text, "html.parser")

    for version in [
        # "download-archive-2023",
        "download-archive-2022",
        "download-archive-2021",
        "download-archive-2020",
        "download-archive-2019",
        "download-archive-2018",
        "download-archive-2017",
        "download-archive-5",
    ]:

        # print(version)
        version_list = soup.select("#" + version + " > div > div[class='download-release-wrapper']")
        result = ''
        for version_ele in version_list:
            # print(version_ele)
            version_value = {'version_code': "", 'version_build_date': "", 'unity_hub_url': "",
                             'platform': {'win': [], 'mac': []}}
            # 获取到了版本号
            version_code = version_ele.select("div[class='release-title']")
            if len(version_code):
                version_value['version_code'] = version_code[0].get_text()
                # print(version_code[0].get_text())

            # get publish date
            version_build_date = version_ele.select("div[class='release-date']")
            if len(version_build_date):
                version_value['version_build_date'] = version_build_date[0].get_text()
                # print(version_build_date[0].get_text())

            # Unity Hub
            unity_hub = version_ele.select("a[class='btn btn-blue']")
            if len(unity_hub) > 0:
                version_value['unity_hub_url'] = unity_hub[0]["href"]

            version_select_win_box = version_ele.select(
                "div[class='release-win dropdown']"
            )
            for version_platform in version_select_win_box:
                # get platform
                platform = version_platform.select("div[class='label']")
                temp_list = []
                if len(platform):
                    # win
                    version_value['platform']['win'] = temp_list
                    for target_list in version_platform.select("ul a"):
                        temp_list.append(
                            {
                                'key': target_list.get_text().replace("\n", "").replace(" ", ""),
                                'value': target_list["href"]
                            }
                        )
            version_select_mac_box = version_ele.select(
                "div[class='release-mac dropdown']"
            )
            for version_platform in version_select_mac_box:
                # get platform
                platform = version_platform.select("div[class='label']")
                temp_list = []
                if len(platform):
                    # mac
                    version_value['platform']['mac'] = temp_list
                    for target_list in version_platform.select("ul a"):
                        temp_list.append(
                            {
                                'key': target_list.get_text().replace("\n", "").replace(" ", ""),
                                'value': target_list["href"]
                            }
                        )

            version_select_linux_box = version_ele.select(
                "div[class='release-linux dropdown']"
            )
            for version_platform in version_select_linux_box:
                # get platform
                platform = version_platform.select("div[class='label']")
                temp_list = []
                if len(platform):
                    # linux
                    version_value['platform']['linux'] = temp_list
                    for target_list in version_platform.select("ul a"):
                        temp_list.append(
                            {
                                'key': target_list.get_text().replace("\n", "").replace(" ", ""),
                                'value': target_list["href"]
                            }
                        )

            res = generate(version_value)
            result += res + '\n'
        # save list
        fo = open(version + ".md", "w+", encoding="utf-8")
        fo.write(result)
        # close file
        fo.close()


f = open("download.html", "r", encoding='utf-8')
download_web_text = f.read()
decode(download_web_text)

print('ok')
