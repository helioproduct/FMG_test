# FMG test  
API который запускает, останавливает, отражает статус, и выдает результат работы процесса на Linux


## Build & Run

### Build docker image:

```console
docker build -t fmg_test .
```  


### Run docker container:
```console
docker run -p 80:80 fmg_test
```  


#### After starting API documentaion will be available on:  
http://0.0.0.0:80

#### Or on  
http://remote-machine-adress:80  




