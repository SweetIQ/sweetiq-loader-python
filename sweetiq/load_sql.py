import pymysql
from config import db

def get_data_from_sql():
    """Gets the data from the database and returns a positions array of dicts
       that correspond to the expected format of SweetIQ's Location API. The Select
       does a part of the mapping using the 'as' aliases. Composition is done
       after we got the data below the request.
    """

    sql = """
        select
          loc_branchid as branch,
          loc_name as name,
          loc_bizcontact as businessContact_name,
          loc_emailcontact as businessContact_email,
          loc_sab as serviceArea,
          loc_addr1 as address,
          loc_addr2 as address_extended,
          loc_city as locality,
          loc_state as region,
          loc_zip as postCode,
          loc_country as country,
          loc_mall as mallName,
          loc_mainphone as phone,
          loc_fax as fax,
          loc_email as emailToPublish,
          loc_trackedwebsite as websiteToTrack,
          loc_publishedwebsite as websiteToPublish,
          loc_cat as categories,                       #comma separated list
          loc_hours as hoursOfOperation,
          loc_hoursadd as hoursAdditionalNotes,
          loc_payments as paymentMethods,
          loc_descsnippet as snippetDescription,
          loc_descshort as shortDescription,
          loc_desclong as longDescription,
          loc_keywords as keywords,
          loc_geo as geomodifiers,
          loc_dirpackage as dirPackage,
          loc_yearfounded as yearFounded,
          loc_info as otherInformation,
          loc_tags as tags,
          loc_logo as imgLogo,
          loc_banner as imgBanner,
          loc_images as imgOthers,
          loc_sabunit as serviceArea_unit,
          loc_sabdistance as serviceArea_distance,
          loc_sabregions as serviceArea_regions,        #comma separated list
          loc_distto as distributionTo,
          loc_distcc as distributionCC,
          loc_storeCode as storeCode,
          loc_brandname as brandName,
          loc_canceldate as canceldate,
          loc_closeddoorsdate as closedDoorsDate,
          loc_socialmediaurls as socialMediaUrls,       #comma separated list
          loc_alternativewebsites as alternateWebsites, #comma separated list
          loc_services as services,                     #comma separated list
          loc_suppresslistings as suppresslistings,
          loc_professional as isProfessional,
          loc_providedlatitude as latitude,
          loc_providedlongitude as longitude
        from location
          where client_id = 73
          and loc_status = 4
        limit 2
    """

    cursor = db.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    locations = []
    for row in cursor.fetchall():

        'We are mapping the results to dicts where the key is the colomn name'
        location = dict(zip(columns, row))
        locations.append(location)

        'We make the compositions for the other objects needed by the API'
        location['businessContact'] = {'name': location['businessContact_name'],
                                       'email': location['businessContact_email']}
        if location['alternateWebsites'] is not None:
            location['alternateWebsites'] = location['alternateWebsites'].split(',')
        if location['categories'] is not None:
            location['categories'] = location['categories'].split(',')
        if location['keywords'] is not None:
            location['keywords'] = location['keywords'].split(',')
        if location['tags'] is not None:
            location['tags'] = location['tags'].split(',')
        if location['imgOthers'] is not None:
            location['imgOthers'] = location['imgOthers'].split(',')
        if location['paymentMethods'] is not None:
            location['paymentMethods'] = location['paymentMethods'].split(',')
        location['serviceArea'] = {'distance': location['serviceArea_distance'],
                                'unit': location['serviceArea_unit']}
        if location['serviceArea_regions'] is not None:
            location['serviceArea_regions'] = location['serviceArea_regions'].split(',')
        if location['services'] is not None:
            location['services'] = location['services'].split(',')
        if location['socialMediaUrls'] is not None:
            socialMediaUrls = location['socialMediaUrls']
            location['socialMediaUrls'] = {}
            for url in socialMediaUrls.split(','):
                if 'facebook' in url:
                    location['socialMediaUrls']['facebook'] = url
                if 'twitter' in url:
                    location['socialMediaUrls']['twitter'] = url
                if 'foursquare' in url:
                    location['socialMediaUrls']['foursquare'] = url
                if 'yelp' in url:
                    location['socialMediaUrls']['yelp'] = url

        location['hoursOfOperationRaw'] = location['hoursOfOperation']
        del location['hoursOfOperation']

    return locations
