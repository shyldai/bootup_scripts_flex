import smbus
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import psutil
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
# Activate the fans
GPIO.output(7, False)
GPIO.output(18, False)

class HealthMonitor:
    device_name = 'Flex-'
    # Message Frequency
    notification_period = 600 # seconds

    # Parameters of Motor Usage
    max_uv_runtime = 3600 #seconds
    # Assume that motors are running if this threshold exceed
    current_threshold = 500 # unit is not defined

    # Parameters of Motor Usage
    max_cpu_runtime = 3600 #seconds
    # Assume that motors are running if this threshold exceed
    cpu_threshold = 95 # percent

    # Parameters of Disk Usage
    disk_usage_threshold = 80 #percent

    # Parameters of Memory Usage
    memory_usage_threshold = 80 #percent

    # Token is created for the warning channel of Slack
    for i in range(5):
        try:
            slack_client = WebClient(token="token-api")
        except:
            time.sleep(5)
    # The slave address of the MCP3021
    mcp3021_address = 0x4b
    # Use i2c bus 1
    i2c_bus = smbus.SMBus(1) 

    def __init__(self):
        initial_message = ' - Rebooted'
        self.send_alert(initial_message)

    def send_alert(self, warning_text):
        """Sends a warning message to a Slack channel using the Slack API.

        Args:
            warning_text (str): The warning message text to send.

        Returns:
            None
        """
        # Create the warning message with the device name and warning text
        text = f"Warning: {self.device_name}{warning_text}"
            
        # Try to send the message via Slack API
        try:
            response = self.slack_client.chat_postMessage(
                channel="#warning",
                text=text
            )
        except:
            for i in range(5):
                try:
                    self.slack_client = WebClient(token="token-api")
                except:
                    time.sleep(5)

    def get_disk_usage(self):
        """Gets the disk usage statistics for the root directory ('/') and prints them to the console.
        
        Returns:
            float: The percentage of disk space used.
        """
        # Get the disk usage statistics for the root directory
        disk = psutil.disk_usage('/')
        
        # Calculate the total, used, and free disk space in GB
        total = disk.total / (1024.0 ** 3)
        used = disk.used / (1024.0 ** 3)
        free = disk.free / (1024.0 ** 3)
        
        # Calculate the percentage of disk space used
        used_percentage = disk.percent
        
        # Print the disk usage statistics to the console
        print(f'Total: {total:.2f} GB')
        print(f'Used: {used:.2f} GB')
        print(f'Free: {free:.2f} GB')
        print(f'Percent Used: {used_percentage}%')
        
        # Return the percentage of disk space used
        return used_percentage


    def get_consumption_measurements(self, duration, interval):
        """Measures the current consumption at regular intervals over a specified duration of time.
        
        Args:
            duration (float): The duration of time to measure consumption in seconds.
            interval (float): The time interval between consumption measurements in seconds.
            
        Returns:
            list: Average of current consumption measurements.
        """
        # Calculate the number of measurements to take
        num_measurements = int(duration / interval)
        
        # Initialize an empty list to store the measurements
        measurements = []
        
        # Take a consumption measurement every interval seconds for the specified duration
        for i in range(num_measurements):
            # Read the current consumption and add it to the measurements list
            word_reading = self.i2c_bus.read_word_data(self.mcp3021_address, 0x00)
            raw_data = ((word_reading & 0xFF00) >> 8) | ((word_reading & 0xFF) << 8)
            measurements.append(raw_data)
            
            # Wait for the specified interval before taking the next measurement
            time.sleep(interval)
        
        return sum(measurements)/num_measurements

    def get_cpu_usage(self, duration, interval):
        """Measures the CPU usage at regular intervals over a specified duration of time.
        
        Args:
            duration (float): The duration of time to measure CPU usage in seconds.
            interval (float): The time interval between CPU usage measurements in seconds.
            
        Returns:
            list: Average of CPU usage measurements as percentages over the specified duration of time.
        """
        # Calculate the number of measurements to take
        num_measurements = int(duration / interval)
        
        # Initialize an empty list to store the measurements
        measurements = []
        
        # Take a CPU usage measurement every interval seconds for the specified duration
        for i in range(num_measurements):
            # Get the current CPU usage as a percentage and add it to the measurements list
            cpu_usage = psutil.cpu_percent()
            measurements.append(cpu_usage)
            
            # Wait for the specified interval before taking the next measurement
            time.sleep(interval)
        
        return sum(measurements)/num_measurements

    def get_memory_percent(self):
        """Calculates the percentage of memory currently in use.
        
        Returns:
            float: The percentage of memory currently in use.
        """
        # Get the current memory usage statistics
        mem_stats = psutil.virtual_memory()
        
        # Calculate the percentage of memory in use
        mem_percent = mem_stats.percent
        
        return mem_percent

