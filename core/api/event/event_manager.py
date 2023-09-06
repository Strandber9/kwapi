from pubsub import pub
from .event import OpenApiEvents
from ...kiwoom import Kiwoom
from .on_event_connect import OnEventConnect

from PyQt5Singleton import Singleton
import asyncio


class EventManager(metaclass=Singleton):

    '''
    EventManager 설명
    '''

    def __init__(self) -> None:
        '''
        초기생성자:
            ---
        '''
        self.publisher = pub
        self.ocx = Kiwoom().ocx

        # OnEventConnect 등록
        OnEventConnect()

    def callApi(self, callString: str, eventListner):
        # self.ocx.dynamicCall("CommConnect()")
        asyncio.run(self.dynamicCall(callString, None))

    async def dynamicCall(self, callString, eventListner):
        self.ocx.dynamicCall(callString)

    def onEventConnect(self, errCode):
        self.sendMessage(OpenApiEvents.ON_EVENT_CONNECT, msgData=errCode)

    def subscribe(self, event: OpenApiEvents, eventListner) -> None:
        # Register listeners
        self.publisher.subscribe(eventListner, event.value)

    def sendMessage(self, event: OpenApiEvents, **msgData) -> None:
        self.publisher.sendMessage(event.value, **msgData)
        print('👌👌👌', event.value)


def listener_bob(arg):
    print('Bob receives news about', arg['headline'])
    print(arg['news'])
    print()


def gg(arg): return print(arg)


if __name__ == '__main__':
    print(OpenApiEvents.ON_EVENT_CONNECT.name)
    em = EventManager()
    em.subscribe(OpenApiEvents.ON_EVENT_CONNECT, gg)
    # em.subscribe(OpenApiEvents.ON_EVENT_CONNECT, listener_bob)

    # Send messages to all listeners of topics
    em.sendMessage(OpenApiEvents.ON_EVENT_CONNECT, arg={
                   'headline': 'Ronaldo', 'news': 'Sold for $1M'})
    # pub.sendMessage('football', arg={'headline': 'Ronaldo', 'news': 'Sold for $1M'})
