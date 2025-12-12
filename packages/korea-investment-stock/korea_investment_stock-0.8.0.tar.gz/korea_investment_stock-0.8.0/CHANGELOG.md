# CHANGELOG

## [Unreleased]

### Added

#### Hybrid Configuration System (v1.1.0) (#76)

**5단계 설정 우선순위 시스템**:

1. 생성자 파라미터 (최고 우선순위)
2. `config` 객체
3. `config_file` 파라미터
4. 환경 변수
5. 기본 config 파일 (`~/.config/kis/config.yaml`)

**새로운 파라미터**:
```python
broker = KoreaInvestment(
    config=Config.from_yaml("config.yaml"),  # Config 객체 주입
    config_file="./my_config.yaml",          # YAML 파일 경로
)
```

**기본 config 파일 자동 탐색**:
```yaml
# ~/.config/kis/config.yaml
api_key: your-api-key
api_secret: your-api-secret
acc_no: "12345678-01"
```

**혼합 사용 (부분 override)**:
```python
config = Config.from_yaml("~/.config/kis/config.yaml")
broker = KoreaInvestment(
    config=config,
    api_key="override-key"  # config보다 우선
)
```

**하위 호환성**: 기존 코드 100% 호환
```python
# 기존 방식 모두 동작
broker = KoreaInvestment(api_key, api_secret, acc_no)  # 생성자 파라미터
broker = KoreaInvestment()  # 환경 변수 자동 감지
```

