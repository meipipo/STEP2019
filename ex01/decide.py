from selenium import webdriver


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


### charの組み合わせを返す関数？
###


def find(f, driver):
    for i in range(0, 10):
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
    ## [!] charsは10文字くらいまでのを入れるリストにしたい
    chars = []
    chars.append("".join(sorted("".join(sorted(p1_list + p2_list + p3_list)))))
    # print(chars)
    for i in range(0, len(chars[0])):
        chars.append(chars[0][:i]+chars[0][i+1:])
    print(chars)
    if (f < 10):
        ## 10文字くらいまでの候補について、
        for c in chars:
            print(c)
            ## 辞書の中にあればfindを1足してbreak？再帰
            if c.lower() in dict_sorted_each:
                f += 1
                word = dictionary[dict_sorted_each.index(c.lower())]
                ## input to the field
                elem_search_word = driver.find_element_by_id("MoveField")
                elem_search_word.send_keys(word)
                elem_search_btn = driver.find_element_by_xpath("//input[@value='Submit']")
                elem_search_btn.click()
                find(f, driver)
        elem_search_btn = driver.find_element_by_xpath("//input[@value='PASS']")
        elem_search_btn.click()
        find(f, driver)

driver.get("https://icanhazwordz.appspot.com/")
find(0, driver)
