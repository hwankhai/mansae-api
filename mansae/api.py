"""
만세력(사주) 계산 API 클래스
"""
from typing import Dict, Tuple
from datetime import datetime
from zoneinfo import ZoneInfo

from .constants import *
from .utils import (
    div, get_min_by_time, disp2days
)

class MansaeAPI:
    """만세력(사주) 계산을 위한 API 클래스"""
    
    def __init__(self, timezone: str = "Asia/Seoul"):
        """
        Args:
            timezone: 사용할 시간대 (기본값: "Asia/Seoul")
        """
        try:
            self.timezone = ZoneInfo(timezone)
        except Exception as e:
            raise ValueError(f"Invalid timezone: {timezone} / 잘못된 시간대입니다: {timezone}")
            
    def _validate_date(self, year: int, month: int, day: int) -> None:
        """날짜 유효성 검사"""
        try:
            datetime(year, month, day)
        except ValueError as e:
            raise ValueError(f"Invalid date: {e} / 잘못된 날짜입니다: {e}")
            
    def _validate_time(self, hour: int, minute: int) -> None:
        """시간 유효성 검사"""
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23 / 시간은 0-23 사이여야 합니다")
        if not (0 <= minute <= 59):
            raise ValueError("Minute must be between 0 and 59 / 분은 0-59 사이여야 합니다")
            
    def _get_time_index(self, hour: int, minute: int) -> int:
        """시간 인덱스 계산 (자시: 0, 축시: 1, ..., 해시: 11)"""
        total_minutes = hour * 60 + minute
        if total_minutes >= 1410:  # 23:30 이후
            return 0
        time_index = ((total_minutes + 30) % 1440) // 120
        return time_index
        
    def _syd_to_so24yd(
        self,
        solar_year: int,
        solar_month: int,
        solar_day: int,
        solar_hour: int,
        solar_min: int
    ) -> Tuple[int, int, int, int, int]:
        """
        그레고리력의 년월시일분으로 60년의 배수, 세차, 월건(태양력),
        일진, 시주를 구함
        """
        # 시간대 적용
        dt = datetime(solar_year, solar_month, solar_day, 
                     solar_hour, solar_min, tzinfo=self.timezone)
        
        displ2min = get_min_by_time(
            UNITY_YEAR, UNITY_MONTH, UNITY_DAY, UNITY_HOUR, UNITY_MIN,
            dt.year, dt.month, dt.day, dt.hour, dt.minute
        )
        
        displ2day = disp2days(
            UNITY_YEAR, UNITY_MONTH, UNITY_DAY,
            dt.year, dt.month, dt.day
        )
        
        # 무인년(1996)입춘시점부터 해당일시까지 경과년수
        so24 = div(displ2min, 525949)
        
        if displ2min >= 0:
            so24 += 1
            
        # 년주 구하기
        so24year = (so24 % 60) * -1
        so24year += 12
        
        if so24year < 0:
            so24year += 60
        elif so24year > 59:
            so24year -= 60
            
        monthmin100 = displ2min % 525949
        monthmin100 = 525949 - monthmin100
        
        if monthmin100 < 0:
            monthmin100 += 525949
        elif monthmin100 >= 525949:
            monthmin100 -= 525949
            
        for i in range(12):
            j = i * 2
            if (MONTH[j] <= monthmin100 and monthmin100 < MONTH[j + 2]):
                so24month = i
                break
                
        # 월주 구하기
        i = so24month
        t = so24year % 10
        t %= 5
        t = t * 12 + 2 + i
        so24month = t
        
        if so24month > 59:
            so24month -= 60
            
        # 일주 구하기
        so24day = displ2day % 60
        so24day *= -1
        so24day += 7
        
        if so24day < 0:
            so24day += 60
        elif so24day > 59:
            so24day -= 60
            
        # 시주 구하기
        if solar_hour == 23 and solar_min >= 30:
            so24day = (so24day + 1) % 60
            i = 0
        else:
            i = self._get_time_index(solar_hour, solar_min)
            
        t = so24day % 10
        t = t * 12 + i
        so24hour = t % 60
        
        return so24, so24year, so24month, so24day, so24hour
        
    def get_saju(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0
    ) -> Dict[str, Dict[str, str]]:
        """
        특정 년월일시의 사주(만세력)를 계산합니다.
        
        Args:
            year: 년도
            month: 월
            day: 일
            hour: 시 (0-23)
            minute: 분 (0-59)
            
        Returns:
            사주 정보를 담은 딕셔너리:
            {
                'year': {'gan': '갑', 'ji': '자', 'ganji': '갑자', 'hganji': '甲子'},
                'month': {'gan': '을', 'ji': '축', 'ganji': '을축', 'hganji': '乙丑'},
                'day': {'gan': '병', 'ji': '인', 'ganji': '병인', 'hganji': '丙寅'},
                'hour': {'gan': '정', 'ji': '묘', 'ganji': '정묘', 'hganji': '丁卯'}
            }
        """
        # 날짜/시간 유효성 검사
        self._validate_date(year, month, day)
        self._validate_time(hour, minute)
        
        # 60간지 인덱스 계산
        _, year_idx, month_idx, day_idx, hour_idx = self._syd_to_so24yd(
            year, month, day, hour, minute
        )
        
        # 년주
        year_gan = GAN[year_idx % 10]
        year_ji = JI[year_idx % 12]
        year_ganji = GANJI[year_idx]
        year_hganji = HGANJI[year_idx]
        
        # 월주
        month_gan = GAN[month_idx % 10]
        month_ji = JI[month_idx % 12]
        month_ganji = GANJI[month_idx]
        month_hganji = HGANJI[month_idx]
        
        # 일주
        day_gan = GAN[day_idx % 10]
        day_ji = JI[day_idx % 12]
        day_ganji = GANJI[day_idx]
        day_hganji = HGANJI[day_idx]
        
        # 시주
        hour_gan = GAN[hour_idx % 10]
        hour_ji = JI[hour_idx % 12]
        hour_ganji = GANJI[hour_idx]
        hour_hganji = HGANJI[hour_idx]
        
        return {
            'year': {
                'gan': year_gan,
                'ji': year_ji,
                'ganji': year_ganji,
                'hganji': year_hganji
            },
            'month': {
                'gan': month_gan,
                'ji': month_ji,
                'ganji': month_ganji,
                'hganji': month_hganji
            },
            'day': {
                'gan': day_gan,
                'ji': day_ji,
                'ganji': day_ganji,
                'hganji': day_hganji
            },
            'hour': {
                'gan': hour_gan,
                'ji': hour_ji,
                'ganji': hour_ganji,
                'hganji': hour_hganji
            }
        } 