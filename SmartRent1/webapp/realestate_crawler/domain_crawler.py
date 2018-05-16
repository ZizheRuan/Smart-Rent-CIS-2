from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pq
import json






def get_house(page_number):
    brower = webdriver.Chrome()
    wait = WebDriverWait(brower, 20)
    brower.get('https://www.domain.com.au/rent/?ssubs=1&suburb=melbourne-vic-3000&page=' + str(page_number))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results__main ul.search-results__results li.search-results__listing')))
    html = brower.page_source
    doc = pq(html).html()
    return doc


def parse_one_page(html):

    pattern = re.compile(
        'listingModel.*?url":"(.*?)"'
        + '.*?images":\["(.*?)"'
        + '.*?price":"\$(.*?)"'
        + '.*?brandName":"(.*?)"'
        + '.*?agentPhoto":(.*?),'
        + '.*?agentName":"(.*?)"'
        + '.*?address":{"street":"(.*?)"'
        + '.*?suburb":"(.*?)"'
        + '.*?state":"(.*?)"'
        + '.*?postcode":"(.*?)"'
        + '.*?beds":(.*?),'
        + '.*?baths":(.*?),'
        + '.*?propertyType":"(.*?)"'

    )

    items = re.findall(pattern, html)
    for item in items:
        yield {

            'urlDetail': 'https://www.domain.com.au' + item[0],
            'houseType': item[12],
            'housePic': item[1],
            'agentPic': item[4],
            'agentPeople': item[5],
            'agentCompany': item[3],
            'price': item[2],
            'location': item[6] + ',' + item[7] + ',' + item[8] + ',' + item[9],
            'bed': item[10],
            'bathroom': item[11]

        }


# def gather_domain_info(pageNumber):
#
#     if pageNumber <=1 :
#         pageNumber = 1
#     house_info = []
#     for currentPage in range(pageNumber):
#         url = 'https://www.domain.com.au/rent/?ssubs=1&suburb=melbourne-vic-3000&page=' + str(currentPage + 1)
#         file = get_house(url)
#         result = parse_one_page(file)
#         currentPage += 1
#         i = 0
#         for item in result:
#             house_info.append(item)
#             i += 1
#
#     return house_info
#
# gather_domain_info(1)

def write_to_file(content):
    with open('result.txt', 'a') as f:
        f.write(json.dumps(content) + '\n')
        f.close()


def gather_domain_info(pageNUmber):
    house_info = []
    for currentPage in range(pageNUmber):
        currentPage += 1
        file = get_house(currentPage)
        # file = open('result.txt', 'r').read()
        results = parse_one_page(file)

        i = 0
        for item in results:
            print(item)
            # write_to_file(item)
            house_info.append(item)
            i += 1
    return house_info



gather_domain_info(5)
