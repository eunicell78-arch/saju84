"""
세운(歲運) 계산 모듈
Annual Luck Calculator Module
"""
from datetime import datetime

# 60갑자
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 60갑자 리스트 생성
SIXTY_JIAZI = []
for i in range(60):
    stem = STEMS[i % 10]
    branch = BRANCHES[i % 12]
    SIXTY_JIAZI.append(stem + branch)


def get_year_jiazi(year: int) -> str:
    """
    특정 연도의 간지 계산
    
    Args:
        year: 연도 (예: 2024)
    
    Returns:
        간지 (예: '甲辰')
    """
    # 1984년 = 甲子년 기준
    base_year = 1984
    offset = (year - base_year) % 60
    return SIXTY_JIAZI[offset]


def get_korean_age(birth_year: int, target_year: int) -> int:
    """
    한국 나이 계산 (전통나이)
    
    Args:
        birth_year: 출생년도
        target_year: 계산할 연도
    
    Returns:
        한국 나이
    """
    return target_year - birth_year + 1


def generate_seun(birth_year: int, current_year: int, past_years: int = 5, future_years: int = 10) -> list:
    """
    세운표 생성
    
    Args:
        birth_year: 출생년도
        current_year: 현재년도
        past_years: 과거 몇 년을 표시할지
        future_years: 미래 몇 년을 표시할지
    
    Returns:
        세운 리스트 [{'년도', '간지', '나이', '현재여부'}, ...]
    """
    seun_list = []
    
    start_year = current_year - past_years
    end_year = current_year + future_years
    
    for year in range(start_year, end_year + 1):
        jiazi = get_year_jiazi(year)
        age = get_korean_age(birth_year, year)
        is_current = (year == current_year)
        
        seun_list.append({
            '년도': year,
            '간지': jiazi,
            '나이': age,
            '현재': is_current
        })
    
    return seun_list


def get_current_seun_info(birth_year: int, current_year: int = None) -> dict:
    """
    현재 세운 정보
    
    Args:
        birth_year: 출생년도
        current_year: 현재년도 (None이면 시스템 현재년도)
    
    Returns:
        {'년도', '간지', '나이'}
    """
    if current_year is None:
        current_year = datetime.now().year
    
    jiazi = get_year_jiazi(current_year)
    age = get_korean_age(birth_year, current_year)
    
    return {
        '년도': current_year,
        '간지': jiazi,
        '나이': age
    }


if __name__ == '__main__':
    # 테스트
    birth_year = 2009
    current_year = 2026
    
    print(f"=== 세운 테스트: {birth_year}년생, 현재 {current_year}년 ===\n")
    
    # 현재 세운
    current_seun = get_current_seun_info(birth_year, current_year)
    print(f"현재: {current_seun['년도']}년 {current_seun['간지']} ({current_seun['나이']}세)\n")
    
    # 세운표
    seun_list = generate_seun(birth_year, current_year, past_years=3, future_years=5)
    
    print("세운표:")
    for seun in seun_list:
        marker = " ← 현재" if seun['현재'] else ""
        print(f"{seun['년도']}년 {seun['간지']:4} ({seun['나이']:2}세){marker}")
    
    # 특정 연도 테스트
    print("\n=== 연도별 간지 확인 ===")
    test_years = [2024, 2025, 2026]
    for year in test_years:
        jiazi = get_year_jiazi(year)
        print(f"{year}년: {jiazi}")
