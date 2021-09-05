docker run -dit --name server -v ~/Documents/projects/chat-sockets/chat-server:/home/server -p 5000:5000 python
docker run -dit --name client1 -v ~/Documents/projects/chat-sockets/chat-server:/home/chat1 python
docker run -dit --name client2 -v ~/Documents/projects/chat-sockets/chat-server:/home/chat2 python
docker run -dit --name client3 -v ~/Documents/projects/chat-sockets/chat-server:/home/chat3 python
docker run -dit --name client4 -v ~/Documents/projects/chat-sockets/chat-server:/home/chat4 python

docker exec -it client1 bash
docker exec -it client2 bash
docker exec -it client3 bash
docker exec -it client4 bash
docker exec -it server bash

docker network create chatnet
docker network connect chatnet server
docker network connect chatnet client1
docker network connect chatnet client2
docker network connect chatnet client3
docker network connect chatnet client4

docker network rm chatnet
docker rm -f client1   
docker rm -f client2 
docker rm -f client3 
docker rm -f client4
docker rm -f server   