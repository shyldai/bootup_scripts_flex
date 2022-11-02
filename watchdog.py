timer = open('/dev/watchdog', 'w')
timer.write('1')
timer.close()
