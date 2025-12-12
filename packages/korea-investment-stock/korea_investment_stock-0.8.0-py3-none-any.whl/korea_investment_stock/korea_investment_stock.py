'''
한국투자증권 python wrapper
'''
import datetime
import json
import os
import pickle
import random
import time
import zipfile
import logging
import re
from pathlib import Path
from typing import Literal, Optional, List
from zoneinfo import ZoneInfo  # Requires Python 3.9+
from datetime import datetime, timedelta

import pandas as pd
import requests
from typing import Dict, Any

from .token_storage import TokenStorage, FileTokenStorage, RedisTokenStorage

# 로거 설정
logger = logging.getLogger(__name__)

EXCHANGE_CODE = {
    "홍콩": "HKS",
    "뉴욕": "NYS",
    "나스닥": "NAS",
    "아멕스": "AMS",
    "도쿄": "TSE",
    "상해": "SHS",
    "심천": "SZS",
    "상해지수": "SHI",
    "심천지수": "SZI",
    "호치민": "HSX",
    "하노이": "HNX"
}

# 해외주식 주문
# 해외주식 잔고
EXCHANGE_CODE2 = {
    "미국전체": "NASD",
    "나스닥": "NAS",
    "뉴욕": "NYSE",
    "아멕스": "AMEX",
    "홍콩": "SEHK",
    "상해": "SHAA",
    "심천": "SZAA",
    "도쿄": "TKSE",
    "하노이": "HASE",
    "호치민": "VNSE"
}

EXCHANGE_CODE3 = {
    "나스닥": "NASD",
    "뉴욕": "NYSE",
    "아멕스": "AMEX",
    "홍콩": "SEHK",
    "상해": "SHAA",
    "심천": "SZAA",
    "도쿄": "TKSE",
    "하노이": "HASE",
    "호치민": "VNSE"
}

EXCHANGE_CODE4 = {
    "나스닥": "NAS",
    "뉴욕": "NYS",
    "아멕스": "AMS",
    "홍콩": "HKS",
    "상해": "SHS",
    "심천": "SZS",
    "도쿄": "TSE",
    "하노이": "HNX",
    "호치민": "HSX",
    "상해지수": "SHI",
    "심천지수": "SZI"
}

CURRENCY_CODE = {
    "나스닥": "USD",
    "뉴욕": "USD",
    "아멕스": "USD",
    "홍콩": "HKD",
    "상해": "CNY",
    "심천": "CNY",
    "도쿄": "JPY",
    "하노이": "VND",
    "호치민": "VND"
}

MARKET_TYPE_MAP = {
    "KR": ["300"],  # "301", "302"
    "KRX": ["300"],  # "301", "302"
    "NASDAQ": ["512"],
    "NYSE": ["513"],
    "AMEX": ["529"],
    "US": ["512", "513", "529"],
    "TYO": ["515"],
    "JP": ["515"],
    "HKEX": ["501"],
    "HK": ["501", "543", "558"],
    "HNX": ["507"],
    "HSX": ["508"],
    "VN": ["507", "508"],
    "SSE": ["551"],
    "SZSE": ["552"],
    "CN": ["551", "552"]
}

MARKET_TYPE = Literal[
    "KRX",
    "NASDAQ",
    "NYSE",
    "AMEX",
    "TYO",
    "HKEX",
    "HNX",
    "HSX",
    "SSE",
    "SZSE",
]

EXCHANGE_TYPE = Literal[
    "NAS",
    "NYS",
    "AMS"
]

MARKET_CODE_MAP: dict[str, MARKET_TYPE] = {
    "300": "KRX",
    "301": "KRX",
    "302": "KRX",
    "512": "NASDAQ",
    "513": "NYSE",
    "529": "AMEX",
    "515": "TYO",
    "501": "HKEX",
    "543": "HKEX",
    "558": "HKEX",
    "507": "HNX",
    "508": "HSX",
    "551": "SSE",
    "552": "SZSE",
}

EXCHANGE_CODE_MAP: dict[str, EXCHANGE_TYPE] = {
    "NASDAQ": "NAS",
    "NYSE": "NYS",
    "AMEX": "AMS"
}

API_RETURN_CODE = {
    "SUCCESS": "0",  # 조회되었습니다
    "EXPIRED_TOKEN": "1",  # 기간이 만료된 token 입니다
    "NO_DATA": "7",  # 조회할 자료가 없습니다
    "RATE_LIMIT_EXCEEDED": "EGW00201",  # Rate limit 초과
}


# Note: retry_on_rate_limit decorator는 enhanced_retry_decorator 모듈에서 import됨


