
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|---	|
|   REST add	|   1.314	|   	|  	|
|   gRPC add	|   0.2822	|   	|    	|
|   REST rawimg	|   3.62	|   	|   	|
|   gRPC rawimg	|    4.1288   |   	|   	|
|   REST dotproduct	|  1.209 	|   	|  	|
|   gRPC dotproduct	|   0.2941 ms	|   	|    	|
|   REST jsonimg	|  1.42 	|   	|   	|
|   gRPC jsonimg	|  6.40     |   	|   	|
|   PING        |    0.26   |      |       |

You should measure the basic latency  using the `ping` command - this can be construed to be the latency without any RPC or python overhead.

You should examine your results and provide a short paragraph with your observations of the performance difference between REST and gRPC. You should explicitly comment on the role that network latency plays -- it's useful to know that REST makes a new TCP connection for each query while gRPC makes a single TCP connection that is used for all the queries.