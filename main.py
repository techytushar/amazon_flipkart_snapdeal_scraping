from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
from selenium import webdriver

#loading the webdriver.
driver = webdriver.PhantomJS('phantomjs')
amazon_url= 'http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
flipkart_url = 'https://www.flipkart.com/search?q='
snapdeal_url = 'https://www.snapdeal.com/search?keyword='
keyword = input('Enter the product you want to search for - ').split()
#adding the seach query to the url.
for item in keyword:
    amazon_url += item+'+'
    flipkart_url += item+'%20'
    snapdeal_url += item+'%20'
#removing the + and %20 at the end of url.
amazon_url = amazon_url[:-1]
flipkart_url = flipkart_url[:-3]
snapdeal_url = snapdeal_url[:-3]

#scraping amazon using requests.
def amazon(url):
    try:
        source = requests.get(url).content
        soup = BeautifulSoup(source,'lxml')
        products = soup.find_all("a",{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
        price = soup.find_all("span", {"class": "a-size-base a-color-price s-price a-text-bold"})
        #checking if the website has the product.
        if(len(products)>0 and len(price)>0):
            #trimming the list to 3 elements
            products = products[0:3]
            price = price[0:3]
            amazon_results = []
            #making new list to use with the tabulate function.
            for item,money in zip(products,price):
                amazon_results.append([item.string,money.text])
            #printing the results in form of table.
            print(tabulate(amazon_results, headers=["Products on Amazon", "Price"], tablefmt="fancy_grid"))
        else:
            print("Amazon does not sell this product.\n")
    except:
        print("An error occured while loading the webpage. Please check your internet connection and try again.\n")

#scraping snapdeal. Same process as of amazon.
def snapdeal(url):
    try:
        source = requests.get(url).content
        soup = BeautifulSoup(source, 'lxml')
        products = soup.find_all("p", {"class": "product-title"})
        price = soup.find_all("span", {"class": "lfloat product-price"})
        if(len(products)>0 and len(price)>0):
            products = products[0:3]
            price = price[0:3]
            results = []
            for item, money in zip(products, price):
                results.append([item.string, money.text])
            print(tabulate(results, headers=["Product on Snapdeal", "Price"], tablefmt="fancy_grid"))
        else:
            print("SnapDeal does not sell this product.")
    except:
        print("An error occured while loading the webpage. Please check your internet connection and try again.")

def print_flipkart(products,price):
    products = products[0:3]
    price = price[0:3]
    results = []
    for item, money in zip(products, price):
        results.append([item.text, money.text])
    print(tabulate(results, headers=["Product on Flipkart", "Price"], tablefmt="fancy_grid"))

#flipkart uses javascript on its website hence scraping it using PhantomJS webdriver.
def flipkart(url):
    try:
        driver.set_page_load_timeout(20)
        driver.get(url)
        products = driver.find_elements_by_css_selector("._2cLu-l")
        price = driver.find_elements_by_css_selector("._1vC4OE")
        if (len(products) > 0 and len(price) > 0):
            print_flipkart(products,price)
        else:
            products = driver.find_elements_by_css_selector("._3wU53n")
            price = driver.find_elements_by_css_selector("._1vC4OE._2rQ-NK")
            if(len(products) > 0 and len(price) > 0):
                print_flipkart(products,price)
            else:
                print("Flipkart does not sell this product.\n")
    except Exception as e:
        print("An error occured while loading the webpage. ",e)
    finally:
        driver.close()

#calling the function
amazon(amazon_url)
snapdeal(snapdeal_url)
flipkart(flipkart_url)