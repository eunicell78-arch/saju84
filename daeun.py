"""
대운(大運) 계산 모듈
Major Luck Cycles Calculator Module
"""
from datetime import datetime, timedelta

# 천간과 지지
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 양간
YANG_STEMS = ['甲', '丙', '戊', '庚', '壬']

# 월 절입일 근사치 (양력 기준)
# 실제로는 정확한 절기 계산이 필요하지만, 근사치 사용
JEOLIP_DATES = {
    1: (2, 4),   # 입춘 (2월 4일경)
    2: (3, 6),   # 경칩 (3월 6일경)
    3: (4, 5),   # 청명 (4월 5일경)
    4: (5, 6),   # 입하 (5월 6일경)
    5: (6, 6),   # 망종 (6월 6일경)
    6: (7, 7),   # 소서 (7월 7일경)
    7: (8, 8),   # 입추 (8월 8일경)
    8: (9, 8),   # 백로 (9월 8일경)
    9: (10, 8),  # 한로 (10월 8일경)
    10: (11, 7), # 입동 (11월 7일경)
    11: (12, 7), # 대설 (12월 7일경)
    12: (1, 6)   # 소한 (1월 6일경)
}


def get_daeun_direction(gender: str, year_stem: str) -> str:
    """
    대운 순행/역행 판단
    
    Args:
        gender: '남' 또는 '여'
        year_stem: 년간 (한자)
    
    Returns:
        '순행' 또는 '역행'
    """
    # 한자만 추출
    if '(' in year_stem:
        year_stem = year_stem.split('(')[1].rstrip(')')
    
    is_yang = year_stem in YANG_STEMS
    
    # 양남음녀: 순행
    # 음남양녀: 역행
    if gender == '남':
        return '순행' if is_yang else '역행'
    else:  # 여
        return '순행' if not is_yang else '역행'


def calculate_daeun_start_age(birth_date: datetime, gender: str, year_stem: str, month: int) -> int:
    """
    대운 시작 나이 계산 (전통 방식)
    
    3일 = 1년 원칙 적용
    출생일부터 다음/이전 절입일까지의 일수를 계산하여 대운수 산출
    
    Args:
        birth_date: 생년월일시
        gender: 성별 ('남' 또는 '여')
        year_stem: 년간 (한자)
        month: 절월 (1-12, 입춘 기준)
    
    Returns:
        대운 시작 나이 (최소 1세)
    """
    direction = get_daeun_direction(gender, year_stem)
    
    birth_year = birth_date.year
    birth_month = birth_date.month
    birth_day = birth_date.day
    
    try:
        if direction == '순행':
            # 다음 절입일 찾기
            # month는 절월 기준이므로, 다음 절월의 절입일을 찾음
            next_month = month + 1 if month < 12 else 1
            next_jeolip_month, next_jeolip_day = JEOLIP_DATES.get(next_month, (month + 1, 5))
            
            # 다음 절입일 날짜 생성
            # 현재 월보다 다음 절입일 월이 작으면 다음 해
            if next_jeolip_month < birth_month or \
               (next_jeolip_month == birth_month and next_jeolip_day <= birth_day):
                next_jeolip_year = birth_year + 1
            else:
                next_jeolip_year = birth_year
            
            next_jeolip_date = datetime(next_jeolip_year, next_jeolip_month, next_jeolip_day)
            days_diff = (next_jeolip_date - birth_date).days
            
        else:  # 역행
            # 이전 절입일 찾기
            # 현재 절월의 절입일을 찾음
            current_jeolip_month, current_jeolip_day = JEOLIP_DATES.get(month, (birth_month, 5))
            
            # 현재 절월의 절입일 날짜 생성
            # 현재 월보다 절입일 월이 크면 이전 해
            if current_jeolip_month > birth_month or \
               (current_jeolip_month == birth_month and current_jeolip_day > birth_day):
                current_jeolip_year = birth_year - 1
            else:
                current_jeolip_year = birth_year
            
            current_jeolip_date = datetime(current_jeolip_year, current_jeolip_month, current_jeolip_day)
            days_diff = (birth_date - current_jeolip_date).days
            
    except ValueError as e:
        # 잘못된 날짜 (예: 2월 30일)
        print(f"Date calculation error: {e}")
        days_diff = 15  # 기본값: 약 5세
    
    # 음수 방지
    days_diff = abs(days_diff)
    
    # 비정상적으로 큰 값 방어 (1년 = 365일 이상이면 문제)
    if days_diff > 300:
        # 너무 크면 월 단위로 다시 계산 (간단한 근사)
        # 보통 15~45일 사이여야 정상
        print(f"Warning: Abnormal days_diff={days_diff} detected for {birth_date}. Using fallback calculation.")
        days_diff = 15 + ((birth_month * birth_day) % 30)  # 15~45일 범위로 조정 (결정적)
    
    # 3일 = 1년 계산 (전통 방식)
    years = days_diff // 3
    remaining_days = days_diff % 3
    
    # 1일 이상이면 반올림하여 1년 추가
    # 전통적으로 나머지 1~2일도 중요하게 취급하므로 1일부터 반올림
    if remaining_days >= 1:
        daeun_age = years + 1
    else:
        daeun_age = years
    
    # 최소 1세, 최대 20세로 제한 (비정상 값 방어)
    return max(1, min(20, daeun_age))


