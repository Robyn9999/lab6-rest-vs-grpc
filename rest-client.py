#!/usr/bin/env python3

from __future__ import print_function

import sys
import time
import base64
import argparse
import requests

IMAGE_FILE = 'Flatirons_Winter_Sunrise_edit_2.jpg'

def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    a, b = 5, 10
    expected_sum = a + b
    add_url = f"{addr}/api/add/{a}/{b}"

    response = requests.post(add_url, headers=headers)
    response.raise_for_status()

    data = response.json()
    received_sum = int(data.get('sum', -1))
    assert received_sum == expected_sum, f"Expected {expected_sum}, got {received_sum}"

    if debug:
        print(f"Verified sum: {a} + {b} = {received_sum}")


def doDotProduct(addr, payload, expected_dot, debug=False):
    url = f"{addr}/api/dotproduct"
    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    received_dot = data.get("dotproduct", data.get("result", data.get("dot_product")))
    assert abs(received_dot - expected_dot) < 1e-6, f"Expected {expected_dot}, got {received_dot}"

    if debug:
        print(f"Verified dot product: {expected_dot} == {received_dot}")


def doRawImage(addr, raw_bytes, debug=False):
    headers = {'content-type': 'application/octet-stream'}
    url = f"{addr}/api/rawimage"

    response = requests.post(url, data=raw_bytes, headers=headers)
    response.raise_for_status()

    data = response.json()
    assert data.get('width', 0) > 0 and data.get('height', 0) > 0, "Invalid image dimensions received"

    if debug:
        print(f"Decoded dimensions: {data['width']}x{data['height']}")


def doJsonImage(addr, payload, debug=False):
    url = f"{addr}/api/jsonimage"

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    assert data.get('width', 0) > 0 and data.get('height', 0) > 0, "Invalid image dimensions received"

    if debug:
        print(f"Decoded dimensions: {data['width']}x{data['height']}")


# ---------------------------------------------------------
# CLI Arguments & Setup
# ---------------------------------------------------------
parser = argparse.ArgumentParser(description='REST client for measuring server operations')
parser.add_argument('host', help='IP address or hostname of the REST server')
parser.add_argument('cmd', choices=['add', 'rawImage', 'dotProduct', 'jsonImage'], help='Operation to perform')
parser.add_argument('reps', type=int, help='Number of repetitions for measurement')
parser.add_argument('-p', '--port', type=int, default=5000, help='Server port (default: 5000)')
parser.add_argument('-d', '--debug', action='store_true', help='Print the response from the server')

args = parser.parse_args()
addr = f"http://{args.host}:{args.port}"

print(f"Running {args.reps} reps of '{args.cmd}' against {addr}")

# Pre-generate payloads so disk I/O and base64 encoding aren't measured in the loop
if args.cmd == 'add':
    bench_call = lambda: doAdd(addr, debug=args.debug)

elif args.cmd == 'dotProduct':
    vec_a = [1.5 * i for i in range(100)]
    vec_b = [0.5 * i for i in range(100)]
    expected_dot = sum(x * y for x, y in zip(vec_a, vec_b))
    payload = {"a": vec_a, "b": vec_b}
    bench_call = lambda: doDotProduct(addr, payload, expected_dot, debug=args.debug)

elif args.cmd == 'rawImage':
    with open(IMAGE_FILE, 'rb') as f:
        raw_bytes = f.read()
    bench_call = lambda: doRawImage(addr, raw_bytes, debug=args.debug)

elif args.cmd == 'jsonImage':
    with open(IMAGE_FILE, 'rb') as f:
        encoded_b64 = base64.b64encode(f.read()).decode('utf-8')
    payload = {"img": encoded_b64}
    bench_call = lambda: doJsonImage(addr, payload, debug=args.debug)

# Warm-up call
bench_call()

# Benchmark loop
start = time.perf_counter()
for _ in range(args.reps):
    bench_call()
delta = ((time.perf_counter() - start) / args.reps) * 1000

print(f"Took {delta:.4f} ms per operation")