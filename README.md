# bootup_scripts

Add the scripts to crontab:

```
crontab -e
```

Examples:

```
@reboot sudo python3 /home/shyldai/shyld/unit_testing/record.py
@reboot sudo python3 /root/jobs/motors_sleep_Flex.py
*/30 * * * * sudo python3 /root/jobs/motors_sleep_Flex.py
```
