# The MIT License (MIT)
#
# Copyright (C) 2025 Fabrício Barros Cabral
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import socket

from random_port.pool import TcpRandomPort, UdpRandomPort


def test_tcp_random_port() -> None:
    begin = 1024
    end = 65535
    port = TcpRandomPort().value()
    assert port >= begin
    assert port <= end


def test_udp_random_port() -> None:
    begin = 1024
    end = 65535
    port = UdpRandomPort().value()
    assert port >= begin
    assert port <= end


def test_tcp_in_use() -> None:
    host = "127.0.0.1"
    begin = 12344
    end = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind((host, begin))
    port = TcpRandomPort(host, begin, end).value()
    server.close()
    assert port == end


def test_udp_in_use() -> None:
    host = "127.0.0.1"
    begin = 12344
    end = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.setblocking(False)
    server.bind((host, begin))
    port = UdpRandomPort(host, begin, end).value()
    server.close()
    assert port == end
