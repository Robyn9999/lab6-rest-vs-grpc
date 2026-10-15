
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	|   1.314	|   	|  	|
|   gRPC add	|   	|   	|    	|
|   REST rawimg	|   4.58	|   	|   	|
|   gRPC rawimg	|       |   	|   	|
|   REST dotproduct	|  6.13 	|   	|  	|
|   gRPC dotproduct	|   	|   	|    	|
|   REST jsonimg	|  7.8 	|   	|   	|
|   gRPC jsonimg	|       |   	|   	|
|   PING        |       |      |       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.