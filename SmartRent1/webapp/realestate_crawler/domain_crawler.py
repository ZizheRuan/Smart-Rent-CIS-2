import re
from pyquery import PyQuery as pq
import json
import csv






def get_house(page_number):
    url = 'https://www.domain.com.au/rent/?ssubs=1&suburb=melbourne-vic-3000&page=' + str(page_number)
    doc = pq(url= url).html()
    return doc


def parse_one_page(html):

    pattern = re.compile(
        'listingModel.*?url":"(.*?)"'
        + '.*?images":\["(.*?)"'
        + '.*?price":"(\$.*?)"'
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




def write_to_file_list(content):
    with open('domain_result.txt', 'wb') as f:
        for item in content:
            f.write(item)
        f.close()
        # f.write(json.dumps(content) + '\n')
        # f.write(content)
        # f.close()


def gather_domain_info(startpageNUmber):
    house_info = []
    with open('domain.csv', 'w') as f:
        for currentPage in range(startpageNUmber):
            currentPage += 1
            file = get_house(currentPage)
            # file = open('result.txt', 'r').read()
            results = parse_one_page(file)

            i = 0

            for item in results:
                # print(item)
                # write_to_file(item)
                house_info.append(item)
                i += 1
                w = csv.DictWriter(f, item.keys())
                if i == 1:
                    w.writeheader()
                    w.writerow(item)
                else:
                    w.writerow(item)

    # print(house_info)
    # print(type(house_info))
    # write_to_file_list(house_info)
    return house_info



# gather_domain_info(5)
