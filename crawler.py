from selenium import webdriver
import time
import csv


def search_product(key):
    driver.find_element_by_id('q').send_keys(key)
    driver.find_element_by_class_name('btn-search').click()
    driver.maximize_window()
    time.sleep(15)


def get_productdata(key):
    pages = driver.find_elements_by_xpath('//div[@class="m-page g-clearfix"]/div[@class="wraper"]/div[@class="inner '
                                          'clearfix"]/div[@class="total"]')
    for i in pages:
        pg = i.get_attribute('textContent')
    number = list(filter(str.isdigit, pg))
    pgnum = 0
    for i in range(len(number)):
        pgnum = pgnum + int(number[i])*(10**(len(number)-1-i))
    #print(pgnum)
    for i in range(round(0.8*pgnum)):
        divs = driver.find_elements_by_xpath('//div[@class="items"]/div[@class="item J_MouserOnverReq  "]')
        for div in divs:
            info = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
            price = float(div.find_element_by_xpath('.//strong').text)
            deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
            number = list(filter(str.isdigit, deal))
            dealnum = 0
            for i in range(len(number)):
                dealnum = dealnum + int(number[i]) * (10 ** (len(number) - 1 - i))
            name = div.find_element_by_xpath('.//div[@class="shop"]/a').text
            with open(key + 'data.csv', 'a', newline="", encoding='utf-8-sig') as filecsv:
                csvwriter = csv.writer(filecsv, delimiter=',')
                csvwriter.writerow([info, price, dealnum, name])
        next_button = driver.find_element_by_css_selector('li.item.next')
        if 'next-disabled' not in next_button.get_attribute('class'):
            next_button.click()
        time.sleep(2)


def main():
    search_product(keyword)
    get_productdata(keyword)


if __name__ == '__main__':
    chrome_driver = r"D:\Chromedriver\chromedriver.exe"
    keyword = input("请输入商品关键字：")
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://www.taobao.com/")
    main()
