import requests
import time 
from random import randint
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import warnings

#새기능 추가에 필요한 import 
#from bs4 import BeautifulSoup
from datetime import datetime
#import requests
import pandas as pd
import re

'''
외부/ 이 파일 내의 함수를 호출하는 py파일에서 이미 collect_text의 to_text를 통해 word list와 
url list를 생성하였을때 이 파일 내의 함수들을 사용할 수 있다. .
그 값 중에서 url list를 이 클래스의 함수가 매개변수로 받았을 때 
기능하는 클래스의 함수를 정의한다. 트리를 생성한다. -> 1layer 
'''

word_to_find = 'NULL'       #지정된 단어를 저장할 클래스 전역변수 
word_count = 1             #지정된 단어의 빈도를 저장할 전역변수
soup_list = []           #soup객체들을 저장할 리스트


def set_word(out_word): 
    '''찾을 단어를 지정해주는 함수.'''
    global word_to_find #함수 내에서 global을 선언해야만 함수 외부의 변수에 접근가능하다. 
    word_to_find = out_word  #매개변수로 전달받은 값을 함수 할당한다. 

def count_word(out_word_list): 
    '''해당 단어의 노출 빈도를 반환한다. '''
    '''
    word_to_find in w_li[i] 라고 코딩하면 제대로 동작하지 않는다. 
    w_li[i]는 리스트 요소이다. 즉 in을 통해 탐색하면, 
    그 요소가 찾고자 하는 단어와 정확히 일치하는 지를 탐색한다. 
    즉 예를 들어 python이라는 단어를 찾고싶다면 정확히 python이라는 
    요소가 존재해야만 word_count+=1을 실행하는 것이다. 
    하지만 find를 통해 탐색하면 그 요소가 정확히 python이라는 단어가 아니라 
    himywordpython 와 같은 요소 존재할 때 python이라는 문자열이 후미에 
    존재하므로 word_count+=1을 실행한다.
    '''
    w_li = out_word_list
    global word_count          #함수 외부의 word_count에 접근하기 위해 global 사용
    global word_to_find        #함수 외부의 word_to_find 에 접근하기 위해 global 사용
                            #전역으로 선언된 변수가 함수에서 사용되면 무조건 global 사용 
    for i in range(len(w_li)):    
        if word_to_find.find(w_li[i]):   
            word_count+=1 
    return word_count

def list_seperate(url_list): 
    '''
    requests 개수 제한을 해결하기 위한 함수. 
    반복문을 통해 전달받은 리스트의 요소들(url 링크)을 하나씩 soup객체로 만들어준다. 
    만들어진 soup객체를 하나씩 total_list 리스트에 더한다. 즉 soup객체가 요소로 들어있는 리스트를 제공한다. 
    그리고 만들어진 total_list 리스트를 반환한다. 
    대부분의 requests요청 거부 혹은 연결 끊어짐과 관련있는 에러는 전부 다 이 함수에서 발생한다. 
    '''
    li = url_list
    total_list = []
    for i in range(len(li)): 
        html_info = requests.get(li[i]).text
        soup = BeautifulSoup(html_info,'html.parser')
        #soup = soup.text # <- 나중에 지워줘도 됨. 순수 soup객체만 받고 싶으면 주석처리 
        #일단은 비교연산 때문에 str로 바꿔놨음. 
        #.split()을 통해 더 깔끔하게 만들 수 있는데, .split()은 전달받은 객체를 
        #리스트로 만들어버린다. 그렇기 때문에 비교연산을 진행할 수가 없다. 즉 3중리스트가 되어버려서 
        #요소 비교하는 방식을 새로 바꿔야함. 그래서 그래서 밖에 for문이 너무 지저분해짐. 
        #그리고 get_text()는 오직 soup객체에만 적용가능
        #이미 text화시킨 soup객체에는 적용불가

        soup_text = soup.get_text()          
        total_list.append(soup_text)

    #type of soup is str
    #type of total_list is list
    print("url adding to list is finished")
    
    return total_list

