from enum import Enum


class OpenApiEvents(Enum):

    # OnReceiveTrData: Tran 수신시 이벤트
    ON_RECEIVE_TR_DATA = "OnReceiveTrData"

    # OnReceiveTrData: 실시간 시세 이벤트
    ON_RECEIVE_REAL_DATA = "OnReceiveRealData"

    # OnReceiveMsg: 수신 메시지 이벤트
    ON_RECEIVE_MSG = "OnReceiveMsg"

    # OnReceiveChejanData: 주문 접수/확인 수신시 이벤트
    ON_RECEIVE_CHEJAN_DATA = "OnReceiveChejanData"

    # OnEventConnect: 통신 연결 상태 변경시 이벤트
    ON_EVENT_CONNECT = "OnEventConnect"

    # OnReceiveRealCondition: 조건검색 실시간 편입,이탈종목 이벤트
    ON_RECEIVE_REAL_CONDITION = "OnReceiveRealCondition"

    # OnReceiveTrCondition: 조건검색 조회응답 이벤트
    ON_RECEIVE_TR_CONDITION = "OnReceiveTrCondition"

    # OnReceiveConditionVer: 로컬에 사용자조건식 저장 성공여부 응답 이벤트
    ON_RECEIVE_CONDITION_VER = "OnReceiveConditionVer"

    def __str__(self):
        return str(self.value)
