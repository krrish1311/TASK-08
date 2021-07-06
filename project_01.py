C:\Users\krris\anaconda3\anaconda_2\python.exe
print("content-type: text/html")
print("Acess-Control-Allow-Origin:*")
print()

import cgi
y = cgi.FieldStorage("x")
o = y.getvalue("x")

import numpy as np 
import pandas as pd
import pytesseract
pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\Tesseract.exe'
import cv2
web_ip = 'http://" + o +":8080/video"
model_license = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
#model_license = cv2.CascadeClassifier('indian_license_plate.xml')
def license_plate(photo):
    plate = model_license.detectMultiScale(photo)
    if len(plate)==0 :
        crop = 0
    else :
        x1=plate[0][0]
        y1=plate[0][1]
        x2=x1 + plate[0][2]
        y2=y1 + plate[0][3]
        crop = photo[y1:y2 , x1:x2]
        #crop = cv2.medianBlur(crop,5)
        #crop = cv2.threshold(crop,0,255,cv2.THRESH_BINARY +cv2.THRESH_OTSU)[1]
    return crop    

#cap = cv2.VideoCapture(0)
cap_mob = cv2.VideoCapture(web_ip)
while True :
    
    ret,photo = cap_mob.read()
    img = cv2.cvtColor(photo , cv2.COLOR_BGR2GRAY)
    plate_img = license_plate(photo)
    if plate_img is not 0 :
        name=pytesseract.image_to_string(plate_img)
        if len(name) >10  :
            cap_mob.release()
            break
        
final_plate = name[3:13]
import requests
import xmltodict
import json
def get_vehicle_info(plate_number):
    r = requests.get("http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={0}&username=USERNAME".format(str(plate_number)))
    data = xmltodict.parse(r.content)
    jdata = json.dumps(data)
    df = json.loads(jdata)
    df1 = json.loads(df['Vehicle']['vehicleJson'])
    return df1
information = get_vehicle_info(final_plate)
print(information)    