### Changed
- **Project Structure**: Reorganized package into feature-based modules (#52)
  - Created `cache/` module for caching functionality
  - Created `token_storage/` module for token storage implementations
  - Moved test files to co-locate with implementation files (co-located tests)
  - Removed `tests/` directory in favor of feature-specific test files
  - All existing import paths remain compatible (backward compatible)
  - Updated version to 0.7.0

## [0.8.0] - 2025-01-XX (Breaking Changes) ⚠️

### ⚠️ BREAKING CHANGES

#### Mock 모드 완전 제거 (#55)

**제거된 기능**: 모의투자 서버 지원 (`mock` 파라미터)

**변경 사항**:

1. **생성자 시그니처 변경**
```python
# v0.7.x (Before)
broker = KoreaInvestment(api_key, api_secret, acc_no, mock=True)

# v0.8.0 (After)
broker = KoreaInvestment(api_key, api_secret, acc_no)
```

2. **제거된 메서드**
- `set_base_url(mock: bool)` 메서드 제거
- 실전 서버 URL 고정: `https://openapi.koreainvestment.com:9443`

3. **제거된 검증**
- `fetch_ipo_schedule()`: 모의투자 검증 로직 제거

**마이그레이션 가이드**:
```python
# Before (v0.7.x)
broker = KoreaInvestment(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    acc_no="12345678-01",
    mock=True  # 또는 mock=False
)

# After (v0.8.0)
broker = KoreaInvestment(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    acc_no="12345678-01"
)
```

**주의사항**:
- ⚠️ v0.8.0부터는 **실전 계좌만 지원**됩니다
- ⚠️ 테스트 환경이 필요한 경우 `unittest.mock` 사용 권장

**단위 테스트 예제**:
```python
from unittest.mock import patch

@patch('korea_investment_stock.requests.get')
def test_fetch_price(mock_get):
    mock_get.return_value.json.return_value = {
        'rt_cd': '0',
        'output1': {'stck_prpr': '70000'}
    }
    broker = KoreaInvestment(api_key, api_secret, acc_no)
    result = broker.fetch_price("005930", "KR")
    assert result['output1']['stck_prpr'] == '70000'
```

### Added

#### API Rate Limiting (#67)

**New Feature**: Automatic rate limiting to manage Korea Investment API's 20 calls/second limit.

**Components**:
- `RateLimiter`: Thread-safe rate limiter using token bucket algorithm
- `RateLimitedKoreaInvestment`: Wrapper class for automatic rate limiting

**Usage**:
```python
from korea_investment_stock import KoreaInvestment, RateLimitedKoreaInvestment

# Create base broker
broker = KoreaInvestment(api_key, api_secret, acc_no)

# Wrap with rate limiting (15 calls/second - conservative)
rate_limited = RateLimitedKoreaInvestment(broker, calls_per_second=15)

# Use as normal - rate limiting applied automatically
result = rate_limited.fetch_price("005930", "KR")
```

**Features**:
- ✅ Thread-safe using `threading.Lock`
- ✅ Default: 15 calls/second (conservative margin)
- ✅ Dynamic rate adjustment at runtime
- ✅ Statistics tracking (total_calls, min_interval)
- ✅ Context manager support
- ✅ Zero changes to existing `KoreaInvestment` class
- ✅ Works with `CachedKoreaInvestment` (recommended combination)

**Benefits**:
- Prevents API rate limit errors
- `examples/stress_test.py` now achieves 100% success (500 API calls)
- Batch processing of stocks is safe and reliable
- Opt-in design: users choose when to enable

**See Also**:
- Implementation guide: `docs/start/1_api_limit_implementation.md`
- PRD: `docs/start/1_api_limit_prd.md`
- CLAUDE.md: "API Rate Limiting" section

### Changed
- 실전 서버로 통일되어 모든 API 일관되게 지원
- 코드베이스 간소화 (mock 관련 로직 제거)
- `examples/stress_test.py` updated to use `RateLimitedKoreaInvestment`

### Removed
- `mock` 파라미터 (Breaking)
- `set_base_url()` 메서드 (Breaking)
- `self.mock` 인스턴스 변수
- IPO Schedule API의 모의투자 검증 로직

## [0.6.0] - 2025-01-19 (Breaking Changes) ⚠️

### 🎯 Major Simplification (#40)
**Philosophy Change**: Transformed from feature-rich library to **pure API wrapper**

This version removes all advanced features to focus on being a thin, reliable wrapper around the Korea Investment Securities OpenAPI. Users who need rate limiting, caching, batch processing, or monitoring should implement these features themselves according to their specific needs.

### ⚠️ BREAKING CHANGES

#### Removed Features (~6,000+ lines of code removed)
- **Rate Limiting System**: Removed EnhancedRateLimiter, BackoffStrategy, Circuit Breaker
  - Users should implement their own rate limiting if needed
- **Caching System**: Removed TTL cache, cache decorators, cache statistics
  - Users should implement their own caching strategy
- **Batch Processing**: Removed batch methods and dynamic batch controller
  - Use loops with `fetch_price()` instead of `fetch_price_list()`
- **Monitoring & Visualization**: Removed stats collection, Plotly dashboards, HTML reports
  - Users should implement their own monitoring
- **Error Recovery**: Removed automatic retry decorators and error recovery system
  - Users should handle errors according to their needs
- **Legacy Module**: Removed deprecated code and unused features

#### API Changes
- **Removed Methods**:
  - `fetch_price_list()` → Use loop with `fetch_price(symbol, market)`
  - `fetch_stock_info_list()` → Use loop with `fetch_stock_info(symbol, market)`
  - `fetch_price_list_with_batch()` → Use loop with `fetch_price()`
  - `fetch_price_list_with_dynamic_batch()` → Use loop with `fetch_price()`
  - All batch processing methods
  - All caching-related methods
  - All statistics and monitoring methods

- **Private → Public Methods** (now part of public API):
  - `__fetch_price()` → `fetch_price(symbol, market)`
  - `__fetch_stock_info()` → `fetch_stock_info(symbol, market)`
  - `__fetch_domestic_price()` → `fetch_domestic_price(market_code, symbol)`
  - `__fetch_etf_domestic_price()` → `fetch_etf_domestic_price(market_code, symbol)`
  - `__fetch_price_detail_oversea()` → `fetch_price_detail_oversea(symbol, market)`

#### Simplified Dependencies
- **Removed**: `websockets`, `pycryptodome`, `crypto`
- **Kept**: `requests`, `pandas` (minimal dependencies)

### ✅ What Remains
- ✅ Stock price queries (domestic & US)
- ✅ Stock information queries
- ✅ IPO schedule queries
- ✅ Unified interface for KR/US stocks via `fetch_price(symbol, market)`
- ✅ Basic error responses from API
- ✅ Context manager support
- ✅ Thread pool executor (basic concurrency)

### 📦 Migration Guide

#### Before (v0.5.0):
```python
# Batch query with automatic rate limiting, caching, retry
stocks = [("005930", "KR"), ("AAPL", "US")]
results = broker.fetch_price_list(stocks)
```

#### After (v0.6.0):
```python
# Simple loop - implement your own rate limiting if needed
stocks = [("005930", "KR"), ("AAPL", "US")]
results = []
for symbol, market in stocks:
    result = broker.fetch_price(symbol, market)
    results.append(result)
    # Add your own rate limiting, caching, retry logic here if needed
```

### 📈 Code Reduction
- Main file: 1,941 → 1,011 lines (48% reduction)
- Total deletion: ~6,000+ lines
- Module count: 15 → 1 (core module only)
- Test files: 18 → 4 (only integration tests remain)

### 🎯 Why This Change?
- **Simplicity**: Focus on doing one thing well - wrapping the API
- **Flexibility**: Users implement features their way
- **Maintainability**: Less code = fewer bugs
- **Transparency**: Pure wrapper with no magic

### 📚 Documentation Updates
- Updated README.md to reflect simple API wrapper approach
- Updated CLAUDE.md to remove advanced architecture details
- Updated examples to show simple usage patterns
- Added `basic_example.py` for simple use cases

## [Unreleased] - 2025-01-14

### 🚀 추가된 기능

#### 미국 주식 통합 지원 (#33) ✨
- **통합 인터페이스**: `fetch_price_list()`로 국내/미국 주식 모두 조회 가능
  - 기존: 국내 주식만 지원
  - 개선: `[("005930", "KR"), ("AAPL", "US")]` 혼합 조회 가능
- **자동 거래소 검색**: NASDAQ, NYSE, AMEX 순으로 자동 탐색
- **추가 재무 정보**: 미국 주식의 경우 PER, PBR, EPS, BPS, 52주 최고/최저가 등 제공
- **향상된 에러 처리**: 거래소별 심볼 검색 실패 시 명확한 에러 메시지
- **캐시 통합**: 미국 주식도 5분 TTL 캐시 적용으로 성능 향상

### 🔧 개선사항

#### API 메서드 캡슐화
- `fetch_etf_domestic_price()` → `__fetch_etf_domestic_price()` (private)
- `fetch_domestic_price()` → `__fetch_domestic_price()` (private)
- 사용자는 통합 인터페이스 `fetch_price_list()` 사용 권장

### ⚠️ 주의사항
- 미국 주식은 **실전투자 계정에서만** 조회 가능 (모의투자 미지원)
- 미국 주식은 실시간 무료시세 제공 (나스닥 마켓센터 기준)

## [Unreleased] - 2024-12-28

### 🏗️ 구조 개선

#### 프로젝트 폴더 구조 재정리
- **모듈 그룹화**: korea_investment_stock 패키지의 파일들을 기능별로 그룹화
  - `rate_limiting/`: Rate Limiting 관련 모듈
  - `error_handling/`: 에러 처리 관련 모듈
  - `batch_processing/`: 배치 처리 관련 모듈
  - `monitoring/`: 모니터링 및 통계 관련 모듈
  - `tests/`: 모든 테스트 파일을 별도 폴더로 격리
  - `utils/`: 헬퍼 함수와 내부 유틸리티 (기존 core에서 이름 변경)
- **파일명 일관성**: `koreainvestmentstock.py` → `korea_investment_stock.py`로 변경
- **메인 모듈 위치 변경**: Python 표준에 맞게 `korea_investment_stock.py`를 패키지 루트로 이동
- **Import 구조 개선**: 각 모듈별 `__init__.py`에서 주요 클래스/함수 export
- **하위 호환성 유지**: 공개 API는 변경 없이 내부 구조만 개선

### 🚀 추가된 기능

#### Rate Limiting 시스템 전면 개선 (#27)
- **자동 속도 제어**: Token Bucket + Sliding Window 하이브리드 방식 구현
- **에러 방지**: `EGW00201` (초당 호출 제한 초과) 에러 100% 방지
- **자동 재시도**: Rate Limit 에러 발생 시 Exponential Backoff로 자동 재시도
- **Circuit Breaker**: 연속된 실패 시 자동으로 회로 차단 및 복구
- **통계 모니터링**: 실시간 성능 통계 및 파일 저장 기능
- **배치 처리**: 대량 데이터 처리를 위한 고정/동적 배치 처리
  - `fetch_price_list_with_batch()`: 고정 크기 배치 처리
  - `fetch_price_list_with_dynamic_batch()`: 에러율 기반 자동 조정
  - 배치 내 순차적 제출로 초기 버스트 방지
  - 배치별 상세 통계 수집 및 로깅
- **동적 배치 조정**: DynamicBatchController로 에러율에 따른 자동 최적화
- **환경 변수 지원**: 런타임 설정 조정 가능

### 🔧 개선사항

#### ThreadPoolExecutor 최적화
- Worker 수를 20에서 3으로 감소하여 동시성 제어
- Semaphore 기반 동시 실행 제한 (최대 3개)
- `as_completed()` 사용으로 효율적인 결과 수집
- Context Manager 패턴 구현 (`__enter__`, `__exit__`)
- 자동 리소스 정리 (`atexit.register`)

#### 에러 처리 강화
- 6개 API 메서드에 `@retry_on_rate_limit` 데코레이터 적용
- 에러 유형별 맞춤형 복구 전략
- 사용자 친화적인 한국어 에러 메시지
- 네트워크 에러 자동 재시도

### 📊 성능 개선
- **안정적인 처리량**: 10-12 TPS 유지 (API 한계의 60%)
- **에러율**: 0% 달성 (목표 <1%)
- **100개 종목 조회**: 8.35초, 0 에러
- **장시간 안정성**: 30초 테스트 313 호출, 0 에러

### 📚 문서화
- README.md에 Rate Limiting 섹션 추가
- 상세한 사용 예제 제공 (`examples/rate_limiting_example.py`)
- 모범 사례 및 권장 설정 안내

### 🔄 하위 호환성
- 기존 API 인터페이스 완전 유지
- 기본 동작은 변경 없음
- 새로운 기능은 옵트인 방식

### 🗑️ 제거된 기능
- WebSocket 관련 코드 제거 (더 이상 사용하지 않음)
- 불필요한 레거시 메서드 제거

### 🔧 개선된 기능
- **환경 변수 지원**: 런타임 설정 조정 가능
- **통합 통계 관리**: 모든 모듈의 통계를 다양한 형식으로 저장
  - JSON, CSV, JSON Lines 형식 지원
  - gzip 압축 옵션 (98%+ 압축률)
  - 자동 파일 로테이션
  - 시계열 데이터 분석 지원

## [이전 버전]

(이전 버전 기록은 향후 추가 예정) 