LiveCrowd
===========

Live Crowd Density Visualization

## Set up

### 1.Install require packages.

    $ pip install tornado
    $ pip install MySQL-python

### 2.Create "config.json" and fill in the blanks of MySQL settings

    $ cp config.json.template config.json
    $ vim config.json #write your sql settings

### 3.Change the host name of web socket in "static/js/main.js"

Change "localhost:8000/data" to "YOUR_MACHINE_NAME.local:8000/data"

### 4.Run and access the page

    $ python main.py

--> localhost:8000/10

You can change the scale of balloons by editing the parameter after slash.
