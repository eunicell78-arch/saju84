from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# 천간 (Heavenly Stems)
HEAVENLY_STEMS_KO = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
HEAVENLY_STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 지지 (Earthly Branches)
EARTHLY_BRANCHES_KO = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
EARTHLY_BRANCHES_HANJA = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 오행 (Five Elements)
FIVE_ELEMENTS = ['목', '화', '토', '금', '수']

# 음력 데이터 (1900-2100년, 한국천문연구원)
LUNAR_DATA = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2, 0x04ae0,
    0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970, 0x0a4b0,
    0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566, 0x0d4a0, 0x0ea50,
    0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0,
    0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0,
    0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260,
    0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558,
    0x0b540, 0x0b6a0, 0x195a6, 0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46,
    0x0ab60, 0x09570, 0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5,
    0x092e0, 0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930, 0x07954,
    0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, 0x05aa0, 0x076a3,
    0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0, 0x056d0, 0x055b2,
    0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0, 0x14b63, 0x09370, 0x049f8, 0x04970,
    0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0, 0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0,
    0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4, 0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50,
    0x055a0, 0x0aba4, 0x0a5b0, 0x052b0, 0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60,
    0x0a570, 0x054e4, 0x0d160, 0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0,
    0x0d150, 0x0f252, 0x0d520
]

# 절기 계산 기본 데이터
SOLAR_TERM_BASE = [
    5.4055, 20.12, 3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04,
    5.678, 21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438,
    7.438, 22.36, 7.18, 21.94
]

def get_lunar_year_days(year: int) -> int:
    """음력 연도의 총 일수 계산"""
    sum_days = 348
    for i in range(12):
        if LUNAR_DATA[year - 1900] & (0x8000 >> i):
            sum_days += 1
    leap_days = get_leap_month_days(year)
    return sum_days + leap_days

def get_leap_month(year: int) -> int:
    """윤달 위치 반환 (0이면 윤달 없음)"""
    return LUNAR_DATA[year - 1900] & 0xf

def get_leap_month_days(year: int) -> int:
    """윤달 일수 반환"""
    if get_leap_month(year):
        return 30 if (LUNAR_DATA[year - 1900] & 0x10000) else 29
    return 0

def get_lunar_month_days(year: int, month: int) -> int:
    """특정 월의 일수 반환"""
    return 30 if (LUNAR_DATA[year - 1900] & (0x10000 >> month)) else 29

def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> Dict[str, int]:
    """음력을 양력으로 변환"""
    base_date = datetime(1900, 1, 31)
    offset = 0
    
    for i in range(1900, year):
        offset += get_lunar_year_days(i)
    
    leap_month = get_leap_month(year)
    is_leap = False
    
    for i in range(1, month):
        if leap_month > 0 and i == leap_month and not is_leap:
            offset += get_leap_month_days(year)
            is_leap = True
            i -= 1
        else:
            offset += get_lunar_month_days(year, i)
    
    if is_leap_month and leap_month == month:
        offset += get_lunar_month_days(year, month)
    
    offset += day - 1
    solar_date = base_date + timedelta(days=offset)
    
    return {
        'year': solar_date.year,
        'month': solar_date.month,
        'day': solar_date.day
    }

def solar_to_lunar(year: int, month: int, day: int) -> Dict:
    """양력을 음력으로 변환"""
    base_date = datetime(1900, 1, 31)
    target_date = datetime(year, month, day)
    offset = (target_date - base_date).days
    
    lunar_year = 1900
    remaining_days = offset
    
    for i in range(1900, 2100):
        year_days = get_lunar_year_days(i)
        if remaining_days < year_days:
            lunar_year = i
            break
        remaining_days -= year_days
    
    leap_month = get_leap_month(lunar_year)
    lunar_month = 1
    is_leap_month = False
    
    for i in range(1, 13):
        if leap_month > 0 and i == leap_month + 1 and not is_leap_month:
            month_days = get_leap_month_days(lunar_year)
            is_leap_month = True
            i -= 1
        else:
            month_days = get_lunar_month_days(lunar_year, i)
            is_leap_month = False
        
        if remaining_days < month_days:
            lunar_month = i
            break
        remaining_days -= month_days
    
    lunar_day = remaining_days + 1
    
    return {
        'year': lunar_year,
        'month': lunar_month,
        'day': lunar_day,
        'is_leap_month': is_leap_month
    }

