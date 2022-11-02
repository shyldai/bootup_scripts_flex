#!/bin/bash
#Each 30 second(line 27) we call ping google.com if 3(Max_threshold) times in a row we dont have ping then we reebot (line 16 to 19)
#2- go to terminal and go to current directory the you save internet.sh run this "$ chmod +x check_inet.sh"
#3- sudo crontab -e
#4- in crontab please write: */30 * * * * path_to/internet.sh

Calculator=0
Max_thereshold=3
ZERO=0
COUNTER=0 
echo $Calculator
echo $Max_thereshold
while [ $COUNTER -le Max_thereshold ]
do
COUNTER=$((COUNTER+1))
echo $COUNTER
X=0
if [ $Calculator -gt $Max_thereshold ];then
  echo "Disconnecting reach to thereshold After 20 second the module will be reboot..."
  sleep 20s
  reboot
  
fi
if ping -c5 google.com; then
    X=1
else
    X=0
fi
sleep 30s
if [ $X -eq $ZERO ];then
   Calculator=$((Calculator+1))
else
   Calculator=$((0))
fi
echo "wake UP"
echo $Calculator
done
