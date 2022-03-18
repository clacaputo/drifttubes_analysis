import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def create_tables(connection):
    
    create_chambers_table = """ CREATE TABLE IF NOT EXISTS chamber (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    channel text,
                                    size integer,
                                    wire integer
                                );"""
                            
    create_voltages_table = """ CREATE TABLE IF NOT EXISTS voltage (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    ch4 INTEGER NOT NULL,
                                    ch5 INTEGER NOT NULL,
                                    ch6 INTEGER NOT NULL,
                                    ch7 INTEGER NOT NULL,
                                    ch8 INTEGER NOT NULL,
                                    ch9 INTEGER NOT NULL,
                                    ch10 INTEGER NOT NULL,
                                    ch11 INTEGER NOT NULL,
                                    ch12 INTEGER NOT NULL,
                                    ch13 INTEGER NOT NULL,
                                    ch14 INTEGER NOT NULL
                                );"""

    create_run_table = """  CREATE TABLE IF NOT EXISTS run (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                date text NOT NULL, 
                                gasFraction1 integer,
                                gasFraction2 integer,
                                GPSP real,
                                voltagesID integer NOT NULL,
                                FOREIGN KEY(voltagesID) REFERENCES voltage(id)
                            );"""

    create_measurement_table = """  CREATE TABLE IF NOT EXISTS measurement (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        voltageScan TEXT NOT NULL,
                                        angle INTEGER,
                                        run_id INTEGER NOT NULL,
                                        FOREIGN KEY(run_id) REFERENCES run(id)
                                    );"""

    create_path_table = """ CREATE TABLE IF NOT EXISTS path (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                absolutePath TEXT NOT NULL,
                                binFile TEXT NOT NULL,
                                decodeFlag INT2,
                                rootFile TEXT,
                                rootFlag INT2,
                                pklFile TEXT,
                                pklFlag INT2,
                                run_id INTEGER NOT NULL,
                                measurement_id INTEGER NOT NULL,
                                FOREIGN KEY(run_id) REFERENCES run(id) FOREIGN KEY(measurement_id) REFERENCES measurement(id)
                            );"""


    

    execute_query(connection, create_chambers_table)
    execute_query(connection, create_voltages_table)
    execute_query(connection, create_run_table)
    execute_query(connection, create_measurement_table)
    execute_query(connection, create_path_table)

def fill_chambers(connection):
    fill_chambers_table = """ INSERT INTO 
                                chamber (channel ,size ,wire )
                              VALUES
                                ('ch4',1,10),
                                ('ch5',1,15),
                                ('ch6',1,20),
                                ('ch7',1,20),
                                ('ch8',1,25),
                                ('ch9',1,40),
                                ('ch10',2,20),
                                ('ch11',2,25),
                                ('ch12',2,40),
                                ('ch13',3,25),
                                ('ch14',3,40)
                                """

    execute_query(connection, fill_chambers_table)


if __name__ == "__main__":
    connection = create_connection("novemberTestBeam.sqlite")
    #create_tables(connection)
    fill_chambers(connection)