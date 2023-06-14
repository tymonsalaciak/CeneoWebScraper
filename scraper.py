import requests
from bs4 import BeautifulSoup
import json

def extract_tag(ancestor, selector=None, attribiute=None, return_list=False): # none może przyjąc rózne zmienne / false w tym przypadku jest zabiegiem logicznym
    try:
        if return_list:
            return [tag.text.strip() for tag in  ancestor.select(selector)]
        if not selector and attribiute:
            return ancestor[attribiute]
        if attribiute:
            return ancestor.select_one(selector)[attribiute].strip()
        return ancestor.select_one(selector).text.strip()
    except (AttributeError, TypeError):
        return None
    

    #extract_tag(opinion,
selectors = {  #struktura opini
        "oinion_id": [None ,"data-entry-id"],
        "author": ["span.user-post__author-name"],
        "recommendation": ["span.user-post__author-recomendation > em"],
        "rating": [".user-post__score-count"],
        "verafied": ["div.review-pz"],
        "post_date":  ["span.user-post__published > time:nth-child(1)","datetime"],
        "purchase_date":  ["span.user-post__published > time:nth-child(2)","datetime"],
        "vote_up":  ["button.vote-yes","data-total-vote"],
        "vote_down":  ["button.vote-no","data-total-vote"],
        "content": ["div.user-post__text"],
        "cons": ["div.review-feature__title--negatives~div.review-feature__item", None, True],
        "pros": ["div.review-feature__title--positives~div.review-feature__item", None, True],
}


#product_code = input("Podaj kod produktu: ")
product_code = "96693065"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews_scroll"

all_opinions = []

while(url):
    print(url)
    response = requests.get(url)
    page_dom = BeautifulSoup(response.text, "html.parser") # dwa argumenty
    opinions = page_dom.select("div.js_product-review") # . odpowiada za class

    
    for opinion in opinions:
        single_opinion = {}
        for  key, value in selectors.items():
            single_opinion[key] = extract_tag(opinion, *value)  # zamiast listy bedziemy mieli lementy niezależne poprzez dodanie *
        all_opinions.append(single_opinion)
    try:
        url = "https://www.ceneo.pl" + extract_tag(page_dom, "a.pagination__next", "href")
    except TypeError:
        url = None
    

with open(f"./opinions/{product_code}.json", "w", encoding="UTF-8") as  jf:
    json.dump(all_opinions, jf, indent=4 , ensure_ascii=False)



    #print(type(opinions))
#print(page_dom.prettify()) # .text .status_code response.text
#[cons.text.strip() for cons in  opinion.select_one("div.review-feature__title--negatives~div.review-feature__item") ]


