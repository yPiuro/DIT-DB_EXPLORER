import sqlite3
import os

def clear_console():
    os.system('cls') if os.name == 'nt' else os.system('clear')

def is_interable(iterable_obj):
    try:
        iter(iterable_obj)
    except:
        return False
    else:
        return True
    

class Database():
    def __init__(self,db:str):
        self.db = db
    def query(self,query:str, silent:bool = False,data:bool = False):
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            if cursor.description and silent != True:
                print('   | '.join(list(map(lambda x: x[0], cursor.description))))
                print('')
            connection.commit()
            if cursor.description and data:
                return cursor.fetchall(),list(map(lambda x: x[0], cursor.description))
            return cursor.fetchall() if cursor.description else None

db = Database('./factbook.db')

def get_data():
    data_labels = db.query("SELECT * FROM facts",silent = True,data=True)[1]
    for country in db.query('SELECT * FROM facts',silent=True):
        pop_per_area = country[data_labels.index("population")] / country[data_labels.index("area")] if country[data_labels.index("area")] and country[data_labels.index("population")] else None
        print(f'{country[data_labels.index("name")].capitalize()} has a population of {country[data_labels.index("population")] if country[data_labels.index("population")] else "N/A"} and an area of {country[data_labels.index("area")] if country[data_labels.index("area")] else "N/A"}\nOn average, there are {round(pop_per_area) if pop_per_area else "N/A"} people per square kilometer\n')

def get_specific_hero():
    name = input('Enter hero name: ')
    clear_console()
    string = ''
    try:
        hero = db.query(f'SELECT * FROM superheroes WHERE name == "{name.capitalize()}" LIMIT 1',silent=True)[0]
    except:
        input('Hero not found!\n')
        clear_console()
    else:
        for i in hero:
            string += f'{db.query("SELECT * FROM superheroes",silent = True,data=True)[1][hero.index(i)].capitalize()}: {i}\n'
        print(string)

def filter_specif_data():
    type = input(f'Enter power type: ')
    if type.lower() == 'telepathy' or type.lower() == 'telekinesis':
        type = 'Telepathy/Telekinesis'
    clear_console()
    string = ''
    try:
        heroes = db.query(f'SELECT * FROM superheroes WHERE type == "{type.capitalize()}"',silent=True)
    except:
        input('Not found!\n')
        clear_console()
    else:   
        for hero in heroes:
            string = ''
            for i in hero:
                string += f'{db.query("SELECT * FROM superheroes",silent = True,data=True)[1][hero.index(i)].capitalize()}: {i}\n'
            print(string)

menu_options = {1:get_data,2:get_specific_hero} #,3:filter_specif_data}

selected_option = None

while selected_option != 3:
    clear_console()
    print('Welcome to the interactive Country Facts console!\n\n')
    print('Options:\n1: Show all countries\n2: Get specific Country data\n3: Quit')
    try:
        selected_option = int(input('> '))
        if selected_option > len(menu_options) + 1 or selected_option < 1:
            raise Exception('Invalid Option')
    except:
        print('Please input a valid option!')
    clear_console()
    if selected_option in menu_options:
        menu_options[selected_option]()
        input('\n\nENTER TO CONTINUE...')