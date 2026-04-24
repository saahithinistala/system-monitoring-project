from monitoring_script import Monitoring
from datetime import datetime
import os

def display():
    print("##########################")
    print("#    MONITORING SCRIPT   #")
    print("##########################")
    print("# 1. Disk Usage          #")
    print("# 2. Service Status      #")
    print("# 3. Log Error Detection #")
    print("# 4. API Health Check    #")
    print("# 5. Exit                #")
    print("##########################")

    choice = int(input("Please enter your choice: "))

    return choice

#####-----MAIN------####
log_path = "logs"
log_file = f"{log_path}/system_health_check_py.log"

if not os.path.isdir(log_path):
    os.makedirs(log_path, exist_ok=True)
    print(f"Log Directory -> {log_path} has been created")

if not os.path.isfile(log_file):
    with open(log_file, "w") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: Log file -> {log_file} has been created\n")

    print(f"Log file -> {log_file} has been created")

monitor = Monitoring(log_file)
user_choice = display()
if user_choice == 1:
    monitor.disk_usage()
elif user_choice == 2:
    service_name = input("Enter the service to be checked: ").strip()
    monitor.service_status(service_name)
elif user_choice == 3:
    app_log = input("Enter application log: ").strip()
    if os.path.isfile(app_log):
        monitor.log_error_detection(app_log)
    else:
        print("Application log not found!!")
elif user_choice == 4:
    api_url = input("Enter the endpoint url: ").strip()
    monitor.api_health_check(api_url)
elif user_choice == 5:
    exit(1)
else:
    print("Invalid input. Please enter 1, 2, 3, 4 or 5")
