from pyquery import PyQuery as pq
import re
import csv



def parse_one_page(pageNumber):

    url = 'https://www.realestate.com.au/rent/in-melbourne,+vic/list-' + str(pageNumber)
    page = pq(url= url)
    ariticle = page('article').items()
    for item in ariticle:
        house_type_info = item.find('a').attr('href')
        find_house_type = re.search('-(.*?)-', house_type_info, re.M).group(1)
        price_info = item.find('p').text()
        test = re.sub('\D', '', price_info)
        if test == '':
            pass
        elif int(test) < 30:
            test = ''
        elif 10009> int(test) > 4000:
            test = test[0:3]
        elif 18000 > int(test) > 10011:
            test = test[0:4]
        elif 18000 < int(test):
            test = test[0:3]
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
            'price': test,
            'location': item.find('img').eq(1).attr('alt'),
            'bed': item.find('dd').eq(0).text(),
            'bathroom': item.find('dd').eq(1).text(),
            'carpark': item.find('dd').eq(2).text(),
            'agentCompanyPic': item.find('a img').attr('src'),


        }




def gather_realestate_info(pageNumber):
    house_info = []
    i = 0
    with open('realestate.csv', 'w') as f:
        for currentPage in range(pageNumber):
            currentPage += 1
            data = parse_one_page(currentPage)
            print(currentPage)
            for item in data:
                house_info.append(item)
                i += 1
                w = csv.DictWriter(f, item.keys())
                if i == 1:
                    w.writeheader()
                    w.writerow(item)
                else:
                    w.writerow(item)

    return house_info


#
# gather_realestate_info(40)

