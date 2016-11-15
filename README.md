o serviço foi escrito em Python e deve ser executado dentro do ambiente Python (ver forma 1) ou em container Docker (ver forma 2)

#forma 1

REVISAR

cd ../env-python/organizacional

source ../teste_env/bin/activate


#forma 2

comando para criar o container com base no Dockerfile:
docker build -t pessoa-srv .

comando para executar o container e iniciar o serviço automaticamente
docker run --name pessoa-serv -v /home/lucasm/workspace/works-experiment/microservices/pessoa:/app-src -p 7070:8000 srv-pessoa

para utilizar o serviço, é só acessar o endereço http://localhost:7070/enterprise


para debugar o funcionamento do serviço no container
docker run --name pessoa-serv --entrypoint=/bin/ash -it -v /home/lucasm/workspace/works-experiment/microservices/pessoa:/app-src -p 7070:8000 srv-pessoa
