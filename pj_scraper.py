#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Nom de l'entreprise ,
# Contact
# Mail
# Secteur d'activite
# Adresse

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from urllib.parse import urlparse



def get_info(driver, secteur_activite, contact_list, verbose):
    #Open all contacts & mail
    btn_adress = driver.find_elements_by_xpath('.//div[@class="ct-itemProducts ct-u-marginBottom20"]//div[@class="ct-main-content"]//div//div[@class="ct-product--description"]//div[@class="buttonShowCo"]')

    for btn in btn_adress:
        btn.click()
    time.sleep(3)
    
    # Get all Entreprises 
    try:
        entreprises = driver.find_elements_by_xpath('.//div[@class="ct-itemProducts ct-u-marginBottom20"]//div[@class="ct-main-content"]//div//div[@class="ct-product--tilte"]')
    except NoSuchElementException:
        entreprises = []
        
    # Get all addresses
    try:
        adresses = driver.find_elements_by_xpath('.//div[@class="ct-itemProducts ct-u-marginBottom20"]//div[@class="ct-main-content"]//div//div[@class="ct-product--description"]')
    except NoSuchElementException:
        adresses = []
    
    # Get phone & mail
    try:
        contacts = driver.find_elements_by_xpath('.//div[@class="ct-itemProducts ct-u-marginBottom20"]//div[@class="ct-main-content"]//div//div[@class="ct-product--description"]//div[contains(@id, "coordonnees")]')
    except NoSuchElementException:
        contacts = []
    
    # Walking through entreprises
    for (entreprise, adress, contact) in zip(entreprises, adresses, contacts):
        entreprise_name = entreprise.text
        adress_loc = adress.text.split('\n')[0]
        contact_phone = contact.text.split('\n')[0]
        
        # Check if mail field exists
        if len(contact.text.split('\n')) > 1:
            contact_mail = contact.text.split('\n')[1]
        else:
            contact_mail = ""
        
        contact_list.append({
                        "Entreprise": entreprise_name,
                        "Contact": contact_phone, 
                        "Mail": contact_mail,
                        "Secteur d'activite": secteur_activite,
                        "Adresse": adress_loc,
                        })    
    
        if verbose:
            print(f"Entreprise: {entreprise_name}")
            print(f"Contact: {contact_phone}")
            print(f"Mail: {contact_mail}")
            print(f"Secteur d'Activite: {secteur_activite}")
            print(f"Adresse: {adress_loc}")
            
            
        
    
    return contact_list
 
def get_contacts(verbose,
                 driver_path,
                 timer):

    '''Gathers contact information from Yellow Page Africa - Specifically Magadascar'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Load Driver 
    driver = webdriver.Chrome(executable_path=driver_path, options=options)
    driver.set_window_size(1120, 1000)
    url = "https://www.lespagesjaunesafrique.com/pays/madagascar/"
    #url = "https://www.lespagesjaunesafrique.com/societes/madagascar/associations/"
    driver.get(url)
    # Where to save all contact 
    contact_list = []
    
    #sect_activites = driver.find_elements_by_xpath('.//a[contains(@href, "/societes/madagascar/")]//div//h3[@class="activites"]')
    
    # Get all Secteur d'Activite name 
    sect_act_name_list = driver.find_elements_by_xpath('.//a[contains(@href, "/societes/madagascar/")]//div//h3[@class="activites"]')
    
    # Get all links linking to each Secteur d'Activite 
    sect_act_link_list = []

    # Retrieve Secteur d'Activite links using 'href' attribute value 
    for i in range(len(sect_act_name_list)):
        sect_act_link_list.append(
                sect_act_name_list[i].find_element_by_xpath('./../..').get_attribute('href')
                )
        # Get the Secteur d'Activite name 
        sect_act_name = sect_act_name_list[i]

    
    # Navigate to Secteur d'Activite link one-by-one 
    for j, link in enumerate(sect_act_link_list):
        driver.get(link)
        time.sleep(5)
        # Get pagination links if exists
        pagination_link_list = []
        try:
            pagination_links = driver.find_elements_by_xpath('.//div[@class="ct-pagination text-center"]//ul[@class="pagination"]//li//a')
            # Create a list of all pagination links 
            for i in range(len(pagination_links)):
                pagination_link_list.append(
                        pagination_links[i].get_attribute("href")
                        )
        except NoSuchElementException:
            print("No pagination")
        
        
        
        # If pagination has existed 
        if pagination_link_list:
            for page_link in pagination_link_list:
                if urlparse(page_link).scheme != '':
                    driver.get(page_link)
                    time.sleep(4)
                    contact_list = get_info(driver, sect_act_name, contact_list, verbose)
        else:
            contact_list = get_info(driver, sect_act_name, contact_list, verbose)
        
        if j==5: 
            return contact_list
   

