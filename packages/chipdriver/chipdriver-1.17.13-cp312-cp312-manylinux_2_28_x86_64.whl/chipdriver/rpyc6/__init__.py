"""Remote Python Call (RPyC) is a transparent and symmetric distributed computing library
Licensed under the MIT license (see `LICENSE` file)


"""
# flake8: noqa: F401
from .core import (SocketStream, TunneledSocketStream, PipeStream, Channel,
                       Connection, Service, BaseNetref, AsyncResult, GenericException,
                       AsyncResultTimeout, VoidService, SlaveService, MasterService, ClassicService)
from .utils.factory import (connect_stream, connect_channel, connect_pipes,
                                connect_stdpipes, connect, ssl_connect, list_services, discover, connect_by_service, connect_subproc,
                                connect_thread, ssh_connect)
from .utils.helpers import async_, timed, buffiter, BgServingThread, restricted
from .utils import classic, exposed, service
from .version import __version__

from .lib import setup_logger, spawn
from .utils.server import OneShotServer, ThreadedServer, ThreadPoolServer, ForkingServer
from . import cli

__author__ = "Tomer Filiba (tomerfiliba@gmail.com)"

globals()['async'] = async_     # backward compatibility
