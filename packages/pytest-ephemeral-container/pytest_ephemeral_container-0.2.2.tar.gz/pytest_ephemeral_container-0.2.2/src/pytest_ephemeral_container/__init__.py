"""
Little utility to do epehemeral containers from within PyTest
"""

import contextlib
import functools
from pathlib import Path
import socket
import time
from types import EllipsisType
import typing
import urllib.request

import docker
import docker.models.containers
import docker.utils
import pytest


class ContextNotExistError(ValueError):
    """
    The given Docker context does not exist.

    This should only happen if your Docker client is misconfigured.
    """


def _docker_3190_workaround():
    """
    Work around for https://github.com/docker/docker-py/issues/3190
    """
    if docker.utils.config.find_config_file() is None:
        # TODO: Prefer .config_path_from_environment() over .home_dir()
        config_path = (
            Path(docker.utils.config.home_dir())
            / docker.utils.config.DOCKER_CONFIG_FILENAME
        )

        if config_path.parent.exists():
            # If .docker doesn't exist, it doesn't contain contexts
            config_path.touch()


@functools.cache
def _get_docker_client(use: str | None = None) -> docker.DockerClient:
    """
    Get a docker client for the given docker context.

    Unlike docker.from_env(), this considers the user's configured context.
    """
    _docker_3190_workaround()

    context = docker.ContextAPI.get_context(use)
    if context is None:
        raise ContextNotExistError(f"Docker context {use!r} not found")
    return docker.DockerClient(
        base_url=context.endpoints["docker"]["Host"], tls=context.TLSConfig
    )


@contextlib.contextmanager
def spawn_container(**props) -> typing.Iterator[docker.models.containers.Container]:
    """
    Creates a tempory container instance using Docker, and automatically cleans it up.
    """
    client = _get_docker_client()

    container = client.containers.run(
        detach=True,
        auto_remove=True,
        **props,
    )
    # TODO: Stream container output

    try:
        yield container
    finally:
        container.stop()


def discover_ports(
    container: docker.models.containers.Container, port: str
) -> typing.Iterable[tuple[str, int]]:
    """
    Given a container & inner port, find the ports/ips its been forwarded to

    eg, (127.0.0.1", 1234)
    """
    ports = None
    while ports is None:
        container.reload()
        try:
            # Dig out the connected port
            ports = container.attrs["NetworkSettings"]["Ports"][port]
        except KeyError:
            time.sleep(0.1)

    for port_config in ports:
        host_ip: str = port_config["HostIp"]
        if host_ip == "0.0.0.0":
            host_ip = "127.0.0.1"
        elif host_ip == "::":
            host_ip = "::1"
        host_port = int(port_config["HostPort"])
        yield host_ip, host_port


def try_tcp_port(
    addr: str, port: int, *, timeout: float | None | EllipsisType = ...
) -> bool:
    """
    Make a test TCP connection.

    Returns if it was successful or not.

    NOTE: This might only check the connection to the Docker proxy.
    """
    if timeout is ...:
        timeout = socket.getdefaulttimeout()

    try:
        sock = socket.create_connection((addr, port), timeout=timeout)
    except OSError:
        return False
    except TimeoutError:
        return False
    else:
        sock.close()
        return True


def try_http(ip, port, *, timeout=0.1):
    """
    Use urllib to attempt a basic HTTP request.

    Doesn't actually care _what_ HTTP response is returned, just that HTTP
    happened.
    """
    try:
        urllib.request.urlopen(f"http://{ip}:{port}", timeout=timeout)
    except ConnectionResetError:
        return False
    except TimeoutError:
        return False
    except urllib.error.URLError:
        return False
    else:
        return True


def wait_for(
    timeout: float = 30.0,
    sleep_time: float = 1.0,
) -> typing.Callable:
    """
    Wait for a function to succeed (presumably a port test).

    eg:

        wait_for(30)(try_tcp_port, "::1", 4242, timeout=0.1)

    * timeout: total time to wait for
    * sleep_time: time to wait between attempts
    """

    def loop(func, *pargs, **kwargs):
        deadline = time.monotonic() + timeout
        while time.monotonic() <= deadline:
            if func(*pargs, **kwargs):
                return
            else:
                time.sleep(sleep_time)
        else:
            raise TimeoutError()

    return loop


def wait_for_port(
    addr: str,
    port: int,
    *,
    timeout: float = 30.0,
    inc_timeout: float = 0.1,
    sleep_time: float = 1.0,
) -> None:
    """
    Shorthand for:

        wait_for(timeout=timeout, sleep_time=sleep_time)(try_tcp_port, addr, port, timeout=inc_timeout)

    NOTE: This might only check the connection to the Docker proxy.
    """
    wait_for(timeout=timeout, sleep_time=sleep_time)(
        try_tcp_port, addr, port, timeout=inc_timeout
    )


def wait_for_http(
    addr: str,
    port: int,
    *,
    timeout: float = 30.0,
    inc_timeout: float = 0.1,
    sleep_time: float = 1.0,
) -> None:
    """
    Shorthand for:

        wait_for(timeout=timeout, sleep_time=sleep_time)(try_http, addr, port, timeout=inc_timeout)
    """
    wait_for(timeout=timeout, sleep_time=sleep_time)(
        try_http, addr, port, timeout=inc_timeout
    )


@pytest.fixture(scope="session")
def dockerclient():
    return _get_docker_client()
