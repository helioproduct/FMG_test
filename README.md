# FMG test  
API который запускает, останавливает, отражает статус, и выдает результат работы процесса на Linux

## Specifications

### Framework:  FastAPI  
### Process:    ping  

*ping google.com 100 times every 5 second*


## Build & Run

### Build docker image:

```console
docker build -t fmg_test .
```  


### Run docker container:
```console
docker run -p 80:80 fmg_test
```  

*port should be free*

#### After starting API documentaion will be available on:  
http://0.0.0.0:80/api/docs  

#### Or on:  
http://remote-machine-adress:80  


## Usage
**Using curl:**

Start process:  
```console
curl -X 'POST' \
  'http://127.0.0.1:8000/api/ping/?command=start' \
  -H 'accept: application/json' \
  -d ''
```  

Stop process:  
```console
curl -X 'POST' \
  'http://127.0.0.1:8000/api/ping/?command=stop' \
  -H 'accept: application/json' \
  -d ''
```  

Get status:  
```console
curl -X GET "http://0.0.0.0/api/ping"
```  

Get result:  
```console
curl -X GET "http://0.0.0.0/api/ping/result"
```  

**Using Swagger UI:**   

http://0.0.0.0:80/api/docs

