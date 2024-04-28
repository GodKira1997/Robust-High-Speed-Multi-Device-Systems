In this project this will make a container that will run a webservice to be able to qurry a value from shared memory at all times.

Note right now it has a chat room interface due to that being the base project I will be making it pretty tomorrow

For your lsl code just put it in the lsl_receiver file. The output of the `make_lsl_loop` call is the one that is passed
into the async thread to manage the shared memory. This will all work with the haproxy setup and as long as the two servers are named
`primary` and `backup`