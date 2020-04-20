# calendarGenerator

Collaboration with George Clark.

Flask application that receives an HTTP request from Java in order to generate the calendar and populate it with events from a TimeMap.
Hosted on Digital Ocean: 
http://165.22.125.196:1337/


Modifications before connection to the History Tools app:

main.py - Endpoint (/generate):
It is going call the main method of creator.py in order to generate the calendar. 
It's listening to incoming polling requests before the delivery of the calendar.

creator.py:
Generates the calendars and each QR code has an assigned event id in order to prompt the user to that particular event from the calendar to a chronology
