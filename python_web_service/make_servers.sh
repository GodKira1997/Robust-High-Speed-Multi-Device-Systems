docker run -d --name primary --net mynetwork pyserver
docker run -d --name backup --net mynetwork pyserver