import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# хромдрайвер
DRIVER_PATH = "chromedriver"

# Поисковый запрос к постам:
# keyword = input('Введите поисковый запрос к постам группы tokyofashion ...')
# print(keyword)

url = "https://vk.com/tokyofashion"
driver = webdriver.Chrome(DRIVER_PATH)
driver.get(url)
driver.refresh()

search_url = driver.find_element_by_class_name('ui_tab_search').get_attribute('href')
driver.get(search_url)

#запрос:
search = driver.find_element_by_id("wall_search")
search.send_keys('одежда')
search.send_keys(Keys.ENTER)

scrollpage = 1
while True:
    time.sleep(2)
    try:
        button = driver.find_element_by_class_name('JoinForm__notNow')
        if button:
            button.click()
    except Exception as e:
        print(e)
    finally:
        driver.find_element_by_tag_name("html").send_keys(Keys.END)
        scrollpage += 1
        time.sleep(1)
        #конец стены постов
        wall = driver.find_element_by_id('fw_load_more')
        stopscroll = wall.get_attribute('style')
        # print(stopscroll)
        if stopscroll == 'display: none;':
            break
# print(scrollpage)
posts = driver.find_elements_by_xpath('//div[@id="page_wall_posts"]//..//img[contains(@alt,"Tokyo Fashion")]/../../..')
# print(posts[0])

p=0
posts_info = []
for post in posts:
    post_data = {}
    post_day = post.find_element_by_class_name('rel_date').text
    post_text = post.find_element_by_class_name('wall_post_text').text
    post_link = post.find_element_by_class_name('post_link').get_attribute('href')
    post_photo_links_list = []
    post_photo_links = post.find_elements_by_xpath('.//a[contains(@aria-label,"Original")]')
    for photo in post_photo_links:
        photo_link = photo.get_attribute('aria-label').split()[2]
        post_photo_links_list.append(photo_link)
    post_likes = int(post.find_elements_by_class_name('like_button_count')[0].text)
    post_share = int(post.find_elements_by_class_name('like_button_count')[1].text)

    post_data['post_day'] = post_day
    post_data['post_text'] = post_text
    post_data['post_link'] = post_link
    post_data['post_photo_links_list'] = post_photo_links_list
    post_data['post_likes'] = post_likes
    post_data['post_share'] = post_share

    posts_info.append(post_data)
    p += 1
    print(p)

db = client['tokyo_posts']
collection = db.collection
collection.insert_many(posts_info)