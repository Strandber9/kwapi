import os

import yaml
# from ..util.singleton import singleton
from common.util.singleton import singleton


@singleton
class TRInfoLookup:

    def __init__(self) -> None:
        # 디렉토리 경로 설정
        self.directory_path = os.path.join(os.getcwd(), 'config', 'yaml')
        # 모든 YAML 파일을 하나의 딕셔너리로 합치기 위한 빈 딕셔너리 생성
        self.tr_info = {}

        # 디렉토리 내의 모든 YAML 파일 찾기
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".yaml"):
                file_path = os.path.join(self.directory_path, filename)
                # YAML 파일을 읽어와 딕셔너리로 변환하여 합치기
                with open(file_path, 'r', encoding='utf-8') as file:
                    yaml_data = yaml.safe_load(file)
                    tr_code, ext = os.path.splitext(filename)
                    self.tr_info[tr_code] = yaml_data

    def getOutputSingle(self, tr_code):
        return self.tr_info[tr_code]['data']['output'].get('single', [])

    def getOutputMultiple(self, tr_code):
        return self.tr_info[tr_code]['data']['output'].get('multiple', [])