def search_deeper(out_url_list): 
    '''
search-deeper 함수 '''
    li = out_url_list
    #print("search-deeper act in here")

    if(len(li)>400):                    #400개 이상이면 예외를 발생시킨다. 사실 400개 넘는 경우가 별로 없다. 
        raise Exception("too big list size")

    if (len(li)<400) & (len(li) >300):  # 400>x>300
        #print("soup act in here")
        j=0
        for i in range(int(len(li)/10)): #int로 나누기연산 감싸야됨. 안하면 float 적용됨. 에러 발생함. 
            soup_list.append(list_seperate(li[j:(j+10)])) 
            #리스트인 전역 변수인 soup_list에 list_seperate에서 반환받은 객체를 리스트에 더한다. 
            j+=10                
            '''
            리스트를 쪼개면 [0:10] -> [10:20] -> [20:30] -> [n:n+10]이와 같은 순서를 따른다. 
            그렇기 때문에 j+=10에서 10씩 증가시켜주고, list_seperate에 li[j:j+10]을 전달하면 
            자동으로 [0:10] -> [10:20] -> [20:30] -> [n:n+10] 순으로 반복해서 전달된다. 
            '''
            time.sleep(1)        #일단 sleep 써놓긴 했는데, 사실 이거 효과는 없는듯 

            '''만약 슬라이싱하고 즉 10등분을 했는데, 그 끝에 남은 수가 있다면 꼬리에 더해서 
            list_seperate에 전달한다. 즉 95라고 치면 90은 위에서 이미 처리하고 5가 남는데, 
            이 5만큼을 리스트 끝에다가 더해주는거. 
            '''
        if i == (int(len(li)/10)):
            soup_list.append(list_seperate(li[j:]))
        #이하로는 범위만 변경되고 나머지는 똑같은 내용입니다. 


    if (len(li)<300) & (len(li) >200): # 300>x>200
        #print("soup act in here")
        j=0
        for i in range(int(len(li)/10)):
            soup_list.append(list_seperate(li[j:(j+10)]))
            j+=10
            time.sleep(1)
        if i == (int(len(li)/10)):
            soup_list.append(list_seperate(li[j:]))

    if (len(li)<200) & (len(li) >100): # 200>x>100
        #print("soup act in here")
        j=0
        for i in range(int(len(li)/10)): 
            soup_list.append(list_seperate(li[j:(j+10)]))
            j+=10
            time.sleep(1)
        if i == (int(len(li)/10)):
            soup_list.append(list_seperate(li[j:]))

    if (len(li)<100) & (len(li) >0): # 100> x> 0
        #print("soup act in here")
        j=0
        for i in range(int(len(li)/10)): 
            soup_list.append(list_seperate(li[j:(j+10)]))
            j+=10
            time.sleep(1)
        if i == (int(len(li)/10)):
            soup_list.append(list_seperate(li[j:]))

    #어차피 리스트의 크기가 0<x<10이라면 굳이 슬라이싱 해줄 필요는 없다. 
    #10개정도의 요청은 거부된 적이 없음. 
    if (len(li)<10) & (len(li)>0): #10>x>0
        soup_list.append(list_seperate(li))

    #0보다 작은값이 전달되면 예외가 발생한다. 
    if len(li) <0:
        raise Exception("잘못된 값이 입력되었습니다.")
    return soup_list


def show_page_include_word(y_list): #전체 리스트인 y_list 
    '''반드시 search_deeper 호출 다음에 호출되어야함. 아니면 NULL값 리던 .
    단어를 포함하는 페이지의 url을 리스트로 반환한다. '''
    store_url_location = [] #단어가 존재하는 url의 위치를 저장한다. 
    if len(y_list) == 0:    #리스트의 크기가 0이면 애초에 #search_deepter에서 반환한 값에
                            #문제가 있는 것이다. 그럴 경우에 예외 호출발생시킨다. 
        raise Exception("search_deeper가 호출되지 않았습니다. ")

    #전달 받은 모든 리스드에서 탐색한다. 
    for i in range(len(soup_list)):
        #soup_list 리스트는 리스트를 요소로 가지고 있는데, 이유는 list_seperate에서 리스트를 반환해줬기 때문에.. 
        #그 리스트의 요소들은 soup객체의 텍스트를 가지고 있는데, 즉 페이지에 있는 문자열들! 
        #거기서 단어의 존재여부를 확인하고, 만약 해당 단어가 그 페이지(그 리스트의 리스트 요소)에 존재한다면
        #그 위치 즉 페이지의 링크 url을 store_url_location에 저장한다. 그리고 그걸 반환한다. 
        
        for j in range(len(soup_list[i])):
            # 2020.10.30 -> word_to_find in soup_list[i][j]: 에서 find로 바꿔줬음.
            # 애초에 요소는 text로 정렬된 str형태이므로 find를 통해 탐색하는 게 더 정확함.  
            if word_to_find.find(soup_list[i][j]):  
                store_url_location.append(y_list[i*10+j])
    return store_url_location
        

