from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from futurelabs.models import ProductsDetails
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
    WAIT= WebDriverWait(driver, 30)
    time.sleep(5)
    try:
         if driver.find_element_by_xpath("//*[contains(@class,'Sk1_X _1-SOk')]"):
             link =WAIT.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'Sk1_X _1-SOk')]")))
             driver.execute_script("arguments[0].click();",link)

         if driver.find_element_by_xpath("//*[contains(@src,'https://img.alicdn.com/tfs/TB1a.Oge_M11u4jSZPxXXahcXXa-48-48.png')]"):
             link1 =WAIT.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@src,'https://img.alicdn.com/tfs/TB1a.Oge_M11u4jSZPxXXahcXXa-48-48.png')]")))
             driver.execute_script("arguments[0].click();",link1)
    except:
         print("Exception on notification")

    info =WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ng-item-wrap ng-item ng-switcher']")))
    info.click()
    info.click()

    country =WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[@class='shipping-text']"))).click()
    country_name =WAIT.until(EC.presence_of_element_located((By.XPATH, "//input[@class='filter-input']")))
    country_name.send_keys("United States")

    countryUS =WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[text() = 'United States']"))).click()
    time.sleep(2)
    saveButton =WAIT.until(EC.presence_of_element_located((By.XPATH, "//button[@class='ui-button ui-button-primary go-contiune-btn']"))).click()

    try:
        # WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[@class='next-input next-medium next-select-inner']")))
        shipment_From = WAIT.until(EC.presence_of_element_located((By.XPATH, "//span[@class='next-input next-medium next-select-inner']"))).click()
        shipment_Country = WAIT.until(EC.presence_of_element_located((By.XPATH, "//ul//li[@title='United States']"))).click()
    except: print("Shipping From US Exceptions")
    time.sleep(2)

    href_list=[]
    for pages in range(2):
        count = 1000
        for i in range(int(5.5)):
            if i != 0:
                driver.execute_script(f"window.scrollTo({count - 1000},{count})")
                count  = count + 1000
            else:
                driver.execute_script(f"window.scrollTo(0,{count})")
                count = count + 1000
            WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='product-container']//div//a[@class= '_3t7zg _2f4Ho']")))
            paths = driver.find_elements(By.XPATH,"//div[@class='product-container']//div//a[@class= '_3t7zg _2f4Ho']")
            for path in paths:
                if path.get_attribute('href') not in href_list:
                    href_list.append(path.get_attribute('href'))
        try:
            WAIT.until(EC.presence_of_element_located((By.XPATH, "//button[@class='next-btn next-medium next-btn-normal next-pagination-item next-next']")))
            next_button = driver.find_element(By.XPATH, "//button[@class='next-btn next-medium next-btn-normal next-pagination-item next-next']").click()
        except: print("No Next Page")
        time.sleep(2)
    print(f"Number of Products: {len(href_list)}")

    via = ["UPS", "USPS", "USPS Priority Mail", "FEDEX"]
    day_via = ["7-Day Delivery", "10-Day Delivery", "12-Day Delivery"]
    all_via = ["UPS", "USPS", "USPS Priority Mail", "FEDEX", "7-Day Delivery", "10-Day Delivery", "12-Day Delivery"]
    products = []
    for product in href_list:
        driver.get(product)
        shipping_option_list = []

        try:
            price = driver.find_element(By.XPATH,"//div[@class='product-price-current']//span[@class='product-price-value']").text
        except:
            price = driver.find_element(By.XPATH,"//div[@class='uniform-banner']//div[2]//div//span").text
        title = driver.find_element(By.XPATH,"//div[@class='product-title']//h1").text
        image = driver.find_element(By.XPATH,"//div[@class='image-viewer']//div[@class='image-view-magnifier-wrap']//img").get_attribute('src')
        url = driver.current_url
        print(title, image, price, url)

        driver.find_element(By.XPATH,"//div[@class='dynamic-shipping']").click()
        time.sleep(3)
        try:
            driver.find_element(By.XPATH,"//div[@class='comet-modal-content']//div[2]//button")
            print("Check", True)
            WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[@class='comet-modal-content']//div[2]//button")))
            driver.find_element(By.XPATH,"//div[@class='comet-modal-content']//div[2]//button").click()
            time.sleep(3)
            WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'comet-modal-body')]/div")))
            shipping_options = driver.find_elements(By.XPATH,"//div[contains(@class,'comet-modal-body')]/div")
        except:
            print("Exception")
            WAIT.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'comet-modal-body')]/div")))
            shipping_options = driver.find_elements(By.XPATH,"//div[contains(@class,'comet-modal-body')]/div")
        a = 1
        shipping_option_list = []
        for ship_option in shipping_options:
            shipping_method = ship_option.find_elements(By.XPATH,"//span[contains(text(),'From')]/..")[a].text.split("via ")[-1]
            shipping_speed = ship_option.find_elements(By.XPATH,"//span[contains(text(),'Estimated')]/..")[a].text.split(": ")[-1]
            shipping_price = ship_option.find_elements(By.XPATH, "//span/strong[contains(text(),'Free Shipping') or contains(text(),'$')]")[a].text
            if "$" in shipping_price:
                shipping_price = shipping_price.split(": ")[-1]
            else:
                shipping_price = "$0.0"
            a = a +1
            if shipping_method in via:
                print(shipping_method)
                print(shipping_speed)
                print(shipping_price)
                shipping_option_hash = {"shipping_method": shipping_method, "shipping_price": shipping_price, "shipping_speed": shipping_speed}
                print(shipping_option_hash)
                shipping_option_list.append(shipping_option_hash)
        if len(shipping_option_list) >= 1:
            product_hash = {"title": title, "price": price, "image": image, "url": url, "shipping_options": shipping_option_list}
            print(product_hash)
            products.append(product_hash)
    save_products(products)


def save_products(products):
    products_to_be_created = []
    for product in products:
        try:
            shipping_options = product["shipping_options"]
            for shipping_option in shipping_options:
                shipping_method = shipping_option["shipping_method"]
                shipping_price = shipping_option["shipping_price"]
                shipping_speed = shipping_option["shipping_speed"]
                title = product["title"]
                price = product["price"]
                image_url = product["image"]
                url = product["url"]
                if '-' in price: continue
                if '$' in price: price = float(price.split("$")[-1])
                if '$' in shipping_price: shipping_price = float(shipping_price.split("$")[-1])
                products_to_be_created.append(
                    ProductsDetails(product_name=title, url=url, image_url=image_url, cost=price,
                                    shipping_price=shipping_price, total_price=float(price + shipping_price),
                                    shipping_method=shipping_method, arrive_by=shipping_speed)
                )
        except: continue
    ProductsDetails.objects.bulk_create(products_to_be_created, ignore_conflicts=True)

