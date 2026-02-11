"""
사주팔자 (Four Pillars of Destiny) Calculator Module
Calculates the Four Pillars based on birth date and time.
"""

from datetime import datetime
from typing import Dict, List

# 천간 (10 Heavenly Stems)
HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
STEMS_HANJA = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 지지 (12 Earthly Branches)
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
BRANCHES_HANJA = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 오행 (Five Elements)
STEMS_ELEMENTS = {
    "갑": "목(木)", "을": "목(木)",
    "병": "화(火)", "정": "화(火)",
    "무": "토(土)", "기": "토(土)",
    "경": "금(金)", "신": "금(金)",
    "임": "수(水)", "계": "수(水)"
}

BRANCHES_ELEMENTS = {
    "자": "수(水)", "축": "토(土)", "인": "목(木)", "묘": "목(木)",
    "진": "토(土)", "사": "화(火)", "오": "화(火)", "미": "토(土)",
    "신": "금(金)", "유": "금(金)", "술": "토(土)", "해": "수(水)"
}

# 월령 (Monthly Branch) - 절기 기준
MONTH_BRANCHES = {
    1: 11,  # 인월 (입춘~경칩)
    2: 0,   # 묘월 (경칩~청명)
    3: 1,   # 진월 (청명~입하)
    4: 2,   # 사월 (입하~망종)
    5: 3,   # 오월 (망종~소서)
    6: 4,   # 미월 (소서~입추)
    7: 5,   # 신월 (입추~백로)
    8: 6,   # 유월 (백로~한로)
    9: 7,   # 술월 (한로~입동)
    10: 8,  # 해월 (입동~대설)
    11: 9,  # 자월 (대설~소한)
    12: 10  # 축월 (소한~입춘)
}


def calculate_year_pillar(year: int) -> tuple:
    """
    연주(年柱) 계산
    갑자년을 기준으로 60갑자 순환
    """
    # 기준: 1984년 = 갑자년
    base_year = 1984
    cycle_year = (year - base_year) % 60
    
    stem_idx = cycle_year % 10
    branch_idx = cycle_year % 12
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def calculate_month_pillar(year: int, month: int) -> tuple:
    """
    월주(月柱) 계산
    연간에 따른 월간 계산 (※ 실제로는 절기 기준이지만 단순화)
    """
    # 연간의 천간에 따라 월간 계산
    year_stem = calculate_year_pillar(year)[0]
    year_stem_idx = HEAVENLY_STEMS.index(year_stem)
    
    # 월간 계산 공식
    if year_stem_idx in [0, 5]:  # 갑기년
        month_stem_base = 2  # 병
    elif year_stem_idx in [1, 6]:  # 을경년
        month_stem_base = 4  # 무
    elif year_stem_idx in [2, 7]:  # 병신년
        month_stem_base = 6  # 경
    elif year_stem_idx in [3, 8]:  # 정임년
        month_stem_base = 8  # 임
    else:  # 무계년
        month_stem_base = 0  # 갑
    
    month_stem_idx = (month_stem_base + month - 1) % 10
    month_branch_idx = (month + 1) % 12
    
    return HEAVENLY_STEMS[month_stem_idx], EARTHLY_BRANCHES[month_branch_idx]


def calculate_day_pillar(year: int, month: int, day: int) -> tuple:
    """
    일주(日柱) 계산
    기준일로부터 날짜 차이를 이용한 60갑자 계산
    """
    # 기준: 1900년 1월 1일 = 갑자일
    base_date = datetime(1900, 1, 1)
    target_date = datetime(year, month, day)
    
    days_diff = (target_date - base_date).days
    cycle_day = days_diff % 60
    
    stem_idx = cycle_day % 10
    branch_idx = cycle_day % 12
    
    return HEAVENLY_STEMS[stem_idx], EARTHLY_BRANCHES[branch_idx]