class KoreaInvestment:
    '''
    한국투자증권 REST API
    '''

    # 기본 설정 파일 경로 (우선순위 순)
    DEFAULT_CONFIG_PATHS = [
        "~/.config/kis/config.yaml",
        "~/.config/kis/config.yml",
    ]

    # 기본 캐시 TTL (시간) - 1주일
    DEFAULT_MASTER_TTL_HOURS = 168

    def __init__(
        self,
        api_key: str | None = None,
        api_secret: str | None = None,
        acc_no: str | None = None,
        config: "Config | None" = None,
        config_file: "str | Path | None" = None,
        token_storage: Optional[TokenStorage] = None
    ):
        """한국투자증권 API 클라이언트 초기화

        설정 우선순위 (5단계):
            1. 생성자 파라미터 (최고 우선순위)
            2. config 객체
            3. config_file 파라미터
            4. 환경 변수 (KOREA_INVESTMENT_*)
            5. 기본 config 파일 (~/.config/kis/config.yaml)

        Args:
            api_key (str | None): 발급받은 API key
            api_secret (str | None): 발급받은 API secret
            acc_no (str | None): 계좌번호 체계의 앞 8자리-뒤 2자리 (예: "12345678-01")
            config (Config | None): Config 객체 (Phase 2에서 추가됨)
            config_file (str | Path | None): 설정 파일 경로
            token_storage (Optional[TokenStorage]): 토큰 저장소 인스턴스

        Raises:
            ValueError: api_key, api_secret, 또는 acc_no가 설정되지 않았을 때
            ValueError: acc_no 형식이 올바르지 않을 때

        Examples:
            # 방법 1: 생성자 파라미터 (기존 방식)
            >>> broker = KoreaInvestment(
            ...     api_key="your-api-key",
            ...     api_secret="your-api-secret",
            ...     acc_no="12345678-01"
            ... )

            # 방법 2: 환경 변수 자동 감지
            >>> broker = KoreaInvestment()

            # 방법 3: Config 객체 사용
            >>> config = Config.from_yaml("~/.config/kis/config.yaml")
            >>> broker = KoreaInvestment(config=config)

            # 방법 4: config_file 파라미터
            >>> broker = KoreaInvestment(config_file="./my_config.yaml")

            # 방법 5: 혼합 사용 (일부만 override)
            >>> broker = KoreaInvestment(config=config, api_key="override-key")
        """
        # 5단계 우선순위로 설정 해결
        resolved = self._resolve_config(
            api_key=api_key,
            api_secret=api_secret,
            acc_no=acc_no,
            config=config,
            config_file=config_file,
        )

        self.api_key = resolved["api_key"]
        self.api_secret = resolved["api_secret"]
        acc_no = resolved["acc_no"]

        # 필수값 검증
        missing_fields = []
        if not self.api_key:
            missing_fields.append("api_key (KOREA_INVESTMENT_API_KEY)")
        if not self.api_secret:
            missing_fields.append("api_secret (KOREA_INVESTMENT_API_SECRET)")
        if not acc_no:
            missing_fields.append("acc_no (KOREA_INVESTMENT_ACCOUNT_NO)")

        if missing_fields:
            raise ValueError(
                "API credentials required. Missing: " + ", ".join(missing_fields) + ". "
                "Pass as parameters, use config/config_file, or set KOREA_INVESTMENT_* environment variables."
            )

        # 계좌번호 형식 검증
        if '-' not in acc_no:
            raise ValueError(f"계좌번호 형식이 올바르지 않습니다. '12345678-01' 형식이어야 합니다. 입력값: {acc_no}")

        self.base_url = "https://openapi.koreainvestment.com:9443"

        # account number - 검증 후 split
        parts = acc_no.split('-')
        if len(parts) != 2 or len(parts[0]) != 8 or len(parts[1]) != 2:
            raise ValueError(f"계좌번호 형식이 올바르지 않습니다. 앞 8자리-뒤 2자리여야 합니다. 입력값: {acc_no}")

        self.acc_no = acc_no
        self.acc_no_prefix = parts[0]
        self.acc_no_postfix = parts[1]

        # resolved에서 token_storage 관련 설정 가져오기
        self._resolved_config = resolved

        # 토큰 저장소 초기화
        if token_storage:
            self.token_storage = token_storage
        else:
            self.token_storage = self._create_token_storage()

        # access token
        self.access_token = None
        if self.token_storage.check_token_valid(self.api_key, self.api_secret):
            token_data = self.token_storage.load_token(self.api_key, self.api_secret)
            if token_data:
                self.access_token = f'Bearer {token_data["access_token"]}'
        else:
            self.issue_access_token()

    def _resolve_config(
        self,
        api_key: str | None,
        api_secret: str | None,
        acc_no: str | None,
        config: "Config | None",
        config_file: "str | Path | None",
    ) -> dict:
        """5단계 우선순위로 설정을 해결

        우선순위:
            1. 생성자 파라미터 (최고 우선순위)
            2. config 객체
            3. config_file 파라미터
            4. 환경 변수
            5. 기본 config 파일 (~/.config/kis/config.yaml)

        Args:
            api_key: 생성자에서 전달된 API key
            api_secret: 생성자에서 전달된 API secret
            acc_no: 생성자에서 전달된 계좌번호
            config: Config 객체
            config_file: 설정 파일 경로

        Returns:
            dict: 해결된 설정 값들
                - api_key: API key
                - api_secret: API secret
                - acc_no: 계좌번호
                - token_storage_type: 토큰 저장소 타입
                - redis_url: Redis URL
                - redis_password: Redis 비밀번호
                - token_file: 토큰 파일 경로
        """
        # 결과 딕셔너리 초기화 (None으로)
        result = {
            "api_key": None,
            "api_secret": None,
            "acc_no": None,
            "token_storage_type": None,
            "redis_url": None,
            "redis_password": None,
            "token_file": None,
        }

        # 5단계: 기본 config 파일에서 로드 (가장 낮은 우선순위)
        default_config = self._load_default_config_file()
        if default_config:
            self._merge_config(result, default_config)

        # 4단계: 환경 변수
        env_config = self._load_from_env()
        self._merge_config(result, env_config)

        # 3단계: config_file 파라미터
        if config_file:
            file_config = self._load_config_file(config_file)
            if file_config:
                self._merge_config(result, file_config)

        # 2단계: config 객체
        if config:
            config_dict = {
                "api_key": config.api_key,
                "api_secret": config.api_secret,
                "acc_no": config.acc_no,
                "token_storage_type": config.token_storage_type,
                "redis_url": config.redis_url,
                "redis_password": config.redis_password,
                "token_file": str(config.token_file) if config.token_file else None,
            }
            self._merge_config(result, config_dict)

        # 1단계: 생성자 파라미터 (최고 우선순위)
        constructor_params = {
            "api_key": api_key,
            "api_secret": api_secret,
            "acc_no": acc_no,
        }
        self._merge_config(result, constructor_params)

        return result

    def _merge_config(self, target: dict, source: dict) -> None:
        """source의 non-None 값으로 target을 업데이트

        Args:
            target: 업데이트할 대상 딕셔너리
            source: 소스 딕셔너리
        """
        for key, value in source.items():
            if value is not None and key in target:
                target[key] = value

    def _load_default_config_file(self) -> dict | None:
        """기본 경로에서 config 파일 로드 시도

        DEFAULT_CONFIG_PATHS에 정의된 경로들을 순서대로 확인하여
        첫 번째 존재하는 파일을 로드합니다.

        Returns:
            dict | None: 로드된 설정 또는 None (파일 없음)
        """
        for path in self.DEFAULT_CONFIG_PATHS:
            expanded_path = Path(path).expanduser()
            if expanded_path.exists():
                return self._load_config_file(expanded_path)
        return None

    def _load_config_file(self, path: "str | Path") -> dict | None:
        """설정 파일 로드 (YAML 형식 지원)

        Args:
            path: 설정 파일 경로

        Returns:
            dict | None: 로드된 설정 또는 None (실패 시)
        """
        try:
            import yaml
        except ImportError:
            # pyyaml이 설치되지 않은 경우
            return None

        path = Path(path).expanduser()
        if not path.exists():
            return None

        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                return None

            # YAML 키를 내부 키로 매핑
            return {
                "api_key": data.get("api_key"),
                "api_secret": data.get("api_secret"),
                "acc_no": data.get("acc_no"),
                "token_storage_type": data.get("token_storage_type"),
                "redis_url": data.get("redis_url"),
                "redis_password": data.get("redis_password"),
                "token_file": data.get("token_file"),
            }
        except Exception:
            return None

    def _load_from_env(self) -> dict:
        """환경 변수에서 설정 로드

        Returns:
            dict: 환경 변수에서 로드된 설정
        """
        return {
            "api_key": os.getenv("KOREA_INVESTMENT_API_KEY"),
            "api_secret": os.getenv("KOREA_INVESTMENT_API_SECRET"),
            "acc_no": os.getenv("KOREA_INVESTMENT_ACCOUNT_NO"),
            "token_storage_type": os.getenv("KOREA_INVESTMENT_TOKEN_STORAGE"),
            "redis_url": os.getenv("KOREA_INVESTMENT_REDIS_URL"),
            "redis_password": os.getenv("KOREA_INVESTMENT_REDIS_PASSWORD"),
            "token_file": os.getenv("KOREA_INVESTMENT_TOKEN_FILE"),
        }

    def _create_token_storage(self) -> TokenStorage:
        """설정 기반 토큰 저장소 생성

        _resolved_config에서 설정을 읽어 토큰 저장소를 생성합니다.
        설정이 없으면 환경 변수에서 읽습니다.

        Returns:
            TokenStorage: 설정된 토큰 저장소 인스턴스

        Raises:
            ValueError: 지원하지 않는 저장소 타입일 때
        """
        # _resolved_config가 있으면 사용, 없으면 환경 변수에서 읽기
        if hasattr(self, "_resolved_config") and self._resolved_config:
            storage_type = self._resolved_config.get("token_storage_type") or "file"
            redis_url = self._resolved_config.get("redis_url") or "redis://localhost:6379/0"
            redis_password = self._resolved_config.get("redis_password")
            token_file = self._resolved_config.get("token_file")
        else:
            # 하위 호환성: 환경 변수에서 읽기
            storage_type = os.getenv("KOREA_INVESTMENT_TOKEN_STORAGE", "file")
            redis_url = os.getenv("KOREA_INVESTMENT_REDIS_URL", "redis://localhost:6379/0")
            redis_password = os.getenv("KOREA_INVESTMENT_REDIS_PASSWORD")
            token_file = os.getenv("KOREA_INVESTMENT_TOKEN_FILE")

        storage_type = storage_type.lower()

        if storage_type == "file":
            file_path = None
            if token_file:
                file_path = Path(token_file).expanduser()
            return FileTokenStorage(file_path)

        elif storage_type == "redis":
            return RedisTokenStorage(redis_url, password=redis_password)

        else:
            raise ValueError(
                f"지원하지 않는 저장소 타입: {storage_type}\n"
                f"'file' 또는 'redis'만 지원됩니다."
            )

    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 - 리소스 정리"""
        self.shutdown()
        return False  # 예외를 전파

    def __handle_rate_limit_error(self, retry_count: int):
        """Rate limit 에러 처리 (Exponential Backoff)
        
        DEPRECATED: Enhanced Backoff Strategy로 대체됨
        이 메서드는 하위 호환성을 위해 유지되며, 향후 제거될 예정입니다.
        
        Args:
            retry_count: 재시도 횟수 (0부터 시작)
        """
        # Exponential backoff: 1, 2, 4, 8, 16, 32초
        wait_time = min(2 ** retry_count, 32)
        
        # Jitter 추가 (0~10% 랜덤 추가 대기)
        jitter = random.uniform(0, 0.1 * wait_time)
        total_wait = wait_time + jitter
        
        print(f"Rate limit 초과. {total_wait:.2f}초 대기 후 재시도... (시도 {retry_count + 1}/5)")
        time.sleep(total_wait)

    def shutdown(self):
        """리소스 정리"""
        # 컨텍스트 매니저 종료 시 호출됨
        # 향후 필요한 정리 작업이 있으면 여기에 추가
        pass


    def issue_access_token(self):
        """OAuth인증/접근토큰발급
        """
        path = "oauth2/tokenP"
        url = f"{self.base_url}/{path}"
        headers = {"content-type": "application/json"}
        data = {
            "grant_type": "client_credentials",
            "appkey": self.api_key,
            "appsecret": self.api_secret
        }

        resp = requests.post(url, headers=headers, json=data)
        resp_data = resp.json()
        self.access_token = f'Bearer {resp_data["access_token"]}'

        # 'expires_in' has no reference time and causes trouble:
        # The server thinks I'm expired but my token.dat looks still valid!
        # Hence, we use 'access_token_token_expired' here.
        # This error is quite big. I've seen 4000 seconds.
        timezone = ZoneInfo('Asia/Seoul')
        dt = datetime.strptime(resp_data['access_token_token_expired'], '%Y-%m-%d %H:%M:%S').replace(
            tzinfo=timezone)
        resp_data['timestamp'] = int(dt.timestamp())
        resp_data['api_key'] = self.api_key
        resp_data['api_secret'] = self.api_secret

        # 토큰 저장소에 저장
        self.token_storage.save_token(resp_data)

    def check_access_token(self) -> bool:
        """check access token

        Returns:
            Bool: True: token is valid, False: token is not valid
        """
        return self.token_storage.check_token_valid(self.api_key, self.api_secret)

    def load_access_token(self):
        """load access token
        """
        token_data = self.token_storage.load_token(self.api_key, self.api_secret)
        if token_data:
            self.access_token = f'Bearer {token_data["access_token"]}'

    def issue_hashkey(self, data: dict):
        """해쉬키 발급
        Args:
            data (dict): POST 요청 데이터
        Returns:
            _type_: _description_
        """
        path = "uapi/hashkey"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        haskkey = resp.json()["HASH"]
        return haskkey

    def fetch_price(self, symbol: str, market: str = "KR") -> dict:
        """국내주식시세/주식현재가 시세
           해외주식현재가/해외주식 현재체결가

        Args:
            symbol (str): 종목코드
            market (str): 시장 코드 ("KR", "KRX", "US" 등)

        Returns:
            dict: API 응답 데이터
        """

        if market == "KR" or market == "KRX":
            stock_info = self.fetch_stock_info(symbol, market)
            symbol_type = self.get_symbol_type(stock_info)
            if symbol_type == "ETF":
                resp_json = self.fetch_etf_domestic_price("J", symbol)
            else:
                resp_json = self.fetch_domestic_price("J", symbol)
        elif market == "US":
            # 기존: resp_json = self.fetch_oversea_price(symbol)  # 메서드 없음
            # 개선: 이미 구현된 fetch_price_detail_oversea() 활용
            resp_json = self.fetch_price_detail_oversea(symbol, market)
            # 참고: 이 API는 현재가 외에도 PER, PBR, EPS, BPS 등 추가 정보 제공
        else:
            raise ValueError("Unsupported market type")

        return resp_json

    def get_symbol_type(self, symbol_info):
        # API 오류 응답 처리
        if symbol_info.get('rt_cd') != '0' or 'output' not in symbol_info:
            return 'Stock'  # 기본값으로 주식 타입 반환

        symbol_type = symbol_info['output']['prdt_clsf_name']
        if symbol_type == '주권' or symbol_type == '상장REITS' or symbol_type == '사회간접자본투융자회사':
            return 'Stock'
        elif symbol_type == 'ETF':
            return 'ETF'

        return "Unknown"

    def fetch_etf_domestic_price(self, market_code: str, symbol: str) -> dict:
        """ETF 주식현재가시세

        Args:
            market_code (str): 시장 분류코드 (예: "J")
            symbol (str): 종목코드
        Returns:
            dict: API 응답 데이터
        """
        path = "uapi/domestic-stock/v1/quotations/inquire-price"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "FHPST02400000"
        }
        params = {
            "fid_cond_mrkt_div_code": market_code,
            "fid_input_iscd": symbol
        }
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()

    def fetch_domestic_price(self, market_code: str, symbol: str) -> dict:
        """국내 주식현재가시세

        Args:
            market_code (str): 시장 분류코드 (예: "J")
            symbol (str): 종목코드
        Returns:
            dict: API 응답 데이터
        """
        path = "uapi/domestic-stock/v1/quotations/inquire-price"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "FHKST01010100"
        }
        params = {
            "fid_cond_mrkt_div_code": market_code,
            "fid_input_iscd": symbol
        }
        resp = requests.get(url, headers=headers, params=params)
        return resp.json()

    def fetch_kospi_symbols(
        self,
        ttl_hours: int = 168,
        force_download: bool = False
    ) -> pd.DataFrame:
        """코스피 종목 코드

        실제 필요한 종목: ST, RT, EF, IF

        ST	주권
        MF	증권투자회사
        RT	부동산투자회사
        SC	선박투자회사
        IF	사회간접자본투융자회사
        DR	주식예탁증서
        EW	ELW
        EF	ETF
        SW	신주인수권증권
        SR	신주인수권증서
        BC	수익증권
        FE	해외ETF
        FS	외국주권

        Args:
            ttl_hours (int): 캐시 유효 시간 (기본 1주일 = 168시간)
            force_download (bool): 강제 다운로드 여부

        Returns:
            DataFrame: 코스피 종목 정보
        """
        base_dir = os.getcwd()
        file_name = "kospi_code.mst.zip"
        url = "https://new.real.download.dws.co.kr/common/master/" + file_name

        self.download_master_file(base_dir, file_name, url, ttl_hours, force_download)
        df = self.parse_kospi_master(base_dir)
        return df

    def fetch_kosdaq_symbols(
        self,
        ttl_hours: int = 168,
        force_download: bool = False
    ) -> pd.DataFrame:
        """코스닥 종목 코드

        Args:
            ttl_hours (int): 캐시 유효 시간 (기본 1주일 = 168시간)
            force_download (bool): 강제 다운로드 여부

        Returns:
            DataFrame: 코스닥 종목 정보
        """
        base_dir = os.getcwd()
        file_name = "kosdaq_code.mst.zip"
        url = "https://new.real.download.dws.co.kr/common/master/" + file_name

        self.download_master_file(base_dir, file_name, url, ttl_hours, force_download)
        df = self.parse_kosdaq_master(base_dir)
        return df

    def fetch_symbols(self):
        """fetch symbols from the exchange

        Returns:
            pd.DataFrame: pandas dataframe
        """
        if self.exchange == "서울":  # todo: exchange는 제거 예정
            df = self.fetch_kospi_symbols()
            kospi_df = df[['단축코드', '한글명', '그룹코드']].copy()
            kospi_df['시장'] = '코스피'

            df = self.fetch_kosdaq_symbols()
            kosdaq_df = df[['단축코드', '한글명', '그룹코드']].copy()
            kosdaq_df['시장'] = '코스닥'

            df = pd.concat([kospi_df, kosdaq_df], axis=0)

        return df

    def _should_download(
        self,
        file_path: Path,
        ttl_hours: int,
        force: bool
    ) -> bool:
        """다운로드 필요 여부 판단

        Args:
            file_path: ZIP 파일 경로
            ttl_hours: 캐시 유효 시간
            force: 강제 다운로드 여부

        Returns:
            bool: True=다운로드 필요, False=캐시 사용
        """
        if force:
            return True

        if not file_path.exists():
            return True

        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        age = datetime.now() - mtime

        if age.total_seconds() > ttl_hours * 3600:
            logger.debug(f"캐시 만료: {file_path} (age={age})")
            return True

        return False

    def download_master_file(
        self,
        base_dir: str,
        file_name: str,
        url: str,
        ttl_hours: int = 168,
        force_download: bool = False
    ) -> bool:
        """master 파일 다운로드 (캐싱 지원)

        Args:
            base_dir (str): 저장 디렉토리
            file_name (str): 파일명 (예: "kospi_code.mst.zip")
            url (str): 다운로드 URL
            ttl_hours (int): 캐시 유효 시간 (기본 1주일 = 168시간)
            force_download (bool): 강제 다운로드 여부

        Returns:
            bool: True=다운로드됨, False=캐시 사용
        """
        zip_path = Path(base_dir) / file_name

        # 다운로드 필요 여부 확인
        if not self._should_download(zip_path, ttl_hours, force_download):
            mtime = datetime.fromtimestamp(zip_path.stat().st_mtime)
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            logger.info(f"캐시 사용: {zip_path} (age: {age_hours:.1f}h, ttl: {ttl_hours}h)")
            return False

        # 다운로드
        logger.info(f"다운로드 중: {url} -> {zip_path}")
        resp = requests.get(url)
        resp.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(resp.content)

        # 압축 해제
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(base_dir)

        return True

    def parse_kospi_master(self, base_dir: str):
        """parse kospi master file

        Args:
            base_dir (str): directory where kospi code exists

        Returns:
            _type_: _description_
        """
        file_name = base_dir + "/kospi_code.mst"
        tmp_fil1 = base_dir + "/kospi_code_part1.tmp"
        tmp_fil2 = base_dir + "/kospi_code_part2.tmp"

        wf1 = open(tmp_fil1, mode="w", encoding="cp949")
        wf2 = open(tmp_fil2, mode="w")

        with open(file_name, mode="r", encoding="cp949") as f:
            for row in f:
                rf1 = row[0:len(row) - 228]
                rf1_1 = rf1[0:9].rstrip()
                rf1_2 = rf1[9:21].rstrip()
                rf1_3 = rf1[21:].strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')
                rf2 = row[-228:]
                wf2.write(rf2)

        wf1.close()
        wf2.close()

        part1_columns = ['단축코드', '표준코드', '한글명']
        df1 = pd.read_csv(tmp_fil1, header=None, encoding='cp949', names=part1_columns)

        field_specs = [
            2, 1, 4, 4, 4,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 1, 1, 1, 1,
            1, 9, 5, 5, 1,
            1, 1, 2, 1, 1,
            1, 2, 2, 2, 3,
            1, 3, 12, 12, 8,
            15, 21, 2, 7, 1,
            1, 1, 1, 1, 9,
            9, 9, 5, 9, 8,
            9, 3, 1, 1, 1
        ]

        part2_columns = [
            '그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',
            '제조업', '저유동성', '지배구조지수종목', 'KOSPI200섹터업종', 'KOSPI100',
            'KOSPI50', 'KRX', 'ETP', 'ELW발행', 'KRX100',
            'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',
            'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',
            'Non1', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',
            'SRI', '기준가', '매매수량단위', '시간외수량단위', '거래정지',
            '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',
            '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',
            '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',
            '상장주수', '자본금', '결산월', '공모가', '우선주',
            '공매도과열', '이상급등', 'KRX300', 'KOSPI', '매출액',
            '영업이익', '경상이익', '당기순이익', 'ROE', '기준년월',
            '시가총액', '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
        ]

        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)
        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        # clean temporary file and dataframe
        del (df1)
        del (df2)
        os.remove(tmp_fil1)
        os.remove(tmp_fil2)
        return df

    def parse_kosdaq_master(self, base_dir: str):
        """parse kosdaq master file

        Args:
            base_dir (str): directory where kosdaq code exists

        Returns:
            _type_: _description_
        """
        file_name = base_dir + "/kosdaq_code.mst"
        tmp_fil1 = base_dir + "/kosdaq_code_part1.tmp"
        tmp_fil2 = base_dir + "/kosdaq_code_part2.tmp"

        wf1 = open(tmp_fil1, mode="w", encoding="cp949")
        wf2 = open(tmp_fil2, mode="w")
        with open(file_name, mode="r", encoding="cp949") as f:
            for row in f:
                rf1 = row[0:len(row) - 222]
                rf1_1 = rf1[0:9].rstrip()
                rf1_2 = rf1[9:21].rstrip()
                rf1_3 = rf1[21:].strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + '\n')

                rf2 = row[-222:]
                wf2.write(rf2)

        wf1.close()
        wf2.close()

        part1_columns = ['단축코드', '표준코드', '한글명']
        df1 = pd.read_csv(tmp_fil1, header=None, encoding="cp949", names=part1_columns)

        field_specs = [
            2, 1, 4, 4, 4,  # line 20
            1, 1, 1, 1, 1,  # line 27
            1, 1, 1, 1, 1,  # line 32
            1, 1, 1, 1, 1,  # line 38
            1, 1, 1, 1, 1,  # line 43
            1, 9, 5, 5, 1,  # line 48
            1, 1, 2, 1, 1,  # line 54
            1, 2, 2, 2, 3,  # line 64
            1, 3, 12, 12, 8,  # line 69
            15, 21, 2, 7, 1,  # line 75
            1, 1, 1, 9, 9,  # line 80
            9, 5, 9, 8, 9,  # line 85
            3, 1, 1, 1
        ]

        part2_columns = [
            '그룹코드', '시가총액규모', '지수업종대분류', '지수업종중분류', '지수업종소분류',  # line 20
            '벤처기업', '저유동성', 'KRX', 'ETP', 'KRX100',  # line 27
            'KRX자동차', 'KRX반도체', 'KRX바이오', 'KRX은행', 'SPAC',  # line 32
            'KRX에너지화학', 'KRX철강', '단기과열', 'KRX미디어통신', 'KRX건설',  # line 38
            '투자주의', 'KRX증권', 'KRX선박', 'KRX섹터_보험', 'KRX섹터_운송',  # line 43
            'KOSDAQ150', '기준가', '매매수량단위', '시간외수량단위', '거래정지',  # line 48
            '정리매매', '관리종목', '시장경고', '경고예고', '불성실공시',  # line 54
            '우회상장', '락구분', '액면변경', '증자구분', '증거금비율',  # line 64
            '신용가능', '신용기간', '전일거래량', '액면가', '상장일자',  # line 69
            '상장주수', '자본금', '결산월', '공모가', '우선주',  # line 75
            '공매도과열', '이상급등', 'KRX300', '매출액', '영업이익',  # line 80
            '경상이익', '당기순이익', 'ROE', '기준년월', '시가총액',  # line 85
            '그룹사코드', '회사신용한도초과', '담보대출가능', '대주가능'
        ]

        df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns)
        df = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)

        # clean temporary file and dataframe
        del (df1)
        del (df2)
        os.remove(tmp_fil1)
        os.remove(tmp_fil2)
        return df

    def fetch_price_detail_oversea(self, symbol: str, market: str = "KR"):
        """해외주식 현재가상세

        Args:
            symbol (str): symbol
        """
        path = "/uapi/overseas-price/v1/quotations/price-detail"
        url = f"{self.base_url}/{path}"

        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "HHDFS76200200"
        }

        if market == "KR" or market == "KRX":
            # API 호출해서 실제로 확인은 못해봄, overasea 이라서 안될 것으로 판단해서 조건문 추가함
            raise ValueError("Market cannot be either 'KR' or 'KRX'.")

        for exchange_code in ["NYS", "NAS", "AMS", "BAY", "BAQ", "BAA"]:
            print("exchange_code", exchange_code)
            params = {
                "AUTH": "",
                "EXCD": exchange_code,
                "SYMB": symbol
            }
            resp = requests.get(url, headers=headers, params=params)
            resp_json = resp.json()
            if resp_json['rt_cd'] != API_RETURN_CODE["SUCCESS"] or resp_json['output']['rsym'] == '':
                continue

            return resp_json
        
        # 모든 거래소에서 실패한 경우
        raise ValueError(f"Unable to fetch price for symbol '{symbol}' in any {market} exchange")

    def fetch_stock_info(self, symbol: str, market: str = "KR"):
        path = "uapi/domestic-stock/v1/quotations/search-info"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "CTPF1604R"
        }

        for market_code in MARKET_TYPE_MAP[market]:
            try:
                params = {
                    "PDNO": symbol,
                    "PRDT_TYPE_CD": market_code
                }
                resp = requests.get(url, headers=headers, params=params)
                resp_json = resp.json()

                if resp_json['rt_cd'] == API_RETURN_CODE['NO_DATA']:
                    continue
                return resp_json

            except Exception as e:
                print(e)
                if resp_json['rt_cd'] != API_RETURN_CODE['SUCCESS']:
                    continue
                raise e

    def fetch_search_stock_info(self, symbol: str, market: str = "KR"):
        """
        국내 주식만 제공하는 API이다
        """
        path = "uapi/domestic-stock/v1/quotations/search-stock-info"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "CTPF1002R"
        }

        if market != "KR" and market != "KRX":
            raise ValueError("Market must be either 'KR' or 'KRX'.")

        for market_ in MARKET_TYPE_MAP[market]:
            try:
                params = {
                    "PDNO": symbol,
                    "PRDT_TYPE_CD": market_
                }
                resp = requests.get(url, headers=headers, params=params)
                resp_json = resp.json()

                if resp_json['rt_cd'] == API_RETURN_CODE['NO_DATA']:
                    continue
                return resp_json

            except Exception as e:
                print(e)
                if resp_json['rt_cd'] != API_RETURN_CODE['SUCCESS']:
                    continue
                raise e

    # IPO 관련 헬퍼 함수들
    def _validate_date_format(self, date_str: str) -> bool:
        """날짜 형식 검증 (YYYYMMDD)"""
        if len(date_str) != 8:
            return False
        try:
            datetime.strptime(date_str, "%Y%m%d")
            return True
        except ValueError:
            return False

    def _validate_date_range(self, from_date: str, to_date: str) -> bool:
        """날짜 범위 유효성 검증"""
        try:
            start = datetime.strptime(from_date, "%Y%m%d")
            end = datetime.strptime(to_date, "%Y%m%d")
            return start <= end
        except ValueError:
            return False

    @staticmethod
    def parse_ipo_date_range(date_range_str: str) -> tuple:
        """청약기간 문자열 파싱
        
        Args:
            date_range_str: "2024.01.15~2024.01.16" 형식의 문자열
            
        Returns:
            tuple: (시작일 datetime, 종료일 datetime) 또는 (None, None)
        """
        if not date_range_str:
            return (None, None)
        
        # "2024.01.15~2024.01.16" 형식 파싱
        pattern = r'(\d{4}\.\d{2}\.\d{2})~(\d{4}\.\d{2}\.\d{2})'
        match = re.match(pattern, date_range_str)
        
        if match:
            try:
                start_str = match.group(1).replace('.', '')
                end_str = match.group(2).replace('.', '')
                start_date = datetime.strptime(start_str, "%Y%m%d")
                end_date = datetime.strptime(end_str, "%Y%m%d")
                return (start_date, end_date)
            except ValueError:
                pass
        
        return (None, None)

    @staticmethod
    def format_ipo_date(date_str: str) -> str:
        """날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)"""
        if len(date_str) == 8:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        elif '.' in date_str:
            return date_str.replace('.', '-')
        return date_str

    @staticmethod
    def calculate_ipo_d_day(ipo_date_str: str) -> int:
        """청약일까지 남은 일수 계산"""
        if '~' in ipo_date_str:
            start_date, _ = KoreaInvestment.parse_ipo_date_range(ipo_date_str)
            if start_date:
                today = datetime.now()
                return (start_date - today).days
        return -999

    @staticmethod
    def get_ipo_status(subscr_dt: str) -> str:
        """청약 상태 판단
        
        Returns:
            str: "예정", "진행중", "마감", "알수없음"
        """
        start_date, end_date = KoreaInvestment.parse_ipo_date_range(subscr_dt)
        if not start_date or not end_date:
            return "알수없음"
        
        today = datetime.now()
        if today < start_date:
            return "예정"
        elif start_date <= today <= end_date:
            return "진행중"
        else:
            return "마감"

    @staticmethod
    def format_number(num_str: str) -> str:
        """숫자 문자열에 천단위 콤마 추가"""
        try:
            return f"{int(num_str):,}"
        except (ValueError, TypeError):
            return num_str

    # IPO Schedule API
    def fetch_ipo_schedule(self, from_date: str = None, to_date: str = None, symbol: str = "") -> dict:
        """공모주 청약 일정 조회
        
        예탁원정보(공모주청약일정) API를 통해 공모주 정보를 조회합니다.
        한국투자 HTS(eFriend Plus) > [0667] 공모주청약 화면과 동일한 기능입니다.
        
        Args:
            from_date: 조회 시작일 (YYYYMMDD, 기본값: 오늘)
            to_date: 조회 종료일 (YYYYMMDD, 기본값: 30일 후)
            symbol: 종목코드 (선택, 공백시 전체 조회)
            
        Returns:
            dict: 공모주 청약 일정 정보
                {
                    "rt_cd": "0",  # 성공여부
                    "msg_cd": "응답코드",
                    "msg1": "응답메시지",
                    "output1": [
                        {
                            "record_date": "기준일",
                            "sht_cd": "종목코드",
                            "isin_name": "종목명",
                            "fix_subscr_pri": "공모가",
                            "face_value": "액면가",
                            "subscr_dt": "청약기간",  # "2024.01.15~2024.01.16"
                            "pay_dt": "납입일",
                            "refund_dt": "환불일",
                            "list_dt": "상장/등록일",
                            "lead_mgr": "주간사",
                            "pub_bf_cap": "공모전자본금",
                            "pub_af_cap": "공모후자본금",
                            "assign_stk_qty": "당사배정물량"
                        }
                    ]
                }
                
        Raises:
            ValueError: 날짜 형식 오류시

        Note:
            - 예탁원에서 제공한 자료이므로 정보용으로만 사용하시기 바랍니다.
            - 실제 청약시에는 반드시 공식 공모주 청약 공고문을 확인하세요.
            
        Examples:
            >>> # 전체 공모주 조회 (오늘부터 30일)
            >>> ipos = broker.fetch_ipo_schedule()
            
            >>> # 특정 기간 조회
            >>> ipos = broker.fetch_ipo_schedule(
            ...     from_date="20240101",
            ...     to_date="20240131"
            ... )
            
            >>> # 특정 종목 조회
            >>> ipo = broker.fetch_ipo_schedule(symbol="123456")
        """
        # 날짜 기본값 설정
        if not from_date:
            from_date = datetime.now().strftime("%Y%m%d")
        if not to_date:
            to_date = (datetime.now() + timedelta(days=30)).strftime("%Y%m%d")
        
        # 날짜 유효성 검증
        if not self._validate_date_format(from_date) or not self._validate_date_format(to_date):
            raise ValueError("날짜 형식은 YYYYMMDD 이어야 합니다.")
        
        if not self._validate_date_range(from_date, to_date):
            raise ValueError("시작일은 종료일보다 이전이어야 합니다.")
        
        path = "uapi/domestic-stock/v1/ksdinfo/pub-offer"
        url = f"{self.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "authorization": self.access_token,
            "appKey": self.api_key,
            "appSecret": self.api_secret,
            "tr_id": "HHKDB669108C0",
            "custtype": "P"  # 개인
        }
        
        params = {
            "SHT_CD": symbol,
            "CTS": "",
            "F_DT": from_date,
            "T_DT": to_date
        }
        
        resp = requests.get(url, headers=headers, params=params)
        resp_json = resp.json()
        
        # 에러 처리
        if resp_json.get('rt_cd') != '0':
            logger.error(f"공모주 조회 실패: {resp_json.get('msg1', 'Unknown error')}")
            return resp_json
        
        return resp_json


# RateLimiter 클래스는 enhanced_rate_limiter.py로 이동됨


if __name__ == "__main__":
    with open("../koreainvestment.key", encoding='utf-8') as key_file:
        lines = key_file.readlines()

    key = lines[0].strip()
    secret = lines[1].strip()
    acc_no = lines[2].strip()

    broker = KoreaInvestment(
        api_key=key,
        api_secret=secret,
        acc_no=acc_no,
        # exchange="나스닥" # todo: exchange는 제거 예정
    )

    balance = broker.fetch_present_balance()
    print(balance)

    # result = broker.fetch_oversea_day_night()
    # pprint.pprint(result)

    # minute1_ohlcv = broker.fetch_today_1m_ohlcv("005930")
    # pprint.pprint(minute1_ohlcv)

    # broker = KoreaInvestment(key, secret, exchange="나스닥")
    # import pprint
    # resp = broker.fetch_price("005930")
    # pprint.pprint(resp)
    #
    # b = broker.fetch_balance("63398082")
    # pprint.pprint(b)
    #
    # resp = broker.create_market_buy_order("63398082", "005930", 10)
    # pprint.pprint(resp)
    #
    # resp = broker.cancel_order("63398082", "91252", "0000117057", "00", 60000, 5, "Y")
    # print(resp)
    #
    # resp = broker.create_limit_buy_order("63398082", "TQQQ", 35, 1)
    # print(resp)



    # import pprint
    # broker = KoreaInvestment(key, secret, exchange="나스닥")
    # resp_ohlcv = broker.fetch_ohlcv("TSLA", '1d', to="")
    # print(len(resp_ohlcv['output2']))
    # pprint.pprint(resp_ohlcv['output2'][0])
    # pprint.pprint(resp_ohlcv['output2'][-1])
