import re
from pyquery import PyQuery as pq
import json
import csv






def get_house(page_number):
    url = 'https://www.domain.com.au/rent/?ssubs=1&suburb=melbourne-vic-3000&page=' + str(page_number)
    doc = pq(url= url).html()
    # print(doc)
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
        test = re.sub('\D', '', item[2])
        if test == '':
            pass
        elif 99999 > int(test) > 4000:
            test = test[0:3]
        else:
            test = test [0:4]
            if int(test) > 2000:
                test = test [0:3]
        house_type = item[12]
        if len(house_type) > 7:
            house_type = house_type[0:9]
        agent_pic = item[4]
        if agent_pic == 'null':
            pass
        else:
            agent_pic = agent_pic[1:][:-1]

        yield {

            'urlDetail': 'https://www.domain.com.au' + item[0],
            # 'houseType': item[12],
            'houseType': house_type,
            'housePic': item[1],
            # 'agentPic': item[4],
            'agentPic': agent_pic,
            'agentPeople': item[5],
            'agentCompany': item[3],
            # 'price': item[2],
            'price': test,
            'location': item[6] + ',' + item[7] + ',' + item[8] + ',' + item[9],
            'bed': item[10],
            'bathroom': item[11]

        }



def gather_domain_info(startpageNUmber):
    house_info = []
    i = 0
    with open('domain.csv', 'w') as f:
        for currentPage in range(startpageNUmber):
            currentPage += 1
            file = get_house(currentPage)
            # file = open('result.txt', 'r').read()
            results = parse_one_page(file)
            print(currentPage)
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

    return house_info



gather_domain_info(20)