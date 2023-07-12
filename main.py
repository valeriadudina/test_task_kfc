import requests
import json
import sqlite3

con = sqlite3.connect("sqlite.db")
cur = con.cursor()
'''
#res = cur.execute('drop table kfc_restaurants_2')
#res_1 = cur.execute('CREATE TABLE "kfc_restaurants_2" (ID integer primary key AUTOINCREMENT, Name varchar(20) , storeId TEXT, streetAddress TEXT, city TEXT, coordinates_lat REAL, coordinates_long REAL, phone_number TEXT, start_time_local TEXT, end_time_local TEXT, regularDaily TEXT, status TEXT, features TEXT, is_breakfast BLOB, breakfast_start_time TEXT, breakfast_end_time TEXT);')
res_4 = cur.execute('delete from kfc_restaurants_2 ')
con.commit()
res_3 = cur.execute('select * from kfc_restaurants_2')
print(res_3.fetchall())
'''
url = "https://api.kfc.digital/api/store/v2/store.get_restaurants"

response = requests.request("GET", url)
if response.status_code == 200:
    data = json.loads(response.text)
    #print(data)
else:
    print(f"Error: {response.status_code}")
f = []
id_num = 0
if data:
    for rest in data.get('searchResults'):
        id_num+=1
        store_id = rest.get('storePublic').get('storeId')
        store_id = rest.get('storePublic').get('storeId')
        name = rest.get('storePublic').get('title').get('ru')
        streetAddress = rest.get('storePublic').get('contacts').get('streetAddress').get('ru')
        city = rest.get('storePublic').get('contacts').get('city').get('ru')
        coordinates_lat = rest.get('storePublic').get('contacts').get('coordinates').get('geometry').get('coordinates')[0]
        coordinates_long = rest.get('storePublic').get('contacts').get('coordinates').get('geometry').get('coordinates')[1]
        if coordinates_lat is None or coordinates_long is None:
            coordinates_lat = 0
            coordinates_long = 0
        phone_number = rest.get('storePublic').get('contacts').get('phone').get('number')
        start_time_local = rest.get('storePublic').get('openingHours').get('regular').get('startTimeLocal')
        end_time_local = rest.get('storePublic').get('openingHours').get('regular').get('endTimeLocal')
        regularDaily = rest.get('storePublic').get('openingHours').get('regular').get('regularDaily')
        status = rest.get('storePublic').get('status')
        features = ' '.join(rest.get('storePublic').get('features'))
        f = lambda a: True if 'breakfast' in a else False
        is_breakfast = f(features)
        if is_breakfast:
            for x in rest.get('storePublic').get('menues'):
                if 'name' in x and x.get('name') == 'Завтрак':

                    breakfast_start_time = x.get('availability').get('regular').get('startTimeLocal')
                    breakfast_end_time = x.get('availability').get('regular').get('endTimeLocal')
        else:
            breakfast_start_time = None
            breakfast_end_time = None
        
        
        print(store_id,'-',  name, '-',streetAddress, '-',city, '-',coordinates_lat, '-',coordinates_long,'-',phone_number,'-',start_time_local, '-',end_time_local,'-',
      regularDaily,'-', status, '-',is_breakfast, '-',breakfast_start_time, '-',breakfast_end_time )
        sql = f"INSERT INTO kfc_restaurants_2 (ID,Name,storeId,streetAddress,city," \
              f"coordinates_lat,coordinates_long,phone_number,start_time_local," \
              f"end_time_local,regularDaily,status,features, is_breakfast,breakfast_start_time, breakfast_end_time ) " \
             f"VALUES ({id_num},'{name}','{store_id}','{streetAddress}','{city}', " \
              f"{coordinates_lat},{coordinates_long},'{phone_number}'," \
              f"'{start_time_local}','{end_time_local}','{regularDaily}','{status}','{features}',{is_breakfast},'{breakfast_start_time}', " \
              f"'{breakfast_end_time}'); "
        print(sql)
        insert = cur.execute(sql)
        con.commit()

#res_3 = cur.execute('select * from kfc_restaurants_2;')
#print(res_3.fetchall())

