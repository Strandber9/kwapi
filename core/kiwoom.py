from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QEventLoop

from common.data.data_lookup import TRInfoLookup
from common.util.singleton import singleton

import sys
import uuid


M = {
    str: "QString",
    int: "int",
}


@singleton
class KiwoomApi:
    def __init__(self) -> None:
        print("__init__")
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self.OnEventConnect)
        self.ocx.OnReceiveMsg.connect(self.OnReceiveMsg)
        self.ocx.OnReceiveTrData.connect(self.OnReceiveTrData)

        self.eventLoop = QEventLoop()
        self.trData = {}

        self.login()

    def OnEventConnect(self, err_code):
        print(f"👌👌👌-OnEventConnect: {err_code}")
        if err_code == 0:
            pass
        self.eventLoop.exit()

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print("📃📃📃----------------88888888888888889999999999999999999999", sScrNo, sRQName, sTrCode, sMsg)

    def OnReceiveTrData(
        self,
        sScrNo,
        sRQName,
        sTrCode,
        sRecordName,
        sPreNext,
        nDataLength,
        sErrorCode,
        sMessage,
        sSplmMsg,
    ):
        print(f"🎁🎁🎁-OnReceiveTrData:{sPreNext}", sScrNo, sRQName, sTrCode)
        if sRQName in self.trData:
            tr_data = self.trData[sRQName]
            outputData = tr_data.setdefault("output", {})

            # 싱글데이터 수신
            outputData["single"] = {
                k: self.dynamicCall("GetCommData", sTrCode, sRecordName, 0, k).strip()
                for k in TRInfoLookup().getOutputSingle(sTrCode)
            }

            # 멀티데이터 수신
            outputData["multiple"] = outputData.get("multiple", []) + [
                {
                    k: self.dynamicCall("GetCommData", sTrCode, sRecordName, index, k).strip()
                    for k in TRInfoLookup().getOutputMultiple(sTrCode)
                }
                for index in range(self.dynamicCall("GetRepeatCnt", sTrCode, sRecordName))
            ]

            # 다음데이터 존재의 경우 CommRqData으로 다음데이터 수신 -- 이거 사용자 쪽에서 컨트롤 하는게 맞지 않을까?
            if sPreNext == "2":
                self.CommRqData(sTrCode, sPreNext, **self.trData[sRQName])
            else:
                # QEventLoop 종료하여 CommRqData wake-up
                print("⏰⏰⏰ QEventLoop - EXIT")
                tr_data["event"].exit()

    def login(self):
        self.ocx.dynamicCall("CommConnect()")
        self.eventLoop.exec_()

    def dynamicCall(self, method, *args):
        params = ",".join([str(M.get(type(v))) for v in args])
        return self.ocx.dynamicCall(f"{method}({params})", list(args))

    def CommRqData(self, trCode, prevNext="0", **kwargs):
        print(f'🚀🚀🚀-CommRqData: {TRInfoLookup().tr_info[trCode].get("desc")}')

        # OnReceiveTrData 를 받아올때까지 대기시켜주는 이벤트 루프 생성
        kwargs.setdefault("event", QEventLoop())

        # YAML파일에서 TR_INFO가져오기
        tr_info = TRInfoLookup().tr_info[trCode]

        # YAML파일에서 화면번호 가져오기
        screenNo = kwargs.setdefault("screenNo", tr_info["screenNo"])

        # 레코드이름 생성 (trCode-UUID) 만약 지정된 rqName이 있으면 이걸 우선으로 사용
        rqName = kwargs.setdefault("rqName", f"{trCode}-{uuid.uuid4()}")

        # 레코드이름으로 전달받은 데이터 입력
        self.trData[rqName] = kwargs

        # 인풋데이터 세팅
        for k, v in kwargs["input"].items():
            self.dynamicCall("SetInputValue", k, v)

        # TR데이터 송신
        self.dynamicCall("CommRqData", rqName, trCode, prevNext, screenNo)

        # QEventLoop 실행하여 응답이올때까지 대기
        if not self.trData[rqName]["event"].isRunning():
            print("⏰⏰⏰ QEventLoop - EXEC")
            self.trData[rqName]["event"].exec_()

        # prevNext 최종이기에 trData에서 삭제
        output_data = self.trData.get(rqName, {})
        if prevNext == "0":
            del self.trData[rqName]

        return output_data


if not QApplication.instance():
    print("-------------")


if __name__ == "__main__":
    import json

    app = QApplication(sys.argv)
    kw = KiwoomApi()
    kw.login()

    # data = kw.dynamicCall("GetLoginInfo", "ACCOUNT_CNT")
    # print(data)

    # data = kw.CommRqData("opt10001", 0, "9999", {
    #     "input": {
    #         "종목코드": "005930"
    #     },
    #     "output": {
    #         "single": [
    #             "종목코드",
    #             "종목명",
    #             "PER",
    #             "PBR",
    #         ]
    #     }
    # })
    # print(f'data: [{data}]')

    # data = kw.CommRqData("opt10003", **{
    #     "input": {
    #         "종목코드": "005930"
    #     },
    #     "output": {
    #         "시간": None,
    #         "체결강도": None,
    #         "누적거래량": None,
    #         "현재가": None,
    #     }
    # })
    # print(f'-----data: [{data}]')

    # data = kw.CommRqData("opt10003", **{
    #     "input": {
    #         "종목코드": "005930"
    #     },
    #     "output": {
    #         "시간": None,
    #         "체결강도": None,
    #         "누적거래량": None,
    #         "현재가": None,
    #     }
    # })
    # print(f'-----data: [{data}]')

    # print(kw.dynamicCall("GetLoginInfo", "ACCNO"))
    # sRQName, sTrCode, nPrevNext, sScreenNo
    data = kw.CommRqData(
        "opw00018",
        **{
            "trCode": "opw00018",
            # "rqName": "",
            "prevNext": "0",
            "screenNo": "",
            "input": {
                "계좌번호": "6196809210",
                "비밀번호": "925299",
                "비밀번호입력매체구분": "00",
                "조회구분": 2,
            },
        },
    )
    print(json.dumps(data.get("output", {}), indent=4, ensure_ascii=False))

    app.exec()

# accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
# user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
# user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명

# account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
# accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
# user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
# user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
# keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
# firewall = kiwoom.GetLoginInfo("FIREW_SECGB")
