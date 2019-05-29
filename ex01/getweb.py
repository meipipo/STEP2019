from selenium import webdriver
import itertools
import re

###############################################################################
###### get the dictionary includes only words with 16 characters or less ######
###### from "https://icanhazwordz.appspot.com/dictionary.words" ###############
###############################################################################
driver = webdriver.Chrome("chromedriver")
driver.get("https://icanhazwordz.appspot.com/dictionary.words")
dicts = driver.find_elements_by_xpath("/html/body/pre")
dict = []
for w in dicts:
    dict.append(w.text)
dictionary = dict[0].split("\n")

def sort_each(w):
    return "".join(sorted(w)).lower()
dict_sorted_each = list(map(sort_each, dictionary))
# print(dict_sorted_each)


###############################################################################
###### get the characters #####################################################
###############################################################################
driver.get("https://icanhazwordz.appspot.com/")
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

    ####################################################################################
    ######## single word anagrams that use all the characters in a given string ########
    ####################################################################################
    chars = "".join(sorted("".join(sorted(p1_list + p2_list + p3_list))))

    print(chars.lower())
    if chars.lower() in dict_sorted_each:
        print(dict_sorted_each.index(chars.lower()))
        word = dictionary[dict_sorted_each.index(chars.lower())]
        elem_search_word = driver.find_element_by_id("MoveField")
        elem_search_word.send_keys(word)
        elem_search_btn = driver.find_element_by_xpath("//input[@value='Submit']")
        elem_search_btn.click()
    else:
        elem_search_btn = driver.find_element_by_xpath("//input[@value='PASS']")
        elem_search_btn.click()
