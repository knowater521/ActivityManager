# FileSubmitter
用来社团，部门，比赛提交作业，作品文件使用。网页提交文件代替FTP，限定zip格式。


# Installation

    pip -u requirement.txt
    python3 runserver.py # This is use for testing mode.
    gunicorn runserver:app # This is use for production mode.


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
