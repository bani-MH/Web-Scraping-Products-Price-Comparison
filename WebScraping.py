import requests
from bs4 import BeautifulSoup

#Function to convert the price's format (example: from '9 900.900DT' to float 9900.900)
def Convert(price_string):
    
    price_string = price_string.replace(' ', '') #Replace any space found in the string with empty character
    
    #Replace any special character found in the string with empty character
    price_string = price_string.replace('\xa0', '') 
    price_string = price_string.replace('\u202f', '')

    price_float = '' #Initialize an empty string to stock the new value in
    for i in range (len(price_string)):
        if (not price_string[i].isalpha()) or price_string[i]==',' or price_string[i]=='.': #Make sure the character of the index i is a digit or ','/'.'
            if (price_string[i]==',' or price_string[i]=='.'): #Replace ',' with '.'
                price_float = price_float + '.'
            else :
                price_float += price_string[i] #If price_string[i] is a digit it will be added to the new string
    price_float = float(price_float) #Change the type of the string containing a float to a numeric value
    return price_float

#Scrape the website TunisiaNet
def ScrapeTunisiaNet(query):
    #Search for the product with the customised url using the {query} variable
    url = f"https://www.tunisianet.com.tn/recherche?controller=search&orderby=price&orderway=asc&s={query}&submit_search="
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser") #Get the whole content of the web page

    prices = soup.find_all("span", itemprop="price") #Extract all the product prices presented in the page using the HTML tag
    labels = soup.find_all("h2", itemprop="name") #Extract all the product names presented in the page using the HTML tag
    
    tab = [] #Declare an empty array

    #Arrange each couple of values in a table case
    for i in range (len(labels)):
        name = labels[i].text.strip()
        tab.append({"productname": name, "pricetag": Convert(prices[i].text)}) #Add a matching couple of variables and convert the price to a float

    #Initialize the default minimum values
    minprice = tab[0]["pricetag"]
    minprice_label = tab[0]["productname"]
    for c in range (len(labels)):
        if (tab[c]["pricetag"] < minprice): #Check if the current price is inferior to the default minimum price
            minprice = tab[c]["pricetag"] #Make it the new minimum value for minprice
            minprice_label = tab[c]["productname"] #Make it the new minimum value for minprice_label
            
    return minprice, minprice_label


#Scrape the website wikitn
def ScrapeSBS(query):
    #Search for the product with the customised url using the {query} variable
    url = f"https://www.sbsinformatique.com/recherche?controller=search&s={query}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser") #Get the whole content of the web page

    prices = soup.find_all("span", class_="price") #Extract all the product prices presented in the page using the HTML tag
    labels = soup.find_all("h6", itemprop="name") #Extract all the product names presented in the page using the HTML tag
    
    tab = [] #Declare an empty array

    #Arrange each couple of values in a table case
    for i in range (len(labels)):
        name = labels[i].text.strip()
        tab.append({"productname": name, "pricetag": Convert(prices[i].text)}) #Add a matching couple of variables and convert the price to a float
 
    #Initialize the minimum values
    minprice = tab[0]["pricetag"]
    minprice_label = tab[0]["productname"]
    for c in range (len(labels)):
        if (tab[c]["pricetag"] < minprice): #Check if the current price is inferior to the default minimum price
            minprice = tab[c]["pricetag"] #Make it the new minimum value for minprice
            minprice_label = tab[c]["productname"] #Make it the new minimum value for minprice_label
            
    return minprice, minprice_label

#Scrape the website Mytek
def ScrapeMyTek(query):
    #Search for the product with the customised url using the {query} variable
    url = f"https://www.mytek.tn/catalogsearch/result/?q={query}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser") #Get the whole content of the web page

    prices = soup.find_all("span", class_="price") #Extract all the product prices presented in the page using the HTML tag
    labels = soup.find_all("a", class_="product-item-link") #Extract all the product names presented in the page using the HTML tag
    
    tab = [] #Declare an empty array

    #Arrange each couple of values in a table case
    for i in range (len(prices)):
        name = labels[i].text.strip()
        tab.append({"productname": name, "pricetag": Convert(prices[i].text)}) #Add a matching couple of variables and convert the price to a float

    #Initialize the minimum values
    minprice = tab[0]["pricetag"]
    minprice_label = tab[0]["productname"]
    for c in range (len(prices)):
        if (tab[c]["pricetag"] < minprice): #Check if the current price is inferior to the default minimum price
            minprice = tab[c]["pricetag"] #Make it the new minimum value for minprice
            minprice_label = tab[c]["productname"] #Make it the new minimum value for minprice_label
            
    return minprice, minprice_label


query = input("Input a product name :\n")
query = query.replace(' ', '+') #Replace any spaces with '+' to fit into the URL used to search for the product

#Retrieve the values into variables
price_Tnet, label_Tnet = ScrapeTunisiaNet(query)
price_Mytek, label_Mytek = ScrapeMyTek(query)
price_SBS, label_SBS = ScrapeSBS(query)

#Cheapest price of the prooduct on each single website
print("Cheapest price on Tunisianet.com.tn : ", label_Tnet, " : ", format(float(price_Tnet), '.3f'), "DT")
print("Cheapest price on SBSinformatique.tn : ", label_SBS, " : ", format(float(price_SBS), '.3f'), "DT")
print("Cheapest price on Mytek.tn : ", label_Mytek, " : ", format(float(price_Mytek), '.3f'), "DT")

#Cheapest price of the prooduct oamong the three websites
print("Cheapest price among the 3 websites : ", format(min(price_Tnet, price_SBS, price_Mytek), '.3f'), " DT")
