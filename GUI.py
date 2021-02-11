import tkinter as tk
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time
import tkinter as tk
from datetime import date
from PIL import Image
from io import BytesIO
import os

nric_="s9235921b"
carplate_="sdr9886j"

today = str(date.today())
today = (today[8:10] + today[5:7] + today[0:4])


web = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
web.get('https://vrl.lta.gov.sg/lta/vrl/action/enquireTransferFeeProxy?FUNCTION_ID=F0501015ET')

def printme():
    global list_ent
    list_ent = [ent_IDtype.get(), ent_NAME.get(), ent_ID.get(), ent_DOB.get(), ent_Role.get(), ent_carplate.get(),ent_gender.get(), ent_License.get(), ent_Occupation.get(), ent_Role.get(), ent_captcha.get()]
    print(list_ent)

    ID = web.find_element_by_name("ownerId")
    ID.send_keys(#ent_ID.get()
        nric_ [-4:])

    carplateLTA = web.find_element_by_name("vehicleNo")
    carplateLTA.send_keys(carplate_#ent_carplate.get())
                          )
    date_in = web.find_element_by_name("transferDate")
    date_in.send_keys(today)

    captcha = web.find_element_by_name("captchaResponse")
    captcha.send_keys(ent_captcha.get())

    agree_button = web.find_element_by_xpath('//*[@id="agreeTCbox"]')
    agree_button.click()

    submit_button_lta = web.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/form/div[1]/div[8]/button')
    submit_button_lta.click()

    time.sleep(2)

    global make_model, vehicle_cc
    make_model = web.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/form/div[1]/div[3]/div[1]/div[2]/div[2]')
    make_model = make_model.text
    vehicle_cc = web.find_element_by_xpath('//*[@id="main-content"]/div[2]/div[2]/form/div[1]/div[4]/div[4]/div[2]/p[2]')
    vehicle_cc = vehicle_cc.text
    return make_model, vehicle_cc


def get_captcha():


    # getting the captcha
    elem = web.find_element_by_tag_name("iframe")

    location = elem.location
    size = elem.size
    png = web.get_screenshot_as_png()

    im = Image.open(BytesIO(png))

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))
    im.save('screenshot.png')


window = tk.Tk()
window.title("Address Entry Form")

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_form.pack()

if os.path.exists("screenshot.png"):
    os.remove("screenshot.png")
    print("file deleted")
    get_captcha()
    print("file created")
else:
    get_captcha()
    print("file created")

img_captcha = tk.PhotoImage(file="screenshot.png")
img_captcha_lbl = tk.Label(master=frm_form, image=img_captcha)
img_captcha_lbl.grid(row=10, column=0, columnspan=2)

lbl_carplate = tk.Label(master=frm_form, text="Carplate:")
ent_carplate = tk.Entry(master=frm_form, width=50)

lbl_carplate.grid(row=4, column=0, sticky="e")
ent_carplate.grid(row=4, column=1)
lbl_ID = tk.Label(master=frm_form, text="ID#:")
ent_ID = tk.Entry(master=frm_form, width=50)

lbl_ID.grid(row=1, column=0, sticky="e")
ent_ID.grid(row=1, column=1)
lbl_NAME = tk.Label(master=frm_form, text="NAME:")
ent_NAME = tk.Entry(master=frm_form, width=50)

lbl_NAME.grid(row=0, column=0, sticky="e")
ent_NAME.grid(row=0, column=1)
lbl_IDtype = tk.Label(master=frm_form, text="NRIC or FIN:")
ent_IDtype = tk.Entry(master=frm_form, width=50)
ent_IDtype.insert(0, "NRIC")
lbl_IDtype.grid(row=5, column=0, sticky=tk.E)
ent_IDtype.grid(row=5, column=1)

lbl_DOB = tk.Label(master=frm_form, text="DOB DDMMYYYY:")
ent_DOB = tk.Entry(master=frm_form, width=50)
lbl_DOB.grid(row=2, column=0, sticky=tk.E)
ent_DOB.grid(row=2, column=1)

lbl_Occupation = tk.Label(master=frm_form, text="Occupation:")
ent_Occupation = tk.Entry(master=frm_form, width=50)
ent_Occupation.insert(0, "Indoor-Others")
lbl_Occupation.grid(row=6, column=0, sticky=tk.E)
ent_Occupation.grid(row=6, column=1)

lbl_License = tk.Label(master=frm_form, text="License date DDMMYYY:")
ent_License = tk.Entry(master=frm_form, width=50)
lbl_License.grid(row=3, column=0, sticky=tk.E)
ent_License.grid(row=3, column=1)

lbl_Role = tk.Label(master=frm_form, text="Role:")
ent_Role = tk.Entry(master=frm_form, width=50)
ent_Role.insert(0, "Main Driver")
lbl_Role.grid(row=7, column=0, sticky=tk.E)
ent_Role.grid(row=7, column=1)

lbl_gender = tk.Label(master=frm_form, text="Male/Female:")
ent_gender = tk.Entry(master=frm_form, width=50)
ent_gender.insert(0, "Male")
lbl_gender.grid(row=8, column=0, sticky=tk.E)
ent_gender.grid(row=8, column=1)

lbl_marital = tk.Label(master=frm_form, text="Married/Single:")
ent_marital = tk.Entry(master=frm_form, width=50)
ent_marital.insert(0, "Married")
lbl_marital.grid(row=9, column=0, sticky=tk.E)
ent_marital.grid(row=9, column=1)

lbl_captcha = tk.Label(master=frm_form, text="captcha:")
ent_captcha = tk.Entry(master=frm_form, width=50)

lbl_captcha.grid(row=10, column=0, sticky=tk.E)
ent_captcha.grid(row=10, column=1)

if os.path.exists("screenshot.png"):
    os.remove("screenshot.png")
    print("file deleted")
    get_captcha()
    print("file created")
else:
    get_captcha()
    print("file created")

img_captcha = tk.PhotoImage(file="screenshot.png")
img_captcha_lbl = tk.Label(master=frm_form, image=img_captcha)
img_captcha_lbl.grid(row=11, column=0, columnspan=2)

frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

btn_submit = tk.Button(master=frm_buttons, text="Submit", command = printme)
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

btn_clear = tk.Button(master=frm_buttons, text="Clear")
btn_clear.pack(side=tk.RIGHT, ipadx=10)

window.mainloop()