# Fourier | Music Streaming App


## Prerequisites:
Install Redis: 
1. `$ sudo apt update`
2. `$ sudo apt-get install redis-server`

> Refer to [docs](https://redis.io/docs/latest/operate/oss_and_stack/install/) if you have any problem running redis.

Install Mailhog:
1. [Guide](https://gist.github.com/dipenparmar12/4e6cd50d8d1303d5e914742f62659116) for Linux
2. [Other Methods](https://kinsta.com/blog/mailhog/)

---

## Start App: 
Start App:  
`$ ./run.sh`

Start Celery workers and Mailhog server  
`$ ./worker.sh`


## Database Schema:
[https://dbdiagram.io/d/Fourier](https://dbdiagram.io/d/Fourier-65378240ffbf5169f05399fe)   

## Video Demo
[Presentation of the Project (Backend)](https://youtu.be/ZIKCX-XWZD0)

[Presentation of the Project (Frontend)](#)

## Swagger API Spec:
[https://app.swaggerhub.com/fourier](https://app.swaggerhub.com/apis/hamees-sayed/fourier-music_streaming_app_open_api_3_0/1.0.0)
