Before any of the haproxy stuff is set up I did it all on a specific network if 
you have your own network setting for the mqtt stuff you should be able to use those
but this is what i did `docker network create --driver=bridge mynetwork`

This is the command that I ran to make the container, 
just know that the `haproxy.cfg` file must be in the same directory you call this from
```
   docker run -d \\
   --name haproxy \\
   --net mynetwork \\
   -v $(pwd):/usr/local/etc/haproxy:ro \\
   -p 80:80 \\
   -p 8404:8404 \\
   haproxytech/haproxy-alpine:2.4
```