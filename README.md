# bootup flex scripts 

Add the scripts to crontab:

```
crontab -e
```

Examples:

```
@reboot sleep 20 && sudo su  && /bin/sh /root/jobs/after_boot_modem_reconnect.sh
@reboot sudo python3 /root/jobs/bootup_scripts/motors_sleep_Flex.py
*/30 * * * * sudo python3 /root/jobs/bootup_scripts/motors_sleep_Flex.py
*/30 * * * * /bin/sh /root/jobs/internet_connection.sh
```
