from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import Property, Agency, Resource
from .realestate_crawler import real_estate_crawler
from .realestate_crawler import domain_crawler
from django.views.decorators import csrf
from .models import Property,Agency,Resource
from decimal import Decimal
import random
import re
import csv
from django.http import HttpResponse
import googlemaps
from datetime import datetime
from os.path import dirname, abspath

# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)


def search_basic(request):
    if request.POST:
        searhInput = request.POST['basic-input']
        print('--------------')
        print(searhInput)
        print('--------------')

        match_umel = re.search("((?i)U(\w*\s*)*(MEL)\w*)|((?i)(MEL)(\w*\s*)*U\w*)", str(searhInput))
        match_rmit = re.search("((?i)R(\w*\s*)*M(\w*\s*)*I(\w*\s*)*T(\w*\s*)*)", str(searhInput))
        if match_umel:
            print('match_umel')
            result_basic = Resource.objects.filter(property__distance_umel__lt=10000).filter(price__gt=300).filter(price__lt=2000).order_by(
                'property__distance_umel', '-property__no_bed', '-property__no_bath').select_related(
                'property').select_related('agency')
            uniName = 'University of Melbourne'
        elif match_rmit:
            print('match_rmit')
            result_basic = Resource.objects.filter(property__distance_rmit__lt=10000).filter(price__gt=300).filter(price__lt=2000).order_by(
                'property__distance_rmit', '-property__no_bed', '-property__no_bath').select_related(
                'property').select_related('agency')
            uniName = 'RMIT University'
        else:
            print('match_other')
            result_basic = Resource.objects.filter(property__address__contains=str(searhInput)).filter(price__gt=300).filter(price__lt=2000).select_related(
                'property').select_related('agency').order_by('price', '-property__no_bed', '-property__no_bath')
            uniName = 'Any'

        # result_basic = result_basic.distinct(result_basic,result_basic.property.address)

        searchResultTemplate = 'webapp/searchBasic.html'
        return render(request, searchResultTemplate, {'result_basic': result_basic, 'uniName': uniName})


def search_advanced(request):
    if request.POST:
        advanced_input = {
            'uniName': request.POST['uni-name'],
            'houseType': request.POST['house-type'],
            'maxPrice': request.POST['max-price'],
            'bedNum': request.POST['bed-num'],
            'distanceRange': request.POST['distance-range']
        }

        if advanced_input['maxPrice']== '' :
            print('empty price found')
            advanced_input['maxPrice'] = 2000
            print(advanced_input['maxPrice'])

        if advanced_input['bedNum']== '' :
            if advanced_input['houseType'] == 'any':
                if advanced_input['uniName'] == 'University of Melbourne':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related(
                        'property').filter(
                        property__distance_umel__lt=advanced_input['distanceRange']).select_related('agency').order_by(
                        'property__distance_umel', '-property__no_bath')

                elif advanced_input['uniName'] == 'RMIT University':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related(
                        'property').filter(
                        property__distance_rmit__lt=advanced_input['distanceRange']).select_related('agency').order_by(
                        'property__distance_rmit', '-property__no_bath')
                else:
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related(
                        'property').select_related('agency').order_by('price', '-property__no_bath')
            else:
                if advanced_input['uniName'] == 'University of Melbourne':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related('property').filter(
                        property__house_type__exact=advanced_input['houseType']).filter(
                        property__distance_umel__lt=advanced_input['distanceRange']).select_related('agency').order_by(
                        'property__distance_umel', '-property__no_bath')

                elif advanced_input['uniName'] == 'RMIT University':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related('property').filter(
                        property__house_type__exact=advanced_input['houseType']).filter(
                        property__distance_rmit__lt=advanced_input['distanceRange']).select_related('agency').order_by(
                        'property__distance_rmit', '-property__no_bath')

                else:
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(
                        price__gt=300).filter(price__lt=2000).select_related('property').filter(
                        property__house_type__exact=advanced_input['houseType']).select_related('agency').order_by('price', '-property__no_bath')
        else:
            if advanced_input['houseType'] == 'any':
                if advanced_input['uniName'] == 'University of Melbourne':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related(
                        'property').filter(
                        property__no_bed__exact=advanced_input['bedNum']).filter(
                        property__distance_umel__lt=advanced_input['distanceRange']).select_related('agency').order_by('property__distance_umel', '-property__no_bed', '-property__no_bath')

                elif advanced_input['uniName'] == 'RMIT University':
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related(
                        'property').filter(
                        property__no_bed__exact=advanced_input['bedNum']).filter(
                        property__distance_rmit__lt=advanced_input['distanceRange']).select_related('agency').order_by('property__distance_rmit', '-property__no_bed', '-property__no_bath')
                else:
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related(
                        'property').filter(
                        property__no_bed__exact=advanced_input['bedNum']).select_related('agency').order_by('price', '-property__no_bed', '-property__no_bath')
            else:
                if advanced_input['uniName'] == 'University of Melbourne' :
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                        property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_umel__lt=advanced_input['distanceRange']).select_related('agency').order_by('property__distance_umel', '-property__no_bed', '-property__no_bath')

                elif advanced_input['uniName'] == 'RMIT University' :
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                        property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_rmit__lt=advanced_input['distanceRange']).select_related('agency').order_by('property__distance_rmit', '-property__no_bed', '-property__no_bath')

                else:
                    result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).filter(price__gt=300).filter(price__lt=2000).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                        property__no_bed__exact=advanced_input['bedNum']).select_related('agency').order_by('price', '-property__no_bed', '-property__no_bath')

        print(result_advanced)

        print('***************')
        print(advanced_input)
        print('***************')
        searchResultTemplate = 'webapp/searchAdvanced.html'
        # return render(request,searchResultTemplate,{'advanced_input':advanced_input})
        return render(request, searchResultTemplate, {'result_advanced': result_advanced, 'uniName': advanced_input['uniName']})


