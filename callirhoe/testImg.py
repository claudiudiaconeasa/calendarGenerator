import calmagick
import callirhoe
import lib
import os
import time

def main_program():
    background = "background.jpg"

    for month in range(1, 13):
      print("For Month " + str(month) + ":")
      print("\tCreating Calendar Dates")
      calmagick.main_program(background, month, True)
      #create the calendar of the current month

      print("\tGathering Event photo and Text")
      os.system("convert 11.png -resize 940x1000 resized.png")
      #make the photo for the current month fit into a size suitable for
      #the calendar

      os.system("convert background2.png resized.png -gravity west -geometry +20+25 -composite out.jpg")
      #combine the resized image with the background for the top

      os.system("convert out.jpg -gravity west -pointsize 32 -size 900x caption:@test.txt outputtext.jpg")
      os.system("convert outputtext-0.jpg outputtext-1.jpg -gravity northwest -geometry +980+75 -composite outputWithText.jpg")
      #use the text to add it to the photo

      print("\tCombining Dates and Event")
      os.system("convert -append outputWithText.jpg HistoryCalendar/HistoryCalendar" + str(month)
                + ".jpg HistoryCalendar/testCalender" + str(month) + ".jpg")
      #combine the photo and text portion to the calendar for month

      print("\tAdding to PDF\n")
      if month == 1:
        os.system("convert HistoryCalendar/testCalender" + str(month) + ".jpg HistoryCalendar.pdf")
      else:
        os.system("convert  HistoryCalendar.pdf HistoryCalendar/testCalender" + str(month) + ".jpg HistoryCalendar.pdf")
        #combine all the months into one printable pdf file

if __name__ == "__main__":
    try:
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
