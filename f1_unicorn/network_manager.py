import rp2
import network
import machine
import uasyncio


class NetworkManager:
    def __init__(
        self,
        country,
        client_timeout=60,
    ):
        rp2.country(country)
        self.interface = network.WLAN(network.STA_IF)

        self._client_timeout = client_timeout
        self.UID = ("{:02X}" * 8).format(*machine.unique_id())

    def isconnected(self):
        return self.interface.isconnected()

    def config(self, var):
        return self.interface.config(var)

    def ifaddress(self):
        if self.interface.isconnected():
            return self.interface.ifconfig()[0]
        return "0.0.0.0"

    def disconnect(self):
        if self.interface.isconnected():
            self.interface.disconnect()

    async def wait(self, mode):
        while not self.isconnected():
            self._handle_status(mode, None)
            await uasyncio.sleep_ms(1000)

    def _handle_status(self, mode, status):
        ...

    def _handle_error(self, mode, msg):
        ...

    async def client(self, ssid, psk):
        if self.interface.isconnected():
            self._handle_status(network.STA_IF, True)
            return

        self.interface.active(True)
        self.interface.config(pm=0xA11140)
        self.interface.connect(ssid, psk)

        try:
            await uasyncio.wait_for(self.wait(network.STA_IF), self._client_timeout)
            self._handle_status(network.STA_IF, True)

        except uasyncio.TimeoutError:
            self.interface.active(False)
            self._handle_status(network.STA_IF, False)
            self._handle_error(network.STA_IF, "WIFI Client Failed")


async def connect_wifi(country, ssid, psk):
    network_manager = NetworkManager(country)
    await network_manager.client(ssid, psk)
    await network_manager.wait(network.STA_IF)


def connect_wifi_sync(country, ssid, psk):
    uasyncio.run(connect_wifi(country, ssid, psk))


def is_connected(country):
    network_manager = NetworkManager(country)
    return network_manager.isconnected()