def saveToTable(request) :
    print('save to table function begin')
    # crawled_info = real_estate_crawler.gather_realestate_info(150)
    crawled_info = domain_crawler.gather_domain_info(47)
    print('crawling finished')
    size = len(crawled_info)
    pList = []
    aList = []
    rList = []
    i = 0
    # i = 574
    # for i in range(0, size):

    existed = []

    for feature in crawled_info:
        # print('loop begin')
        # feature = crawled_info[i]
        # print('saving crawled_info'+str(i))
        if ((feature['location'] is None)
            or(feature['housePic'] is None)or(feature['bed'] is None)
                                                                             or(feature['bathroom'] is None)
                                                                                or (feature['houseType'] is None)
                                                                                    or (feature['agentPeople'] is None)
                                                                                        or (
                        feature['agentPic'] is None)or(feature['agentPic']=='null')or(feature['agentCompany'] is None)or(feature['urlDetail'] is None)
                                                                                        or (
                                    feature['price'] == '99999')or(feature['price'] is None)or(feature['price'] == '')) is True:
            print('failure found')
            continue


        elif feature['location'] not in existed:
            existed.append(feature['location'])
            print ('True')
        else:
            print('False')
            continue


        print('success found No.'+str(i))
        pList.append(Property())
        aList.append(Agency())
        rList.append(Resource())
        pList[i].address = feature['location']
        pList[i].house_img = feature['housePic']
        pList[i].loc_rating = 5
        pList[i].fac_rating = 5
        pList[i].tran_rating = 5
        pList[i].comment = 'good'
        pList[i].no_bed = feature['bed']
        pList[i].no_bath = 1
        if feature['bathroom'] != '' :
            pList[i].no_bath = feature['bathroom']
        pList[i].house_type = feature['houseType']

        # random.seed(a=None, version=2)
        # random1 = random.randint(200,10000)
        # random2 = random.randint(200,10000)
        # random3 = random.randint(15,95)
        # random4 = random.randint(15,95)
        # pList[i].distance_umel = random1
        # pList[i].distance_rmit = random2
        # pList[i].duration_umel = random3
        # pList[i].duration_rmit = random4
        pList[i].save()

        aList[i].name = feature['agentPeople']
        aList[i].agent_img = feature['agentPic']
        aList[i].company = feature['agentCompany']
        aList[i].company_logo = 'https://www.siasat.com/wp-content/uploads/2017/11/real-estate.jpg'
        aList[i].fri_rating = 5
        aList[i].res_rating = 5
        aList[i].bond_rating = 5
        aList[i].comment = 'good'
        aList[i].save()

        rList[i].property = pList[i]
        rList[i].agency = aList[i]
        rList[i].link = feature['urlDetail']
        # ===================================================
        rList[i].price = int(feature['price'])

        # ===================================================
        # replaced1 = re.sub(r'\,', '', feature['price'])
        # replaced2 = re.sub(r'p', '', replaced1)
        # replaced3 = re.sub(r'w', '', replaced2)
        # replaced4 = re.search('\w{4}|(\w{3})',replaced3,re.IGNORECASE).group(1)
        # if replaced4 is None:
        #     replaced4 = re.search('(\w{4})|\$(\w{3})', replaced3, re.IGNORECASE).group(1)
        # rList[i].price = replaced4
        # print(feature['price']+'==========>>>'+replaced1+'==========>>>'+replaced4)
        # ===================================================

        rList[i].save()
        print(rList[i])
        print('r is saved')
        i = i+1

    showResultTemplate = 'webapp/showResult.html'
    return render(request, showResultTemplate, {'crawled_info':crawled_info})


