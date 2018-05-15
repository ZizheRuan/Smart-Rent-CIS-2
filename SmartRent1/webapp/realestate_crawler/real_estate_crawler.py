import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool


# 用来爬取realestate信息,获取单个页面信息
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 从返回的页面数据中用正则表达式提取所需信息
def parse_one_page(html):

    # re.S 表示可以匹配任意的字符
    pattern = re.compile('data-featured-status.*?<a href="(.*?)" >' +
                         '.*?property-(.*?)-'
                         '.*?data-src="(.*?)"' +
                         '.*?agent-photo" src="(.*?)"' +
                         '.*?title="(.*?),' +
                         '\s(.*?)"' +
                         # '.*?priceText">(.*?)<' +
                         '.*?"priceText">\$(\d.*?\d+).*?</p>' +     ### get price; type = int
                         '.*?listingName.>(.*?)<' +
                         '.*?Bedrooms</span></dt> <dd>(\d+)<' +
                         '.*?Bathrooms</span></dt> <dd>(\d+)<', re.S)
    items = re.findall(pattern, html)

    # 格式化，变成字典
    for item in items:
        yield {
            'urlDetail': 'https://www.realestate.com.au' + item[0],
            'houseType': item[1],
            'housePic': item[2],
            'agentPic': item[3],
            'agentPeople': item[4],
            'agentCompany': item[5],
            'price': item[6],
            'location': item[7],
            'bed': item[8],
            'bathroom': item[9]
        }


# 写入文档
# 文档格式为txt
# encoding = 'utf-8'
# ensure_ascii = False
# 确保写入的是中文而不是ascii码
def write_to_file(content):
    with open('result.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()


# 写入文档，格式为CSV
def write_to_csv(content):
    with open('result.csv', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')
        f.close()


# 返回房源信息，需要输入两个参数：
#   pagenumber参数表示要获取多少页房源信息
#   cityName参数表示搜索的区域
# 可以增加其他参数，如'邮编'等
# return a list, which contain house_info （dictionary type)
def gather_information(pageNumber, cityName):
    if pageNumber <= 1:
        pageNumber = 1
    house_info = []
    for currentPage in range(pageNumber):
        url = 'https://www.realestate.com.au/rent/in-' + cityName + ',+vic/list-' + str(currentPage+1)
        html = get_one_page(url)
        parsePage = parse_one_page(html)
        currentPage += 1
        i = 0
        for item in parsePage:
            write_to_file(item)
            house_info.append(item)
            i += 1
    # print(house_info)
    return house_info

# gather_information(1, 'melbourne')
# -------------多线程，提升速度，需要修改
# def info_return(page_number):
#     pool = Pool()
#     resultlist = pool.map(gather_information, range(page_number))
#     write_to_file(resultlist)
#     return resultlist
