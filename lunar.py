"""
음력 변환 모듈
Lunar Calendar Conversion Module

음력을 양력으로 변환하는 기능을 제공합니다.
1900년~2100년 범위를 지원합니다.
"""

from datetime import datetime, timedelta
from typing import Dict, List


# 음력 데이터 테이블 (1900-2100)
# 각 항목의 하위 4비트(bits 0-3): 윤달 위치 (0=윤달없음, 1-12=해당 월이 윤달)
# 상위 13비트(bits 4-16): 각 달의 크기 (0=29일, 1=30일)
# 최상위 비트(bit 16): 윤달 크기 (0=29일, 1=30일)
LUNAR_INFO = [
    0x04bd8,  # 1900
    0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,  # 1901-1909
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0,  # 1910-1918
    0x14977, 0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570,  # 1919-1927
    0x052f2, 0x04970, 0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3,  # 1928-1936
    0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0,  # 1937-1945
    0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0,  # 1946-1954
    0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6, 0x0ab50, 0x04b60, 0x0aae4,  # 1955-1963
    0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0, 0x04dd5, 0x04ad0,  # 1964-1972
    0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6, 0x095b0, 0x049b0,  # 1973-1981
    0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570, 0x04af5,  # 1982-1990
    0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,  # 1991-1999
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0,  # 2000-2008
    0x0cab5, 0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176,  # 2009-2017
    0x052b0, 0x0a930, 0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0,  # 2018-2026
    0x0d260, 0x0ea65, 0x0d530, 0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0,  # 2027-2035
    0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577,  # 2036-2044
    0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0, 0x14b63, 0x09370, 0x049f8, 0x04970,  # 2045-2053
    0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0, 0x0a2e0, 0x0d2e3, 0x0c960,  # 2054-2062
    0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4, 0x052d0, 0x0a9b8,  # 2063-2071
    0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0, 0x0b273,  # 2072-2080
    0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,  # 2081-2089
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150,  # 2090-2098
    0x0f252, 0x0d520  # 2099-2100
]


# 1900년 1월 31일이 음력 1900년 1월 1일
SOLAR_BASE_DATE = datetime(1900, 1, 31)
LUNAR_BASE_YEAR = 1900
MIN_YEAR = 1900
MAX_YEAR = 2100


def get_leap_month(year: int) -> int:
    """
    해당 연도의 윤달 월을 반환
    
    Args:
        year: 연도
        
    Returns:
        윤달 월 (0이면 윤달 없음, 1-12이면 해당 월에 윤달)
    """
    if year < MIN_YEAR or year > MAX_YEAR:
        return 0
    
    year_info = LUNAR_INFO[year - LUNAR_BASE_YEAR]
    return year_info & 0x0F  # 하위 4비트가 윤달 위치


def get_lunar_month_days(year: int, month: int) -> int:
    """
    음력 특정 월의 일수를 반환
    
    Args:
        year: 연도
        month: 월 (1-12)
        
    Returns:
        일수 (29 또는 30)
    """
    if year < MIN_YEAR or year > MAX_YEAR:
        return 29
    
    year_info = LUNAR_INFO[year - LUNAR_BASE_YEAR]
    
    # 해당 월의 비트 확인 (1=30일, 0=29일)
    # bit 4부터 시작하고, 1월이 bit 4, 12월이 bit 15
    if year_info & (0x8000 >> (month - 1)):
        return 30
    return 29


def get_leap_month_days(year: int) -> int:
    """
    윤달의 일수를 반환
    
    Args:
        year: 연도
        
    Returns:
        윤달 일수 (윤달 없으면 0)
    """
    leap_month = get_leap_month(year)
    if leap_month == 0:
        return 0
    
    year_info = LUNAR_INFO[year - LUNAR_BASE_YEAR]
    
    # bit 16 (0x10000)이 윤달 크기 (1=30일, 0=29일)
    if year_info & 0x10000:
        return 30
    return 29


def lunar_year_days(year: int) -> int:
    """
    음력 한 해의 총 일수를 반환
    
    Args:
        year: 연도
        
    Returns:
        연도의 총 일수
    """
    total = 0
    for month in range(1, 13):
        total += get_lunar_month_days(year, month)
    
    # 윤달 일수 추가
    total += get_leap_month_days(year)
    
    return total


