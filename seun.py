"""
세운(歲運) 계산 모듈
Annual Fortune Calculation Module
"""

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


def get_year_jiazi(year: int) -> tuple:
    """
    연도를 60갑자로 변환
    
    1984년 = 甲子년 기준
    
    Args:
        year: 연도 (예: 2024)
    
    Returns:
        (천간, 지지) 튜플 (예: ('甲', '辰'))
    """
    base_year = 1984  # 甲子년
    offset = (year - base_year) % 60
    return SIXTY_JIAZI[offset]


def calculate_seun(birth_year: int, current_year: int, 
                   past_years: int = 5, future_years: int = 10) -> list:
    """
    세운(연운) 계산
    
    Args:
        birth_year: 출생 연도
        current_year: 현재 연도
        past_years: 과거 몇 년 (기본 5년)
        future_years: 미래 몇 년 (기본 10년)
    
    Returns:
        세운 리스트 [
            {'year': 2024, 'stem': '甲', 'branch': '辰', 'age': 41, 'is_current': True},
            ...
        ]
    """
    seun_list = []
    
    start_year = current_year - past_years
    end_year = current_year + future_years
    
    for year in range(start_year, end_year + 1):
        stem, branch = get_year_jiazi(year)
        age = year - birth_year + 1  # 전통 나이 (만 나이 + 1)
        
        seun_list.append({
            'year': year,
            'stem': stem,
            'branch': branch,
            'age': age,
            'is_current': (year == current_year)
        })
    
    return seun_list


def get_current_seun(birth_year: int, current_year: int) -> dict:
    """
    현재 세운만 가져오기
    
    Returns:
        {'year': 2024, 'stem': '甲', 'branch': '辰', 'age': 41}
    """
    stem, branch = get_year_jiazi(current_year)
    age = current_year - birth_year + 1
    
    return {
        'year': current_year,
        'stem': stem,
        'branch': branch,
        'age': age
    }
