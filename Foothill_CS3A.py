"""
The program first asks the user for their name, then printing out a 
welcome statement and a menu of choices for an Air BNB menu list. 
programs creates a table in regards to the user's home currency. 
The program also accepts a header from the user and shows a copyright. 
new code for module 7 has data for NY boroughs,property types, and prices. 
The code for module 8 codes for the load data function. The code for 
module 9 creates a table called basedon the choice the user chooses from the menu.

Code is a summer project from Foothill Course CS3A.
"""

import csv
import sys

from enum import Enum

""" Global variable """
home_currency = ""

# Need to download file and/or change file path in order to run code
filename = "./AB_NYC_2019.csv"

""" Custom exceptions"""


class EmptyDataSetError(Exception):
    def __init__(self, message):
        self.message = message


class NoMatchingItemsError(Exception):
    def __init__(self, message):
        self.message = message


"""
Enum class called and set for the index 0 (Location) and index 1 
(Property-Type) for the load data dictionary.
Set is used to create unique values from the dictionary for when 
the user chooses what location/property type they want.
"""


class DataSet:
    """
    Enum class for getting max/min/avg data
    """

    class Stats(Enum):
        AVG = 1
        MIN = 2
        MAX = 3

    """
    Function to print out the data table of max/min/avg based on
    the user's choice from menu.
    There is also an enum class for getting location type or property
    type based on the index of the tuple inside the array.
    """

    def display_cross_table(self, stats: Stats):
        if not self._data:
            print("No dataset loaded, please load")

        prop_type = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
        loc_type = list(self._labels[DataSet.Categories.LOCATION])

        print(f"{' ':<20}", end="")
        if stats == DataSet.Stats.AVG:
            for header1 in prop_type:
                print(f"{header1:20}", end="")
            print()
            for loc1 in loc_type:
                print(f"{loc1:<20}", end="")
                for prop1 in prop_type:
                    table1 = self._cross_table_statistics(loc1, prop1)
                    print(f"${table1[2]:<20.2f}", end="")
                print()

        if stats == DataSet.Stats.MIN:
            for header2 in prop_type:
                print(f"{header2:<20}", end=" ")
            print()
            for loc2 in loc_type:
                print(f"{loc2:<20}", end="")
                for prop2 in prop_type:
                    table2 = self._cross_table_statistics(loc2, prop2)
                    print(f"${table2[0]:<20.2f}", end="")
                print()

        if stats == DataSet.Stats.MAX:
            for header3 in prop_type:
                print(f"{header3:<20}", end=" ")
            print()
            for loc3 in loc_type:
                print(f"{loc3:<20}", end="")
                for prop3 in prop_type:
                    table3 = self._cross_table_statistics(loc3, prop3)
                    print(f"${table3[1]:<20.2f}", end="")
                print()

    class Categories(Enum):
        LOCATION = 0
        PROPERTY_TYPE = 1

    def _initialize_sets(self):
        if not self._data:
            raise EmptyDataSetError
        for tup_data in self._data:
            self._labels[DataSet.Categories.LOCATION].add(tup_data[0])
            self._labels[DataSet.Categories.PROPERTY_TYPE].add(tup_data[1])

    copyright = "No copyright has been set"

    """
    Takes the Borough and Property type, then returns the min, max, and 
    average property prices based on the user's choices. If the user
    enters a selection not part of the data from the file or there isn't
    data loaded from the file, it raises an exception.
    """

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        if not self._data:
            raise EmptyDataSetError("There are no properties loaded.")

        data = [float(r) for (b, p, r) in self._data if
                b == descriptor_one and p == descriptor_two]
        if len(data) == 0:
            return "N/A", "N/A", "N/A"
        else:
            data1 = min(data), max(data), round((sum(data) / len(data)), 2)
            return tuple(data1)

    """ Data loaded in from a csv file """
    def load_file(self):
        self._data = []
        line_count = 0
        with open(filename, 'r') as csvfile:
            csvdata = csv.reader(csvfile, delimiter=',')
            headers = next(csvdata)
            for csvline in csvdata:
                self._data.append((csvline[1], csvline[2], (csvline[3])))
                line_count = line_count + 1
        print(f"Lines of AirBNB Data Loaded: {len(self._data)}")
        self._initialize_sets()

    """ Default data consisting of NYC boroughs, property 
    types, and prices.
    """

    def load_default_data(self):
        self._data = [("Staten Island", "Private Room", 70),
                      ("Brooklyn", "Private Room", 50),
                      ("Bronx", "Private Room", 40),
                      ("Brooklyn", "Entire Home/Apt", 150),
                      ("Manhattan", "Private Room", 125),
                      ("Manhattan", "Entire Home/Apt", 196),
                      ("Brooklyn", "Private Room", 110),
                      ("Manhattan", "Entire Home/Apt", 170),
                      ("Manhattan", "Entire Home/Apt", 165),
                      ("Manhattan", "Entire Home/Apt", 121),
                      ("Manhattan", "Entire Home/Apt", 100),
                      ("Brooklyn", "Private Room", 65),
                      ("Queens", "Entire Home/Apt", 350),
                      ("Manhattan", "Private Room", 98),
                      ("Brooklyn", "Entire Home/Apt", 200),
                      ("Bronx", "Entire Home/Apt", 150),
                      ("Brooklyn", "Private Room", 99),
                      ("Brooklyn", "Private Room", 120)]
        self._initialize_sets()

    def __init__(self, header=""):
        self._data = None
        self._labels = {DataSet.Categories.LOCATION: set(),
                        DataSet.Categories.PROPERTY_TYPE: set()}
        try:
            self.header = header
        except ValueError:
            self._header = ""

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, title: str):
        if len(title) > 30:
            raise ValueError()
        self._header = title


