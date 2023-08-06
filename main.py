from sqlalchemy import create_engine
import sqlite3
from selenium.webdriver.common.by import By
from client_info import password, login
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.implicitly_wait(2)

# connect to login page
driver.get("https://www.linkedin.com/home")
driver.implicitly_wait(5)
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

    # Load
    engine = create_engine('sqlite:///applicant_db.sqlite3', echo=True)
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
    company_name = input("Input company name: ")
    if company_name == "":
        return
    #link= 'https://www.linkedin.com/search/results/COMPANIES/?origin=SWITCH_SEARCH_VERTICAL&sid=x_P'
    #'https://www.linkedin.com/search/results/COMPANIES/?companyHqGeo=%5B%22101165590%22%2C%22101282230%22%2C%22102264497%22%2C%22103350119%22%2C%22105015875%22%2C%22105072130%22%2C%22105646813%22%5D&companySize=%5B%22I%22%5D&industryCompanyVertical=%5B%221862%22%5D&origin=FACETED_SEARCH&sid=K-9'

    print("Company info collected successfully.")
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