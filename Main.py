from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import pynput
import time
from GUI import *


#initialize a path to the website

chrome_options.add_argument("--headless")

def main():
    PATH = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(PATH)

    # create list for the dropdown menus that need to be edited
    input_dropdown_ids = ["_9999999:EP_PolicyForm_insuredForm_insuredSOABO_vehicleInsuredSOABO_make_container",
                          "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_vehicleInsuredSOABO_model_container",
                          "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_vehicleInsuredSOABO_capacityNew_container",
                          "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_vehicleInsuredSOABO_numberofSeats",
                          "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_fieldValueMap_MT_IMPORTED_RECOND_container",
                          "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_fieldValueMap_MT_PARALLEL_IMPORT_container"]

    # initialize the excel spreadsheet
    df = pd.read_excel("db1.xlsx")

    # create list for the dropdown menu information that needs to be entered
    input_dropdown = [make_model[0:make_model.index('/')].strip(),
                      make_model[(make_model).index('/') + 1:-1].lstrip().rstrip(),
                      int(vehicle_cc[0:vehicle_cc.index('c')].strip())]

    cc_rounding = [1700, 2400, 2600, 2700, 2800, 3400, 4000]
    cc_rounded = min(cc_rounding, key=lambda x: abs(input_dropdown[2] - x))

    # open the main page and input the username and password
    driver.get(
        "https://incsso.income.com.sg/login/login.jsp?TYPE=33554432&REALMOID=06-3ee64485-af17-4712-98ff-7f87e1e40c11&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=pd_ebao_apache&TARGET=-SM-HTTP%3a%2f%2fgiportal%2eincome%2ecom%2esg%2finsurance%2fgs%2fep%2fwebflow%2fagent--main--flow%3fexecution%3de6s1%26syskey_request_token%3d269d889ef92bf6c434c2b133f16190f0")

    search = driver.find_element_by_name("USER")
    search.send_keys("A572499")

    search = driver.find_element_by_name("PASSWORD")
    search.send_keys("57249901Teck")

    login = driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div/button')
    login.click()

    # select the specific path to move to the input information table
    newB = driver.find_element_by_xpath('//*[@id="id20_menu2_menu"]/table/tbody/tr/td[2]/span[2]')
    newB.click()

    gpc = driver.find_element_by_xpath('//*[@id="cmSubMenuID1Table"]/tbody/tr[1]/td[2]')
    gpc.click()

    driver.execute_script("window.scrollTo(0, 300)")

    # find and initialize the first dropdown menu and click on it to open up the dropdown and make the website create the <div for the dropdown menu and list
    make1 = driver.find_element_by_id(input_dropdown_ids[0])
    make1.click()

    # find the <div that has the dropdown list
    make_elem = driver.find_elements_by_xpath("//div[@id='ext-gen677']/div[@class='x-combo-list-item']")

    time.sleep(1)

    # iterate through every element in the dropdown <div to find the text in the child <div that matches the car_make
    for i in range(2, len(make_elem) + 2):
        car_make = driver.find_element_by_xpath('//*[@id="ext-gen677"]/div[%s]' % i).text
        if car_make == input_dropdown[0]:
            # once a match is found go to child <div and click on it to input the car_make
            make = driver.find_element_by_xpath('//*[@id="ext-gen677"]/div[%s]' % i)
            make.click()
            break

    time.sleep(2)

    # find and initialize the second dropdown menu and click on it to open up the dropdown and make the website create the <div for the dropdown menu and list
    model1 = driver.find_element_by_id(input_dropdown_ids[1])
    model1.click()

    # find the <div that has the dropdown list
    model_elem = driver.find_elements_by_xpath("//div[@id='ext-gen699']/div[@class='x-combo-list-item']")

    # iterate through the car_model to find how many spaces there are in the string and their index
    space_list = []
    for j in range(len(input_dropdown[1])):
        if (input_dropdown[1][j] == " "):
            space_list.append(j)

    # create string for similar_car_models
    similar_car_models = []

    time.sleep(1)

    # iterate through every child <div in the dropdown <div to find similar models
    for i in range(2, len(model_elem) + 2):
        car_model = driver.find_element_by_xpath('//*[@id="ext-gen699"]/div[%s]' % i).text
        # if first part of model_name is the same then append to similar_car_models list
        if car_model == input_dropdown[1][0:space_list[0]]:
            similar_car_models.append(car_model)

    time.sleep(1)

    # while loop too cut down the number of car models by expanding the search
    # search is expanded by increasing the string length up to each space index
    while len(similar_car_models) > 1:
        # create second car model list or clear it
        similar_car_models_2 = []
        # iterate through each car model and check if it still matches the car_model
        for j in similar_car_models:
            # increase the space index of the reference model
            for i in range(1, len(space_list)):
                # if a match is found then append to second list
                if j == input_dropdown[1][0:space_list[space_list[i]]]:
                    similar_car_models_2.append(j)
        # assign list 2 to list1 and if there are still more then 1 items in the list redo the process
        similar_car_models = similar_car_models_2

    time.sleep(2)

    # check if the list has only 1 car model match
    if len(similar_car_models) == 1:
        # change from list to string with 1 model
        car_model = similar_car_models[0]
        # once again iterate through each model to find the on that matches the model
        for i in range(2, len(model_elem) + 2):
            car_model1 = driver.find_element_by_xpath('//*[@id="ext-gen699"]/div[%s]' % i).text
            # if match is found then find the child <div that has that model and click it to input the model into dropdown
            if car_model1 == car_model:
                model = driver.find_element_by_xpath('//*[@id="ext-gen699"]/div[%s]' % i)
                model.click()
                break

    driver.find_element_by_id(
        "_9999999:EP_PolicyForm_insuredForm_insuredSOABO_fieldValueMap_MT_OFF_PEAK_container").click()
    driver.find_element_by_xpath("//div[@id='ext-gen720']/div[3]").click()

    time.sleep(2)
    driver_info_page = driver.find_element_by_id("_9999999:addMotorDriver_btn")
    driver_info_page.click()
    time.sleep(2)

    date_birth = str(list_ent[3])
    register_date = str(list_ent[7])
    Name_id = str(list_ent[1])
    driver_id = nric_

    driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_driverName").send_keys(Name_id)
    driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_driverCertificateNo").send_keys(
        driver_id)

    if list_ent[0] == "NRIC":
        driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_idType_container").click()
        driver.find_element_by_xpath("//div[@id='ext-gen119']/div[2]").click()
    elif list_ent[0] == "FIN":
        driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_idType_container").click()
        driver.find_element_by_xpath("//div[@id='ext-gen119']/div[3]").click()
    else:
        driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_idType_container").click()
        driver.find_element_by_xpath("//div[@id='ext-gen119']/div[4]").click()

    driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_dateOfBirth").click()
    # driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_dateOfBirth").send_keys('20/12/2000')
    keyboard = pynput.keyboard.Controller()
    for i in range(len(date_birth)):
        keyboard.press(date_birth[i])
        time.sleep(.1)

    time.sleep(1)

    driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_drivingLicenseRegisterDate").click()
    for i in range(len(register_date)):
        keyboard.press(register_date[i])
        time.sleep(.1)

    time.sleep(1)

    driver.find_element_by_id(
        "_10000060:EP_PolicyForm_insuredForm_motorDriverForm_occupationOfMainDriver_container").click()
    driver.find_element_by_xpath("//div[@id='ext-gen145']/div[4]").click()

    driver.find_element_by_id("_10000060:EP_PolicyForm_insuredForm_motorDriverForm_driverRoleId_container").click()
    driver.find_element_by_xpath("//div[@id='ext-gen166']/div[2]").click()

    driver.find_element_by_id(
        "_10000060:EP_PolicyForm_insuredForm_motorDriverForm_reservedObject_gender_container").click()
    driver.find_element_by_xpath("//div[@id='ext-gen191']/div[2]").click()

    driver.find_element_by_id(
        "_10000060:EP_PolicyForm_insuredForm_motorDriverForm_reservedObject_marital_container").click()
    driver.find_element_by_xpath("//div[@id='ext-gen212']/div[2]").click()

    time.sleep(1)

    driver.find_element_by_id("_10000060:addMotorDriverInformation_btn").click()
    time.sleep(1)

    no1 = driver.find_element_by_id(input_dropdown_ids[4])
    no1.click()

    no1_elem = driver.find_element_by_xpath("//div[@id='ext-gen682']/div[3]").click()

    no2 = driver.find_element_by_id(input_dropdown_ids[5])
    no2.click()

    no2_elem = driver.find_element_by_xpath("//div[@id='ext-gen704']/div[3]").click()

    time.sleep(1)

    cc1 = driver.find_element_by_id(input_dropdown_ids[2])
    cc1.click()

    # find the <div that has the dropdown list
    cc_elem = driver.find_elements_by_xpath("//div[@id='ext-gen725']/div[@class='x-combo-list-item']")

    time.sleep(1)

    # iterate through every element in the dropdown <div to find the text in the child <div that matches the car_make
    for i in range(2, len(cc_elem) + 2):
        car_cc = int(driver.find_element_by_xpath('//*[@id="ext-gen725"]/div[%s]' % i).text)
        print(car_cc)
        if car_cc == cc_rounded:
            # once a match is found go to child <div and click on it to input the car_make
            cc = driver.find_element_by_xpath('//*[@id="ext-gen725"]/div[%s]' % i)
            cc.click()
            print("hello")
            break

    time.sleep(2)
    print("cc passed")

    no_seats = driver.find_element_by_id(input_dropdown_ids[3])
    no_seats.send_keys(5)

    time.sleep(1)

    # this code is needed, it doesnt really do anything, but code doesnt submit without this code, i dont know why and at this point in too afraid to ask
    try:
        driver.find_element_by_id("_9999999:addMotorDriver_btn").click()
        driver.find_element_by_id("_10000060:Back_btn").click()
    except:
        pass

    try:
        driver.find_element_by_name("_9999999:calculatePremium_btn").click()
    except:
        print("F")

    time.sleep(5)


main()
