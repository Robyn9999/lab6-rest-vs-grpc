
|  Method 	     | Local ms | Same-Zone  	|  Different Region 	|
|---	|---	|---	     |---	         |---	|
|   REST add	|   2.298	|   3.055	     |   314.18	|
|   gRPC add	|   0.8822	|   1.101	    |    157.4779	|
|   REST rawimg	|   4.6448	|   39.9922	    |  1244.47 	|
|   gRPC rawimg	|    3.7363   |  20.3699 	|    197.8654	|
|   REST dotproduct	|  2.4401 	|   3.36  	|314.0317
|   gRPC dotproduct	|   0.8363 	|   1.14	| 142.7431   	|
|   REST jsonimg	|  51.3039 	|   69.034	|   1426.1577	|
|   gRPC jsonimg	|  22.2681  |   44.27	|   197.5447	|
|   PING        |    0.054      |     0.386       |   141.024    | 

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.


Rest overall preforms slower thanb gRPC. For local ms the main difference is the serialization and framework runtime since protocol buffers unpack rapidly in c++ where as REST incurs python routing. 