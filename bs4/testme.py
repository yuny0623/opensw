import bs4expand as ex

#예시1 
x,y = ex.to_text("https://github.com/")  #분석하려는 url을 매개변수로 주면 해당 페이지에 있는 단어들과 url로 처리되어 있는 문자열들을 리스트 형태로 반환
ex.set_word("python")  # 찾으려는 단어 설정
n = ex.count_word(x) # 해당 단어 빈도수 반환 
print(n)

#예시2
li = ex.search_deeper(y)
url_contain_word =ex.show_page_include_word(y) # url 리스트에서 페이지에 설정된 단어가 있는 url 리스트를 반환 
ex.html_link_file(y,url_contain_word) # html 파일로 생성
print(url_contain_word)

#예시3
ex.image_take("https://github.com/") # 매개변수로 준 url에 있는 이미지들을 뽑아 html 파일로 생성

#예시4 임의로 만든 15개의 카테고리 중 매개변수로 준 url이 어떤 카테고리에 속하는지 분석
s_1 = ex.make_set_of_word("https://stackoverflow.com/") 
print(s_1)
s_2 = ex.make_set_of_word("https://www.nature.com/") #페이지에 대한 간단한 분석 리턴 
print(s_2)

#bs4활용 크롤링 기능 / 키워드, 날짜를 입력하면 해당 기사들을 뽑아 엑셀파일로 저장
ex.main()