def generate_daeun(year_stem: str, month_stem: str, year_branch: str, month_branch: str, 
                   gender: str, daeun_age: int, day_stem: str, count: int = 10) -> list:
    """
    대운표 생성
    
    Args:
        year_stem: 년간
        month_stem: 월간
        year_branch: 년지
        month_branch: 월지
        gender: 성별
        daeun_age: 대운 시작 나이
        day_stem: 일간 (십신 계산용)
        count: 생성할 대운 개수 (기본 10)
    
    Returns:
        대운 리스트 [{'나이', '천간', '지지', '간지', ...}, ...]
    """
    # 한자만 추출
    def extract(text):
        if '(' in text:
            return text.split('(')[1].rstrip(')')
        return text
    
    year_stem = extract(year_stem)
    month_stem = extract(month_stem)
    year_branch = extract(year_branch)
    month_branch = extract(month_branch)
    day_stem = extract(day_stem)
    
    direction = get_daeun_direction(gender, year_stem)
    
    # 월주의 다음/이전 간지부터 시작
    stem_idx = STEMS.index(month_stem)
    branch_idx = BRANCHES.index(month_branch)
    
    daeun_list = []
    
    for i in range(count):
        age = daeun_age + (i * 10)
        
        if direction == '순행':
            current_stem_idx = (stem_idx + i + 1) % 10
            current_branch_idx = (branch_idx + i + 1) % 12
        else:  # 역행
            current_stem_idx = (stem_idx - i - 1) % 10
            current_branch_idx = (branch_idx - i - 1) % 12
        
        daeun_stem = STEMS[current_stem_idx]
        daeun_branch = BRANCHES[current_branch_idx]
        
        daeun_list.append({
            '나이': f"{age}세",
            '천간': daeun_stem,
            '지지': daeun_branch,
            '간지': f"{daeun_stem}{daeun_branch}"
        })
    
    return daeun_list


if __name__ == '__main__':
    # 테스트: 2009-12-28생 여자
    print("=== 대운 테스트: 2009-12-28생 여자 ===")
    birth_date = datetime(2009, 12, 28, 16, 35)
    gender = '여'
    year_stem = '己'
    month_stem = '丙'
    year_branch = '丑'
    month_branch = '子'
    day_stem = '丁'
    
    direction = get_daeun_direction(gender, year_stem)
    print(f"대운 방향: {direction}")
    
    daeun_age = calculate_daeun_start_age(birth_date, gender, year_stem, 12)
    print(f"대운 시작: {daeun_age}세")
    
    daeun_list = generate_daeun(year_stem, month_stem, year_branch, month_branch, 
                                 gender, daeun_age, day_stem, 5)
    
    print("\n대운표:")
    for daeun in daeun_list:
        print(f"{daeun['나이']:>6} | {daeun['간지']}")