def main():
    """ Politely ask the user for their name, then welcome them.
    Then ask for the user's home currency.
    """
    global home_currency
    user_name = input("Please enter your name: ")
    print("Hi " + user_name + "," + " welcome to Foothill's "
                                    "database project.")
    while True:
        home_currency = input("What is your home currency? ")
        if home_currency in conversions:
            break

    air_bnb = DataSet()
    air_bnb.copyright = "Copyright 2021 Atul Venkatesan"
    while True:
        try:
            user_header = input("Enter a header for the menu: ")
            air_bnb.header = user_header
            break
        except ValueError:
            print("Please enter a header that isn't greater than "
                  "30 characters! ")
            continue
    menu(air_bnb)


def print_menu():
    """ Print a menu of choices for the user to select from. """
    print("Main Menu")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Load Data")
    print("5 - Quit")


def menu(dataset: DataSet):
    """ Loop that constantly prints out the menu,
        unless the user quits. """
    global home_currency
    currency_options(home_currency)

    menu_loop = True
    print(dataset.copyright)
    while menu_loop:
        print(dataset.header)
        print_menu()
        user_choice = input("Which would you like to browse? ")
        try:
            user_num = int(user_choice)
        except ValueError:
            """ If the user enters something that's not a number, the
            loop restarts from the start after sendin
            g a warning/reminder."""
            print("Next time, please enter a number!")
            continue

        """ Since there isn't any data, there needs to be a print 
        statement stating that there is no data or that the user is 
        quitting the program."""
        if 1 <= user_num <= 5:
            """ When the user enters a valid integer. """
            if user_num == 1:
                dataset.display_cross_table(DataSet.Stats.AVG)
            if user_num == 2:
                dataset.display_cross_table(DataSet.Stats.MIN)
            if user_num == 3:
                dataset.display_cross_table(DataSet.Stats.MAX)
            if user_num == 4:
                # dataset.load_default_data()
                dataset.load_file()
                print("Data Loaded")
            if user_num == 5:
                """ The user chooses to quit the function. Exit. """
                print("Quitting")
                break
        else:
            """ User prints a number that isn't valid. """
            print("That number is not part of the range of given "
                  "choices. "
                  "Please try again.")
            continue
    """ Exit statement."""
    print("Thank you for visiting us, hope to see you soon! Goodbye!")


