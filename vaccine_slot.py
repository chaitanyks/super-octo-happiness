import requests
import time
from datetime import datetime, timedelta

# -------------------------------------
ageRange = 20
area_pincodes = ["477660"]
total_days_range = 2
# -------------------------------------
flag = True  # print on output
refresh_time = 3 # waiting time
# -------------------------------------

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(total_days_range)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]
api = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

print("Starting search for Covid vaccine slots.")

while True:
    total_vaccine_center = 0
    vaccine_count = 0

    for pincode in area_pincodes:
        for given_date in actual_dates:
            URL = api.format(pincode, given_date)
            result = requests.get(URL, headers=header)
            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if flag:
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if session["min_age_limit"] <= ageRange and session["available_capacity"] > 0:
                                    print('Pincode: ' + pincode + "\n" + "\t" + " Available on: {}".format(given_date))
                                    print("\t", center["name"] + "\t", center["block_name"])
                                    print("\t Price: ", center["fee_type"] + "\n" + "\t Availablity : ",
                                          session["available_capacity"])
                                    vaccine_count = vaccine_count + session["available_capacity"]
                                    if session["vaccine"] != '':
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")
                                    total_vaccine_center = total_vaccine_center + 1
            else:
                print("No Response!")

    if total_vaccine_center:
        print("Number of Vaccination slots are available : {}".format(total_vaccine_center))
        print("Number of Vaccine are available : {}".format(vaccine_count))
    else:
        print("Loading", end=" ")

    dt = datetime.now() + timedelta(minutes=refresh_time)

    while datetime.now() < dt:
        print(".", end=" ")
        time.sleep(12)
    print("")
