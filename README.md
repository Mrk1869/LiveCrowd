LiveCrowd
===========

![Live Crowd Density Visualization](https://www.dropbox.com/s/t2kkka8ophgk6jt/github_live_crowd_ss.png?raw=1)

## Set up

### 1.Install require packages.

    $ pip install tornado
    $ pip install MySQL-python

### 2.Create "config.json" and fill in the blanks of MySQL settings

    $ cp config.json.template config.json
    $ vim config.json #write your sql settings

### 3.Run and access to the web page.

    $ python main.py
