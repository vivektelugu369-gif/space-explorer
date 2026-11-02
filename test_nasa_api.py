import requests

url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
try:
    response = requests.get(url,timeout=15)
    response.raise_for_status()
    data = response.json()
        # print(type(data))
    picture = data[0]
    print("Title:",picture["title"])
    print("Date:",picture["date"])
    print("Image URL:",picture["hdurl"])
    print("Media Type:",picture["media_type"])

    print("\n Open this image in ypur browser:")
    print(picture['hdurl'])
except requests.exceptions.RequestException as error:
    print("API Error:",error)



    # print("Title:",data['title'])
    # print("Date:",data['date'])
    # print("Image url:",data['url'])
# else:
#     print('Request failed:',response.status_code)