def validate_lunar_date(year: int, month: int, day: int, is_leap_month: bool = False) -> bool:
    """
    음력 날짜의 유효성을 검증
    
    Args:
        year: 음력 연도
        month: 음력 월
        day: 음력 일
        is_leap_month: 윤달 여부
        
    Returns:
        유효하면 True, 아니면 False
    """
    # 연도 범위 확인
    if year < MIN_YEAR or year > MAX_YEAR:
        return False
    
    # 월 범위 확인
    if month < 1 or month > 12:
        return False
    
    # 윤달 확인
    if is_leap_month:
        leap_month = get_leap_month(year)
        if leap_month != month:
            return False
        max_day = get_leap_month_days(year)
    else:
        max_day = get_lunar_month_days(year, month)
    
    # 일 범위 확인
    if day < 1 or day > max_day:
        return False
    
    return True


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> Dict:
    """
    음력을 양력으로 변환
    
    Args:
        year (int): 음력 연도 (1900-2100)
        month (int): 음력 월 (1-12)
        day (int): 음력 일 (1-29/30)
        is_leap_month (bool): 윤달 여부 (기본값: False)
        
    Returns:
        dict: {'year': 양력연도, 'month': 양력월, 'day': 양력일}
        
    Raises:
        ValueError: 유효하지 않은 날짜
    """
    # 입력 검증
    if not validate_lunar_date(year, month, day, is_leap_month):
        if year < MIN_YEAR or year > MAX_YEAR:
            raise ValueError(f"연도는 {MIN_YEAR}년부터 {MAX_YEAR}년 사이여야 합니다.")
        if is_leap_month and get_leap_month(year) != month:
            raise ValueError(f"{year}년 {month}월은 윤달이 아닙니다.")
        if month < 1 or month > 12:
            raise ValueError(f"월은 1부터 12 사이여야 합니다.")
        
        max_day = get_leap_month_days(year) if is_leap_month else get_lunar_month_days(year, month)
        raise ValueError(f"{year}년 {'윤' if is_leap_month else ''}{month}월은 {max_day}일까지입니다.")
    
    # 음력 1900년 1월 1일부터 입력 날짜까지의 일수 계산
    total_days = 0
    
    # 1900년부터 입력 연도 전년도까지의 일수
    for y in range(LUNAR_BASE_YEAR, year):
        total_days += lunar_year_days(y)
    
    # 입력 연도의 1월부터 입력 월 전월까지의 일수
    for m in range(1, month):
        total_days += get_lunar_month_days(year, m)
    
    # 윤달 처리
    leap_month = get_leap_month(year)
    if leap_month > 0 and leap_month < month:
        # 입력 월 이전에 윤달이 있으면 윤달 일수 추가
        total_days += get_leap_month_days(year)
    elif is_leap_month:
        # 현재 월이 윤달이면 평달 일수 추가
        total_days += get_lunar_month_days(year, month)
    
    # 입력 일수 추가
    total_days += day - 1  # 1일은 0일 차이
    
    # 양력 기준일에 일수를 더함
    solar_date = SOLAR_BASE_DATE + timedelta(days=total_days)
    
    return {
        'year': solar_date.year,
        'month': solar_date.month,
        'day': solar_date.day
    }


