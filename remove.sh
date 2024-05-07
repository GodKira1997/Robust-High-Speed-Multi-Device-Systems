docker rm monitor
docker rm sensor1
docker rm sensor2
docker rm primary
docker rm backup

docker image build -t python:monitor /home/godkira/ds_project/Monitor
docker image build -t python:sensor1 /home/godkira/ds_project/Sensor1
docker image build -t python:sensor2 /home/godkira/ds_project/Sensor2