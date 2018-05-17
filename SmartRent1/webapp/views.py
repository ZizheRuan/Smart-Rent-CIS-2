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
            result_basic = Resource.objects.filter(property__distance_umel__lt=10000).order_by(
                'property__distance_umel', '-property__no_bed', '-property__no_bath').select_related(
                'property').select_related('agency')
            uniName = 'University of Melbourne'
        elif match_rmit:
            print('match_rmit')
            result_basic = Resource.objects.filter(property__distance_rmit__lt=10000).order_by(
                'property__distance_rmit', '-property__no_bed', '-property__no_bath').select_related(
                'property').select_related('agency')
            uniName = 'RMIT University'
        else:
            print('match_other')
            result_basic = Resource.objects.filter(property__address__contains=str(searhInput)).select_related(
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
            'bedNum': request.POST['bed-num']
        }
        if advanced_input['houseType'] == 'any':
            if advanced_input['uniName'] == 'University of Melbourne':
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related(
                    'property').filter(
                    property__no_bed__exact=advanced_input['bedNum']).filter(
                    property__distance_umel__lt=10000).select_related('agency').order_by('property__distance_umel', '-property__no_bed', '-property__no_bath')

            elif advanced_input['uniName'] == 'RMIT University':
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related(
                    'property').filter(
                    property__no_bed__exact=advanced_input['bedNum']).filter(
                    property__distance_rmit__lt=10000).select_related('agency').order_by('property__distance_rmit', '-property__no_bed', '-property__no_bath')
            else:
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related(
                    'property').filter(
                    property__no_bed__exact=advanced_input['bedNum']).select_related('agency').order_by('price', '-property__no_bed', '-property__no_bath')
        else:
            if advanced_input['uniName'] == 'University of Melbourne' :
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                    property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_umel__lt=10000).select_related('agency').order_by('property__distance_umel', '-property__no_bed', '-property__no_bath')

            elif advanced_input['uniName'] == 'RMIT University' :
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                    property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_rmit__lt=10000).select_related('agency').order_by('property__distance_rmit', '-property__no_bed', '-property__no_bath')

            else:
                result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
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

        random.seed(a=None, version=2)
        random1 = random.randint(200,10000)
        random2 = random.randint(200,10000)
        random3 = random.randint(15,95)
        random4 = random.randint(15,95)
        pList[i].distance_umel = random1
        pList[i].distance_rmit = random2
        pList[i].duration_umel = random3
        pList[i].duration_rmit = random4
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


import csv
from django.http import HttpResponse

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