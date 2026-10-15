import sys
import time
import base64
import grpc

import lab6_pb2
import lab6_pb2_grpc

IMAGE_FILE = 'Flatirons_Winter_Sunrise_edit_2.jpg'

def main():
    if len(sys.argv) < 4:
        print("Usage: python grpc-client.py <host> <endpoint> <iterations>")
        print("Endpoints: add, dotproduct, rawimage, jsonimage")
        sys.exit(1)

    host = sys.argv[1]
    endpoint = sys.argv[2].lower()
    iterations = int(sys.argv[3])

    # Connect to the gRPC server
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ('grpc.max_send_message_length', 50 * 1024 * 1024)
    ]
    channel = grpc.insecure_channel(f"{host}:50051", options=options)
    stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

    # Pre-generate request payloads so disk read/encoding is NOT measured in the loop
    if endpoint == "add":
        req = lab6_pb2.addMsg(a=123, b=456)
        rpc_call = lambda: stub.Add(req)

    elif endpoint in ("dotproduct", "sum"):
        vec_a = [1.5 * i for i in range(100)]
        vec_b = [0.5 * i for i in range(100)]
        req = lab6_pb2.dotProductMsg(a=vec_a, b=vec_b)
        rpc_call = lambda: stub.DotProduct(req)

    elif endpoint == "rawimage":
        with open(IMAGE_FILE, 'rb') as f:
            raw_data = f.read()
        req = lab6_pb2.rawImageMsg(img=raw_data)
        rpc_call = lambda: stub.RawImage(req)

    elif endpoint == "jsonimage":
        with open(IMAGE_FILE, 'rb') as f:
            b64_str = base64.b64encode(f.read()).decode('utf-8')
        req = lab6_pb2.jsonImageMsg(img=b64_str)
        rpc_call = lambda: stub.JsonImage(req)

    else:
        print(f"Unknown endpoint: {endpoint}")
        sys.exit(1)

    # Warm-up call (establishes channel handshake & connections)
    _ = rpc_call()

    # Benchmark loop
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = rpc_call()
    end_time = time.perf_counter()

    total_time_ms = (end_time - start_time) * 1000.0
    ms_per_query = total_time_ms / iterations

    print(f"Endpoint: {endpoint}")
    print(f"Total iterations: {iterations}")
    print(f"Total time: {total_time_ms:.2f} ms")
    print(f"Average time per query: {ms_per_query:.4f} ms")

if __name__ == '__main__':
    main()