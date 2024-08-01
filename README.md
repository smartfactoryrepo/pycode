mosquitto_modbus.py
-------------
This code reads data from a Modbus server and publishes it to an MQTT broker using Mosquitto client. 
It continuously connects to the Modbus server, reads a specific register, and sends the data to an MQTT topic.
The topic string is composed of two parts separated by a /: the first part is the client ID, and the second part is the channel name, typically the name of the data being sent.
In this example, the ID is 2023, and the data sent is a test number.
The main program runs the Modbus reading loop in a separate thread and handles MQTT subscriptions and message publishing.

mqtt_to_db.py
------------
This Python script connects to an MQTT broker, subscribes to the topic "2023/test", and saves incoming messages to an SQLite database.
It ensures the database directory exists, creates a messages table if it doesn't exist, and handles incoming messages by printing and storing them. 
The script maintains the MQTT connection and gracefully closes the database connection upon termination.

read_db.py
-----------
This Python script continuously reads and displays new rows from an SQLite database table. 
It initially prints all existing rows and then checks for new rows every second, printing them as they are found. 
The database connection is handled in a separate thread, and the main program runs indefinitely until interrupted by the user, at which point it gracefully shuts down.
