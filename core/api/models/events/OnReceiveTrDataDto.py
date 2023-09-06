# -*- coding: utf-8 -*-
"""

"""
from typing import Any, Optional, Callable, List
from dataclasses import dataclass
from functools import wraps
from inspect import signature

from abc import ABCMeta, abstractmethod


@dataclass
class OnReceiveTrDataDto:
    """
    서버통신 후 데이터를 받은 시점을 알려준다.
    void OnReceiveTrData(LPCTSTR sScrNo, LPCTSTR sRQName, LPCTSTR sTrCode,
        LPCTSTR sRecordName, LPCTSTR sPreNext, LONG nDataLength, LPCTSTR sErrorCode,
        LPCTSTR sMessage, LPCTSTR sSplmMsg)

    sScrNo – 화면번호
    sRQName – 사용자구분 명
    sTrCode – Tran 명
    sRecordName – Record 명
    """

    screen_no: str
    request_name: str
    transaction_code: str
    record_name: str


class KiwoomOpenApiPlusEventHandler(metaclass=ABCMeta):
    def OnReceiveTrData_handler(self, screen_no: str, request_name: str, transaction_code: str, record_name: str):
        self.OnReceiveTrData({screen_no, request_name, transaction_code, record_name})

    @abstractmethod
    def OnReceiveTrData(self, data: OnReceiveTrDataDto):
        pass


# @OnReceiveTrDataDto.decorate
def OnReceiveTrData(
    screen_no: str,
    request_name: str,
    transaction_code: str,
    record_name: str,
    data: Optional[OnReceiveTrDataDto] = None,
):
    print("OnReceiveTrData")


if __name__ == "__main__":
    OnReceiveTrData("1", "2", "3", "4")