def make_set_of_word(single_url): #여기서 single_url은 리스트가 아닌 하나의 url이다. 
    '''
    https://relatedwords.io/ 에서는 연관단어에 대해 500개 정도의 단어를 제공한다. 
    requests를 통해 해당 사이트에서 단어를 가져오고 리스트로 변환해서 할당한다. 
    분석을 원하는 사이트가 있으면 make_set_of_word에 매개변수로 링크를 전달한다. 
    전달된 링크는 또다시 requests를 통해 soup객체로 변환되고, 텍스트화 및 split된다. 
    그리고 최종적으로 카테고리에 있는 분류중에서 가장 많은 빈도 수를 기록한 카테고리가 
    해당 페이지의 분류가 된다.
    '''
    url = single_url                         
    category_list = [                       #카테고리이다. 사이트가 어떤 사이트인지 분류하기 위함. 15개의 카테고리
        "programming","opensource","book","government",
        "shopping","food","blog","album","study","academy",
        "laboratory","gallery","portfolio","bank","essay"]

    number_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #카테고리별 연관단어의 출현빈도를 저장할 리스트 

    s = "https://relatedwords.io/"          #연관단어를 긁어올 사이트/ 후미에 카테고리중 하나를 추가할 예정

    html = requests.get(url).text           #분석을 원하는 사이트를 requests를 통해 soup객체로 만든다. 
    soup_url = BeautifulSoup(html,"html.parser")
    soup_url = soup_url.get_text()
    soup_url = soup_url.split()             #사이트에 관한 텍스트 리스트이다. (split은 리스트로 변환된다.)

    double_list_soup = []                    #이중 리스트 생성 예정   
    
    for i in range(len(category_list)):     #15번반복됨. 카테고리가 15개이기 때문에 
        print(str(i)+" --> in catagory for code")
        url_in_here = s+category_list[i]            #카테고리별로 단어를 url에 추가해준다. 
        print(url_in_here)
        html_doc = requests.get(url_in_here).text    
        soup = BeautifulSoup(html_doc,'html.parser') #연관단어 페이지의  soup객체 
        href_list = []                      #값을 전달하기 위해 임시로 사용한 list객체 
                                            #이것을 선언하지 않으면 soup객체에서 태그를 뽑아
                                            #리스트로 전달하는 과정이 복잡해짐. 
        
        for link in soup.find_all('a'):       #a태그 분류 
            #print(type(soup.find_all('a'))) #<class 'bs4.element.ResultSet'>
            #print(type(link.get('href')))   #<class 'str'>
            href_list.append(link.get('href')) #href속성을 찾아서 href_list에 임시로 저장한다. 

        double_list_soup.append(href_list)     #href_list를 통째로 double_list_soup에 할당한다. 이중 리스트 생성

    # print()
    # print("category cal is finish")
    # print()
    # print("length of double_list_soup is " + str(len(double_list_soup))) #15 가 출력됨. 즉 15개의 카테고리별로 잘 생성되었다는 뜻. 
    # print("factor length of doule list is " + str(len(double_list_soup[0]))) # 502가 출력됨. 카테고리 별로 각 단어들이 잘 생성됨. 
    #                             # 이중 리스트로 15개의 각각 502개씩의 요소가 생성됨. (502가 아닌 경우도 존재)
    # print() 
    # print("appending word is finish")

    print()
    for i in range(len(double_list_soup)): #15번 반복됨. 
        for j in range(len(double_list_soup[i])): #얘는 502인경우도 있고, 그보다 작은 경우도 있음. 
            if double_list_soup[i][j].startswith('/'): #단어이면 실행한다. 단어에는 /가 붙어서 값이 전달되기 때문에 /를 없애줘야 한다. 
                double_list_soup[i][j] = double_list_soup[i][j].replace("/","") #/가 붙은 단어에서 /를 ""로 바꾼다. 즉 삭제 
            else:                         #/로 시작하지 않는 경우는 http가 붙는 경우이다. 이값은 필요가 없다. 
                #원래 여기서 del을 통해 필요없는 http요소를 삭제하려고 했는데, 그렇게 하면 index에러가 발생한다. 
                #즉 del을 하게 되면 아예 요소가 하나 사라지고 for문 내에서 i 와 j의 범위가 아예 바뀐다. 
                #그래서 굳이 삭제하지 않고, 해당카테고리명을 그 자리에 추가해주는 방식을 취했다. 
                double_list_soup[i][j] = double_list_soup[i][j].replace(double_list_soup[i][j],category_list[i])

    #print("sorting double_list_soup is finished")
    #print(len(double_list_soup[0]))
    print()

    #페이지를 분석하기 위한 for문 
    #double_list_soup 내의 단어를 soup_url 즉 (사이트에 관한 split된 soup객체)가 포함하고 있다면 
    # number_count의 i번째 요소를 1씩 증가시킨다. 즉 빈도 수를 저장한다. 
    for i in range(len(double_list_soup)):
        for j in range(len(double_list_soup[i])):
            if double_list_soup[i][j] in (soup_url):
                number_count[i]+=1

    #number_count에서 가장 큰 수를 찾아내고, 그 위치 즉 인덱스를 저장한다. 
    for i in range(len(number_count)):
        print(number_count[i])
        if number_count[i] == max(number_count):
            index = i

    #출력문
    print(str(max(number_count))+" is in "+str(index)+" location")

    #반환할 문자열이다. 결론이다. 해당페이지가 카테고리 중 어느 카테고리에 가장 큰 비중을 갖는 지를 할당한다. 
    conclusion_str = "The page is about " + category_list[index] #분석에 대한 결과 (어떤 페이지 인지. )

    return conclusion_str #분석에 대한 결과를 반환한다. 


