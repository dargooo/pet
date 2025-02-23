import sys
import requests
import json
import mysql.connector

# curl -d "grant_type=client_credentials&client_id=w47BEjTrqDXNg0WDEqVCpmQtiYUWaIrhmg9HenATYrbSKWFmr4&client_secret=X7KbzXt1VN8TeXTOhat6LAaGvDLmrMtwNZ3a8AyW" https://api.petfinder.com/v2/oauth2/token
api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJ3NDdCRWpUcnFEWE5nMFdERXFWQ3BtUXRpWVVXYUlyaG1nOUhlbkFUWXJiU0tXRm1yNCIsImp0aSI6ImJiNGY5MzFmN2YwNjQ1MmNlYzE5YWUyYjQ5Yjk0ZjYwOGY1Njc0NTlmZGM0ZGQyMDlkYzI2YjgzMzhhNzA5NGZlYWYyYmYxYTM5NDQxMTk2IiwiaWF0IjoxNTgzNjI5Njk3LCJuYmYiOjE1ODM2Mjk2OTcsImV4cCI6MTU4MzYzMzI5Niwic3ViIjoiIiwic2NvcGVzIjpbXX0.u5S4omvuc0UQpeB6wjeu3iUXryI3Gq1kf1-IIvIsT82_-8BQ3nnevnbPfmy7eOnHj7keFXawbUiExp02-GW79PHVtd7UxzVwiivJf8ba56FXv1swOdxMUJ1heqEz_ACRZUsFYiLwcWkFdh2iPSrE_KrffDf8z81GXaOoUPlblqexJvJSLscQitpzc2h57l4RpKmc5A6KmY3qUrN3vUI-3SxehMhXg3tLpL77HEBaVBGSlqfcP4hR9jnAexWcuIGQYxJykwIoHgyxc3pmr9PRuCTDVg6IgpzhhOBHtiGP4kjlJSR9iHamGaE_8pgsJ4m_PO03VNKAY9Jy1DuQBKKM-Q'
api_url_base = 'https://api.petfinder.com/v2'
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}
species = ['dog', 'cat']
count = 1

try:
    cnx = mysql.connector.connect(user='coasttocoast_yijun', password='sql41149.',
                                  host='localhost', database='coasttocoast_petadoptionapp')
    cursor = cnx.cursor()
except:
    print("Log in mysql db failed!")

def get_json(i):
    global count
    x = species[i]
    api_url = api_url_base + '/types/%s/breeds' % x
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        breed_list = json.loads(response.content.decode('utf-8'))['breeds']
        insert_query = "INSERT INTO breed VALUES (%s, %s, %s)"
        for x in breed_list:
            query_data = (count, i, x['name'])
            count += 1
            cursor.execute(insert_query, query_data)
    else:
        print("Failed to connect to " + api_url)


def main(argv):
    for i in range(0, len(species)):
        insert_query = "INSERT INTO species VALUES (%s, %s)"
        query_data = (i, species[i])
        cursor.execute(insert_query, query_data)
        get_json(i)
    cnx.commit()
    cursor.close()
    cnx.close()
 

if __name__=="__main__":
    main(sys.argv)
