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
import random
import socket
from abc import ABC, abstractmethod


class RandomPort(ABC):
    @abstractmethod
    def value(self) -> int:
        pass


class TcpRandomPort(RandomPort):
    def __init__(
        self, host: str = "127.0.0.1", begin: int = 1024, end: int = 65536
    ) -> None:
        self.__host = host
        self.__begin = begin
        self.__end = end

    def value(self) -> int:
        def is_tcp_port_in_use(host: str, port: int) -> bool:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
                try:
                    sckt.bind((host, port))
                except OSError:
                    return True
                return False

        port = random.randint(self.__begin, self.__end)
        while is_tcp_port_in_use(self.__host, port):
            port = random.randint(self.__begin, self.__end)
        return port


class UdpRandomPort(RandomPort):
    def __init__(
        self, host: str = "127.0.0.1", begin: int = 1024, end: int = 65536
    ) -> None:
        self.__host = host
        self.__begin = begin
        self.__end = end

    def value(self) -> int:
        def is_udp_port_in_use(host: str, port: int) -> bool:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sckt:
                try:
                    sckt.bind((host, port))
                except OSError:
                    return True
                return False

        port = random.randint(self.__begin, self.__end)
        while is_udp_port_in_use(self.__host, port):
            port = random.randint(self.__begin, self.__end)
        return port
