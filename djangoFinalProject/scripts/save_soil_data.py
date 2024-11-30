import sqlite3
import serial
import json
import time
import os

# Set the path for the database file
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'npk_data.db')

# Check if the database file already exists
if os.path.exists(db_path):
    print(f"Connecting to existing database at: {db_path}")
else:
    print(f"Creating new database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table for soil data if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS soil_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nitrogen REAL,
    phosphorus REAL,
    potassium REAL,
    soilpH REAL,
    temperature REAL,
    humidity REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def check_saved_data():
    try:
        cursor.execute("SELECT COUNT(*) FROM soil_data")
        count = cursor.fetchone()[0]
        print(f"\nCurrent records in database: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT * FROM soil_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)
            latest = cursor.fetchone()
            print(f"Latest record: {latest}")
    except sqlite3.Error as e:
        print(f"Database check error: {e}")

# Set up the serial connection
serial_port = "COM9"
baud_rate = 9600

print("Attempting to connect to serial port...")

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Successfully connected to {serial_port}")
except serial.SerialException as e:
    print(f"Error: {e}")
    print("Please make sure:")
    print("1. Arduino IDE's Serial Monitor is closed")
    print("2. The correct COM port is selected")
    print("3. Try running the script as administrator")
    exit(1)

print("Listening for data on serial port...")

# Initialize time for interval tracking
last_saved_time = time.time()
save_interval = 10  # Changed to 10 seconds for testing (from 5 * 60)

try:
    while True:
        if ser.in_waiting > 0:
            # Read data from the serial port
            line = ser.readline().decode('utf-8').strip()
            try:
                # Parse the JSON data
                data = json.loads(line)

                # Extract values
                nitrogen = data.get("nitrogen", None)
                phosphorus = data.get("phosphorus", None)
                potassium = data.get("potassium", None)
                soilpH = data.get("soilpH", None)
                temperature = data.get("temperature", None)
                humidity = data.get("humidity", None)

                # Get the current time
                current_time = time.time()

                # Save to SQLite database only if the interval has passed
                if current_time - last_saved_time >= save_interval:
                    cursor.execute("""
                    INSERT INTO soil_data (nitrogen, phosphorus, potassium, soilpH, temperature, humidity)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (nitrogen, phosphorus, potassium, soilpH, temperature, humidity))
                    conn.commit()

                    last_saved_time = current_time  # Update the last saved time
                    print(f"Data saved: {data}")
                    check_saved_data()  # Check and display saved data after insertion
                else:
                    print(f"Waiting {int(save_interval - (current_time - last_saved_time))} seconds until next save...")

            except json.JSONDecodeError:
                print("Invalid JSON data received")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping...")
    ser.close()
    conn.close()