def image_take(url):
    '''
    원하는 페이지에서 이미지태그를 긁어서 리스트로 모아줌. 해당 리스트를 html doc에 순서대로 
    넣어주는데, 따로 파일을 만들어서 생성해줌. 그 파일열면 페이지에 무슨 이미지가 있는지, 
    전부 확인할 수 있음.  
    '''
    url_use = url
    html_doc = requests.get(url_use).text
    soup = BeautifulSoup(html_doc,'html.parser')

    li = [] # 빈 리스트 생성. img 태그에서 src속성을 갖고 있는 텍스트를 모두 저장한다. 

    for link in soup.find_all('img'):
        li.append(link.get('src'))

    #html 문서 기본 양식 -> 이미지 바둑판으로 보이게 수정하기. 
    html_doc_top = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        img{
            width:100px;
            height:100px;
            float:left;
        }
    </style>
    </head>
    <body>
    <h1>ALL IMAGE COLLECTED</h1>
    '''
    html_doc_middle = "" # body에 들어갈 내용을 html_doc_middle에 쓴다. 

    html_doc_bottom = '''
    </body>
    </html>'''
    #C:\Python38\Lib\site-packages\bs4\collected_info_in_here
    #warnings.filterwarnings(action = 'ignore')
    # open 내에 경로는 항상 백슬래쉬 두개로 써주기. -> \\ 안하면 경고표시뜸. 
    f = open("C:/Python38/Lib/site-packages/bs4/collected_info_in_here/image_file.html",mode = "wt",encoding="utf-8")

    for i in range(len(li)): #리스트의 길이만큼 반복한다. 즉 페이지에 있는 이미지태그의 개수만큼 반복 
        if li[i] == None:    #가끔 이미지태그에서 긁어온 값인데 값 자체가 None을 반환하는 경우가 있다. 
                            #이 경우에 무조건 에러가 발생함. 
                            #왜 None값이 나오고, 어디서 발생하는 지는 잘 모르겠음. 그런데 가끔 None값을 
                            #반환하는 이미지태그가 있음. --> 
                            #보완점 -> 만약 None 값 반환하는 태그도 실제로는 이미지라면 따로 빼서 처리해주기. 
            continue


        # body에 이미지 태그를 페이지 내의 링크를 걸어서 추가시킨다. 
        html_doc_middle +=('<img src = "'+li[i]+'">'+"<br>"+'\n') 


    #s에 top middle bottom을 더함으로써 하나의 html 문서 완성 
    s = html_doc_top + html_doc_middle + html_doc_bottom

    #파일에 쓰고 닫아준다. 
    f.write(s)
    f.close()

def html_link_file(url_list,selected_list):
    '''
    메인 페이지에 걸려있는 모든 링크들을 html doc에 넣어서 링크집합을 만들어준다. 
    찾고자하는 단어를 포함하는 링크는 SELECTED URL LIST 로 분류되어 하단에 따로 표시된다. 
    내용은 image_make와 같다. 동일하게 동작한다. 다만 함수의 매개변수로 selected_list를 하나 더 받는다. 
    show_page_include_word에서 단어를 포함하는 링크의 리스트를 반환했는데, 그 반환한 값이 
    selected_list 매개변수에 들어오는 것이다. 
    '''

    html_doc_top = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    </head>
    <body>
    <h1>ALL URL LIST</h1>
    '''
    html_doc_middle = ""
    html_doc_bottom = '''   
    </body>
    </html>'''

    f = open("C:/Python38/Lib/site-packages/bs4/collected_info_in_here/html_file.html",mode = "wt",encoding="utf-8")
    for i in range(len(url_list)):
        html_doc_middle +=('<a href = "'+url_list[i]+'">'+url_list[i]+"</a>"+"\n"+"<br>")

    html_doc_middle+='<h1>SELECTED URL LIST </h1><br>'

    for i in range(len(selected_list)):
        html_doc_middle +=('<a href = "'+selected_list[i]+'">'+selected_list[i]+"</a>"+"\n"+"<br>")

    s = html_doc_top + html_doc_middle + html_doc_bottom
    f.write(s)
    f.close()

