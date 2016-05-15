# FileSubmitter / Activity Manager
用来社团,部门,比赛,活动的报名与文件成功提交。 使用网页提交文件代替FTP上传,自动规范文件名,方便快捷。


# Installation
    Edit the Environment.py with your database configuration and baseurl.

    pip -u requirement.txt
    python3 runserver.py # This is use for testing mode.
    gunicorn runserver:app # This is use for production mode.
    # using gunicorn -k gevent runserver:app to enable gevent mode.


# Notes:
It's recommended to set up an nginx to proxy the network and use supervisor to control the project running.


# Nginx Configuration

    location /  
    # using ^~/upload/ to specify the prefix when you using mutiply programming language.
        {
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $host;
          proxy_set_header   Remote_Addr    $remote_addr;
          proxy_redirect off;
          proxy_pass http://127.0.0.1:8000;
          client_max_body_size 100m; 
        }
    # Copy Static folder to your web directory if needed.
        
        
# Supervisor Configuration
    [program:upload]
    command = /usr/local/bin/gunicorn  runserver:app
    directory = /home/FileSubmitter
    user = www
    autostart = true
    autorestart = true
    stderr_logfile = /tmp/stderr.log
    stdout_logfile = /tmp/stdout.log

# How to use
- In the first time you need to add an activity and Admin manually in the database.
- Then you can simply login via the admin account in baseurl/activity_name/login to login,click the admin pannel in the navigation bar to get more settings and set more activities.
- Because the file download moudle is unstable and unconvience.Is's recommand to set up a FTP server in the Upload directory to download all Files.
- After set up the server.Visit baseurl to get activities list.

