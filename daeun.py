"""
대운(大運) 계산 모듈
Great Fortune Calculation Module
"""
from datetime import datetime, timedelta

# 60갑자 순환
SIXTY_JIAZI = [
    ('甲', '子'), ('乙', '丑'), ('丙', '寅'), ('丁', '卯'), ('戊', '辰'), ('己', '巳'),
    ('庚', '午'), ('辛', '未'), ('壬', '申'), ('癸', '酉'), ('甲', '戌'), ('乙', '亥'),
    ('丙', '子'), ('丁', '丑'), ('戊', '寅'), ('己', '卯'), ('庚', '辰'), ('辛', '巳'),
    ('壬', '午'), ('癸', '未'), ('甲', '申'), ('乙', '酉'), ('丙', '戌'), ('丁', '亥'),
    ('戊', '子'), ('己', '丑'), ('庚', '寅'), ('辛', '卯'), ('壬', '辰'), ('癸', '巳'),
    ('甲', '午'), ('乙', '未'), ('丙', '申'), ('丁', '酉'), ('戊', '戌'), ('己', '亥'),
    ('庚', '子'), ('辛', '丑'), ('壬', '寅'), ('癸', '卯'), ('甲', '辰'), ('乙', '巳'),
    ('丙', '午'), ('丁', '未'), ('戊', '申'), ('己', '酉'), ('庚', '戌'), ('辛', '亥'),
    ('壬', '子'), ('癸', '丑'), ('甲', '寅'), ('乙', '卯'), ('丙', '辰'), ('丁', '巳'),
    ('戊', '午'), ('己', '未'), ('庚', '申'), ('辛', '酉'), ('壬', '戌'), ('癸', '亥')
]

# 절입일 근사 (매년 양력 날짜)
JEOLIP_DATES = [
    (2, 4),   # 입춘
    (3, 6),   # 경칩
    (4, 5),   # 청명
    (5, 6),   # 입하
    (6, 6),   # 망종
    (7, 7),   # 소서
    (8, 8),   # 입추
    (9, 8),   # 백로
    (10, 8),  # 한로
    (11, 7),  # 입동
    (12, 7),  # 대설
    (1, 6),   # 소한
]


def get_daeun_direction(gender: str, year_stem_hanja: str) -> str:
    """
    대운 순행/역행 판단
    
    양남음녀: 순행 (양년생 남자, 음년생 여자)
    음남양녀: 역행 (음년생 남자, 양년생 여자)
    
    Args:
        gender: '남' 또는 '여'
        year_stem_hanja: 년간 한자 (예: '己')
    
    Returns:
        '순행' 또는 '역행'
    """
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    year_stem_yang = year_stem_hanja in yang_stems
    
    if gender == '남':
        return '순행' if year_stem_yang else '역행'
    else:  # 여
        return '순행' if not year_stem_yang else '역행'


def find_next_jeolip(birth_date: datetime) -> datetime:
    """다음 절입일 찾기 (간략화)"""
    month = birth_date.month
    day = birth_date.day
    
    # 현재 월의 절입일 찾기
    for jeolip_month, jeolip_day in JEOLIP_DATES:
        if jeolip_month == month:
            if day < jeolip_day:
                # 이번 달 절입
                return datetime(birth_date.year, month, jeolip_day)
            else:
                # 다음 절입 찾기
                next_idx = JEOLIP_DATES.index((month, jeolip_day)) + 1
                if next_idx >= len(JEOLIP_DATES):
                    next_idx = 0
                next_month, next_day = JEOLIP_DATES[next_idx]
                
                if next_month > month:
                    return datetime(birth_date.year, next_month, next_day)
                else:
                    return datetime(birth_date.year + 1, next_month, next_day)
    
    # 기본값: 다음 입춘
    return datetime(birth_date.year + 1, 2, 4)


def find_prev_jeolip(birth_date: datetime) -> datetime:
    """이전 절입일 찾기 (간략화)"""
    month = birth_date.month
    day = birth_date.day
    
    # 현재 월의 절입일 찾기
    for jeolip_month, jeolip_day in JEOLIP_DATES:
        if jeolip_month == month:
            if day >= jeolip_day:
                # 이번 달 절입
                return datetime(birth_date.year, month, jeolip_day)
            else:
                # 이전 절입 찾기
                prev_idx = JEOLIP_DATES.index((month, jeolip_day)) - 1
                if prev_idx < 0:
                    prev_idx = len(JEOLIP_DATES) - 1
                prev_month, prev_day = JEOLIP_DATES[prev_idx]
                
                if prev_month < month:
                    return datetime(birth_date.year, prev_month, prev_day)
                else:
                    return datetime(birth_date.year - 1, prev_month, prev_day)
    
    # 기본값: 이전 입춘
    return datetime(birth_date.year - 1, 2, 4)


def calculate_daeun_age(birth_date: datetime, direction: str) -> int:
    """
    대운 시작 나이 계산
    
    3일 = 1년
    
    Args:
        birth_date: 생년월일시
        direction: '순행' 또는 '역행'
    
    Returns:
        대운 시작 나이 (만 나이 + 3)
    """
    if direction == '순행':
        jeolip = find_next_jeolip(birth_date)
    else:
        jeolip = find_prev_jeolip(birth_date)
    
    days = abs((jeolip - birth_date).days)
    daeun_age = (days // 3) + 3  # 3일=1년, 최소 3세
    
    return daeun_age


def get_daeun_pillars(month_stem_hanja: str, month_branch_hanja: str, 
                      direction: str, count: int = 10) -> list:
    """
    대운 기둥 생성
    
    Args:
        month_stem_hanja: 월간 한자
        month_branch_hanja: 월지 한자
        direction: '순행' 또는 '역행'
        count: 생성할 대운 개수 (기본 10개)
    
    Returns:
        대운 기둥 리스트 [(천간, 지지), ...]
    """
    # 월주의 60갑자 인덱스 찾기
    month_pillar = (month_stem_hanja, month_branch_hanja)
    
    try:
        current_idx = SIXTY_JIAZI.index(month_pillar)
    except ValueError:
        # 찾을 수 없으면 기본값
        current_idx = 0
    
    daeun_list = []
    for i in range(count):
        if direction == '순행':
            idx = (current_idx + i + 1) % 60
        else:  # 역행
            idx = (current_idx - i - 1) % 60
        
        daeun_list.append(SIXTY_JIAZI[idx])
    
    return daeun_list


def calculate_daeun(birth_date: datetime, gender: str, 
                    year_stem_hanja: str, month_stem_hanja: str, 
                    month_branch_hanja: str, birth_year: int) -> dict:
    """
    대운 전체 계산
    
    Returns:
        {
            'direction': '순행' or '역행',
            'start_age': 3,
            'pillars': [
                {'age': 3, 'stem': '己', 'branch': '丑'},
                ...
            ]
        }
    """
    direction = get_daeun_direction(gender, year_stem_hanja)
    start_age = calculate_daeun_age(birth_date, direction)
    pillars = get_daeun_pillars(month_stem_hanja, month_branch_hanja, direction, 10)
    
    result_pillars = []
    current_age = start_age
    for stem, branch in pillars:
        result_pillars.append({
            'age': current_age,
            'stem': stem,
            'branch': branch
        })
        current_age += 10
    
    return {
        'direction': direction,
        'start_age': start_age,
        'pillars': result_pillars
    }
