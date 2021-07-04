from numpy import product
import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',

}

#아두이노키트(메카솔루션)
#aduino product_no = ['2851993975',]
#aduino merchat_no = ['510126385',]

# 이 정보를 빼오는 방법을 몰라서 하나하나 수기로 일단 작성(proto) 차례대로 보석십자수(라임나무),보석십자수(하루클래스)
# 보석십자수(지니맘),보석십자수(비트백),보석십자수(델로나),보석십자수(아트조이),보석십자수(아이러브페인팅)
ProductNo_list = ['4266112558','5153958110','351505221','2232690080','5080715984','4976080841','4563544976']
merchantNo_list = ['500105879','510830988','500131588','500044749','510520938','500054193','510325189']


# productNo 과 merchatNo과 page_num으로부터 api서버에 보낼 적절한 url 생성.
def getProductUrl(_originProductNo,_merchantNo,_page_num):
    return f"https://smartstore.naver.com/i/v1/reviews/paged-reviews?originProductNo={_originProductNo}&page={_page_num}&pageSize=30&merchantNo={_merchantNo}&sortType=REVIEW_RANKING"

def getReviewDict(_originProductNo,_merchantNo,i):
    review_page_num = 1
    review_request_url = getProductUrl(_originProductNo,_merchantNo,review_page_num)

    review_res = requests.get(review_request_url,headers=headers)

    # id : 고객의 고유아이디, reviewServiceType : 
    entire_review_dict = {
        "id":[],
        "reviewServiceType":[],
        "reviewType":[],
        "reviewContent":[],
        "createDate":[],
        "channelServiceType":[],
        "reviewScore":[],
        "productName":[],
        "productOptionContent":[],
    }
    if review_res.status_code != 200:
        return None

    while review_res.text != 'OK':
        review_dict = review_res.json()
        print(f"\r{review_page_num}",end='')
        review_list = review_dict['contents']

        for review in review_list:
            entire_review_dict['id'].append(review['id'])
            entire_review_dict['reviewServiceType'].append(review['reviewServiceType'])
            entire_review_dict['reviewType'].append(review['reviewType'])
            entire_review_dict['reviewContent'].append(review['reviewContent'])
            entire_review_dict['createDate'].append(review['createDate'])
            entire_review_dict['channelServiceType'].append(review['channelServiceType'])
            entire_review_dict['reviewScore'].append(review['reviewScore'])
            entire_review_dict['productName'].append(review['productName'])
            entire_review_dict['productOptionContent'].append(review['productOptionContent'])


        #Move to next page
        review_page_num = review_page_num + 1
        review_request_url = getProductUrl(_originProductNo,_merchantNo,review_page_num)

        review_res = requests.get(review_request_url,headers=headers)
        if review_res.status_code != 200:
            continue 
        #print(review_res)

    
    #print(review_request_url.format(review_page_num))

    # id 를 index로 해서 csv파일로 저장.
    df = pd.DataFrame(entire_review_dict)
    df = df.set_index('id')
    df.to_csv(f'{i}-{datetime.date.today().isoformat()}.csv')
    print(f" Finish! {i}")

def main():
    for idx,value in enumerate(zip(ProductNo_list,merchantNo_list)):
        pno,mno = value
        getReviewDict(pno,mno,idx)

if __name__ == '__main__':
    main()