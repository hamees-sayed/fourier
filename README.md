# Fourier | Music Streaming App


## Prerequisites:
Install Redis: 
```bash
$ sudo apt update
$ sudo apt-get install redis-server
```

> Refer to [docs](https://redis.io/docs/latest/operate/oss_and_stack/install/) if you have any problem running redis.

Install Mailhog:  
1. [Guide](https://gist.github.com/dipenparmar12/4e6cd50d8d1303d5e914742f62659116) for Linux
2. [Other Methods](https://kinsta.com/blog/mailhog/)

---

## Start App: 
Make the scripts executable:
```bash
$ chmod +x run.sh
$ chmod +x worker.sh
```
Start Redis Server: 
```bash
$ sudo service redis-server start
```
Start client/server:  
```bash
$ ./run.sh
```

Start Mailhog Server:
```bash
$ Mailhog
```

Start Celery workers:  
```bash
$ ./worker.sh
```

## Video Demo
[Presentation of the Project](https://youtu.be/ZIKCX-XWZD0)

## Database Schema:
[https://dbdiagram.io/d/Fourier](https://dbdiagram.io/d/Fourier-65378240ffbf5169f05399fe)   

## Swagger API Spec:
[https://app.swaggerhub.com/fourier](https://app.swaggerhub.com/apis/hamees-sayed/fourier-music_streaming_app_open_api_3_0/1.0.0)
