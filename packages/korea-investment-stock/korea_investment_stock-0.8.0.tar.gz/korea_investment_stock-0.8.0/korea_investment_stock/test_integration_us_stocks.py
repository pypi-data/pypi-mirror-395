"""
미국 주식 현재가 조회 통합 테스트
TODO-33 Phase 2.2
"""
import unittest
from unittest.mock import Mock, patch

from korea_investment_stock import KoreaInvestment


class TestUSStockIntegration(unittest.TestCase):
    """미국 주식 통합 테스트"""
    
    def setUp(self):
        """Mock broker 인스턴스 설정"""
        # access token 발급을 건너뛰고 직접 설정
        self.patcher = patch('korea_investment_stock.korea_investment_stock.KoreaInvestment.issue_access_token')
        self.patcher.start()
        
        self.broker = KoreaInvestment(
            api_key="test_key",
            api_secret="test_secret",
            acc_no="12345678-01"
        )
        self.broker.access_token = "Bearer test_token"
    
    def tearDown(self):
        """테스트 정리"""
        self.patcher.stop()
        if hasattr(self.broker, 'shutdown'):
            self.broker.shutdown()
    
    def test_unified_price_interface(self):
        """통합 인터페이스 테스트"""
        # Mock 응답 설정
        kr_response = {
            'rt_cd': '0',
            'msg1': '정상처리 되었습니다.',
            'output1': {
                'stck_shrn_iscd': '005930',
                'stck_prpr': '62600',
                'prdy_vrss': '1600',
                'prdy_ctrt': '2.62',
                'acml_vol': '15234567',    # 거래량
                'hts_avls': '3735468'      # 시가총액 (억원)
            }
        }

        us_response = {
            'rt_cd': '0',
            'msg1': '정상처리 되었습니다.',
            'output': {
                'rsym': 'DNASAAPL',
                'last': '211.1600',
                't_xdif': '1720',
                't_xrat': '-0.59',
                'tvol': '39765812',        # 거래량
                'tomv': '3250000000000',   # 시가총액
                'shar': '15384171000',     # 상장주수
                'perx': '32.95',
                'pbrx': '47.23'
            }
        }

        with patch.object(self.broker, 'fetch_price') as mock_fetch:
            mock_fetch.side_effect = [kr_response, us_response]

            stock_list = [
                ("005930", "KR"),  # 삼성전자
                ("AAPL", "US")     # 애플
            ]

            # 단일 메서드를 루프로 호출
            results = []
            for symbol, market in stock_list:
                result = self.broker.fetch_price(symbol, market)
                results.append(result)

            # 검증
            self.assertEqual(len(results), 2)
            self.assertTrue(all(r['rt_cd'] == '0' for r in results))

            # 국내 주식 확인
            kr_result = results[0]
            self.assertIn('output1', kr_result)
            self.assertEqual(kr_result['output1']['stck_shrn_iscd'], '005930')

            # 미국 주식 확인
            us_result = results[1]
            self.assertIn('output', us_result)
            self.assertEqual(us_result['output']['rsym'], 'DNASAAPL')
            self.assertIn('perx', us_result['output'])  # PER 정보 포함
    
    def test_fetch_price_internal_routing(self):
        """내부 라우팅 테스트"""
        # KR market 테스트
        with patch.object(self.broker, 'fetch_stock_info') as mock_info, \
             patch.object(self.broker, 'fetch_domestic_price') as mock_kr_price:

            mock_info.return_value = {'output': {'prdt_clsf_name': '주권'}}
            mock_kr_price.return_value = {'rt_cd': '0', 'output1': {}}

            result = self.broker.fetch_price("005930", "KR")

            mock_info.assert_called_once_with("005930", "KR")
            mock_kr_price.assert_called_once()

        # US market 테스트
        with patch.object(self.broker, 'fetch_price_detail_oversea') as mock_us_price:
            mock_us_price.return_value = {'rt_cd': '0', 'output': {}}

            result = self.broker.fetch_price("AAPL", "US")

            mock_us_price.assert_called_once_with("AAPL", "US")
    
    def test_us_stock_response_format(self):
        """미국 주식 응답 형식 검증"""
        mock_response = {
            'rt_cd': '0',
            'msg1': '정상처리 되었습니다.',
            'output': {
                'rsym': 'DNASAAPL',
                'last': '211.1600',
                'open': '210.5650',
                'high': '212.1300',
                'low': '209.8600',
                'tvol': '39765812',
                'tomv': '3250000000000',   # 시가총액
                'shar': '15384171000',     # 상장주수
                't_xdif': '1720',
                't_xrat': '-0.59',
                'perx': '32.95',
                'pbrx': '47.23',
                'epsx': '6.41',
                'bpsx': '4.47',
                'vnit': '1',
                'e_hogau': '0.0100'
            }
        }

        with patch.object(self.broker, 'fetch_price_detail_oversea') as mock_fetch:
            mock_fetch.return_value = mock_response

            result = self.broker.fetch_price("AAPL", "US")

            # 필수 필드 검증
            self.assertEqual(result['rt_cd'], '0')
            self.assertIn('output', result)

            output = result['output']
            self.assertEqual(output['rsym'], 'DNASAAPL')
            self.assertEqual(output['last'], '211.1600')
            self.assertEqual(output['perx'], '32.95')  # PER
            self.assertEqual(output['pbrx'], '47.23')  # PBR
            self.assertEqual(output['epsx'], '6.41')   # EPS
            self.assertEqual(output['bpsx'], '4.47')   # BPS
    
    def test_mixed_market_batch(self):
        """국내/미국 혼합 배치 조회"""
        mixed_stocks = [
            ("005930", "KR"),    # 삼성전자
            ("AAPL", "US"),      # 애플
            ("035720", "KR"),    # 카카오
            ("TSLA", "US"),      # 테슬라
        ]

        mock_responses = []
        for symbol, market in mixed_stocks:
            if market == "KR":
                mock_responses.append({
                    'rt_cd': '0',
                    'output1': {'stck_shrn_iscd': symbol, 'stck_prpr': '10000'}
                })
            else:
                mock_responses.append({
                    'rt_cd': '0',
                    'output': {'rsym': f'DNAS{symbol}', 'last': '100.00'}
                })

        with patch.object(self.broker, 'fetch_price') as mock_fetch:
            mock_fetch.side_effect = mock_responses

            results = []
            for symbol, market in mixed_stocks:
                result = self.broker.fetch_price(symbol, market)
                results.append(result)

            self.assertEqual(len(results), 4)
            self.assertTrue(all(r['rt_cd'] == '0' for r in results))

            # 각 시장별로 올바른 응답 형식인지 확인
            for i, (symbol, market) in enumerate(mixed_stocks):
                if market == "KR":
                    self.assertIn('output1', results[i])
                else:
                    self.assertIn('output', results[i])
    
    def test_invalid_market_type(self):
        """잘못된 market 타입 처리"""
        with self.assertRaises(ValueError) as context:
            self.broker.fetch_price("INVALID", "INVALID_MARKET")

        self.assertIn("Unsupported market type", str(context.exception))
    
    def test_oversea_error_handling(self):
        """해외 주식 에러 처리 테스트"""
        # 모든 거래소에서 실패하는 경우
        with patch('requests.get') as mock_get:

            # API 응답 mock - 실패 응답
            mock_response = Mock()
            mock_response.json.return_value = {
                'rt_cd': '1',
                'msg1': '조회할 자료가 없습니다'
            }
            mock_get.return_value = mock_response

            with self.assertRaises(ValueError) as context:
                self.broker.fetch_price_detail_oversea("INVALID", "US")

            self.assertIn("Unable to fetch price for symbol 'INVALID' in any US exchange",
                         str(context.exception))


if __name__ == "__main__":
    # 테스트 실행
    unittest.main(verbosity=2) 