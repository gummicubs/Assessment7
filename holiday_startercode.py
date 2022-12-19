import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass

def convert_date(date):
    date = str(date)
    dayy = int(date[:4])
    daym = int(date[5:7])
    dayd = int(date[8:])
    return datetime.date(dayy, daym, dayd)

def menu():
    menu = """
    Holiday Menu
    ================
    1. Add a Holiday
    2. Remove a Holiday
    3. Save Holiday List
    4. View Holidays
    5. Exit
    """
    print(menu)
    option = input('What would you like to do? Please enter the corresponding number.')
    while option not in ['1', '2', '3', '4', '5']:
        option = input('This is not a valid option. Please select a valid option.')
    return option

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    
    def __init__(self,name, date):
        if (not isinstance(name, str)) or (not isinstance(date, datetime.date)):
            raise('Incorrect input type')
        else:
            self.name = name
            self.date = date
    
    def __str__(self):
        return f'{self.name}: {self.date}'
        # String output
        # Holiday output when printed.
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList():
    
    
    def __init__(self):
        self.innerHolidays = []
   
        
    def addHoliday(self,holidayObj):
        if (not isinstance(holidayObj, Holiday)):
            raise('This is not a holiday object')        
        # Make sure holidayObj is an Holiday Object by checking the type
        else:
            if holidayObj in self.innerHolidays:
                return f'This holiday is already in the list.'
            else:
                self.innerHolidays.append(holidayObj)
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday
                return f'You have added {holidayObj} as a holiday!'



    def read_json(self, filelocation):
        with open(filelocation, 'r') as f:
            f=json.load(f)
            for i in range(len(f["holidays"])):
                hday = f["holidays"][i]['name']
                day = convert_date(f["holidays"][i]['date'])
                self.addHoliday(Holiday(hday, day))
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.


    def findHoliday(self, HolidayName, Date):
        date = convert_date(Date)
        for i in range(len(self.innerHolidays)):
            if (self.innerHolidays[i].name.lower() == HolidayName.lower() and self.innerHolidays[i].date == date):
                hday = self.innerHolidays[i]
        return hday
        # Find Holiday in innerHolidays
        # Return Holiday


    def removeHoliday(self, HolidayName, Date):
        hday = self.findHoliday(HolidayName, Date)
        # Find Holiday in innerHolidays by searching the name and date combination.
        self.innerHolidays.remove(hday)
        print(f'{hday} has been removed from the holiday list.')
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday


    def save_to_json(self, filelocation):
        with open(filelocation, 'w') as f:
            for i in range(len(self.innerHolidays)):
                self.innerHolidays[i].date = str(self.innerHolidays[i].date)
                f.write(json.dumps(self.innerHolidays[i].__dict__, indent = 4))
        return 'Your changes have been saved.'
        # Write out json file to selected file.
        
        
    def scrapeHolidays(self):
        for Y in range(2020,2025):
            response = requests.get("https://www.timeanddate.com/holidays/us/"+str(Y))
            soup = BeautifulSoup(response.text, 'html.parser')
            a = soup.find_all('tr')
            for i in range(3,len(a)):
                try:
                    c = a[i]
                    b = str(c.find_all('a'))
                    rename = b.split('>')[1]
                    name = rename.split('<')[0]
                    day = (datetime.datetime.fromtimestamp(int(str(c).split('"')[1])/1000))+datetime.timedelta(days = 1)
                    new = Holiday(name, day.date())
                    self.addHoliday(new)
    #                 print(i)
    #                 print(name, day.date())
                except:
                    continue  


    def numHolidays(self):
        return len(self.innerHolidays)
        # Return the total number of holidays in innerHolidays
