#!/usr/bin/env python
# coding: utf-8

# # Dependencies

# In[ ]:


#get_ipython().system('pip install selenium')
#get_ipython().system('sudo apt-get update ')
#get_ipython().system('sudo apt install chromium-chromedriver')


# # Environment

# In[1]:


import requests
import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import unquote
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver= webdriver.Chrome('chromedriver',options=options)


# # Methods

# In[ ]:


#method to get category names
def fileName_generator(linkOfCategories):

  categoryName = linkOfCategories.rsplit('/')
    
  filename = categoryName[-3].replace(' ' , '-') +'-'+ categoryName[-2].replace(' ' , '-')

  return filename

#method to get page counts of a specific category
def pageCount_getter(url):

  driver= webdriver.Chrome('chromedriver',options=options)
  
  driver.get(url)
  
  try:
  
    driver.find_elements_by_css_selector("div.paging ul")[0]
  
    pages = driver.find_elements_by_css_selector("div.paging ul")[0]
  
    if(pages.text[-2] == ' ' or pages.text[-2]== '.'):
      
      totalpages = pages.text[-1]
    
    elif(pages.text[-2] != ' ' or pages.text[-2] != '.') and (pages.text[-3] != ' ' or pages.text[-3] != '.'):
    
        totalpages = pages.text[-3] + pages.text[-2] + pages.text[-1]
    
    elif(pages.text[-2] != ' ' or pages.text[-2] != '.'):
    
      totalpages = pages.text[-2] + pages.text[-1]
    
    if(totalpages[0] == ' '):
    
      totalpages = totalpages[1:]
    
    return totalpages
  
  except:
  
    return 1


# # Scrapper Code

# In[ ]:


if(os.path.exists('/Files/') == False):
  
  parent_dir = "/Files/"
  
  path = os.path.join(parent_dir) 
  
  os.mkdir(path) 

  print("Directory named as 'Files' is created")

else:
  
  print("Directory exists")

# code to get maincategories links
mainUrl = "https://www.basiqdental.nl/"

driver.get(mainUrl)

elements = driver.find_elements_by_css_selector("div.wrapper a")

count = 0

mainCategories = []

for element in elements:

  if(element.get_attribute("href") == "https://www.basiqdental.nl/nl-nl/klantenservice/accountinformatie"):

    break

  count = count + 1

for x in range(count):

  mainCategories.append([])

i = 0

for element in elements:

  if(element.get_attribute("href") == "https://www.basiqdental.nl/nl-nl/klantenservice/accountinformatie"):

    break

  mainCategories[i] = element.get_attribute("href")

  i = i + 1

p = 0

while p<len(mainCategories):

#code to get all sub-categories of every main category
  driver= webdriver.Chrome('chromedriver',options=options)

  driver.get(mainCategories[p])

  subcategories = driver.find_elements_by_css_selector("ul.leftCatMenu-list a")

  subCategories = []
  
  for x in range(len(subcategories)):

    subCategories.append([])
  
  i = 0
  
  for subcategory in subcategories:
  
    subCategories[i] = unquote(subcategory.get_attribute("href"))
  
    i = i + 1

  k = 0
  
  while k<(len(subCategories) + 1):
  
    pageCounter = 0

    pageNumber = 0

    y = 0 

    boolean = False

    if(k < len(subCategories)):

      numberOfPages = int(pageCount_getter(subCategories[k]))

      filename = fileName_generator(subCategories[k])

      if(os.path.exists('/Files/'+filename + '.csv')):

        boolean = True
    
    else:
    
      numberOfPages = int(pageCount_getter(mainCategories[p]))

      filename = fileName_generator(mainCategories[p])

      if(os.path.exists('/Files/'+filename + '.csv')):
        
        boolean = True
    
    if(boolean == True):
    
      print("Category name: " + filename)
    
      print("File already exists")
    
    else:
    
      arr = []

      for x in range(numberOfPages*20):

        arr.append([])

        for j in range(8):

          arr[x].append([])

      while pageCounter < numberOfPages: 
    
        if(k < len(subCategories)):

          driver= webdriver.Chrome('chromedriver',options=options)
    
          driver.get(subCategories[k] + '?page=' + str((pageNumber) + 1))
          
          filename = fileName_generator(subCategories[k])
    
        else:

          driver= webdriver.Chrome('chromedriver',options=options)
    
          driver.get(mainCategories[p] + '?page=' + str((pageNumber) + 1))

          filename = fileName_generator(mainCategories[p])

        page=driver.execute_script("return document.documentElement.outerHTML")

        driver.quit()

        soup = BeautifulSoup(page, 'lxml')

        i = 0

        items = soup.find_all('tr')

        print("Category name: " + filename)

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
            
              newBrand = brand.text.strip()
            
              newManufacturer = manufacturer
            
            elif (check2.text.strip().encode("utf-8") == "Code fabrikant:"):
            
              manufacturer = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find('div', attrs={'class': 'attr-box'}).find('span', attrs={'class': 'attr-title'})
            
              brand = 'null'
            
              newManufacturer = manufacturer.text.strip()
            
              newBrand = brand
          
          else:
          
            brand = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find_all('div', attrs={'class': 'attr-box'})[0].find('span', attrs={'class': 'attr-title'})
          
            manufacturer = soup.find_all('div', attrs={'class': 'specifications-row table-row'})[i].find_all('div', attrs={'class': 'attr-box'})[1].find('span', attrs={'class': 'attr-title'})
          
            newBrand = brand.text.strip()
          
            newManufacturer = manufacturer.text.strip()
          
          price = soup.find_all('span', attrs={'class': 'lbl-price '})[i]
          
          newprice = price.text.strip()[2:]
          
          artNo = soup.find_all('span', attrs={'class': 'product-id'})[i]
          
          unit = soup.find_all('span', attrs={'class': 'lbl-uom'})[i]
          
          productURL = soup.find_all('td', attrs={'class': 'plp-cell product-description'})[i].find('a')['href']
          
          fields = ['Title', 'Brand','manufacturer','artNo','unit','imageLink','Price', 'ProductURL']

      #Storing values in an array

          arr[y][0] = title.text.strip()
          
          arr[y][1] = newBrand
          
          arr[y][2] = newManufacturer
          
          arr[y][3] = artNo.text.strip()
          
          arr[y][4] = unit.text.strip()
          
          arr[y][5] = ("https://www.basiqdental.nl"+newlink).strip()
          
          arr[y][6] = newprice
          
          arr[y][7] = ("https://www.basiqdental.nl"+productURL).strip()
          
          i = i + 1
          
          y = y + 1
        
        pageNumber = pageNumber + 1
        
        pageCounter = pageCounter + 1

      #Creating and writing on a file

      with open('/Files/'+filename+'.csv', 'a+') as csvfile: 

          csvwriter = csv.writer(csvfile) 

          csvwriter.writerow(fields) 

          csvwriter.writerows(arr)

      csvfile.close()
   
    k = k + 1
  
  p = p + 1