# TODO: Create a main function to monitor hardware regularly
# We can also use paralle processing
def monitoring():
    #add all of the monitoring scripts here
    pass
health_monitoring = HealthMonitor()

active_motor_time = 0
active_cpu_time = 0

idle_motor_time = 0
idle_cpu_time = 0

t_warning_motor = 0
t_warning_disk = 0
t_warning_cpu = 0
t_warning_memory = 0


while True:
    ############## Current Consumption ###############
    # Measure the current consumption every 0.5 seconds over a 5-second duration
    current_usage = health_monitoring.get_consumption_measurements(duration=5.0, interval=0.5)

    if current_usage > health_monitoring.current_threshold:
        print('Warning Motors are ON')
        active_motor_time = time.time()
    else:
        print('Idle')
        idle_motor_time = time.time()

    # Motor Usage Alert
    active_motor_duration = active_motor_time - idle_motor_time
    if time.time() - t_warning_motor < health_monitoring.notification_period:
        # Send a single message on every 10 min
        pass
    elif active_motor_duration > health_monitoring.max_uv_runtime:
        warning_text = " - Motors are active for {} minutes".format(active_motor_duration/60)
        health_monitoring.send_alert(warning_text)
        # Log the last time a warning send
        t_warning_motor = time.time()

    ############## Disk Usage ###############
    if time.time() - t_warning_disk < health_monitoring.notification_period:
        # Send a single message on every 10 min
        pass
    else:
        disk_usage = health_monitoring.get_disk_usage()
        if disk_usage > health_monitoring.disk_usage_threshold:
            warning_text = " - {}% of the disk is in use.".format(disk_usage)
            health_monitoring.send_alert(warning_text)
        # Watch out to indentation, we should get disk usage in every 10 minutes
        # Log the last time a warning send
        t_warning_disk = time.time()

    ############## CPU Usage ###############
    # Get measurements for a minute in each 10 second
    avg_cpu_usage = health_monitoring.get_cpu_usage(duration=60, interval=10)
    if avg_cpu_usage > health_monitoring.cpu_threshold:
        print('Warning CPU usage over {}%', health_monitoring.cpu_threshold)
        active_cpu_time = time.time()
    else:
        print('Low cpu usage')
        idle_cpu_time = time.time()
    
    active_cpu_duration = active_cpu_time - idle_cpu_time
    if time.time() - t_warning_cpu < health_monitoring.notification_period:
        # Send a single message on every 10 min
        pass
    elif active_cpu_duration > health_monitoring.max_cpu_runtime:
        warning_text = " - Cpu usage over 95 percent for {} minutes".format(active_cpu_duration/60)
        health_monitoring.send_alert(warning_text)

        # Log the last time a warning send
        t_warning_cpu = time.time()

    ############## Memory Consumption ###############
    if time.time() - t_warning_memory < health_monitoring.notification_period:
        # Send a single message on every 10 min
        pass
    else:
        memory_usage = health_monitoring.get_memory_percent()
        if memory_usage > health_monitoring.memory_usage_threshold:
            warning_text = " - {}% of the memory is in use.".format(memory_usage)
            health_monitoring.send_alert(warning_text)
            # Watch out to indentation, we should get memory usage regularly
            # Log the last time a warning send
            t_warning_memory = time.time()
        else:
            print('low memory usage', memory_usage)