""" Dictionary containing table of currency conversions """
conversions = {
    "USD": 1,
    "EUR": 0.84,
    "CAD": 1.23,
    "GBP": 0.72,
    "CHF": 0.92,
    "NZD": 1.41,
    "AUD": 1.32,
    "JPY": 110.8
}

""" This function converts one currency to another based on the 
values from the table.
"""


def currency_converter(source_curr, target_curr, quantity):
    sc = quantity / conversions[source_curr]
    tc = conversions[target_curr]
    if quantity < 0:
        raise ValueError
    amount = round(sc * tc, 2)
    return amount


"""
Currency converter table using f-strings
"""


def currency_options(base_curr):
    currencies = list(conversions.keys())
    currencies.remove(base_curr)
    print(f"Options for converting from {base_curr}:")
    print(f"{home_currency:>10}", end="")
    for currency in currencies:
        print(f"{currency:>10}", end="")
    print()
    for i in list(range(10, 100, 10)):
        print(f"{i:10.2f}", end="")
        for currency in currencies:
            amount = currency_converter(base_curr, currency, i)
            print(f"{amount:10.2f}", end="")
        print()


if __name__ == "__main__":
    main()

"""
Sample Run:
Please enter your name: Atul
Hi Atul, welcome to Foothill's database project.
What is your home currency? GBP
Enter a header for the menu: --- HEADER ---
Options for converting from GBP:
       GBP       USD       EUR       CAD       CHF       NZD       AUD       JPY
     10.00     13.89     11.67     17.08     12.78     19.58     18.33   1538.89
     20.00     27.78     23.33     34.17     25.56     39.17     36.67   3077.78
     30.00     41.67     35.00     51.25     38.33     58.75     55.00   4616.67
     40.00     55.56     46.67     68.33     51.11     78.33     73.33   6155.56
     50.00     69.44     58.33     85.42     63.89     97.92     91.67   7694.44
     60.00     83.33     70.00    102.50     76.67    117.50    110.00   9233.33
     70.00     97.22     81.67    119.58     89.44    137.08    128.33  10772.22
     80.00    111.11     93.33    136.67    102.22    156.67    146.67  12311.11
     90.00    125.00    105.00    153.75    115.00    176.25    165.00  13850.00
Copyright 2021 Atul Venkatesan
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 1
No dataset loaded, please load
                    
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 4
Lines of AirBNB Data Loaded: 48895
Data Loaded
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 1
                    Shared room         Entire home/apt     Private room        
Staten Island       $57.44               $173.85              $62.29               
Manhattan           $88.98               $249.24              $116.78              
Brooklyn            $50.53               $178.33              $76.50               
Bronx               $59.80               $127.51              $66.79               
Queens              $69.02               $147.05              $71.76               
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 2
                    Shared room          Entire home/apt      Private room         
Staten Island       $13.00               $48.00               $20.00               
Manhattan           $10.00               $0.00                $10.00               
Brooklyn            $0.00                $0.00                $0.00                
Bronx               $20.00               $28.00               $0.00                
Queens              $11.00               $10.00               $10.00               
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 3
                    Shared room          Entire home/apt      Private room         
Staten Island       $150.00              $5000.00             $300.00              
Manhattan           $1000.00             $10000.00            $9999.00             
Brooklyn            $725.00              $10000.00            $7500.00             
Bronx               $800.00              $1000.00             $2500.00             
Queens              $1800.00             $2600.00             $10000.00            
--- HEADER ---
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
5 - Quit
Which would you like to browse? 5
Quitting
Thank you for visiting us, hope to see you soon! Goodbye!

"""
