"""
대운(大運) 계산 모듈
Great Fortune Calculation Module

대운은 10년 단위의 큰 운세를 나타냄
"""
from datetime import datetime, timedelta

# 60갑자 순서
JIAZI_60 = []
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

for i in range(60):
    JIAZI_60.append(STEMS[i % 10] + BRANCHES[i % 12])

# 24절기 근사 날짜 (양력 기준, 간단히 처리)
# 실제로는 천문학적 계산이 필요하지만, 여기서는 근사값 사용
SOLAR_TERMS = {
    1: (6, '小寒'), 2: (4, '立春'), 3: (6, '驚蟄'), 4: (5, '清明'),
    5: (6, '立夏'), 6: (6, '芒種'), 7: (7, '小暑'), 8: (8, '立秋'),
    9: (8, '白露'), 10: (8, '寒露'), 11: (8, '立冬'), 12: (7, '大雪')
}


def get_daeun_direction(gender: str, year_stem: str) -> str:
    """
    대운 순행/역행 판단
    
    양남음녀: 순행 (양년생 남자, 음년생 여자)
    음남양녀: 역행 (음년생 남자, 양년생 여자)
    """
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    is_yang_year = year_stem in yang_stems
    
    if gender == '남':
        return '순행' if is_yang_year else '역행'
    else:  # 여
        return '순행' if not is_yang_year else '역행'


def calculate_daeun_start_age(birth_date: datetime, gender: str, year_stem: str, month: int) -> int:
    """
    대운 시작 나이 계산
    
    생일부터 다음/이전 절입까지의 일수를 계산하여
    3일 = 1년 공식 적용
    """
    direction = get_daeun_direction(gender, year_stem)
    
    # 절입일 근사 (실제로는 정확한 만세력 데이터 필요)
    # 여기서는 간단히 처리
    term_day = SOLAR_TERMS.get(month, (5, ''))[0]
    
    if direction == '순행':
        # 다음 절입까지
        if birth_date.day < term_day:
            days = term_day - birth_date.day
        else:
            # 다음 달 절입
            next_month = month + 1 if month < 12 else 1
            next_term_day = SOLAR_TERMS.get(next_month, (5, ''))[0]
            days_in_month = 30  # 간단히 30일로 근사
            days = (days_in_month - birth_date.day) + next_term_day
    else:
        # 이전 절입까지
        if birth_date.day > term_day:
            days = birth_date.day - term_day
        else:
            # 이전 달 절입
            prev_month = month - 1 if month > 1 else 12
            prev_term_day = SOLAR_TERMS.get(prev_month, (5, ''))[0]
            days = birth_date.day + (30 - prev_term_day)  # 간단히 근사
    
    # 3일 = 1년 공식
    daeun_age = (days // 3) + 1
    
    # 최소 1세, 최대 10세로 제한 (일반적 범위)
    return max(1, min(10, daeun_age))


def generate_daeun(month_stem: str, month_branch: str, direction: str, 
                   start_age: int, count: int = 10) -> list:
    """
    대운표 생성
    
    Args:
        month_stem: 월간
        month_branch: 월지
        direction: '순행' 또는 '역행'
        start_age: 대운 시작 나이
        count: 생성할 대운 개수 (기본 10개)
    
    Returns:
        [{'age': 나이, 'stem': 천간, 'branch': 지지, 'pillar': 간지}, ...]
    """
    # 월주의 60갑자 인덱스 찾기
    month_pillar = month_stem + month_branch
    
    try:
        current_idx = JIAZI_60.index(month_pillar)
    except ValueError:
        # 찾을 수 없으면 0부터 시작
        current_idx = 0
    
    daeun_list = []
    
    for i in range(count):
        age = start_age + (i * 10)
        
        if direction == '순행':
            pillar_idx = (current_idx + i + 1) % 60
        else:  # 역행
            pillar_idx = (current_idx - i - 1) % 60
        
        pillar = JIAZI_60[pillar_idx]
        stem = pillar[0]
        branch = pillar[1]
        
        daeun_list.append({
            'age': age,
            'stem': stem,
            'branch': branch,
            'pillar': pillar
        })
    
    return daeun_list


def calculate_daeun(birth_date: datetime, gender: str, 
                    year_stem: str, month_stem: str, month_branch: str) -> dict:
    """
    대운 종합 계산
    
    Returns:
        {
            'direction': '순행' or '역행',
            'start_age': 시작 나이,
            'list': 대운 목록
        }
    """
    direction = get_daeun_direction(gender, year_stem)
    start_age = calculate_daeun_start_age(birth_date, gender, year_stem, birth_date.month)
    daeun_list = generate_daeun(month_stem, month_branch, direction, start_age)
    
    return {
        'direction': direction,
        'start_age': start_age,
        'list': daeun_list
    }
