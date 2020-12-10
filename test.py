from dronekit import connect
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=921600)
