import csv
import random
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials

#interact with the google docs api using own credentials
print("Authorizing access to spreadsheet")
scope = ["https://spreadsheets.google.com/feeds"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(credentials)

#open the wanted sheet
print("Opening spreadsheet")
sheet = client.open_by_key('1BNti0T_yNtpwsparOIbHb21nthnVfNVPe4ZGUAQTB6o').sheet1

#convert spreadsheet to a csv file
print("Creating CSV file from spreadsheet")
filename = "Events/events.csv"
with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(sheet.get_all_values())
