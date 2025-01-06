"""
만세력 API 테스트
"""
import unittest
from datetime import datetime
from zoneinfo import ZoneInfo
from mansae import MansaeAPI

class TestMansaeAPI(unittest.TestCase):
    def setUp(self):
        """테스트 설정"""
        self.api = MansaeAPI()
        
    def test_get_saju(self):
        """사주 계산 테스트"""
        # 기본 테스트
        saju = self.api.get_saju(2024, 1, 6, 12, 30)
        
        self.assertIn('year', saju)
        self.assertIn('month', saju)
        self.assertIn('day', saju)
        self.assertIn('hour', saju)
        
        # 각 요소의 세부 정보가 존재하는지 확인
        for element in ['year', 'month', 'day', 'hour']:
            self.assertIn('gan', saju[element])
            self.assertIn('ji', saju[element])
            self.assertIn('ganji', saju[element])
            self.assertIn('hganji', saju[element])
            
        # 값의 형식 확인
        self.assertEqual(len(saju['year']['gan']), 1)  # 천간은 1자
        self.assertEqual(len(saju['year']['ji']), 1)   # 지지는 1자
        self.assertEqual(len(saju['year']['ganji']), 2)  # 간지는 2자
        self.assertEqual(len(saju['year']['hganji']), 2)  # 한자 간지는 2자
        
    def test_specific_dates(self):
        """특정 날짜 테스트"""
        # 1998년 7월 24일 0시 48분
        saju = self.api.get_saju(1998, 7, 24, 0, 48)
        self.assertEqual(saju['hour']['ganji'], '경자')
        self.assertEqual(saju['hour']['hganji'], '庚子')
        
        # 2024년 1월 6일 12시 30분
        saju = self.api.get_saju(2024, 1, 6, 12, 30)
        self.assertEqual(saju['year']['ganji'], '갑진')
        self.assertEqual(saju['month']['ganji'], '을축')
        self.assertEqual(saju['day']['ganji'], '기사')
        self.assertEqual(saju['hour']['ganji'], '경오')
        
    def test_timezone_handling(self):
        """시간대 처리 테스트"""
        # 도쿄 시간대로 API 인스턴스 생성
        tokyo_api = MansaeAPI("Asia/Tokyo")
        seoul_api = MansaeAPI("Asia/Seoul")
        
        # 같은 시각에 대한 계산 결과 비교
        tokyo_saju = tokyo_api.get_saju(2024, 1, 6, 12, 30)
        seoul_saju = seoul_api.get_saju(2024, 1, 6, 12, 30)
        
        # 시간대가 다르므로 시주가 다를 수 있음
        self.assertEqual(tokyo_saju['year']['ganji'], seoul_saju['year']['ganji'])
        self.assertEqual(tokyo_saju['month']['ganji'], seoul_saju['month']['ganji'])
        self.assertEqual(tokyo_saju['day']['ganji'], seoul_saju['day']['ganji'])
        
    def test_invalid_timezone(self):
        """잘못된 시간대 테스트"""
        with self.assertRaises(ValueError):
            MansaeAPI("Invalid/Timezone")
            
    def test_invalid_dates(self):
        """잘못된 날짜 테스트"""
        # 존재하지 않는 날짜
        with self.assertRaises(ValueError):
            self.api.get_saju(2024, 2, 30)
            
        # 잘못된 시간
        with self.assertRaises(ValueError):
            self.api.get_saju(2024, 1, 1, 24, 0)
            
        with self.assertRaises(ValueError):
            self.api.get_saju(2024, 1, 1, 12, 60)
            
    def test_time_boundaries(self):
        """시간 경계값 테스트"""
        # 자시 시작 (23:30)
        saju1 = self.api.get_saju(2024, 1, 6, 23, 30)
        # 자시 끝 (01:29)
        saju2 = self.api.get_saju(2024, 1, 7, 1, 29)
        
        self.assertEqual(saju1['hour']['ji'], '자')
        self.assertEqual(saju2['hour']['ji'], '자')
        
if __name__ == '__main__':
    unittest.main() 