import io
import base64
from concurrent import futures
import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc

class Lab6Servicer(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        total = request.a + request.b
        return lab6_pb2.addReply(sum=total)

    def DotProduct(self, request, context):
        # Calculate dot product: sum(a_i * b_i)
        result = sum(x * y for x, y in zip(request.a, request.b))
        return lab6_pb2.dotProductReply(dotproduct=result)

    def RawImage(self, request, context):
        # Decode raw bytes directly using io.BytesIO
        img_stream = io.BytesIO(request.img)
        with Image.open(img_stream) as img:
            w, h = img.size
        return lab6_pb2.imageReply(width=w, height=h)

    def JsonImage(self, request, context):
        # Decode base64 string back into raw bytes, then inspect dimensions
        img_bytes = base64.b64decode(request.img.encode('utf-8'))
        img_stream = io.BytesIO(img_bytes)
        with Image.open(img_stream) as img:
            w, h = img.size
        return lab6_pb2.imageReply(width=w, height=h)


def serve():
    # Increase maximum message size if testing with high-res images (>4MB default)
    options = [
        ('grpc.max_receive_message_length', 50 * 1024 * 1024),
        ('grpc.max_send_message_length', 50 * 1024 * 1024)
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server listening on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()