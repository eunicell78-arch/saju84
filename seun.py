"""
세운(歲運) 계산 모듈
Year Fortune Calculation Module

매년의 간지를 계산
"""

# 60갑자
JIAZI_60 = []
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

for i in range(60):
    JIAZI_60.append(STEMS[i % 10] + BRANCHES[i % 12])


def get_year_jiazi(year: int) -> str:
    """
    연도의 간지 계산
    
    기준: 1984년 = 甲子년
    """
    base_year = 1984
    offset = (year - base_year) % 60
    return JIAZI_60[offset]


def calculate_seun(birth_year: int, current_year: int, past_years: int = 5, 
                   future_years: int = 10) -> list:
    """
    세운 계산 (과거~현재~미래)
    
    Args:
        birth_year: 출생년도
        current_year: 현재년도
        past_years: 과거 몇 년
        future_years: 미래 몇 년
    
    Returns:
        [{'year': 연도, 'jiazi': 간지, 'age': 나이, 'is_current': bool}, ...]
    """
    seun_list = []
    
    start_year = current_year - past_years
    end_year = current_year + future_years
    
    for year in range(start_year, end_year + 1):
        jiazi = get_year_jiazi(year)
        age = year - birth_year + 1  # 한국 나이
        
        seun_list.append({
            'year': year,
            'jiazi': jiazi,
            'age': age,
            'is_current': (year == current_year)
        })
    
    return seun_list
