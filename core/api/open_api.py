import asyncio


class OpenApi:
    ''' 
    '''

    def __init__(self) -> None:
        self.result_futures = {}

    def call(self):
        result_future = asyncio.Future()
        self.result_futures[id(result_future)] = result_futurepass
