from ...kiwoom import Kiwoom
from PyQt5Singleton import Singleton
from .event_manager import EventManager


class OnEventConnect(metaclass=Singleton):
    def __init__(self) -> None:
        self.ocx = Kiwoom().ocx
        self.ocx.OnEventConnect.connect(self.onEventConnect)

        self.pub = EventManager().publisher

    async def call(self, callString):
        result_future = asyncio.Future()

        self.pub.Topic

        self.result_futures[id(result_future)] = result_future

        self.callLibraryMethod(callString)

        err_code = await result_future
        return err_code

    def callLibraryMethod(self, callString):
        threading.Thread(target=self._callLibraryMethodAsync,
                         args=(callString,)).start()

    def onEventConnect(self, errCode):
        self.pub.sendMessage(OpenApiEvents.ON_EVENT_CONNECT, msgData=errCode)
