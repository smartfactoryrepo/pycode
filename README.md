mqtt_to_db.py
-------------
This code reads data from a Modbus server and publishes it to an MQTT broker using Mosquitto client. 
It continuously connects to the Modbus server, reads a specific register, and sends the data to an MQTT topic.
The topic string is composed of two parts separated by a /: the first part is the client ID, and the second part is the channel name, typically the name of the data being sent.
In this example, the ID is 2023, and the data sent is a test number.
The main program runs the Modbus reading loop in a separate thread and handles MQTT subscriptions and message publishing.
