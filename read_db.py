import sqlite3

import time

import threading


# Absolute path to the database file

db_path = '/home/qubip/mqttdb/mqtt_data.db'


# Function to create a new database connection

def create_connection():

    conn = sqlite3.connect(db_path)

    return conn, conn.cursor()


# Function to read and return new rows from the 'messages' table

def read_new_rows(last_row_id, cursor):

    cursor.execute('SELECT rowid, * FROM messages WHERE rowid > ?', (last_row_id,))

    rows = cursor.fetchall()

    return rows


# Function to read all rows from the 'messages' table

def read_all_rows(cursor):

    cursor.execute('SELECT rowid, * FROM messages')

    rows = cursor.fetchall()

    return rows


# Function to update the displayed messages

def update_messages():

    conn, cursor = create_connection()

    last_row_id = 0


    # Read all rows initially

    all_rows = read_all_rows(cursor)

    for row in all_rows:

        print(f"Topic: {row[1]}, Payload: {row[2]}")

        last_row_id = row[0]  # Update the last_row_id to the latest one


    try:

        while True:

            new_rows = read_new_rows(last_row_id, cursor)

            if new_rows:

                for row in new_rows:

                    print(f"Topic: {row[1]}, Payload: {row[2]}")

                last_row_id = new_rows[-1][0]

            time.sleep(1)

    except KeyboardInterrupt:

        print("Interrupted by user")

    finally:

        conn.close()

        print("Database connection closed")


# Start the thread to update messages

thread = threading.Thread(target=update_messages)

thread.daemon = True  # This will allow the thread to exit when the main program exits

thread.start()


# Keep the main program running to allow the thread to continue working

try:

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("Main program interrupted by user")

finally:

    print("Shutting down the program")

