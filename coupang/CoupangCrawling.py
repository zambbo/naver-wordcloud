import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date
    
# browser에게 신원을 밝히기 위해 사용.
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

# url로부터 해당 웹사이트의 html source를 가져옴.
def getResponse(_url):
    res = requests.get(_url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    return soup

# 해당페이지의 url_list를 가져옴.
def getCoupangUrlList(_soup):
    #각각의 item의 url앞에 붙여줘야 함.
    base_url = "https://www.coupㄹㄹang.com/"
    #해당페이지의 모든 item들의 list
    itemList = _soup.select("ul#productList li")
    url_list = []
    for item in itemList:
        try:
            url = item.select_one("a").attrs['href']
            url = base_url + url
            url_list.append(url)
        except:
            print("no url error")
            continue
    return url_list

# 마지막 페이지번호를 가져옴.
def getLastPage(_soup):
    
    last_page_index = _soup.select_one("a.btn-last")
    if last_page_index:
        last_page_index = last_page_index.text.strip()
    else:
        return 1
    return int(last_page_index)

# 해당 Item에대해서 모든 item_url 의 list를 구함.
def getAllCoupangUrlList(_keyword):
    coupang_base_url = "https://www.coupang.com/np/search?q={}&page={}"
    
    total_list = []
    first_page = coupang_base_url.format(_keyword,1)
    
    last_page_index = getLastPage(getResponse(first_page))

    for page in range(1,last_page_index+1):
        url = coupang_base_url.format(_keyword,page)
        cur_url_list = getCoupangUrlList(getResponse(url))

        #전체 list에 현재 페이지의 url list를 이어붙인다.
        total_list.extend(cur_url_list)
    
    return total_list

# 비율로 되어있는 star-rating 을 star-num으로 변환.
def transStarRainting2Num(_star_rating):
    #pure한 숫자만 가져옴.
    rating = _star_rating[7:-4]
    if rating:
        rating = int(rating)
    else:
        return "0.0점"
    #
    rating = rating/20
    return str(rating)+"점"

#쿠팡 url로부터 ProductID을 알아내어 반환.
def getProductIdFromUrl(_url):
    url_idx = _url.index('products')
    question = _url.index('?')
    productId = _url[url_idx+9:question]
    return productId

#해당 item의 리뷰들을 전부 가져옴
def getAllReviewsText(_productId):
    base_rurl = 'https://www.coupang.com/vp/product/reviews?productId='+_productId+'&page={}'
    page_num = 1
    
    ret_review_list = []
    url = base_rurl.format(page_num)
    soup = getResponse(url)
    review_list = soup.find_all("article",class_='sdp-review__article__list')
    while review_list:
        bonmun_list = []
        for review in review_list:
            review_text = review.find("div",class_='sdp-review__article__list__review__content')
            if review_text is not None:
                bonmun_list.append(review_text.text.strip())

        ret_review_list.extend(bonmun_list)

        page_num = page_num + 1
        url = base_rurl.format(page_num)
        soup = getResponse(url)
        review_list = soup.find_all("article",class_='sdp-review__article__list')

    return ret_review_list

#해당 페이지의 필요한 정보를 전부 수집한 뒤 데이터 반환.
# 데이터는 상품명,별점,리뷰갯수,리뷰리스트로 이루어진 dictionary형태.
def getItemData(_url):
    
    # url로부터 soup 객체 생성
    _soup = getResponse(_url)
    #item name
    product_name = _soup.select_one("div.prod-buy-header h2.prod-buy-header__title").text

    # 상품번호
    productId = getProductIdFromUrl(_url)
    #star num   ex) 별점 5점
    star_rating = _soup.select_one("span.rating-star-num")['style']
    star_num = transStarRainting2Num(star_rating)

    #해당 아이템 review전체
    review_list = getAllReviewsText(productId)
    return {'item_name':product_name,'star_rating':star_num,'review_num':len(review_list),'review_list':review_list}

def getAllItemData(_keyword):
    url_list = getAllCoupangUrlList(_keyword)
    item_list = []
    for idx,url in enumerate(url_list):
        print(idx)
        item_data = getItemData(url)
        item_list.append(item_data)
    return item_list

# 아이템 이름을 입력받고 아이템 정보를 csv파일에 저장. 
def coupangCrawler():
    item_name = input("크롤링할 상품 이름을 입력하세요(쿠팡): ")
    today = date.today()
    filename = f'Coupang_{item_name}_{today.year}_{today.month}_{today.day}'
    item_data_list = getAllItemData(item_name)
    # item_name, star_rating, review_num, review_list
    main_list = []
    for item_data in item_data_list:
        main_list.append([item_data['item_name'],item_data['star_rating'],item_data['review_num'],item_data['review_list']])
    
    df = pd.DataFrame(main_list)
    df.columns = ['item_name','star_rating','review_num','review_list']
    df.to_csv(filename+'.csv')
    print("Finish Crawling!")
  
coupangCrawler()