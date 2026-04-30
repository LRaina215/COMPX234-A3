# COMPX234 Assignment 3 - TCP Tuple Space Client/Server

## Overview

This project implements a TCP-based tuple space system in Python.

The system consists of:

- A multi-threaded TCP server
- A TCP client that reads requests from a file
- A shared tuple space stored on the server
- Support for `PUT`, `READ`, and `GET` operations
- A length-prefixed communication protocol
- Periodic server statistics output
- Support for multiple concurrent clients

The server maintains all tuples in memory using a Python dictionary. Clients do not store tuple data locally. Each client opens one TCP connection to the server, sends one or more requests during that session, receives one response per request, and then closes the connection.

---

## Files

```text
TCP_Mlti_Server.py
TCP_Mlti_Client.py
request-simple-test.txt
request-multithread-test.txt
README.md
```

## Test Cases

### Test Case 1: Basic Sequential Test

This test uses `request-simple-test.txt`.

Contents of `request-simple-test.txt`:

```text
PUT a 1
READ a
GET a
READ a
```

Start the server in one terminal:

```bash
python3 TCP_Mlti_Server.py 51234
```

Run the client in another terminal:

```bash
python3 TCP_Mlti_Client.py localhost 51234 request-simple-test.txt
```

Expected client output:

```text
PUT a 1: OK (a, 1) added
READ a: OK (a, 1) read
GET a: OK (a, 1) removed
READ a: ERR a does not exist
```

This test verifies that the server can add a tuple, read it without removing it, remove it using `GET`, and return an error when reading a removed key.

---

### Test Case 2: Concurrent Client Test

This test uses both `request-simple-test.txt` and `request-multithread-test.txt`.

Contents of `request-simple-test.txt`:

```text
PUT a 1
READ a
GET a
READ a
```

Contents of `request-multithread-test.txt`:

```text
PUT b 2
READ b
PUT a 999
READ a
GET b
READ b
```

Start the server in one terminal:

```bash
python3 TCP_Mlti_Server.py 51234
```

Run the two clients concurrently in another terminal:

```bash
python3 TCP_Mlti_Client.py localhost 51234 request-simple-test.txt &

python3 TCP_Mlti_Client.py localhost 51234 request-multithread-test.txt &
wait
```

Because the two clients run concurrently, the exact output order may vary.

A successful concurrent test should show that both clients receive responses and that the server accepts two client connections.

Example server output:

```text
New client connected from (...)
New client connected from (...)
```

The server summary should show at least:

```text
Total clients: 2
```

The total number of operations should match the total number of valid request lines across both files.

This test verifies that the server can handle multiple clients at the same time, that each client is handled by a separate thread, and that all clients share the same server-side tuple space safely.