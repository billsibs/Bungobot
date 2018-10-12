Bungo Bot

A bot tool used to post Bungie API data into a discord channel


The bot can be turned into a service (for Ubuntu) by:

Creating a service file:
* vi /lib/systemd/system/bungobot.service
> [Unit]
>
> Description=Bungo Bot service
> After=multi-user.target
> 
> [Service]
>
> Type=simple
> ExecStart=/usr/bin/python3 /home/bill/bungobot/bungo.py
>
> [Install]
>
> WantedBy=multi-user.target


Reload systemctl and start the service
* sudo systemctl daemon-reload
* sudo systemctl start bungobot