def get_solar_term_date(year: int, term_index: int) -> datetime:
    """특정 절기의 날짜 계산"""
    century = year // 100
    year_in_century = year % 100
    
    term_coeff = 0.2422
    leap_year_adjust = (year_in_century // 4) - (century // 4)
    
    day = int(SOLAR_TERM_BASE[term_index] + term_coeff * year_in_century + leap_year_adjust)
    month = (term_index // 2) + 1
    
    # Ensure day is valid for the month
    if day < 1:
        day = 1
    elif month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
        day = 31
    elif month in [4, 6, 9, 11] and day > 30:
        day = 30
    elif month == 2:
        # Check for leap year
        is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_day = 29 if is_leap else 28
        if day > max_day:
            day = max_day
    
    return datetime(year, month, day)

def get_year_pillar(year: int) -> Tuple[str, str, str, str]:
    """연주 계산"""
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return (
        HEAVENLY_STEMS_KO[stem_idx],
        EARTHLY_BRANCHES_KO[branch_idx],
        HEAVENLY_STEMS_HANJA[stem_idx],
        EARTHLY_BRANCHES_HANJA[branch_idx]
    )

def get_month_pillar(year: int, month: int, day: int) -> Tuple[str, str, str, str]:
    """월주 계산 (절기 기준)"""
    date = datetime(year, month, day)
    
    # 입춘 기준 연도 조정
    lichun_date = get_solar_term_date(year, 2)
    adjusted_year = year if date >= lichun_date else year - 1
    
    # 절기 기준 월 계산
    solar_term_month = 1
    for i in range(0, 24, 2):
        term_date = get_solar_term_date(adjusted_year, i)
        if date >= term_date:
            solar_term_month = (i // 2) + 1
    
    # 월주 천간 계산
    year_stem = (adjusted_year - 4) % 10
    month_stem_idx = ((year_stem % 5) * 2 + solar_term_month + 1) % 10
    
    # 월주 지지 매핑
    month_branches = {
        1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7,
        7: 8, 8: 9, 9: 10, 10: 11, 11: 0, 12: 1
    }
    month_branch_idx = month_branches.get(solar_term_month, 2)
    
    return (
        HEAVENLY_STEMS_KO[month_stem_idx],
        EARTHLY_BRANCHES_KO[month_branch_idx],
        HEAVENLY_STEMS_HANJA[month_stem_idx],
        EARTHLY_BRANCHES_HANJA[month_branch_idx]
    )

def get_day_pillar(year: int, month: int, day: int) -> Tuple[str, str, str, str]:
    """일주 계산 (60갑자 순환)"""
    base_date = datetime(1992, 10, 24)
    base_ganji_num = 9
    
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    target_ganji_num = (base_ganji_num + days_diff) % 60
    if target_ganji_num < 0:
        target_ganji_num += 60
    
    stem_idx = target_ganji_num % 10
    branch_idx = target_ganji_num % 12
    
    return (
        HEAVENLY_STEMS_KO[stem_idx],
        EARTHLY_BRANCHES_KO[branch_idx],
        HEAVENLY_STEMS_HANJA[stem_idx],
        EARTHLY_BRANCHES_HANJA[branch_idx]
    )

def get_hour_pillar(day_stem_ko: str, hour: int, minute: int) -> Tuple[str, str, str, str]:
    """시주 계산"""
    adjusted_hour = 0 if hour == 23 else hour
    total_minutes = adjusted_hour * 60 + minute
    shichen = ((total_minutes + 60) // 120) % 12
    
    day_stem_idx = HEAVENLY_STEMS_KO.index(day_stem_ko)
    hour_stem_base = (day_stem_idx % 5) * 2
    hour_stem_idx = (hour_stem_base + shichen) % 10
    
    return (
        HEAVENLY_STEMS_KO[hour_stem_idx],
        EARTHLY_BRANCHES_KO[shichen],
        HEAVENLY_STEMS_HANJA[hour_stem_idx],
        EARTHLY_BRANCHES_HANJA[shichen]
    )

def get_element(stem_or_branch: str, is_stem: bool = True) -> str:
    """오행 반환"""
    if is_stem:
        elements = {'갑': '목', '을': '목', '병': '화', '정': '화', '무': '토', 
                   '기': '토', '경': '금', '신': '금', '임': '수', '계': '수'}
    else:
        elements = {'자': '수', '축': '토', '인': '목', '묘': '목', '진': '토', '사': '화',
                   '오': '화', '미': '토', '신': '금', '유': '금', '술': '토', '해': '수'}
    return elements.get(stem_or_branch, '')

def get_yin_yang(stem_or_branch: str, is_stem: bool = True) -> str:
    """음양 반환"""
    if is_stem:
        idx = HEAVENLY_STEMS_KO.index(stem_or_branch)
    else:
        idx = EARTHLY_BRANCHES_KO.index(stem_or_branch)
    return '양' if idx % 2 == 0 else '음'

def calculate_four_pillars(birth_info: Dict) -> Dict:
    """사주팔자 계산"""
    year = birth_info['year']
    month = birth_info['month']
    day = birth_info['day']
    hour = birth_info['hour']
    minute = birth_info['minute']
    is_lunar = birth_info.get('is_lunar', False)
    is_leap_month = birth_info.get('is_leap_month', False)
    
    # 음력을 양력으로 변환
    if is_lunar:
        solar = lunar_to_solar(year, month, day, is_leap_month)
        solar_year, solar_month, solar_day = solar['year'], solar['month'], solar['day']
        lunar_date = {'year': year, 'month': month, 'day': day, 'is_leap_month': is_leap_month}
    else:
        solar_year, solar_month, solar_day = year, month, day
        lunar_date = solar_to_lunar(year, month, day)
    
    # 사주 계산
    year_pillar = get_year_pillar(solar_year)
    month_pillar = get_month_pillar(solar_year, solar_month, solar_day)
    day_pillar = get_day_pillar(solar_year, solar_month, solar_day)
    hour_pillar = get_hour_pillar(day_pillar[0], hour, minute)
    
    return {
        'solar_date': {'year': solar_year, 'month': solar_month, 'day': solar_day},
        'lunar_date': lunar_date,
        'year': {'ko': year_pillar[0], 'branch_ko': year_pillar[1], 
                'hanja': year_pillar[2], 'branch_hanja': year_pillar[3]},
        'month': {'ko': month_pillar[0], 'branch_ko': month_pillar[1],
                 'hanja': month_pillar[2], 'branch_hanja': month_pillar[3]},
        'day': {'ko': day_pillar[0], 'branch_ko': day_pillar[1],
               'hanja': day_pillar[2], 'branch_hanja': day_pillar[3]},
        'hour': {'ko': hour_pillar[0], 'branch_ko': hour_pillar[1],
                'hanja': hour_pillar[2], 'branch_hanja': hour_pillar[3]},
        'elements': {
            'year': {'stem': get_element(year_pillar[0]), 'branch': get_element(year_pillar[1], False)},
            'month': {'stem': get_element(month_pillar[0]), 'branch': get_element(month_pillar[1], False)},
            'day': {'stem': get_element(day_pillar[0]), 'branch': get_element(day_pillar[1], False)},
            'hour': {'stem': get_element(hour_pillar[0]), 'branch': get_element(hour_pillar[1], False)}
        },
        'yin_yang': {
            'year': {'stem': get_yin_yang(year_pillar[0]), 'branch': get_yin_yang(year_pillar[1], False)},
            'month': {'stem': get_yin_yang(month_pillar[0]), 'branch': get_yin_yang(month_pillar[1], False)},
            'day': {'stem': get_yin_yang(day_pillar[0]), 'branch': get_yin_yang(day_pillar[1], False)},
            'hour': {'stem': get_yin_yang(hour_pillar[0]), 'branch': get_yin_yang(hour_pillar[1], False)}
        }
    }