def calculate_hour_pillar(year: int, month: int, day: int, hour: int) -> tuple:
    """
    시주(時柱) 계산
    일간에 따른 시간 계산
    """
    # 일간 구하기
    day_stem = calculate_day_pillar(year, month, day)[0]
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    
    # 시지 계산 (2시간 단위)
    hour_branch_idx = ((hour + 1) // 2) % 12
    
    # 시간 계산 공식
    if day_stem_idx in [0, 5]:  # 갑기일
        hour_stem_base = 0  # 갑
    elif day_stem_idx in [1, 6]:  # 을경일
        hour_stem_base = 2  # 병
    elif day_stem_idx in [2, 7]:  # 병신일
        hour_stem_base = 4  # 무
    elif day_stem_idx in [3, 8]:  # 정임일
        hour_stem_base = 6  # 경
    else:  # 무계일
        hour_stem_base = 8  # 임
    
    hour_stem_idx = (hour_stem_base + hour_branch_idx) % 10
    
    return HEAVENLY_STEMS[hour_stem_idx], EARTHLY_BRANCHES[hour_branch_idx]


def calculate_four_pillars(year: int, month: int, day: int, hour: int, gender: str = "남") -> Dict:
    """
    사주팔자 전체 계산
    
    Args:
        year: 출생 연도
        month: 출생 월
        day: 출생 일
        hour: 출생 시간 (0-23)
        gender: 성별 ("남" 또는 "여")
    
    Returns:
        사주팔자 정보를 담은 딕셔너리
    """
    # 각 기둥 계산
    year_stem, year_branch = calculate_year_pillar(year)
    month_stem, month_branch = calculate_month_pillar(year, month)
    day_stem, day_branch = calculate_day_pillar(year, month, day)
    hour_stem, hour_branch = calculate_hour_pillar(year, month, day, hour)
    
    # 오행 분석
    stems = [year_stem, month_stem, day_stem, hour_stem]
    branches = [year_branch, month_branch, day_branch, hour_branch]
    
    stems_elements = [STEMS_ELEMENTS[s] for s in stems]
    branches_elements = [BRANCHES_ELEMENTS[b] for b in branches]
    
    # 오행 카운트
    element_count = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
    for elem in stems_elements + branches_elements:
        elem_key = elem.split("(")[0]
        element_count[elem_key] = element_count.get(elem_key, 0) + 1
    
    result = {
        # 기본 정보
        "birth_date": f"{year}년 {month}월 {day}일 {hour}시",
        "gender": gender,
        
        # 사주팔자
        "year_pillar": f"{year_stem}{year_branch}",
        "year_hanja": f"{STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]}{BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]}",
        
        "month_pillar": f"{month_stem}{month_branch}",
        "month_hanja": f"{STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]}{BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]}",
        
        "day_pillar": f"{day_stem}{day_branch}",
        "day_hanja": f"{STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]}{BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]}",
        
        "hour_pillar": f"{hour_stem}{hour_branch}",
        "hour_hanja": f"{STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]}{BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]}",
        
        # 천간/지지
        "stems": stems,
        "branches": branches,
        
        # 오행 정보
        "stems_elements": stems_elements,
        "branches_elements": branches_elements,
        "element_count": element_count,
        
        # 일간 (본인)
        "day_stem": day_stem,
        "day_stem_element": STEMS_ELEMENTS[day_stem]
    }
    
    return result


def format_saju_display(result: Dict) -> str:
    """
    사주팔자를 보기 좋게 포맷팅
    """
    output = []
    output.append("=" * 50)
    output.append(f"📅 생년월일시: {result['birth_date']} ({result['gender']})")
    output.append("=" * 50)
    output.append("")
    output.append("【 사주팔자 四柱八字 】")
    output.append("")
    output.append(f"  時柱(시주)    日柱(일주)    月柱(월주)    年柱(연주)")
    output.append(f"  {result['hour_hanja']:^8}  {result['day_hanja']:^8}  {result['month_hanja']:^8}  {result['year_hanja']:^8}")
    output.append(f"  ({result['hour_pillar']})     ({result['day_pillar']})     ({result['month_pillar']})     ({result['year_pillar']})")
    output.append("")
    output.append("【 오행 분석 五行 】")
    output.append("")
    output.append(f"천간(天干): {' / '.join(result['stems_elements'])}")
    output.append(f"지지(地支): {' / '.join(result['branches_elements'])}")
    output.append("")
    output.append("오행 분포:")
    for element, count in result['element_count'].items():
        bar = "■" * count + "□" * (8 - count)
        output.append(f"  {element}(木火土金水): {bar} ({count})")
    output.append("")
    output.append(f"일간(日干): {result['day_stem']} - {result['day_stem_element']}")
    output.append("=" * 50)
    
    return "\n".join(output)