def aboutView(request):
    return render(request,'webapp/about.html')


def detailView(request,id):
    resource = get_object_or_404(Resource,pk=id)
    return render(request,'webapp/detail.html',{'resource':resource})


def updateView(request):
    if request.POST:
        ratings = {
            'loc-rating': request.POST['loc-rating'],
            'fac-rating': request.POST['fac-rating'],
            'tran-rating': request.POST['tran-rating'],
            'fri-rating': request.POST['fri-rating'],
            'res-rating': request.POST['res-rating'],
            'bond-rating': request.POST['bond-rating'],
            'resource-id': request.POST['resource-id'],
        }

        property_to_update_rating = Property.objects.get(pk=ratings['resource-id'])
        agency_to_update_rating = Agency.objects.get(pk=ratings['resource-id'])

        property_to_update_rating.loc_rating = (  property_to_update_rating.loc_rating + Decimal(ratings['loc-rating'].strip('"'))  )/2
        property_to_update_rating.fac_rating = (  property_to_update_rating.fac_rating + Decimal(ratings['fac-rating'].strip('"'))  )/2
        property_to_update_rating.tran_rating = (  property_to_update_rating.tran_rating + Decimal(ratings['tran-rating'].strip('"'))  )/2

        agency_to_update_rating.fri_rating = (  agency_to_update_rating.fri_rating + Decimal(ratings['fri-rating'].strip('"'))  )/2
        agency_to_update_rating.res_rating = (  agency_to_update_rating.res_rating + Decimal(ratings['res-rating'].strip('"'))  )/2
        agency_to_update_rating.bond_rating = (  agency_to_update_rating.bond_rating + Decimal(ratings['bond-rating'].strip('"'))  )/2

        property_to_update_rating.save()
        agency_to_update_rating.save()

        # =========CODE TO RESET RATINGS TO 5 POINTS.========DO NOT DELETE==============
        # property_to_update_rating = Property.objects.get(pk=ratings['resource-id'])
        # agency_to_update_rating = Agency.objects.get(pk=ratings['resource-id'])
        # property_to_update_rating.loc_rating = 5
        # property_to_update_rating.fac_rating = 5
        # property_to_update_rating.tran_rating = 5
        # agency_to_update_rating.fri_rating = 5
        # agency_to_update_rating.res_rating = 5
        # agency_to_update_rating.bond_rating = 5
        # property_to_update_rating.save()
        # agency_to_update_rating.save()

        print(ratings)

        return render(request,'webapp/updateRatings.html',{'ratings':ratings})



