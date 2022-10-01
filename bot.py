from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from AliExpress_Products.models import ProductsDetails
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def scrape_aliex_data(search):
    search = search.replace(" ", "+")
    URL = f"https://www.aliexpress.com/af/bottle.html?trafficChannel=af&d=y&CatId=0&SearchText={search}&ltype=affiliate&SortType=default&shipFromCountry=US&page=1"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    # S=Service(ChromeDriverManager().install())
    S=Service("/var/www/superfuturelabs/chromedriver/stable/chromedriver")
    driver = webdriver.Chrome(options=options, service=S)
    driver.get(URL)
    WAIT= WebDriverWait(driver, 60)

    # try:
    #     if driver.find_element_by_xpath("//*[contains(@class,'Sk1_X _1-SOk')]"):
    #         link =WAIT.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'Sk1_X _1-SOk')]")))
    #         driver.execute_script("arguments[0].click();",link)

    #     if driver.find_element_by_xpath("//*[contains(@src,'https://img.alicdn.com/tfs/TB1a.Oge_M11u4jSZPxXXahcXXa-48-48.png')]"):
    #         link1 =WAIT.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@src,'https://img.alicdn.com/tfs/TB1a.Oge_M11u4jSZPxXXahcXXa-48-48.png')]")))
    #         driver.execute_script("arguments[0].click();",link1)
    # except Exception as e:
    #     print(e)

    info =WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ng-item-wrap ng-item ng-switcher']")))
    info.click()
    info.click()

    country =WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[@class='shipping-text']"))).click()
    country_name =WAIT.until(EC.presence_of_element_located((By.XPATH, "//input[@class='filter-input']")))
    country_name.send_keys("United States")

    countryUS =WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'United States']"))).click()
    time.sleep(2)
    saveButton =WAIT.until(EC.presence_of_element_located((By.XPATH, "//button[@class='ui-button ui-button-primary go-contiune-btn']"))).click()

    time.sleep(2)
    shipment_From = driver.find_element(By.XPATH, "//span[@class='next-input next-medium next-select-inner']").click()
    shipment_Country = driver.find_element(By.XPATH, "//ul//li[@title='United States']").click()
    time.sleep(2)

    href_list=[]
    count = 1000
    for i in range(5):
        if i != 0:
            driver.execute_script(f"window.scrollTo({count - 1000},{count})")
            count = count + 1000
        else:
            driver.execute_script(f"window.scrollTo(0,{count})")
            count = count + 1000

        WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='product-container']//div//a[@class= '_3t7zg _2f4Ho']")))
        paths = driver.find_elements(By.XPATH,"//div[@class='product-container']//div//a[@class= '_3t7zg _2f4Ho']")
        for path in paths:
            if path.get_attribute('href') not in href_list:
                href_list.append(path.get_attribute('href'))
                # print(path.get_attribute('href'))

    # paths = driver.find_elements_by_xpath("//div[@class='product-container']//div[2]//a")

    # for path in paths:
    #     if '_3t7zg _2f4Ho' in path.get_attribute('class'):
    #         href_list.append(path.get_attribute('href'))
    #         print(path.get_attribute('href'))
    #     else:
    #         continue
    print(href_list)
    print(len(href_list))

    # for product in href_list:
        # print(product)
        # driver.get(product)

        # driver.find_element_by_xpath("//div[@class='dynamic-shipping']").click()
        # time.sleep(3)
        # try:
            # if driver.find_element_by_xpath("//div[@class='comet-modal-content']//div[2]//button"):
                # print("Check", True)
                # driver.find_element_by_xpath("//div[@class='comet-modal-content']//div[2]//button").click()

                # shipping_options = driver.find_elements_by_xpath("//div[@class='comet-modal-content']//div[@class='comet-modal-body _1yog9']//div[@class='_3yzHC']")
                # print("Shipping Options", shipping_options)
                # for ship_option in shipping_options:
                    # if ship_option.find_element_by_xpath("//div[@class='dynamic-shipping']//div[1]//span//span//strong").text == "Free Shipping":
                        # shipping_method = ship_option.find_element_by_xpath("//div[@class='dynamic-shipping']//div[2]//span[5]").text
                        # shipping_method = shipping_method.split("via ")[-1]
                        # print(shipping_method)
        # except:
            # print("Exception")
            # driver.find_element_by_xpath("//div[@class='comet-modal-content']//div[2]//button").click()
            # shipping_options = driver.find_elements_by_xpath("//div[@class='comet-modal-content']//div[@class='comet-modal-body _1yog9']//div[@class='_3yzHC']")
            # print("Shipping Options", shipping_options)
            # for ship_option in shipping_options:
                # if ship_option.find_element_by_xpath("//div[@class='dynamic-shipping']//div[1]//span//span//strong").text == "Free Shipping":
                    # shipping_method = ship_option.find_element_by_xpath("//div[@class='dynamic-shipping']//div[2]//span[5]").text
                    # shipping_method = shipping_method.split("via ")[-1]
                    # print(shipping_method)
        # try:
        #     price = driver.find_element_by_xpath("//div[@class='product-price-current']//span[@class='product-price-value']").text
        # except:
        #     price = driver.find_element_by_xpath("//div[@class='uniform-banner']//div[2]//div//span").text
        # title = driver.find_element_by_xpath("//div[@class='product-title']//h1").text
        # image = driver.find_element_by_xpath("//div[@class='image-viewer']//div[@class='image-view-magnifier-wrap']//img").get_attribute('src')
        # url = driver.current_url

        # print(title, image, price, url)

    # products = []
    # shipping_option_list = []
    # shipping_option_hash = {"shipping_method": shipping_method, "shipping_price": shipping_price, "shipping_speed": shipping_speed, "estimate_time": estimate_time}
    # product_hash = {"title": title, "price": price, "image": image, "url": url, "shipping_options": shipping_option_list}


def save_products(products):
    products_to_be_created = []
    for product in products:
        shipping_options = product["shipping_options"]
        for shipping_option in shipping_options:
            shipping_method = shipping_option["shipping_method"]
            shipping_price = shipping_option["shipping_price"]
            shipping_speed = shipping_option["shipping_speed"]
            estimate_time = shipping_option["estimate_time"]
            title = product["title"]
            price = product["price"]
            image_url = product["image"]
            url = product["url"]
            products_to_be_created.append(
                ProductsDetails(product_name=title, url=url, image_url=image_url, cost=price,
                                shipping_price=shipping_price, total_price=float(price + shipping_price),
                                shipping_method=shipping_method, shipping_speed=shipping_speed,
                                arrive_by=estimate_time)
            )
    ProductsDetails.objects.bulk_create(products_to_be_created, ignore_conflicts=True)

