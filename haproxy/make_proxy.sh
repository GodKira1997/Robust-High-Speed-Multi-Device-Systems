docker run -d \
   --name pyproxy \
   --net mynetwork \
   -v $(pwd):/usr/local/etc/haproxy:ro \
   -p 80:80 \
   -p 8404:8404 \
   haproxytech/haproxy-alpine:2.4

