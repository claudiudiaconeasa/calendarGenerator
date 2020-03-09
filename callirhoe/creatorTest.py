import calmagick
import callirhoe
import lib
import os
import sys

def createTop(month, currentPhoto, currentText, currentQR):
    print("\tGathering Event photo and Text")
    os.system("convert " + currentPhoto + " -resize 940x1000" +
             " Resources/resized" + str(month) + ".png")
    #make the photo for the current month fit into a size suitable for
    #the calendar

    os.system("convert Resources/background2.png Resources/resized" +
              str(month) + ".png -gravity west -geometry +20+25 " +
              "-composite Resources/outPhoto" + str(month) + ".jpg")
    #combine the resized image with the background for the top

    os.system("convert Resources/outPhoto" + str(month) +
              ".jpg -gravity west -pointsize 40 -size 900x " +
              "caption:@" + currentText + " Resources/outputtext" + str(month) + ".jpg")
    os.system("convert Resources/outputtext" + str(month) + "-0.jpg Resources/outputtext" +
              str(month) + "-1.jpg -gravity northwest -geometry +980+125" +
              " -composite Resources/outputWithText" + str(month) + ".jpg")
    #use the text to add it to the photo

    print("\tAdding QR code")
    os.system("convert " + currentQR + " -resize 200x200 " + currentQR)
    os.system("convert Resources/outputWithText" + str(month) + ".jpg " +
              currentQR + " -gravity northeast -geometry -5-5 -composite " +
              "Resources/outputWithText" + str(month) + ".jpg")
    #add the qr code to the calendar

def createPDF(month, CalendarName):
    print("\tCombining Dates and Event")
    os.system("convert -append Resources/outputWithText" + str(month) +
              ".jpg HistoryCalendar/HistoryCalendar" + str(month)
              + ".jpg HistoryCalendar/testCalender" + str(month) + ".jpg")
    #combine the photo and text portion to the calendar for month

    print("\tAdding to PDF\n")
    if month == 1:
      os.system("convert HistoryCalendar/testCalender" + str(month) +
                ".jpg " + CalendarName + ".pdf")
    else:
      os.system("convert " + CalendarName + ".pdf HistoryCalendar/testCalender" +
                str(month) + ".jpg " + CalendarName + ".pdf")
      #combine all the months into one printable pdf file

def main_program():
    CalendarName = sys.argv[1]
    background = "Resources/background.jpg"

    for month in range(1, 13):
      print("For Month " + str(month) + ":")
      print("\tCreating Calendar Dates")
      calmagick.main_program(background, month, True)
      #create the calendar of the current month

      currentPhoto = "Events/Event" + str(month) + ".jpg"
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
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
