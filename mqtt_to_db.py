# -*- coding: utf-8 -*-


import os

import paho.mqtt.client as mqtt

import sqlite3


# Absolute path to the database file

db_path = '/home/qubip/mqttdb/mqtt_data.db'


# Ensure the directory for the database exists

os.makedirs(os.path.dirname(db_path), exist_ok=True)


print(f"Database path: {db_path}")


# Function to create a new database connection

def create_connection():

    conn = sqlite3.connect(db_path)

    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS messages

                 (topic TEXT, payload TEXT)''')

    conn.commit()

    return conn, c


# Create the initial connection and table if it doesn't exist

conn, c = create_connection()


# Function to handle the connection

def on_connect(client, userdata, flags, rc):

    print(f"Connected with result code {rc}")

    client.subscribe("2023/test")


# Function to handle incoming messages

def on_message(client, userdata, msg):

    print(f"{msg.topic} {msg.payload}")

    c.execute("INSERT INTO messages (topic, payload) VALUES (?, ?)",

              (msg.topic, msg.payload.decode()))

    conn.commit()


# Configure the MQTT client

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message


# Connect to the MQTT broker

client.connect("192.168.101.63", 1884, 60)


# Loop to maintain the connection

try:

    client.loop_forever()

except KeyboardInterrupt:

    print("Interrupted by user")

finally:

    # Close the database connection when the program terminates

    conn.close()

    print("Database connection closed")

