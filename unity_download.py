from bs4 import BeautifulSoup
import urllib.request
import ssl

# download web page
def download_web():
    context = ssl._create_unverified_context()
    url = 'https://unity3d.com/get-unity/download/archive'
    html = urllib.request.urlopen(url,context=context).read()
    return html


# decode
def decode(text):
    soup = BeautifulSoup(text, "lxml")

    result = {}

    for version in [
        "version-2021",
        "version-2020",
        "version-2019",
        "version-2018",
        "version-2017",
        "version-5",
        "version-4",
        "version-3",
    ]:

        result[version] = []
        # print(version)
        version_list = soup.select("#" + version + " > div > div[class='row clear']")
        for version_ele in version_list:
            # print(version_ele)
            version_value = {'version_code': "", 'version_build_date': "", 'unity_hub_url': "",
                             'platform': {'win': [], 'mac': []}}
            # 获取到了版本号
            version_code = version_ele.select("div[class='g4'] h4")
            if len(version_code):
                version_value['version_code'] = version_code[0].get_text()
                # print(version_code[0].get_text())

            # get publish date
            version_build_date = version_ele.select("div[class='g4'] p")
            if len(version_build_date):
                version_value['version_build_date'] = version_build_date[0].get_text()
                # print(version_build_date[0].get_text())

            # Unity Hub
            unityhub = version_ele.select("a[class='btn bg-gr left fw500 unityhub']")
            if len(unityhub) > 0:
                version_value['unity_hub_url'] = unityhub[0]["href"]

            version_select_box = version_ele.select(
                "div[class='select-box light link-list rel']"
            )
            mac_index = 0
            for version_platform in version_select_box:
                # get platform
                platform = version_platform.select("div[class='trigger']")
                temp_list = []
                if len(platform):
                    # get download url
                    # tem = platform[0].get_text()
                    if mac_index | 0 == 0:
                        # if str.lower(tem).find('(mac)'):
                        # mac
                        version_value['platform']['mac'] = temp_list
                        for target_list in version_platform.select("ul[class='options'] a"):
                            temp_list.append({'key': target_list.get_text(), 'value': target_list["href"]})
                    else:
                        # win
                        version_value['platform']['win'] = temp_list
                        for target_list in version_platform.select("ul[class='options'] a"):
                            temp_list.append({'key': target_list.get_text(), 'value': target_list["href"]})
                mac_index += 1
            result[version].append(version_value)
    return result


# generate md file
def generate(dict):
    result = []
    for big_version_key, big_version_value in dict.items():
        line = ['## Unity ' + big_version_key.replace('version-', '') + '.x']

        for version_value in big_version_value:
            line.append("\n### Unity Version :" + version_value['version_code'])
            line.append("\tPublish Date :" + version_value['version_build_date'])
            line.append("\n> Unity Hub :" + version_value['unity_hub_url'])
            line.append('\n\n')
            win_list = version_value['platform']['win']
            line.append('### Windows \n\n')
            for item in win_list:
                line.append("> " + item['key'] + '   ' + item['value'] + '\n\n')
            mac_list = version_value['platform']['mac']
            line.append('### Mac \n\n')
            for item in mac_list:
                line.append("> " + item['key'] + '   ' + item['value'] + '\n\n')
        result.append(''.join(line))
    return '\n\n'.join(result)


res = decode(download_web())

res = generate(res)

# save list
fo = open("download.md", "w+")
fo.write(res)
# close file
fo.close()

print('ok')