def resetRatings(request):

    for i in range (1,1127):
        random.seed(a=None, version=2)

        property_to_update_rating = Property.objects.get(pk=i)
        agency_to_update_rating = Agency.objects.get(pk=i)
        property_decimal_loc = random.randint(0, 9)
        property_decimal_fac= random.randint(0, 9)
        property_decimal_tran= random.randint(0, 9)
        property_integer = random.randint(3, 4)
        property_to_update_rating.loc_rating = property_integer + 0.1*property_decimal_loc
        property_to_update_rating.fac_rating = property_integer + 0.1*property_decimal_fac
        property_to_update_rating.tran_rating = property_integer + 0.1*property_decimal_tran
        agency_decimal_loc = random.randint(0, 9)
        agency_decimal_fac = random.randint(0, 9)
        agency_decimal_tran = random.randint(0, 9)
        agency_integer = random.randint(3, 4)
        agency_to_update_rating.fri_rating = agency_integer + 0.1*agency_decimal_loc
        agency_to_update_rating.res_rating = agency_integer + 0.1*agency_decimal_fac
        agency_to_update_rating.bond_rating = agency_integer + 0.1*agency_decimal_tran
        property_to_update_rating.save()
        agency_to_update_rating.save()

        print(property_to_update_rating.loc_rating)

    # property_to_update_rating_93 = Property.objects.get(pk=93)
    # agency_to_update_rating_93 = Agency.objects.get(pk=93)
    # property_to_update_rating_93.loc_rating = 4.5
    # property_to_update_rating_93.fac_rating = 4.5
    # property_to_update_rating_93.tran_rating = 4.5
    # agency_to_update_rating_93.fri_rating = 4.8
    # agency_to_update_rating_93.res_rating = 4.8
    # agency_to_update_rating_93.bond_rating = 4.8
    #
    # property_to_update_rating_2 = Property.objects.get(pk=1125)
    # agency_to_update_rating_2 = Agency.objects.get(pk=1125)
    # property_to_update_rating_2.loc_rating = 4.5
    # property_to_update_rating_2.fac_rating = 4.5
    # property_to_update_rating_2.tran_rating = 4.5
    # agency_to_update_rating_2.fri_rating = 3.5
    # agency_to_update_rating_2.res_rating = 3.5
    # agency_to_update_rating_2.bond_rating = 3.5
    #
    # # print(agency_to_update_rating_93.fri_rating)
    # # print(agency_to_update_rating_2.fri_rating)
    #
    # print(property_to_update_rating_93.address)
    # print(property_to_update_rating_2.address)

    return render(request,'webapp/resetRatings.html')




def exportCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csvForDistance.csv"'

    writer = csv.writer(response)
    for i in range(14824,15909):
        property_to_write = Property.objects.get(pk=i)
        writer.writerow([i, property_to_write.address])
        print('object No.'+str(i)+'has been saved')
    print('writting finished')
    return response

#Never run getDistance function please!!(will change Database)
def getDistance(request):
    gmaps = googlemaps.Client(key='AIzaSyCuO8vC3nj-kg8a01oQxCMR11E5bJfFfB8')
    now = datetime.now()
    route = dirname(abspath(__file__)) + '/csvForDistance.csv'
    with open(route, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        column = [row[1] for row in reader]
    size_column = len(column)
    locationList = []
    for item in range(1125,size_column):
        locationList.append(column[item])
    i = 0
    j = 1126
    for location in locationList:
        direction1 = gmaps.directions('Union House, University of Melbourne, Tin Alley, Parkville VIC 3010', location,
                                    mode='walking', departure_time = now)
        direction2 = gmaps.directions('Building 80, Melbourne VIC 3004', location,
                                     mode='walking', departure_time=now)
        distance_umel = direction1[0]['legs'][0]['distance']['value']
        distance_rmit = direction2[0]['legs'][0]['distance']['value']
        duration_umel = direction1[0]['legs'][0]['duration']['text']
        duration_rmit = direction2[0]['legs'][0]['duration']['text']
        i += 1

        print("Hello  " + location + "  " + str(j))
        print("unimelb:  " + str(distance_umel))
        print("rmit:  " + str(distance_rmit))

        distance_umel_to_update = get_object_or_404(Property, pk=j)
        distance_umel_to_update.distance_umel = distance_umel
        distance_umel_to_update.save()

        distance_rmit_to_update = get_object_or_404(Property, pk=j)
        distance_rmit_to_update.distance_rmit = distance_rmit
        distance_rmit_to_update.save()

        duration_umel_to_update = get_object_or_404(Property, pk=j)
        duration_umel_to_update.duration_umel = duration_umel
        duration_umel_to_update.save()

        duration_rmit_to_update = get_object_or_404(Property, pk=j)
        duration_rmit_to_update.duration_rmit = duration_rmit
        duration_rmit_to_update.save()

        print("unimelb:  " + duration_umel)
        print("rmit:  " + duration_rmit)

        j += 1
        return render(request, 'webapp/distance.html')
