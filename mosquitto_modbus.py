import subprocess
import threading
from pymodbus.client import ModbusTcpClient
import sys
import time

DEFAULT_BROKER = "192.168.101.63"
DEFAULT_PORT = "1883"
DEFAULT_CAFILE = "/home/enrico/ca.crt"
DEFAULT_CERTFILE = "/home/enrico/client.crt"
DEFAULT_KEYFILE = "/home/enrico/client.key"
DEFAULT_MODBUS_IP = "192.168.101.212"
DEFAULT_MODBUS_PORT = "502"
DEFAULT_MODBUS_REGISTER = "32770"
DEFAULT_MODBUS_ID = "1"
topic = "2023/test"
process = None
is_connected = False
subscriptions = {}
modbus_read_interval = 1000  # Default to 1000 milliseconds (1 second)
modbus_reading_active = False

def run_command(command, success_message):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(success_message)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

def handle_process_output(process, topic):
    global is_connected
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            if 'Enter PEM pass phrase:' in output:
                password = request_password()
                process.stdin.write(password + '\n')
                process.stdin.flush()
            if 'connected' in output.lower() or 'connack' in output.lower():
                print(f"Connected to broker: {DEFAULT_BROKER}")
                is_connected = True
            if 'disconnected' in output.lower():
                print("Disconnected from broker")
                is_connected = False
    rc = process.poll()
    return rc
'''
def run_mosquitto_pub(message):
    global process
    command = f"mosquitto_pub -h {DEFAULT_BROKER} -p {DEFAULT_PORT} --cafile {DEFAULT_CAFILE}  -t 2023/test -m \"{message}\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    threading.Thread(target=handle_process_output, args=(process, '')).start()
''' 
def run_mosquitto_pub(message):
    global process
        
    command = f"mosquitto_pub -h {DEFAULT_BROKER} -p {DEFAULT_PORT} --cafile {DEFAULT_CAFILE} --cert {DEFAULT_CERTFILE} --key {DEFAULT_KEYFILE} -t {topic} -m \"{message}\""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    threading.Thread(target=handle_process_output, args=(process, '')).start()
    
def run_mosquitto_sub():
    global process
    command = f"mosquitto_sub -h {DEFAULT_BROKER} -p {DEFAULT_PORT} --cafile {DEFAULT_CAFILE} --cert {DEFAULT_CERTFILE} --key {DEFAULT_KEYFILE} -t {topic}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    
    threading.Thread(target=handle_process_output, args=(process, topic)).start()
   
'''
def run_mosquitto_sub():
    global process
    topic = "2023/test"
    command = f"mosquitto_sub -h {DEFAULT_BROKER} -p {DEFAULT_PORT} --cafile {DEFAULT_CAFILE} --cert {DEFAULT_CERTFILE} --key {DEFAULT_KEYFILE} -t 2023/test"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    threading.Thread(target=handle_process_output, args=(process, topic)).start()
'''
def read_modbus_and_publish():
    client = ModbusTcpClient(DEFAULT_MODBUS_IP, int(DEFAULT_MODBUS_PORT))

    if client.connect():
        result = client.read_holding_registers(int(DEFAULT_MODBUS_REGISTER), 1, unit=int(DEFAULT_MODBUS_ID))
        if not result.isError():
            value = result.registers[0]
            print(f"Value read from the register {DEFAULT_MODBUS_REGISTER}: {value}")
            run_mosquitto_pub(str(value))
        client.close()
    else:
        print("Modbus connection failed")

def modbus_reading_loop():
    global modbus_reading_active
    while modbus_reading_active:
        read_modbus_and_publish()
        time.sleep(modbus_read_interval / 1000)	

def start_modbus_reading_loop():
    global modbus_reading_active
    modbus_reading_active = True
    modbus_reading_loop_thread = threading.Thread(target=modbus_reading_loop)
    modbus_reading_loop_thread.start()

def stop_modbus_reading():
    global modbus_reading_active
    modbus_reading_active = False

if __name__ == "__main__":
    print("Starting Modbus reading and MQTT publishing...")
    run_mosquitto_sub()  # Subscribe to the topic
    start_modbus_reading_loop()  # Start the Modbus reading and publishing loop

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_modbus_reading()
        print("Stopped by user.")

