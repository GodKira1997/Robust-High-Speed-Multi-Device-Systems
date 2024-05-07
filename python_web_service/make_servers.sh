docker run -d --name primary --net mynetwork pyserver primary --log
docker run -d --name backup --net mynetwork pyserver backup --log