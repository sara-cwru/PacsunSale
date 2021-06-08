from bs4 import BeautifulSoup
import sys
import pip._vendor.requests
import re 

sort_by = sys.argv[1]

items = []
pictures = {}
links ={}
reg_prices = {}
sale_prices = {}
differences_by_price = {}
differences_by_item = {}
percentages = {}
percentages_by_item = {}
# https://www.pacsun.com/womens/sale/?srule=Featured&start=0&sz=24 


no_more = False
start_number = 0
# print('test1')

while (no_more == False):

    # convert start number to string to be used in url
    str_start_number = str(start_number)
    # print(start_number)
    # url of page
    # if (style is not None):
    URL = 'https://www.pacsun.com/womens/sale/?srule=Featured&start=' + (str_start_number)

    # getting page content
    page = pip._vendor.requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')  
    products = soup.find_all('li', class_='rwd-col-2 rwd-col-lrg-4')
    # products = soup.find_all('div', class_='product-data')  

    # check if we have reached the end
    if (len(products) == 0):
        no_more = True

        # print('test2')

        # getting each product
    for product in products:
        # print('test3')
        item_html = product.find('a', class_='name-link')
        picture_html = product.find('img')

        # get item name
        item = item_html.get('title')
        # print('test4')

        if item not in items:
            items.append(item)
            # print(item)

            # get item picture
            picture_link = picture_html['src']
            pictures[item] = picture_link
            # print(picture_link)

            # get item link
            link = item_html.get('href')
            links[item] = link
            # print(item + '\t' + link)
            # print(links[item])

            # finding regular price
            reg_price_html = product.find('div', class_='price-standard left cart-promo-strike')
            if (reg_price_html is not None):
                reg_price = reg_price_html(text=True)
                reg_price = re.search("\d*\.\d*", reg_price[0])
                reg_prices[item] = reg_price[0]
                # print(reg_prices[item])

            # finding sale price
            sale_price_html = product.find('div', class_='price-promo')
            if (sale_price_html is not None):
                sale_price = sale_price_html(text=True)
                sale_price = re.search("\d*\.\d*", sale_price[0])
                sale_prices[item] = sale_price[0]

            # finding difference 
            price_diff = float(reg_price[0]) - float(sale_price[0])
            price_diff = round(price_diff, 2)
            if price_diff not in differences_by_price:
                differences_by_price[price_diff] = list()
            differences_by_price[price_diff].append(item)
            differences_by_item[item] = price_diff

            # finding difference percentages
            price_percentage_diff = price_diff / float(reg_price[0])
            price_percentage_diff = round(price_percentage_diff, 2)
            price_percentage_diff = "{:.0%}".format(price_percentage_diff)
            if price_percentage_diff not in percentages:
                percentages[price_percentage_diff] = list()
            percentages[price_percentage_diff].append(item)
            # percentages[price_percentage_diff] = item
            percentages_by_item[item] = price_percentage_diff

    start_number += 24

# sorting by percentages
if (sort_by == 'percentages'):
    sorted_items = []
    for i in sorted (percentages.keys(), reverse = True) :
        price_list = percentages.get(i)
        for item in price_list :
            sorted_items.append(item)

    index = 0
    for item in sorted_items:
        view_link = '<a href="%s">%s</a>' % (links[item], item)
        # print(differences[price] + '<br>')
        img_link = '<a href=%s><img src="%s"> </a>' % (links[item], pictures[item])
        print(img_link + '<br><br>')
        print(view_link + '<br>')
        print('PERCENT SAVED: ' + str(percentages_by_item[item])+ '<br>')
        print('SAVED: $' + str(differences_by_item[item]) + '<br>')
        print('Original: $' + str(reg_prices[item]) + '<br>')
        print('Sale: $' + str(sale_prices[item]) + '<br> <br> <br><br>')
        index += 1

#sorting by difference
if (sort_by == 'differences'):
    sorted_items = []
    for i in sorted (differences_by_price.keys(), reverse = True) :
        price_list = differences_by_price.get(i)
        for item in price_list :
            sorted_items.append(item)

    index = 0
    for item in sorted_items:
        view_link = '<a href="%s">%s</a>' % (links[item], item)
        # print(differences[price] + '<br>')
        img_link = '<a href=%s><img src="%s"> </a>' % (links[item], pictures[item])
        print(img_link + '<br><br>')
        print(view_link + '<br>')
        print('PERCENT SAVED: ' + str(percentages_by_item[item])+ '<br>')
        print('SAVED: $' + str(differences_by_item[item]) + '<br>')
        print('Original: $' + str(reg_prices[item]) + '<br>')
        print('Sale: $' + str(sale_prices[item]) + '<br> <br> <br><br>')
        index += 1