
|  Method 	| Local ms 	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	|   2.1298	|   	|  	|
|   gRPC add	|   0.2822	|   	|    	|
|   REST rawimg	|   4.6448	|   	|   	|
|   gRPC rawimg	|    0.3363   |   	|   	|
|   REST dotproduct	|  2.4401 	|   	|  	|
|   gRPC dotproduct	|   0.3363 	|   	|    	|
|   REST jsonimg	|  41.3039 	|   	|   	|
|   gRPC jsonimg	|  10.2681    |   	|   	|
|   PING        |    0.044   |      |       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.