'''
url_from_out을 매개변수로 받은 뒤에 soup객체와 함께 페이지의 소스코드를 텍스트화시킨 html_info를 제공받는다. 
그후 soup객체를 가공해서 리스트로 만든 뒤 soup_str_translate을 반환한다. 
url_list라는 리스트를 생성하는데 페이지에 존재하는 모든 링크를 리스트에 할당한다. 
동시에 http를 포함하는 문자열 중에서 exe가 포함되지 않은 문자열을 url_list라는 리스트로 반환한다. 

for link in soup.find_all('a'):
    print(link.get('href'))    

--> 을 사용하면 쉽게 하이퍼링크만 뽑아낼 수 있다. 근데 이 기능만 사용하면 exe파일과 같이 다른 페이지로 
넘어가는 link가 아닌 다른 link들도 함께 sorting된다. 그러므로 따로 조건을 더 달아줘야함. 
'''

def to_text(url_from_out):
    url = url_from_out     
    html_info = requests.get(url).text   
    soup = BeautifulSoup(html_info,'html.parser') 

    soup_text = soup.get_text()            #soup객체를 텍스트로 만들어서 soup_text에 할당하기. 
    soup_str_translate = soup_text.split() #soup_text객체를 공백 구분해서 soup_str_translate에 할당. 

    url_list = []                    #모든 링크는 url_list의 리스트를 통해 접근 가능하다. 
    for link in soup.find_all('a'):  #soup객체 내에 존재하는 모든 링크를 list로 만들어준다. 
        url_list.append(link.get('href'))
    

    new_url_list = []               #새로운 리스트를 생성해서 가공된 url list를 할당한다.                 
    for i in range(len(url_list)):  
        try:
            #http가 있는 문자열 즉 연결 가능한 링크만 따로 모아서 new_url_list에 할당한다.
            #가끔 None을 반환하는 링크가 있다. 그럴 경우는 제외시킨다. 
            #exe 파일도 제외시킨다. 
            if ((url_list[i][0:4] == "http") & (url_list[i] != None)):    
                if "exe" not in url_list[i]:   #실행파일이 아닌 경우에만
                    new_url_list.append(url_list[i]) 
        except TypeError:                      #TypeError가 발생하는 경우가 있음. 그럴 경우에는 무시하고 진행
            continue

    #해당되는 기호들이 있으면 제거한다. word_list에 정리된 단어들을 할당한다. 
    word_list = []
    for word in soup_str_translate:
        symbols = """▶↑~!@#$%^&*()_-+={[}]|\\;:"‘'·<>?/.,ⓒ """ 
        for i in range(len((symbols))):

            #해당 symbols내의 기호가 있으면 '' 내부의 것으로 바꾼다. 
            #근데 '' 안에 아무것도 없으니 제거하는것과 마찬가지 기능을 함. 
            word = word.replace(symbols[i], '')  

        if len(word) > 0:
            word_list.append(word)
    
    return word_list,new_url_list #가공된 word에 관한 리스트와 url에 관한 리스트를 반환시켜 준다. 2개 반환..