# What is this for?
    
    
    def filter_holidays_by_week(self, year, week_number):
        self.holidays = []
        # Use a Lambda function to filter by week number and save this as holidays, 
        # use the filter on innerHolidays
        # holidays = lambda year,week_number: self.innerHolidays.date.isocalendar
        for i in range(len(self.innerHolidays)):
            (yr, wknm, day) = self.innerHolidays[i].date.isocalendar()
            if (wknm == int(week_number) and yr == int(year)):
                self.holidays.append(self.innerHolidays[i])
        return self.holidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays        


    def displayHolidaysInWeek(self, year, week_number):
        holidays = self.filter_holidays_by_week(year, week_number)
        for i in range(len(holidays)):
            print(holidays[i].__str__())
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.   
        
        
#     def getWeather(weekNum):
#         # Convert weekNum to range between two days
#         # Use Try / Except to catch problems
#         # Query API for weather in that week range
#         # Format weather information and return weather string.


# Need to double check since no holidays is in current week
    def viewCurrentWeek(self):
        current = datetime.date.today()
        (yr, wknm, day) = current.isocalendar()
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        self.displayHolidaysInWeek(yr,wknm)
        print('Currently, we are unable to tell you the weather for the week. Please come back to tyy again.')
        return wknm
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results      



def main():
    # Large Pseudo Code steps
    # -------------------------------------
#     # 1. Initialize HolidayList Object
    h_list = HolidayList()
#     # 2. Load JSON file via HolidayList read_json function
    h_list.read_json('holiday.json')
#     # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    h_list.scrapeHolidays()
#     # 3. Create while loop for user to keep adding or working with the Calender
    app_on = True
    while app_on:
#     # 4. Display User Menu (Print the menu)
        option = menu()
# Created menu function
#     # 5. Take user input for their action based on Menu and check the user input for errors
# Done within menu function
#     # 6. Run appropriate method from the HolidayList object depending on what the user input is
        if option == '1':
            holiday_name = input('What is the name of the holiday you would like to add?')
            holidate = input('What is the date of the holiday you would like to add? Please enter the date in YYYY,MM,DDD format.')
            holiday = Holiday(holiday_name, convert_date(holidate))
            print(h_list.addHoliday(holiday))
            continue
# Check to ensure date is a real date        
        elif option == '2':
            holiday_name = input('What is the name of the holiday you would like to remove?')
            holidate = input('What is the date of the holiday you would like to remove? Please enter the date in YYYY,MM,DDD format.')
            h_list.removeHoliday(holiday_name, holidate)
            continue
# Check to ensure holiday is in holiday        
        elif option == '3':
            print(h_list.save_to_json('holiday_list'))
            continue
# Check if user wants to save        
        elif option == '4':
            yr = input('Which year would you like to view holidays for?')
            wk = input('Which week number would you like to view holidays for? (#1-52) If you would like to view the current week, you may leave this blank')
            if wk == '':
                wk = h_list.viewCurrentWeek()
            h_list.displayHolidaysInWeek(yr,wk)
            continue
# h_list.displayHolidaysInWeek(2021,2)        
# Weather?
        elif option == '5':
            leave = input('Are you sure you want to exit? (y/n)')
            if leave.lower() == 'y':
                print('Goodbye!')
                app_on = False
# Need to break while loop
# Need to ask if it is okay if changes can be lost
            else:
                print("Let's bring you back to the menu.")
# Need to continue while loop
        
#     # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to con

if __name__ == "__main__":
    main();


# # Additional Hints:
# # ---------------------------------------------
# # You may need additional helper functions both in and out of the classes, add functions as you need to.
# #
# # No one function should be more then 50 lines of code, if you need more then 50 lines of code
# # excluding comments, break the function into multiple functions.
# #
# # You can store your raw menu text, and other blocks of texts as raw text files 
# # and use placeholder values with the format option.
# # Example:
# # In the file test.txt is "My name is {fname}, I'm {age}"
# # Then you later can read the file into a string "filetxt"
# # and substitute the placeholders 
# # for example: filetxt.format(fname = "John", age = 36)
# # This will make your code far more readable, by seperating text from code.

