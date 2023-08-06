import selenium.common.exceptions
from sqlalchemy import create_engine
import sqlite3
from selenium.webdriver.common.by import By
from client_info import password, login
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

#chrome_options = ChromeOptions()
#chrome_options.add_argument('--headless')

# Load
engine = create_engine('sqlite:///applicant_db.sqlite3', echo=True)


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(5)


# connect to login page

time.sleep(5)
driver.implicitly_wait(20)
driver.get("https://www.linkedin.com/home")
time.sleep(5)
driver.refresh()
time.sleep(5)
#driver.add_cookie({"name": "foo", "value": "bar"})

driver.implicitly_wait(5)

# input login mail or telephone for LinkedIn
input_login = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/div/form/div[1]/div[1]/div/div/input')
input_login.send_keys(login)

driver.implicitly_wait(5)
# input password for your LinkedIn
input_password = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/div/form/div[1]/div[2]/div/div/input')
input_password.send_keys(password)

driver.implicitly_wait(5)

# submit button click
submit_button = driver.find_element(By.XPATH, '/html/body/main/section[1]/div/div/form/div[2]/button')
submit_button.click()

driver.implicitly_wait(5)

# Funtion to scrape data from LinkedIn page
def collect_applicant_info():

    linkedin = input("Input application link: ")
    if linkedin == "":
        return
    driver.get(linkedin)

    driver.implicitly_wait(5)
    full_name = driver.find_element(By.XPATH,
        '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1')
    full_name = full_name.text

    driver.implicitly_wait(5)
    name_parts = full_name.split()

    # first name applicant
    first_name = name_parts[0]
    print(f'Name: {first_name}')

    # last name applicant
    last_name = name_parts[-1]
    print(f'Last name: {last_name}')

    # Current company applicant
    current_company = driver.find_element(By.XPATH,
        '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/ul/li[1]/button/span/div')
    current_company = current_company.text
    print(f'Current company: {current_company}')

    # title applicant
    title = driver.find_element(By.XPATH,
        '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]')
    title = title.text
    print(f'Titile: {title}')

    # location applicant
    location = driver.find_element(By.XPATH,
        '/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]')
    location = location.text
    print(f'Location: {location}')


    applicant_dict = {
        'linkedin': linkedin,
        'first_name': first_name,
        'last_name': last_name,
        'current_company': current_company,
        'title': title,
        'location': location}

    applicant_df = pd.DataFrame(applicant_dict, index=[0],
                                columns=['linkedin', 'first_name', 'last_name', 'current_company', 'title', 'location'])


    conn = sqlite3.connect('applicant_db.sqlite3')
    cursor = conn.cursor()

    create_table_query = """
        CREATE TABLE IF NOT EXISTS applicants(
            linkedin TEXT,
            first_name TEXT,
            last_name TEXT,
            current_company TEXT,
            title TEXT,
            location TEXT
        );
    """
    cursor.execute(create_table_query)

    applicant_df.to_sql("applicants", engine, if_exists='append', index=False)
    cursor.close()

    ### sava in csv

    #output_file = "test.csv"
    #applicant_df.to_csv(output_file, index=False, mode='a', header=not pd.read_csv(output_file).empty)

    print("Applicant info collected successfully.\n")
    return collect_applicant_info()

