"""
만세력 계산에 필요한 유틸리티 함수들
"""
import numpy as np
from typing import Tuple

def div(a: float, b: float) -> int:
    """정수 몫을 반환"""
    return int(a / b)

def degree_low(d: float) -> float:
    """각도를 0~360도 이내로 정규화"""
    di = d
    i = div(d, 360)
    di = d - (i * 360)
    
    while di >= 360 or di < 0:
        if di > 0:
            di -= 360
        else:
            di += 360
            
    return di

def moon_sun_degree(day: float) -> float:
    """태양황력과 달황경의 차이 (1996 기준)"""
    # 평균 황경
    sl = float(day * 0.98564736 + 278.956807)
    
    # 근일점 황경
    smin = 282.869498 + 0.00004708 * day
    
    # 근점이각
    sminangle = np.pi * (sl - smin) / 180
    
    # 황경차
    sd = 1.919 * np.sin(sminangle) + 0.02 * np.sin(2 * sminangle)
    
    # 진황경
    sreal = degree_low(sl + sd)
    
    # 평균 황경
    ml = 27.836584 + 13.17639648 * day
    
    # 근지점 황경
    mmin = 280.425774 + 0.11140356 * day
    
    # 근점이각
    mminangle = np.pi * (ml - mmin) / 180
    
    # 교점황경
    msangle = 202.489407 - 0.05295377 * day
    msdangle = np.pi * (ml - msangle) / 180
    
    # 황경차
    md = (5.06889 * np.sin(mminangle) +
          0.146111 * np.sin(2 * mminangle) +
          0.01 * np.sin(3 * mminangle) -
          0.238056 * np.sin(sminangle) -
          0.087778 * np.sin(mminangle + sminangle) +
          0.048889 * np.sin(mminangle - sminangle) -
          0.129722 * np.sin(2 * msdangle) -
          0.011111 * np.sin(2 * msdangle - mminangle) -
          0.012778 * np.sin(2 * msdangle + mminangle))
    
    # 진황경
    mreal = degree_low(ml + md)
    re = degree_low(mreal - sreal)
    
    return re

def disp_time_day(year: int, month: int, day: int) -> int:
    """year의 1월 1일부터 해당 일자까지의 날짜수 계산"""
    e = 0
    
    for i in range(1, month):
        e += 31
        if i in [2, 4, 6, 9, 11]:
            e -= 1
            
        if i == 2:
            e -= 2
            if (year % 4) == 0:
                e += 1
            if (year % 100) == 0:
                e -= 1
            if (year % 400) == 0:
                e += 1
            if (year % 4000) == 0:
                e -= 1
                
    e += day
    return e

def disp2days(y1: int, m1: int, d1: int, y2: int, m2: int, d2: int) -> int:
    """y1,m1,d1일부터 y2,m2,d2까지의 일수 계산"""
    if y2 > y1:
        p1 = disp_time_day(y1, m1, d1)
        p1n = disp_time_day(y1, 12, 31)
        p2 = disp_time_day(y2, m2, d2)
        pp1 = y1
        pp2 = y2
        pr = -1
    else:
        p1 = disp_time_day(y2, m2, d2)
        p1n = disp_time_day(y2, 12, 31)
        p2 = disp_time_day(y1, m1, d1)
        pp1 = y2
        pp2 = y1
        pr = 1
        
    if y2 == y1:
        dis = p2 - p1
    else:
        dis = p1n - p1
        ppp1 = pp1 + 1
        ppp2 = pp2 - 1
        
        for k in range(ppp1, ppp2 + 1):
            dis += disp_time_day(k, 12, 31)
            
        dis += p2
        dis *= pr
        
    return dis

def get_min_by_time(
    uy: int, umm: int, ud: int, uh: int, umin: int,
    y1: int, mo1: int, d1: int, h1: int, mm1: int
) -> int:
    """두 시점 사이의 시간(분) 계산"""
    dispday = disp2days(uy, umm, ud, y1, mo1, d1)
    t = dispday * 24 * 60 + (uh - h1) * 60 + (umin - mm1)
    return t 