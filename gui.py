import sqlite3
from nicegui import ui

class Database():
    def __init__(self,db:str):
        self.db = db
    def query(self,query:str,data:bool = False):
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            if cursor.description and data:
                return cursor.fetchall(),list(map(lambda x: x[0], cursor.description))
            return cursor.fetchall() if cursor.description else None

config = type("object", (object,), {})()

config.db = False

columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'required': True, 'align': 'left','sortable': True},
    {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
]

rows = []

tables = {}

#    {'name': 'Alice', 'age': 18},
#    {'name': 'Bob', 'age': 21}

def set_DB(db_path:str):
    config.db = Database(db_path)
    query = config.db.query("SELECT name FROM sqlite_master WHERE type='table' and name != 'sqlite_sequence'")
    tables.clear()
    for x in query:
        tables[query.index(x)+1] = x[0]
    dropdown.update()
    
def set_table(table:str):
    print(table)
    config.table = table
    query = config.db.query(f'SELECT * from {table}',data=True)
    columns.clear()
    for x in query[1]:
        if x == query[1][0]:
            columns.append({'name': f'{x}', 'label': f'{x.upper()}', 'field': f'{x.lower()}', 'required': True, 'align': 'left','sortable': True})
        else:
            columns.append({'name': f'{x}', 'label': f'{x.capitalize()}', 'field': f'{x.lower()}', 'sortable': True})
    rows.clear()
    for x in query[0]:
        obj = {}
        for i in x:
            obj[query[1][x.index(i)]] = i
        rows.append(obj)
    print(rows)
    card.refresh()
    ui.notify(f'Loaded table: {table}')


with ui.row().classes('justify-between w-full'):
    with ui.row():
        db_input = ui.input(label='Path to DB',on_change= lambda value:set_DB(db_input.value) if '.db' in db_input.value else None,placeholder='./data.db').classes('w-fit')
    with ui.row():
       dropdown = ui.select(tables, on_change=lambda e: set_table(tables[e.value])).bind_visibility_from(config,'db').style('min-width: 6rem;')

@ui.refreshable
def card():
    with ui.card().classes('place-self-center my-10'):
        ui.label('Database Content')
        ui.table(columns=columns, rows=rows, row_key='name').classes('overflow-x-auto').style('max-height: 28rem')

def button():
    card.refresh()


card()  
with ui.row().classes('fixed-bottom bottom-5 place-content-center space-x-32'):
    ui.button('Refresh Table',on_click=button)
    ui.button('Refresh Table',on_click=button)
ui.run(native=True, title='Database explorer')