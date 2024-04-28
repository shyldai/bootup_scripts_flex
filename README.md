# bootup flex scripts 

Add the scripts to crontab:

```
crontab -e
```

Examples:

```
@reboot sleep 18 && sudo su &&sudo python3 /root/jobs/modem_wakeup.py
@reboot sleep 20 && sudo su  && /bin/sh /root/jobs/after_boot_modem_reconnect.sh
*/15 * * * * /bin/sh /root/jobs/internet_connection.sh
@reboot sleep 19 && sudo su && sudo python3 /root/jobs/health_monitoring.py >> /var/log/myscript.log 2>&1
```
