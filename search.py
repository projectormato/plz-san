import os
import googleapiclient.discovery
import random
import requests
import itertools

api_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
search_engine = os.environ.get("GOOGLE_SEARCH_ENGINE")
DUMMY_IMAGE = False
DEBUG = False

base_dir = os.path.dirname(os.path.abspath(__file__))

service = googleapiclient.discovery.build(
        "customsearch", "v1", developerKey=api_key)

name_parts = list(itertools.chain(
        range(ord("a"), ord("z") + 1),
        range(ord("A"), ord("Z") + 1),
        range(ord("0"), ord("9") + 1),
        ))

def image_search(query):
    if DUMMY_IMAGE:
        return ["http://www.teu.ac.jp/infomation/2014/images/2014CS_gakubucho.jpg"]
    response = service.cse().list(
                q=query,
                cx=search_engine,
                lr="lang_ja",
                num=10,
                start=1,
                searchType="image"
            ).execute()
    items = response["items"]
    links = [item.get("link") for item in items]
    if DEBUG:
        print("--- searched images ---")
        for i in links:
            print(i)
    return links


def only_https(url_list):
    return [url for url in url_list if url.startswith("https")]


def one(query):
    url_list = image_search(query)
    return random.choice(only_https(url_list))


def random_name(length):
    return "".join(chr(random.choice(name_parts)) for x in range(length))


def delete_files(dir_name):
    for filename in os.listdir(dir_name):
        if not filename.startswith("."):
            os.remove(dir_name + filename)


# get root like this: request.url_root
def one_include_http(query):
    url = random.choice(image_search(query))
    if url.startswith("https"):
        return url
    if DEBUG:
        print("--- one image ---")
        print(url)
    echo = "https://ximagecho.herokuapp.com/echo?url="
    return echo + url
