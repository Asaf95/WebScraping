import pandas as pd; import requests; from bs4 import BeautifulSoup

rows = [];  counter = 0   # we use these later on.
Web_N = 'https://kualastyle.com/collections/%D7%A7%D7%95%D7%A0%D7%A1%D7%95%D7%9C%D7%95%D7%AA-%D7%9E%D7%A2%D7%95%D7%A6%D7%91%D7%95%D7%AA?sort_by=best-selling'
Agent_N = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

"Scraping the web and converting to XML "
headers = {'User-Agent': Agent_N}   # create an anonymous agent (so we won't get blocked):
r = requests.get(Web_N, headers=headers)    # request website:
soup = BeautifulSoup(r.content, 'lxml')

"Getting the relevant data from our category:"
productlist = soup.find_all('div',class_='product-list-item')     # getting links for all items in the page
all_imgs = soup.find_all('img', class_='only-image')    # getting the images for each product
ctg = soup.find('h1', class_='page-title').text     # getting the category of our products

"""Here we iterate over every link, enter each product page, 
and scrape the information we need. We add this to a dictionary everytime for the final DF"""
for item in productlist:  # 'item' is what we got from the main page
    link = 'https://kualastyle.com' + item.find_all('a', href=True)[0]['href']  # get URL from the main page and creating the URL for every product
    r = requests.get(link, headers=headers)  # Getting the raw data of the product page
    soup = BeautifulSoup(r.content, 'lxml')  # converting the data to "XML"
    prodName = (soup.find('div', class_='product-details').text.strip()).partition('\n')[0]  # name of the product
    Price = soup.find('span', class_="product-price-minimum money").text.strip()  # price of the product
    Size = soup.find('div', class_='easyslider-content-wrapper').ul.text.strip()  # size of the product
    Description = (soup.find('div', class_='easyslider-content-wrapper').span.text).partition('מידות')[0]

    url_Image = all_imgs[2 * counter]['src']  # url_Image of the description
    productsDic = {'prodName': prodName, 'category': ctg, 'Price': Price, 'Size': Size, 'Description': Description,
                   'url_Image': url_Image}
    rows.append(productsDic)
    df = pd.DataFrame(rows)  # creating new DF everytime with the new product
    counter += 1  # Moving to the next product :)

df.to_csv(r'C:\products.csv', index=False, header=True, encoding='utf-8-sig')
