import calmagick
import callirhoe
import lib
import os
import sys
import requests
import qrcode
import csv
import pandas
import random
import time
import urllib

def readCSV(month, filename, mode):
    """
        Reads the csv file given as an input using pandas and return
        all the rows with events for the current month
    """
    #get all the rows for the current month
    reader = csv.DictReader(open(filename))
    rows = [row for row in reader if "/%02d/" % month in row["Date"] and row["Media"] != ""]

    if mode == "manual":
        #display options for manual mode
        count = 0
        for row in rows:
            print("\tOption " + str(count + 1) + ":")
            print("\t\t" + row["Title"])
            count = count + 1
        #get the choice from the user
        choice = raw_input("\n\t Please choose event for month " + str(month) + ": ")
        choiceNo = int(choice)
        while choiceNo > count or choiceNo < 1:
            choice = raw_input("\tInvalid choice, please choose a number between 1 and " +
                  str(count) + " for this month: ")
            choiceNo = int(choice)
        #return the chosen event
        return rows[choiceNo - 1]
    else:
        #return a random row from the month
        return random.choice(rows)

def downloadImage(month, urlImage):
    """
        Downloads and saves the image for the given month
        from the given url
    """

    #gets the image content from the url
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    image = requests.get(urlImage, header)
    #create a file and save the contents of the image to it
    file = open("Events/Event" + str(month) + ".jpg", "wb")
    file.write(image.content)
    file.close()

def createQR(month, urlQr):
    """
        This generates a qr code based on the given link for the current
        month and saves it as qr(month).jpg so it can be stitched
        to the top half of the calendar
    """

    #saves the qr code from the given link for the given month
    qrImage = qrcode.make(urlQr)
    qrImage.save("Events/qr" + str(month) + ".png")

def createTop(month, currentPhoto, currentText, currentQR):
    """
        Create the top portion of the calendar, this stitches the current
        event image onto a self created background for the top half, then
        adds the text for that event next to the image. It then also adds
        the qr code for the
    """
    print("\tCreating Top Half")
    #make the photo for the current month fit into a size suitable for
    #the calendar
    os.system("convert " + currentPhoto + " -resize 940x1000" +
             " Resources/resized" + str(month) + ".png")

    #combine the resized image with the background for the top
    os.system("convert Resources/background2.png Resources/resized" +
              str(month) + ".png -gravity west -geometry +20+25 " +
              "-composite Resources/outPhoto" + str(month) + ".jpg")

    #use the text to add it to the photo
    os.system("convert Resources/outPhoto" + str(month) +
              ".jpg -gravity west -pointsize 40 -size 900x " +
              "caption:@" + currentText + " Resources/outputtext" + str(month) + ".jpg")
    os.system("convert Resources/outputtext" + str(month) + "-0.jpg Resources/outputtext" +
              str(month) + "-1.jpg -gravity northwest -geometry +980+150" +
              " -composite Resources/outputWithText" + str(month) + ".jpg")

    #add the qr code to the calendar
    print("\tAdding QR code")
    os.system("convert " + currentQR + " -resize 150x150 " + currentQR)
    os.system("convert Resources/outputWithText" + str(month) + ".jpg " +
              currentQR + " -gravity northeast -geometry -5-5 -composite " +
              "Resources/outputWithText" + str(month) + ".jpg")

def createPDF(month, CalendarName):
    """
        Append the top portion of the calendar to the calendar dates of
        the bottom part. Then create a new pdf of the calendar (if the
        current month is January), and add all the calendar months to the
        pdf
    """

    #combine the photo and text portion to the calendar for month
    print("\tCombining Dates and Event")
    os.system("convert -append Resources/outputWithText" + str(month) +
              ".jpg HistoryCalendar/HistoryCalendar" + str(month)
              + ".jpg HistoryCalendar/testCalender" + str(month) + ".jpg")

    print("\tAdding to PDF\n")
    #combine all the months into one printable pdf file
    if month == 1:
        os.system("convert HistoryCalendar/testCalender" + str(month) +
                ".jpg " + CalendarName + ".pdf")
    else:
        os.system("convert " + CalendarName + ".pdf HistoryCalendar/testCalender" +
                str(month) + ".jpg " + CalendarName + ".pdf")

def main_program(csvFile, name):
    CalendarName = name
    background = "Resources/background.jpg"

    modeChoice = 'n'
    while modeChoice != "y" and modeChoice != "n":
        modeChoice = raw_input("Please choose 'y' or 'n': ")
    if modeChoice == "y":
        mode = "manual"
    else:
        mode = "random"
    #choose the mode

    for month in range(1, 13):
      print("For Month " + str(month) + ":")

      print("\tGathering Event photo and Text")
      monthInfo = readCSV(month, csvFile, mode)
      #retreive the info of a random event for the current month

      print("\tCreating Calendar Dates")
      calmagick.main_program(background, month, True)
      #create the calendar of the current month

      downloadImage(month, monthInfo["Media"])
      createQR(month, monthInfo["Source URL"])
      #get the photo for that event and create qr code

      currentPhoto = "Events/Event" + str(month) + ".jpg"
      writeText = open("Events/Event" + str(month) + ".txt", "w")
      currentTextInfo = (monthInfo["Title"] + "\n\n" + monthInfo["Date"] +
                    "\n\n" + monthInfo["Description"])
      writeText.write(currentTextInfo)
      writeText.close()
      currentText = "Events/Event" + str(month) + ".txt"
      currentQR = "Events/qr" + str(month) + ".png"
      #get the saved event details

      createTop(month, currentPhoto, currentText, currentQR)
      #create the top part of the calendar with text, image
      #and qr code

      createPDF(month, CalendarName)
      #combine the calendar and top half to create the pdf


if __name__ == "__main__":
    try:
        csvFile = sys.argv[1]
        main_program(csvFile, 'calendar')
    except lib.Abort as e:
        sys.exit(e.args[0])
