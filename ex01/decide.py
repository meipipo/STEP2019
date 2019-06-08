from selenium import webdriver
import re

driver = webdriver.Chrome("chromedriver")
driver.get("https://icanhazwordz.appspot.com/dictionary.words")
dicts = driver.find_elements_by_xpath("/html/body/pre")
dict = []
for w in dicts:
    dict.append(w.text)
dictionary = dict[0].split("\n")
## 辞書中の全ての単語をアルファベットでソートし小文字にしたリスト
def sort_each(w):
    return "".join(sorted(w)).lower()
dict_sorted_each = list(map(sort_each, dictionary))
# print(dict_sorted_each[:10])


### charの組み合わせを返す関数
def next(wordlist, word):
    for i in range(0, len(word)):
        newword = word[:i]+word[i+1:]
        if (len(newword)>12):
            wordlist.append(newword)
            next(wordlist, newword)
    return list(set(wordlist))


def find(f, driver):
    chars1 = driver.find_elements_by_xpath("//div[@class='letter p1']")
    chars2 = driver.find_elements_by_xpath("//div[@class='letter p2']")
    chars3 = driver.find_elements_by_xpath("//div[@class='letter p3']")
    p1_list = []
    p2_list = []
    p3_list = []
    for c in chars1:
        p1_list.append(c.text)
    for c in chars2:
        p2_list.append(c.text)
    for c in chars3:
        p3_list.append(c.text)

    wordlist = []
    fstchar = "".join(sorted("".join(sorted(p1_list + p2_list + p3_list)).lower()))
    chars = sorted(next(wordlist, fstchar), key=lambda x:len(x), reverse=True)

    if (f < 10):
        ## 10文字くらいまでの候補について、
        for c in chars:
            print(c)
            ## 辞書の中にあればfindを1足してbreak？再帰
            if c.lower() in dict_sorted_each:
                f += 1
                word = dictionary[dict_sorted_each.index(c.lower())]
                print(word)
                ## input to the field
                elem_search_word = driver.find_element_by_id("MoveField")
                elem_search_word.send_keys(word)
                elem_search_btn = driver.find_element_by_xpath("//input[@value='Submit']")
                elem_search_btn.click()
                find(f, driver)
                break
        elem_search_btn = driver.find_element_by_xpath("//input[@value='PASS']")
        elem_search_btn.click()
        find(f, driver)

driver.get("https://icanhazwordz.appspot.com/")
find(0, driver)
