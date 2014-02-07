LiveCrowd
===========

![Live Crowd Density Visualization](https://dl.dropboxusercontent.com/u/12208857/img/live_crowd_ss.png)

## Set up

### 1.Install require packages.

    $ pip install tornado
    $ pip install MySQL-python

### 2.Create "config.json" and fill in the blanks of MySQL settings

    $ cp config.json.template config.json
    $ vim config.json #write your sql settings

### 3.Run and access to the web page.

    $ python main.py
