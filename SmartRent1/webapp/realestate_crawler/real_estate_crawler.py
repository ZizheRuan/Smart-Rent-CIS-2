from pyquery import PyQuery as pq
import re
import csv



def parse_one_page(pageNumber, cityName):

    url = 'https://www.realestate.com.au/rent/in-' + cityName + ',+vic/list-' + str(pageNumber)
    # url = 'https://www.realestate.com.au/rent/in-melbourne,+vic/list-' + str(pageNumber)
    page = pq(url= url)
    ariticle = page('article').items()
    for item in ariticle:


        house_type_info = item.find('a').attr('href')
        find_house_type = re.search('-(.*?)-', house_type_info, re.M).group(1)
        price_info = item.find('p').text()
        find_price = re.search('\$(.*?)\s', price_info, re.M)
        if find_price == None:
            find_price = 99999
        else:
            find_price = find_price.group(1)
        agent_people_info = item.find('div .agent-wrapper img').attr('alt')
        if agent_people_info != None:
            find_agent_people = re.search('(.*?),', agent_people_info, re.M).group(1)
        else:
            find_agent_people = None
        yield {

            'urlDetail': 'https://www.realestate.com.au' + item.find('a').attr('href'),
            'houseType': find_house_type,
            'housePic': item.find('img').eq(2).attr('data-src'),
            'agentPic': item.find('div .agent-wrapper img').attr('src'),
            'agentPeople': find_agent_people,
            'agentCompany': item.find('img').attr('alt'),
            'price': find_price,
            'location': item.find('img').eq(1).attr('alt'),
            'bed': item.find('dd').eq(0).text(),
            'bathroom': item.find('dd').eq(1).text(),
            'carpark': item.find('dd').eq(2).text(),
            'agentCompanyPic': item.find('a img').attr('src'),


        }


        # return house_info




def gather_realestate_info(pageNumber, cityName):
    # currentPage = 0
    house_info = []
    i = 0
    with open('realestate.csv', 'w') as f:
        for currentPage in range(pageNumber):
            currentPage += 1
            data = parse_one_page(currentPage, cityName)

            for item in data:
                house_info.append(item)
                i += 1
                w = csv.DictWriter(f, item.keys())
                if i == 1:
                    w.writeheader()
                    w.writerow(item)
                    # print('start')
                else:
                    w.writerow(item)
                    # print(i)

    return house_info

# gather_realestate_info(100, 'melbourne')















# import requests
# from requests.exceptions import RequestException
# import re
# import json
# from multiprocessing import Pool
#
#
# # 用来爬取realestate信息,获取单个页面信息
# def get_one_page(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None
#
# # 从返回的页面数据中用正则表达式提取所需信息
# def parse_one_page(html):
#
#     # re.S 表示可以匹配任意的字符
#     pattern = re.compile('data-featured-status.*?<a href="(.*?)" >' +
#                          '.*?property-(.*?)-'
#                          '.*?data-src="(.*?)"' +
#                          '.*?agent-photo" src="(.*?)"' +
#                          '.*?title="(.*?),' +
#                          '\s(.*?)"' +
#                          # '.*?priceText">(.*?)<' +
#                          '.*?"priceText">\$(\d.*?\d+).*?</p>' +     ### get price; type = int
#                          '.*?listingName.>(.*?)<' +
#                          '.*?Bedrooms</span></dt> <dd>(\d+)<' +
#                          '.*?Bathrooms</span></dt> <dd>(\d+)<', re.S)
#     items = re.findall(pattern, html)
#
#     # 格式化，变成字典
#     for item in items:
#         yield {
#             'urlDetail': 'https://www.realestate.com.au' + item[0],
#             'houseType': item[1],
#             'housePic': item[2],
#             'agentPic': item[3],
#             'agentPeople': item[4],
#             'agentCompany': item[5],
#             'price': item[6],
#             'location': item[7],
#             'bed': item[8],
#             'bathroom': item[9]
#         }
#
#
# # 写入文档
# # 文档格式为txt
# # encoding = 'utf-8'
# # ensure_ascii = False
# # 确保写入的是中文而不是ascii码
# def write_to_file(content):
#     with open('realestate_result.txt', 'a', encoding = 'utf-8') as f:
#         f.write(json.dumps(content, ensure_ascii = False) + '\n')
#         f.close()
#
#
# # 写入文档，格式为CSV
# def write_to_csv(content):
#     with open('result.csv', 'a', encoding = 'utf-8') as f:
#         f.write(json.dumps(content, ensure_ascii = False) + '\n')
#         f.close()
#
#
# # 返回房源信息，需要输入两个参数：
# #   pagenumber参数表示要获取多少页房源信息
# #   cityName参数表示搜索的区域
# # 可以增加其他参数，如'邮编'等
# # return a list, which contain house_info （dictionary type)
# def gather_information(pageNumber, cityName):
#     house_info = []
#     for currentPage in range(pageNumber):
#         url = 'https://www.realestate.com.au/rent/in-' + cityName + ',+vic/list-' + str(currentPage+1)
#         html = get_one_page(url)
#         parsePage = parse_one_page(html)
#         currentPage += 1
#         i = 0
#         for item in parsePage:
#             write_to_file(item)
#             house_info.append(item)
#             i += 1
#     return house_info
#