#아직 구현 x 
# def get_image(url):
#     response = requests.get(url)
#     html = response.textsoup = BeautifulSoup(html,'html.parser')
#     imgs= soup.select('img')
#     for img in imgs:
#         t_url = img['src'].split('/')[-1]
#         print(t_url)
#         urlretrieve(img['src'],'./images/'+t_url)


##2020.11.20 새로 추가. ############################################################
###################################################################################
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< naver 뉴스 검색시 리스트 크롤링하는 프로그램 > _select사용
- 크롤링 해오는 것 : 링크,제목,신문사,날짜,내용요약본
- 날짜,내용요약본  -> 정제 작업 필요
- 리스트 -> 딕셔너리 -> df -> 엑셀로 저장 
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#각 크롤링 결과 저장하기 위한 리스트 선언 
title_text=[]
link_text=[]
source_text=[]
date_text=[]
contents_text=[]
result={}

#엑셀로 저장하기 위한 변수
now = datetime.now() #파일이름 현 시간으로 저장하기

#내용 정제화 함수 
def contents_cleansing(contents):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '', 
                                      str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '', 
                                       first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    print(contents_text)
    

def crawler(maxpage,query,sort,s_date,e_date):

    s_from = s_date.replace(".","")
    e_to = e_date.replace(".","")
    page = 1  
    maxpage_t =(int(maxpage)-1)*10+1   # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    
    while page <= maxpage_t:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)
        
        response = requests.get(url)
        html = response.text
        print(response)
        #뷰티풀소프의 인자값 지정
        soup = BeautifulSoup(html, 'html.parser')
 
        #<a>태그에서 제목과 링크주소 추출
        atags = soup.select(".news_tit")
        
        #atags = soup.select('._sp_each_title')
        print(atags)
        for atag in atags:
            title_text.append(atag.text)     #제목
            print('제목')
            print(atag.text)
            link_text.append(atag['href'])   #링크주소
            print('링크주소')
            print(atag['href'])
            
        #신문사 추출
        source_lists = soup.select('.info.press')
        for source_list in source_lists:
            source_text.append(source_list.text)    #신문사
            print('신문사')
            print(source_list.text)      
        
        #본문요약본
        contents_lists = soup.select('.dsc_wrap')
        for contents_list in contents_lists:
            #print('==='*40)
            print('본문요약본')
            contents_cleansing(contents_list) #본문요약 정제화

        #모든 리스트 딕셔너리형태로 저장
        result= { "title":title_text ,  "source" : source_text ,"contents": contents_text ,"link":link_text }  
        print('결과')

        print(page)
        df = pd.DataFrame(result)
        
        page += 10 
    
    # 새로 만들 파일이름 지정
    #df = pd.DataFrame(result)  #df로 변환
    outputFileName = '%s-%s-%s'% (now.year, now.month, now.day)+query+'merging.xlsx'
    df.to_excel(outputFileName,sheet_name='sheet1')
    
    print(df)

def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    
    maxpage = input("최대 크롤링할 페이지 수 입력하시오: ")  
    query = input("검색어 입력: ")  
    sort = input("뉴스 검색 방식 입력(관련도순=0  최신순=1  오래된순=2): ")    #관련도순=0  최신순=1  오래된순=2
    s_date = input("시작날짜 입력(2019.01.04):")  #2019.01.04
    e_date = input("끝날짜 입력(2019.01.05):")   #2019.01.05
    
    crawler(maxpage,query,sort,s_date,e_date) 
    