def collect_company_info():
    linkedin_company_link = []
    company_name = []
    company_website = []
    industry = []
    employees_on_linkedin = []
    company_size = []
    hq = []

    link_sources = input("Input link for your searches: ")
    if link_sources == "":
        return

    # Link for your task
    #link_sources = "https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22102974008%22%2C%22104341318%22%2C%22106137034%22%2C%22101464403%22%2C%22104738515%22%2C%22103819153%22%2C%22100456013%22%2C%22103119917%22%2C%22104514075%22%2C%22105333783%22%2C%22101855366%22%2C%22106693272%22%2C%22101452733%22%2C%22100288700%22%2C%22100364837%22%2C%22104677530%22%2C%22104508036%22%2C%22105117694%22%2C%22100565514%22%2C%22102890719%22%2C%22106670623%22%2C%22101165590%22%2C%22101282230%22%2C%22102264497%22%2C%22103350119%22%2C%22105015875%22%2C%22105072130%22%2C%22105646813%22%5D&companySize=%5B%22I%22%5D&industryCompanyVertical=%5B%221862%22%5D&origin=FACETED_SEARCH&sid=rLp"


    driver.get(link_sources)
    driver.implicitly_wait(5)
    time.sleep(3)


    li_elements = driver.find_elements(By.CSS_SELECTOR, 'li.reusable-search__result-container')


    for li_element in li_elements[:3]:

        a_elements = li_element.find_elements(By.CSS_SELECTOR, 'a.app-aware-link.scale-down')
        for a_element in a_elements:
            linkedin_company = a_element.get_attribute('href')
            linkedin_company_link.append(linkedin_company)


    #linkedin_company_link
    for link in linkedin_company_link:
        driver.get(link)
        time.sleep(5)
        driver.implicitly_wait(5)

        i_company_name = driver.find_element(By.CSS_SELECTOR, 'h1.ember-view.text-display-medium-bold.org-top-card-summary__title')
        i_company_name = i_company_name.text
        company_name.append(i_company_name)

        driver.implicitly_wait(5)
        time.sleep(3)
        i_company_website = driver.find_element(By.CSS_SELECTOR, 'a.ember-view.org-top-card-primary-actions__action')
        i_company_website = i_company_website.get_attribute('href')
        company_website.append(i_company_website)

        try:
            driver.implicitly_wait(5)
            time.sleep(3)
            i_industry = driver.find_element(By.CSS_SELECTOR, 'div.inline-block.div.org-top-card-summary-info-list__info-item')
            i_industry = i_industry.text
            industry.append(i_industry)
        except selenium.common.exceptions.NoSuchElementException:
            i_industry = '-'
            industry.append(i_industry)


        try:
            driver.implicitly_wait(5)
            time.sleep(3)
            i_employees_on_linkedin = driver.find_element(By.CSS_SELECTOR, 'span.t-normal.t-black--light.link-without-visited-state.link-without-hover-state')
            i_employees_on_linkedin = i_employees_on_linkedin.text.strip()
            employees_on_linkedin.append(i_employees_on_linkedin)
        except selenium.common.exceptions.NoSuchElementException:
            i_employees_on_linkedin = "-"
            employees_on_linkedin.append(i_employees_on_linkedin)


        try:
            driver.implicitly_wait(5)
            time.sleep(3)
            i_company_size = driver.find_element(By.CSS_SELECTOR, 'dd.t-black--light.text-body-medium.mb1')
            i_company_size = i_company_size.text.strip()
            company_size.append(i_company_size)
        except selenium.common.exceptions.NoSuchElementException:
            i_company_size = "-"
            company_size.append(i_company_size)

        try:
            driver.implicitly_wait(5)
            time.sleep(3)
            i_hq = driver.find_element(By.CSS_SELECTOR, 'div.inline-block.div.org-top-card-summary-info-list__info-item')
            i_hq = i_hq.text.strip()
            hq.append(i_hq)
        except selenium.common.exceptions.NoSuchElementException:
            i_hq = "-"
            hq.append(i_hq)

    companies_dict = {
        'linkedin_company_link':linkedin_company_link,
        'company_name': company_name,
        'company_website': company_website,
        'industry': industry,
        'employees_on_linkedin': employees_on_linkedin,
        'company_size': company_size,
        'hq': hq
    }

    companies_df = pd.DataFrame(companies_dict,
        columns=['linkedin_company_link', 'company_name', 'company_website',
                 'industry', 'employees_on_linkedin', 'company_size', 'hq'])

    # Load

    conn = sqlite3.connect('applicant_db.sqlite3')
    cursor = conn.cursor()

    # crea
    create_table_query_1 = """
            CREATE TABLE IF NOT EXISTS companies(
                linkedin_company_link TEXT,
                company_name TEXT,
                company_website TEXT,
                industry TEXT,
                employees_on_linkedin TEXT,
                company_size TEXT,
                hq TEXT
            );
        """
    cursor.execute(create_table_query_1)

    companies_df.to_sql("companies", engine, if_exists='append', index=False)
    cursor.close()


    print("Companys info collected successfully.")
    return collect_company_info()

while True:
    print("1. Collect info about applicant")
    print("2. Collect info about company")
    rpc_call = input("Which RPC would you like to make (or nothing to stop chatting): ")

    if rpc_call == "":
        driver.quit()
        break

    elif rpc_call == "1":
        collect_applicant_info()

    elif rpc_call == "2":
        collect_company_info()

    else:
        print("Invalid input. Please enter a valid option.")