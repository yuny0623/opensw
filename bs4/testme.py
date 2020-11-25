from bs4 import bs4expand as ex

#예시1 
x,y = ex.to_text("https://github.com/") # 가장 먼저 사용해야함. 리스트 반환 
ex.set_word("python") #찾고싶은 단어를 초기화. 
n = ex.count_word(x) #단어의 빈도수를 반환 . 
print(n)

#예시2
li = ex.search_deeper(y)
url_contain_word =ex.show_page_include_word(y) 
print(url_contain_word)

#예시3
ex.html_link_file(y,url_contain_word) 
ex.image_take("https://github.com/")

# #예시4 
# s = ex.make_set_of_word("") #페이지에 대한 간단한 분석 리턴 
# print(s)

#https://www.goldmansachs.com/ 
#https://www.nature.com/
#https://stackoverflow.com/

#bs4활용 크롤링 기능. 
ex.main()