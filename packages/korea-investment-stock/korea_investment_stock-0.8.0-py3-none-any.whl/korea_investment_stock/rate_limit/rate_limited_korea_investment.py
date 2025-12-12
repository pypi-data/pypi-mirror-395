from typing import Dict, Any
from korea_investment_stock import KoreaInvestment
from .rate_limiter import RateLimiter


class RateLimitedKoreaInvestment:
    """
    속도 제한이 적용된 KoreaInvestment 래퍼

    기존 KoreaInvestment 객체를 래핑하여 모든 API 호출에
    자동으로 속도 제한을 적용합니다.

    Example:
        >>> broker = KoreaInvestment(api_key, api_secret, acc_no)
        >>> rate_limited = RateLimitedKoreaInvestment(broker, calls_per_second=15)
        >>> result = rate_limited.fetch_price("005930", "KR")
    """

    def __init__(
        self,
        broker: KoreaInvestment,
        calls_per_second: float = 15.0
    ):
        """
        Args:
            broker: 기존 KoreaInvestment 인스턴스
            calls_per_second: 속도 제한 (기본값: 15회/초)
        """
        self._broker = broker
        self._rate_limiter = RateLimiter(calls_per_second)

    # === Context Manager 지원 ===
    def __enter__(self):
        """Context manager 진입"""
        self._broker.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager 종료"""
        return self._broker.__exit__(exc_type, exc_val, exc_tb)

    # === 래핑된 API 메서드 (속도 제한 적용) ===

    def fetch_price(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 가격 조회

        Args:
            symbol: 종목 코드
            market: 시장 구분 ("KR" 또는 "US")

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_price(symbol, market)

    def fetch_domestic_price(self, market_code: str, symbol: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 국내 주식 가격 조회

        Args:
            market_code: 시장 코드
            symbol: 종목 코드

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_domestic_price(market_code, symbol)

    def fetch_etf_domestic_price(self, market_code: str, symbol: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 ETF 가격 조회

        Args:
            market_code: 시장 코드
            symbol: 종목 코드

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_etf_domestic_price(market_code, symbol)

    def fetch_price_detail_oversea(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 해외 주식 가격 조회

        Args:
            symbol: 종목 코드
            market: 시장 구분

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_price_detail_oversea(symbol, market)

    def fetch_stock_info(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 종목 정보 조회

        Args:
            symbol: 종목 코드
            market: 시장 구분 ("KR" 또는 "US")

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_stock_info(symbol, market)

    def fetch_search_stock_info(self, symbol: str, market: str) -> Dict[str, Any]:
        """
        속도 제한이 적용된 종목 검색

        Args:
            symbol: 종목 코드
            market: 시장 구분 ("KR" 또는 "US")

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_search_stock_info(symbol, market)

    def fetch_kospi_symbols(self) -> Dict[str, Any]:
        """
        속도 제한이 적용된 KOSPI 종목 리스트 조회

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_kospi_symbols()

    def fetch_kosdaq_symbols(self) -> Dict[str, Any]:
        """
        속도 제한이 적용된 KOSDAQ 종목 리스트 조회

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_kosdaq_symbols()

    def fetch_ipo_schedule(self) -> Dict[str, Any]:
        """
        속도 제한이 적용된 IPO 일정 조회

        Returns:
            API 응답 딕셔너리
        """
        self._rate_limiter.wait()
        return self._broker.fetch_ipo_schedule()

    # === IPO 헬퍼 메서드들 (9개) ===

    def get_ipo_schedule_details(self, *args, **kwargs):
        """속도 제한이 적용된 IPO 일정 상세 조회"""
        self._rate_limiter.wait()
        return self._broker.get_ipo_schedule_details(*args, **kwargs)

    def get_upcoming_ipos(self, *args, **kwargs):
        """속도 제한이 적용된 예정된 IPO 조회"""
        self._rate_limiter.wait()
        return self._broker.get_upcoming_ipos(*args, **kwargs)

    def get_recent_ipos(self, *args, **kwargs):
        """속도 제한이 적용된 최근 IPO 조회"""
        self._rate_limiter.wait()
        return self._broker.get_recent_ipos(*args, **kwargs)

    def get_ipo_by_company(self, *args, **kwargs):
        """속도 제한이 적용된 회사별 IPO 조회"""
        self._rate_limiter.wait()
        return self._broker.get_ipo_by_company(*args, **kwargs)

    def get_ipo_by_date_range(self, *args, **kwargs):
        """속도 제한이 적용된 기간별 IPO 조회"""
        self._rate_limiter.wait()
        return self._broker.get_ipo_by_date_range(*args, **kwargs)

    def get_ipo_statistics(self, *args, **kwargs):
        """속도 제한이 적용된 IPO 통계 조회"""
        self._rate_limiter.wait()
        return self._broker.get_ipo_statistics(*args, **kwargs)

    def filter_ipos_by_market(self, *args, **kwargs):
        """속도 제한이 적용된 시장별 IPO 필터링"""
        self._rate_limiter.wait()
        return self._broker.filter_ipos_by_market(*args, **kwargs)

    def get_ipo_calendar(self, *args, **kwargs):
        """속도 제한이 적용된 IPO 캘린더 조회"""
        self._rate_limiter.wait()
        return self._broker.get_ipo_calendar(*args, **kwargs)

    def format_ipo_schedule(self, *args, **kwargs):
        """속도 제한이 적용된 IPO 일정 포맷"""
        self._rate_limiter.wait()
        return self._broker.format_ipo_schedule(*args, **kwargs)

    # === 유틸리티 메서드 ===

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """
        속도 제한 통계 조회

        Returns:
            {
                'calls_per_second': float,
                'min_interval': float,
                'last_call': float,
                'total_calls': int
            }
        """
        return self._rate_limiter.get_stats()

    def adjust_rate_limit(self, calls_per_second: float) -> None:
        """
        런타임 중 속도 제한 동적 조정

        Args:
            calls_per_second: 새로운 초당 호출 수

        Raises:
            ValueError: calls_per_second가 0 이하인 경우
        """
        self._rate_limiter.adjust_rate_limit(calls_per_second)
