
# commands to install the dependencies
!pip install selenium
!apt-get update 
!apt install chromium-chromedriver

import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()

options.add_argument('--headless')

options.add_argument('--no-sandbox')

options.add_argument('--disable-dev-shm-usage')

driver= webdriver.Chrome('chromedriver',options=options)

url="https://www.basiqdental.nl/nl-nl/compomeren/?page="

pageCounter = 0

pageNumber = 0

y = 0

numberOfPages = 2

arr = []

for x in range(numberOfPages*20):

  arr.append([])

  for j in range(8):

    arr[x].append([])

while pageCounter < numberOfPages: 
  
  driver= webdriver.Chrome('chromedriver',options=options)

  driver.get(url + str((pageNumber) + 1))

  page=driver.execute_script("return document.documentElement.outerHTML")

  driver.quit()

  soup = BeautifulSoup(page, 'lxml')

  i = 0

  items = soup.find_all('tr')

  print("Page number = " + str(pageNumber + 1))

  print("Number of items =" + str(len(items) - 1))
  
  while i < len(items) - 1:
    
    link = soup.find_all('span', attrs={'class': 'thumbnail'})[i].find('img')['src']
  
    newlink = link.replace("/small/", "/large/")
   
    title = soup.find_all('a', attrs={'class': 'product-title js-product-title'})[i]

    check = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find_all('div', attrs={'class': 'attr-box'})
    
    if(len(check) == 1):
      
      check2 = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find('div', attrs={'class': 'attr-box'}).find('span', attrs={'class': 'name'})
      
      if(check2.text.strip().encode("utf-8") == "Merk:"):
      
        brand = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find('div', attrs={'class': 'attr-box'}).find('span', attrs={'class': 'attr-title'})
      
        manufacturer = 'null'
      
        newBrand = brand.text.strip().encode("utf-8")
      
        newManufacturer = manufacturer
      
      elif (check2.text.strip().encode("utf-8") == "Code fabrikant:"):
      
        manufacturer = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find('div', attrs={'class': 'attr-box'}).find('span', attrs={'class': 'attr-title'})
      
        brand = 'null'
      
        newManufacturer = manufacturer.text.strip().encode("utf-8")
      
        newBrand = brand
    
    else:
    
      brand = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find_all('div', attrs={'class': 'attr-box'})[0].find('span', attrs={'class': 'attr-title'})
    
      manufacturer = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find_all('div', attrs={'class': 'attr-box'})[1].find('span', attrs={'class': 'attr-title'})
    
      newBrand = brand.text.strip().encode("utf-8")
    
      newManufacturer = manufacturer.text.strip().encode("utf-8")
    
    price = soup.find_all('span', attrs={'class': 'lbl-price '})[i]
    
    newprice = price.text.strip()[2:]
    
    artNo = soup.find_all('span', attrs={'class': 'product-id'})[i]
    
    unit = soup.find_all('span', attrs={'class': 'lbl-uom'})[i]
    
    productURL = soup.find_all('td', attrs={'class': 'plp-cell product-description'})[i].find('a')['href']
    
    fields = ['Title', 'Brand','manufacturer','artNo','unit','imageLink','Price', 'ProductURL']

#Storing values in an array

    arr[y][0] = title.text.strip().encode("utf-8")
    
    arr[y][1] = newBrand
    
    arr[y][2] = newManufacturer
    
    arr[y][3] = artNo.text.strip().encode("utf-8")
    
    arr[y][4] = unit.text.strip().encode("utf-8")
    
    arr[y][5] = "https://www.basiqdental.nl"+newlink.encode("utf-8").strip()
    
    arr[y][6] = newprice
    
    arr[y][7] = "https://www.basiqdental.nl"+productURL.encode("utf-8").strip()
    
    i = i + 1
    
    y = y + 1
  
  pageNumber = pageNumber + 1
  
  pageCounter = pageCounter + 1

#Creating and writing on a file

filename = "compomeren_products.csv"

with open(filename, 'a+') as csvfile: 

    csvwriter = csv.writer(csvfile) 

    csvwriter.writerow(fields) 

    csvwriter.writerows(arr)

csvfile.close()
