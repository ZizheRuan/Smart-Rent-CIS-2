from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .models import Property, Agency, Resource
from .realestate_crawler import real_estate_crawler
from django.views.decorators import csrf
from .models import Property,Agency,Resource
from decimal import Decimal
import random
import re


# Create your views here.
def indexView(request):
    template_name = "webapp/index.html"
    return render(request,template_name)

def getData(request):
    print('hahahha')
    data = real_estate_crawler.gather_information(1, 'melbourne')
    page = data[0]
    agent_name = page['agent']
    agent_img = page['agentPic']
    house_type = page['houseType']
    original_link = page['urlDetail']
    house_img = page['housePic']
    price = page['price']
    location = page['location']
    bed = page['bed']
    bath = page['bathroom']
    showDataTemplate='webapp/showData.html'
    return render(request, showDataTemplate, {'page': page, 'agent_name': agent_name, 'agent_img': agent_img, 'house_type': house_type,
                                              'original_link': original_link, 'house_img': house_img, 'price': price,
                                              'location': location, 'bed': bed, 'bath': bath})


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
                'property__distance_umel').select_related(
                'property').select_related('agency')
        elif match_rmit:
            print('match_rmit')
            result_basic = Resource.objects.filter(property__distance_rmit__lt=10000).order_by(
                'property__distance_rmit').select_related(
                'property').select_related('agency')
        else:
            print('match_other')
            result_basic = Resource.objects.filter(property__address__contains=str(searhInput)).select_related(
                'property').select_related('agency')

        # result_basic = result_basic.distinct(result_basic,result_basic.property.address)
        for each in result_basic:
            print(each.price + '   ' + str(each.property.no_bed)+ '   ' +' Distance-umel: '+str(each.property.distance_umel)
                  +' Distance-rmit: '+str(each.property.distance_rmit))

        searchResultTemplate = 'webapp/searchBasic.html'
        return render(request, searchResultTemplate, {'result_basic': result_basic})


def search_advanced(request):
    if request.POST:
        advanced_input = {
            'uniName': request.POST['uni-name'],
            'houseType': request.POST['house-type'],
            'maxPrice': request.POST['max-price'],
            'bedNum': request.POST['bed-num']
        }

        if advanced_input['uniName'] == 'University of Melbourne' :
            result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_umel__lt=10000).select_related('agency').order_by('property__distance_umel')

        elif advanced_input['uniName'] == 'RMIT University' :
            result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                property__no_bed__exact=advanced_input['bedNum']).filter(property__distance_rmit__lt=10000).select_related('agency').order_by('property__distance_rmit')

        else:
            result_advanced = Resource.objects.filter(price__lt=advanced_input['maxPrice']).select_related('property').filter(property__house_type__exact=advanced_input['houseType']).filter(
                property__no_bed__exact=advanced_input['bedNum']).select_related('agency').order_by('price')

        print(result_advanced)
        for each in result_advanced:
            print(each.price + '   ' + str(each.property.no_bed)+'   ' + str(each.property.house_type)+' Distance-umel: '+str(each.property.distance_umel)
                  +' Distance-rmit: '+str(each.property.distance_rmit))

        print('***************')
        print(advanced_input)
        print('***************')
        searchResultTemplate = 'webapp/searchAdvanced.html'
        # return render(request,searchResultTemplate,{'advanced_input':advanced_input})
        return render(request, searchResultTemplate, {'result_advanced': result_advanced, 'uniName': advanced_input['uniName']})

def saveToTable(request) :
    crawled_info = real_estate_crawler.gather_information(1, 'melbourne')
    size = len(crawled_info)
    pList = []
    aList = []
    rList = []
    for i in range(0, size):
        feature = crawled_info[i]
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
        pList[i].no_bath = feature['bathroom']
        pList[i].house_type = feature['houseType']

        random.seed(a=None, version=2)
        random1 = random.randint(200,10000)
        random2 = random.randint(200,10000)
        pList[i].distance_umel = random1
        pList[i].distance_rmit = random2
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
        rList[i].price = feature['price']
        rList[i].save()
        print(rList[i])
        print('r is saved')

    showResultTemplate = 'webapp/showResult.html'
    return render(request, showResultTemplate, {'crawled_info':crawled_info})

def queryTable(request):
    # rr = Resource.objects.filter(price__lt=500)

    # ---------------------------------
    # rr = Resource.objects.filter(price__lt=500).select_related('property').select_related('agency').filter(propertyproperty__no_bed__exact=2)
    # print(rr)
    # for each in rr:
    #     print(each.price +'   ' + str(each.property.no_bed))
    # ---------------------------------

    # rr_filtered = rr.values()
    # print(rr_filtered)
    # for eachrr in rr:
    #     eachpp = eachrr.property_set.all()
    #     print(eachpp)
    # ppReady = pp.filter(address__contains='1').filter(no_bed__contains='2')
    # print(ppReady)
    showQuery = 'webapp/showQuery.html'
    return render(request, showQuery)


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