def solar_to_lunar(year: int, month: int, day: int) -> Dict:
    """
    양력을 음력으로 변환
    
    Args:
        year (int): 양력 연도
        month (int): 양력 월
        day (int): 양력 일
        
    Returns:
        dict: {'year': 음력연도, 'month': 음력월, 'day': 음력일, 'is_leap_month': 윤달여부}
        
    Raises:
        ValueError: 유효하지 않은 날짜
    """
    # 양력 날짜 검증
    try:
        solar_date = datetime(year, month, day)
    except ValueError:
        raise ValueError(f"유효하지 않은 양력 날짜: {year}년 {month}월 {day}일")
    
    # 기준일과의 일수 차이 계산
    if solar_date < SOLAR_BASE_DATE:
        raise ValueError(f"날짜는 {SOLAR_BASE_DATE.strftime('%Y년 %m월 %d일')} 이후여야 합니다.")
    
    total_days = (solar_date - SOLAR_BASE_DATE).days
    
    # 음력 연도와 월, 일 계산
    lunar_year = LUNAR_BASE_YEAR
    lunar_month = 1
    lunar_day = 1
    is_leap_month = False
    
    # 연도 찾기
    while True:
        year_days = lunar_year_days(lunar_year)
        if total_days < year_days:
            break
        total_days -= year_days
        lunar_year += 1
        
        if lunar_year > MAX_YEAR:
            raise ValueError(f"날짜는 {MAX_YEAR}년 이전이어야 합니다.")
    
    # 월과 일 찾기
    leap_month = get_leap_month(lunar_year)
    
    for m in range(1, 13):
        # 평달
        month_days = get_lunar_month_days(lunar_year, m)
        if total_days < month_days:
            lunar_month = m
            lunar_day = total_days + 1
            is_leap_month = False
            break
        total_days -= month_days
        
        # 윤달 확인
        if m == leap_month and leap_month > 0:
            leap_days = get_leap_month_days(lunar_year)
            if total_days < leap_days:
                lunar_month = m
                lunar_day = total_days + 1
                is_leap_month = True
                break
            total_days -= leap_days
    
    return {
        'year': lunar_year,
        'month': lunar_month,
        'day': lunar_day,
        'is_leap_month': is_leap_month
    }


if __name__ == '__main__':
    # 테스트 케이스
    print("=== 음력 → 양력 변환 테스트 ===")
    
    # 테스트 1: 음력 2009년 11월 13일 → 양력 2009년 12월 28일
    result1 = lunar_to_solar(2009, 11, 13)
    print(f"음력 2009년 11월 13일 → 양력 {result1['year']}년 {result1['month']}월 {result1['day']}일")
    assert result1['year'] == 2009 and result1['month'] == 12 and result1['day'] == 28, "Test 1 failed"
    
    # 테스트 2: 음력 2009년 윤5월 15일 (2010이 아니라 2009에 윤5월이 있음)
    result2 = lunar_to_solar(2009, 5, 15, is_leap_month=True)
    print(f"음력 2009년 윤5월 15일 → 양력 {result2['year']}년 {result2['month']}월 {result2['day']}일")
    
    # 테스트 3: 경계값 테스트 (1900년)
    result3 = lunar_to_solar(1900, 1, 1)
    print(f"음력 1900년 1월 1일 → 양력 {result3['year']}년 {result3['month']}월 {result3['day']}일")
    assert result3['year'] == 1900 and result3['month'] == 1 and result3['day'] == 31, "Test 3 failed"
    
    # 테스트 4: 경계값 테스트 (2100년)
    result4 = lunar_to_solar(2100, 12, 1)
    print(f"음력 2100년 12월 1일 → 양력 {result4['year']}년 {result4['month']}월 {result4['day']}일")
    
    # 테스트 5: 2012년 윤4월 테스트
    result5 = lunar_to_solar(2012, 4, 15, is_leap_month=True)
    print(f"음력 2012년 윤4월 15일 → 양력 {result5['year']}년 {result5['month']}월 {result5['day']}일")
    
    print("\n=== 양력 → 음력 변환 테스트 ===")
    
    # 역변환 테스트
    result6 = solar_to_lunar(2009, 12, 28)
    print(f"양력 2009년 12월 28일 → 음력 {result6['year']}년 {result6['month']}월 {result6['day']}일")
    assert result6['year'] == 2009 and result6['month'] == 11 and result6['day'] == 13, "Test 6 failed"
    
    result7 = solar_to_lunar(2009, 6, 21)
    leap_str = "윤" if result7['is_leap_month'] else ""
    print(f"양력 2009년 6월 21일 → 음력 {result7['year']}년 {leap_str}{result7['month']}월 {result7['day']}일")
    
    print("\n=== 에러 처리 테스트 ===")
    try:
        lunar_to_solar(2010, 5, 15, is_leap_month=True)
    except ValueError as e:
        print(f"✓ 윤달 오류 처리: {e}")
    
    try:
        lunar_to_solar(1899, 1, 1)
    except ValueError as e:
        print(f"✓ 범위 초과 처리: {e}")
    
    try:
        lunar_to_solar(2009, 2, 31)
    except ValueError as e:
        print(f"✓ 유효하지 않은 날짜 처리: {e}")
    
    print("\n✅ 모든 테스트 통과!")
