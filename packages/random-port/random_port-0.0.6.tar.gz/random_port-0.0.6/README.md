# Random Port

## Introduction

Usually we need start a TCP or UDP server (mainly to use in tests) but, which
port must be used? So, random-port is the answer. It generate a free random
TCP or UDP port to be used for any server.

## How to install

Install it using `pip` command:

```bash
pip install random-port
```

in your project folder.

## Usage

- To use a TCP random port:

```python
from random_port.pool import TcpRandomPort

port = TcpRandomPort().value()
```

- To use a UDP random port:

```python
from random_port.pool import UdpRandomPort

port = UdpRandomPort().value()
```

## License

The MIT License (MIT)

Copyright (C) 2025 Fabrício Barros Cabral

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
