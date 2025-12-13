"""MSunPV Read library for Python.

See: https://ard-tek.com/

Source: https://github.com/thanatos-vf-2000/msunpv

Init MSunPV connection.

    Args:
        ip (str): Hostname or IP address of MSunPV 2*2 or 4*4

    Raises:
        KeyError: Hostname or IP address empty
        
"""

import logging
import asyncio
import aiohttp
from aiohttp import ClientSession
import time

from .data import MSunPVDataStatus, MSunPVDataIndex
from .webconnect import MSunPVWebConnect
from .exceptions import (
    MSunPVException,
    MSunPVConnectionException,
    MSunPVXMLDataException,
)


_LOG = logging.getLogger(__name__)

class MSunPVRead:
    """Class to Read the MSunPV using webconnect module."""
    
    DataMSunPVDataStatus: MSunPVDataStatus  #: Data from MSunPV status.xml
    DataMSunPVDataIndex: MSunPVDataIndex    #: Data from MSunPV index.xml
    last_read_td: float                     #: Last read MSunPV status.xml
    last_read_ti: float                     #: Last read MSunPV index.xml
    _ip: str
    _session: ClientSession
    _running: bool
    
    
    def __init__(self, ip: str):
        """Init MSunPVRead reader class.

        Args:
            ip (str): Hostname or IP address of MSunPV 2*2 or 4*4

        Raises:
            MSunPVConnectionException: Hostname or IP address empty
            
        """
        self._ip = ip
        self._running = False
        self.last_read_td = None
        self.last_read_ti = None
        self._client = None
        self.DataMSunPVDataStatus = None
        self.DataMSunPVDataIndex = None
    
    async def start(self):
        """Initializes the HTTP session and the MSunPVWebConnect object.

        Args:

        Raises:
            MSunPVConnectionException: Hostname or IP address empty
            
        """
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        )
        _LOG.debug("%s - Start new session...", self.__class__.__name__)
        try:
            self._client = MSunPVWebConnect(self._session, self._ip)
            self._running = True
            self.last_read_td = time.time()
            _LOG.debug("%s - New session open.", self.__class__.__name__)
        except:
            self._running = False
            _LOG.warning("%s - Start new session — Hostname or IP address empty.", self.__class__.__name__)
            raise MSunPVConnectionException(f"Hostname or IP address empty")

    async def stop(self):
        """Properly closes the HTTP session.

        Args:

        Raises:
            
        """
        _LOG.debug("%s - Stop session...", self.__class__.__name__)
        self._running = False
        if self._session:
            await self._session.close()
        _LOG.debug("%s - Session closed.", self.__class__.__name__)

    async def refresh_data(self, All: bool = False):
        """Reads data from WebConnect once.
        Read MSunPV data from status.xml and index.xml and update local variables:
            - MSunPVDataStatus
            - MSunPVDataIndex
            
        Args:

        Raises:
            MSunPVXMLDataException: Message
            
        """
        _LOG.debug("%s - Start Refresh Data...", self.__class__.__name__)
        if not self._client:
            _LOG.warning("%s - MSunPVRead not started (call start()).", self.__class__.__name__)
            raise MSunPVXMLDataException("MSunPVRead not started (call start()).")

        try:
            _LOG.debug("%s - Start Refresh Status...", self.__class__.__name__)
            self.DataMSunPVDataStatus = await self._client.get_status()
            self.last_read_td = time.time()
        except Exception as e:
            _LOG.warning("%s - MSunPVXMLDataException...", self.__class__.__name__)
            raise MSunPVXMLDataException( f"{e}" )
        
        if All == True or self.DataMSunPVDataIndex == None:
            try:
                _LOG.debug("%s - Start Refresh Index...", self.__class__.__name__)
                self.DataMSunPVDataIndex = await self._client.get_index()
                self.last_read_ti = time.time()
            except Exception as e:
                _LOG.warning("%s - MSunPVXMLDataException...", self.__class__.__name__)
                raise MSunPVXMLDataException( f"{e}" )
        
        _LOG.debug("%s - End Refresh Data.", self.__class__.__name__)
        
        return True

    async def wait_for(self, seconds: float):
        """
        Number of seconds to wait since the last status.xml call.
        
        Args:
            seconds (float): number of seconds.
            
        Raises:
            
        """
        _LOG.debug("%s - Start Wait for %s...", self.__class__.__name__, seconds)
        if self.last_read_td is None:
            # Si aucune lecture n'a encore été faite → on attend entièrement
            _LOG.debug("%s - Wait for %ss.", self.__class__.__name__,seconds)
            await asyncio.sleep(seconds)
            return

        now = time.time()
        elapsed = now - self.last_read_td

        remaining = seconds - elapsed

        if remaining > 0:
            _LOG.debug("%s - Wait for %ss.", self.__class__.__name__,remaining)
            await asyncio.sleep(remaining)

        _LOG.debug("%s - End Wait for %s.", self.__class__.__name__, seconds)
        # sinon : on sort immédiatement

    
    