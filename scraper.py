import requests 
import json 
import pandas as pd 

class RealtorScraper:
    def __init__(self, page_numbers: int) -> None:
        self.page_numbers = page_numbers
    
    def send_request(self, page_number: int, offset_parameter: int) -> dict:

        url = "https://www.realtor.com/api/v1/hulk?client_id=rdc-x&schema=vesta"
        headers = {"content-type": "application/json"}

        body = r'{"query":"\n\nquery ConsumerSearchMainQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $sort_type: SearchSortType, $client_data: JSON, $geoSupportedSlug: String!, $bucket: SearchAPIBucket, $by_prop_type: [String])\n{\n  home_search: home_search(query: $query,\n    sort: $sort,\n    limit: $limit,\n    offset: $offset,\n    sort_type: $sort_type,\n    client_data: $client_data,\n    bucket: $bucket,\n  ){\n    count\n    total\n    results {\n      property_id\n      list_price\n      primary_photo (https: true){\n        href\n      }\n      source {\n        id\n        agents{\n          office_name\n        }\n        type\n        spec_id\n        plan_id\n      }\n      community {\n        property_id\n        description {\n          name\n        }\n        advertisers{\n          office{\n            hours\n            phones {\n              type\n              number\n            }\n          }\n          builder {\n            fulfillment_id\n          }\n        }\n      }\n      products {\n        brand_name\n        products\n      }\n      listing_id\n      matterport\n      virtual_tours{\n        href\n        type\n      }\n      status\n      permalink\n      price_reduced_amount\n      other_listings{rdc {\n      listing_id\n      status\n      listing_key\n      primary\n    }}\n      description{\n        beds\n        baths\n        baths_full\n        baths_half\n        baths_1qtr\n        baths_3qtr\n        garage\n        stories\n        type\n        sub_type\n        lot_sqft\n        sqft\n        year_built\n        sold_price\n        sold_date\n        name\n      }\n      location{\n        street_view_url\n        address{\n          line\n          postal_code\n          state\n          state_code\n          city\n          coordinate {\n            lat\n            lon\n          }\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      tax_record {\n        public_record_id\n      }\n      lead_attributes {\n        show_contact_an_agent\n        opcity_lead_attributes {\n          cashback_enabled\n          flip_the_market_enabled\n        }\n        lead_type\n      }\n      open_houses {\n        start_date\n        end_date\n        description\n        methods\n        time_zone\n        dst\n      }\n      flags{\n        is_coming_soon\n        is_pending\n        is_foreclosure\n        is_contingent\n        is_new_construction\n        is_new_listing (days: 14)\n        is_price_reduced (days: 30)\n        is_plan\n        is_subdivision\n      }\n      list_date\n      last_update_date\n      coming_soon_date\n      photos(limit: 2, https: true){\n        href\n      }\n      tags\n      branding {\n        type\n        photo\n        name\n      }\n    }\n  }\n  geo(slug_id: $geoSupportedSlug) {\n    parents {\n      geo_type\n      slug_id\n      name\n    }\n    geo_statistics(group_by: property_type) {\n      housing_market {\n        by_prop_type(type: $by_prop_type){\n          type\n           attributes{\n            median_listing_price\n            median_lot_size\n            median_sold_price\n            median_price_per_sqft\n            median_days_on_market\n          }\n        }\n        listing_count\n        median_listing_price\n        median_rent_price\n        median_price_per_sqft\n        median_days_on_market\n        median_sold_price\n        month_to_month {\n          active_listing_count_percent_change\n          median_days_on_market_percent_change\n          median_listing_price_percent_change\n          median_listing_price_sqft_percent_change\n        }\n      }\n    }\n    recommended_cities: recommended(query: {geo_search_type: city, limit: 20}) {\n      geos {\n        ... on City {\n          city\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_neighborhoods: recommended(query: {geo_search_type: neighborhood, limit: 20}) {\n      geos {\n        ... on Neighborhood {\n          neighborhood\n          city\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_counties: recommended(query: {geo_search_type: county, limit: 20}) {\n      geos {\n        ... on HomeCounty {\n          county\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_zips: recommended(query: {geo_search_type: postal_code, limit: 20}) {\n      geos {\n        ... on PostalCode {\n          postal_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n  }\n}","variables":{"query":{"status":["for_sale","ready_to_build"],"primary":true,"state_code":"NY"},"client_data":{"device_data":{"device_type":"web"},"user_data":{"last_view_timestamp":-1}},"limit":42,"offset":42,"zohoQuery":{"silo":"search_result_page","location":"New York","property_status":"for_sale","filters":{},"page_index":"2"},"sort_type":"relevant","geoSupportedSlug":"","by_prop_type":["home"]},"operationName":"ConsumerSearchMainQuery","callfrom":"SRP","nrQueryType":"MAIN_SRP","visitor_id":"eff16470-ceb5-4926-8c0b-6d1779772842","isClient":true,"seoPayload":{"asPath":"/realestateandhomes-search/New-York/pg-2","pageType":{"silo":"search_result_page","status":"for_sale"},"county_needed_for_uniq":false}}'
        json_body = json.loads(body)

        json_body["variables"]["page_index"] = page_number
        json_body["seoPayload"] = page_number
        json_body["variables"]["offset"] = offset_parameter

        r = requests.post(url=url, json=json_body, headers=headers)
        json_data = r.json()
        return json_data
    
    def extract_features(self, entry: dict) -> dict:


        feature_dict = {
            "id": entry["property_id"][:9],
            "statusType":entry["status"],
            "statusText":' ',
            "unformattedPrice": entry["list_price"],
            "address": ' '.join([','.join([str(entry["location"]["address"]["line"]), str(entry["location"]["address"]["city"]), str(entry["location"]["address"]["state_code"])]), str(entry["location"]["address"]["postal_code"])]),
            "addressStreet": entry["location"]["address"]["line"],
            "addressCity": entry["location"]["address"]["city"],
            "addressState": entry["location"]["address"]["state_code"],
            "addressZipcode": entry["location"]["address"]["postal_code"],
            "beds": entry["description"]["beds"],
            "baths": entry["description"]["baths"],
            "area": entry["description"]["sqft"],
            "zestimate": 0,
            "homeType": entry["description"]["type"],
            "rentZestimate": 0,
            "isPreforclosureAuction": entry["flags"]["is_foreclosure"],
            "taxAssessedValue": 0,
            "lotAreaRaw": entry["description"]["lot_sqft"]
        }

        return feature_dict
    
    def parse_json_data(self) -> list:
        offset_parameter = 42
        
        feature_dict_list = []
        
        for i in range(1, self.page_numbers):
            json_data = self.send_request(page_number=i, offset_parameter=offset_parameter)
            offset_parameter += 42
            
            for entry in json_data["data"]["home_search"]["results"]:
                feature_dict = self.extract_features(entry)
                feature_dict_list.append(feature_dict)
                
        return feature_dict_list
    
    def create_dataframe(self) -> pd.DataFrame:
        feature_dict_list = self.parse_json_data()

        df = pd.DataFrame(feature_dict_list)

        df = df.fillna(0)

        df['homeType'] = df['homeType'].str.replace('multi_family', 'MULTI_FAMILY')
        df['homeType'] = df['homeType'].str.replace('coop', 'MULTI_FAMILY')
        df['homeType'] = df['homeType'].str.replace('single_family', 'SINGLE_FAMILY')
        df['homeType'] = df['homeType'].str.replace('townhomes', 'TOWNHOUSE')
        df['homeType'] = df['homeType'].str.replace('condos', 'CONDO')
        df['homeType'] = df['homeType'].str.replace('apartment', 'APARTMENT')
        df['statusType'] = df['statusType'].str.replace('for_sale', 'FOR_SALE')

        df['area'] = df['area'].astype(int)
        df['beds'] = df['beds'].astype(int)
        df['baths'] = df['baths'].astype(int)
        df['unformattedPrice'] = df['unformattedPrice'].astype(int)
        df['lotAreaRaw'] = df['lotAreaRaw'].astype(int)

        return df

if __name__ == "__main__":
    r = RealtorScraper(page_numbers=206)
    df = r.create_dataframe()
    df.to_csv('houses.csv', index=False)