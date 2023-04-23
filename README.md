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
http://0.0.0.0:80

#### Or on:  
http://remote-machine-adress:80  


## Usage
**Using curl:**

Start process:  
```console
curl -X POST "http://0.0.0.0/api/ping/start"
```  

Stop process:  
```console
curl -X POST "http://0.0.0.0/api/ping/stop"
```  

Get status:  
```console
curl -X GET "http://0.0.0.0/api/ping"
```  

Get status:  
```console
curl -X GET "http://0.0.0.0/api/ping/result"
```  



