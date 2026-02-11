"""
사주팔자 계산 모듈
Four Pillars (Saju) Calculator Module
"""
from datetime import datetime
from typing import Dict, Tuple

# 천간 (Heavenly Stems) - 10개
HEAVENLY_STEMS = ['갑(甲)', '을(乙)', '병(丙)', '정(丁)', '무(戊)', '기(己)', '경(庚)', '신(辛)', '임(壬)', '계(癸)']
HEAVENLY_STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 지지 (Earthly Branches) - 12개
EARTHLY_BRANCHES = ['자(子)', '축(丑)', '인(寅)', '묘(卯)', '진(辰)', '사(巳)', '오(午)', '미(未)', '신(申)', '유(酉)', '술(戌)', '해(亥)']
EARTHLY_BRANCHES_HANJA = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 오행 (Five Elements)
STEM_ELEMENTS = {
    '갑(甲)': '목(木)', '을(乙)': '목(木)',
    '병(丙)': '화(火)', '정(丁)': '화(火)',
    '무(戊)': '토(土)', '기(己)': '토(土)',
    '경(庚)': '금(金)', '신(辛)': '금(金)',
    '임(壬)': '수(水)', '계(癸)': '수(水)'
}

BRANCH_ELEMENTS = {
    '자(子)': '수(水)', '축(丑)': '토(土)', '인(寅)': '목(木)', '묘(卯)': '목(木)',
    '진(辰)': '토(土)', '사(巳)': '화(火)', '오(午)': '화(火)', '미(未)': '토(土)',
    '신(申)': '금(金)', '유(酉)': '금(金)', '술(戌)': '토(土)', '해(亥)': '수(水)'
}

# 음양 (Yin-Yang)
STEM_YIN_YANG = {
    '갑(甲)': '양', '을(乙)': '음',
    '병(丙)': '양', '정(丁)': '음',
    '무(戊)': '양', '기(己)': '음',
    '경(庚)': '양', '신(辛)': '음',
    '임(壬)': '양', '계(癸)': '음'
}

BRANCH_YIN_YANG = {
    '자(子)': '양', '축(丑)': '음', '인(寅)': '양', '묘(卯)': '음',
    '진(辰)': '양', '사(巳)': '음', '오(午)': '양', '미(未)': '음',
    '신(申)': '양', '유(酉)': '음', '술(戌)': '양', '해(亥)': '음'
}

# 월별 지지 (양력 기준 근사)
# 1월=丑, 2월=寅, 3월=卯, 4월=辰, 5월=巳, 6월=午, 7월=未, 8월=申, 9월=酉, 10월=戌, 11월=亥, 12월=子
MONTH_BRANCHES = ['축(丑)', '인(寅)', '묘(卯)', '진(辰)', '사(巳)', '오(午)', 
                  '미(未)', '신(申)', '유(酉)', '술(戌)', '해(亥)', '자(子)']

# 시간별 지지
HOUR_BRANCHES = {
    (23, 1): '자(子)', (1, 3): '축(丑)', (3, 5): '인(寅)', (5, 7): '묘(卯)',
    (7, 9): '진(辰)', (9, 11): '사(巳)', (11, 13): '오(午)', (13, 15): '미(未)',
    (15, 17): '신(申)', (17, 19): '유(酉)', (19, 21): '술(戌)', (21, 23): '해(亥)'
}


def get_stem_branch(year: int) -> Tuple[str, str]:
    """연도를 천간지지로 변환"""
    # 갑자년(1984)을 기준으로 계산
    base_year = 1984
    diff = year - base_year
    
    stem_idx = diff % 10
    branch_idx = diff % 12
    
    # 갑자(0,0) 시작
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return stem, branch


def get_month_pillar(year: int, month: int) -> Tuple[str, str]:
    """월주 계산"""
    # 월지는 양력 기준 근사 (1월=丑, 2월=寅, ..., 12월=子)
    branch = MONTH_BRANCHES[month - 1] if 1 <= month <= 12 else MONTH_BRANCHES[0]
    
    # 월간 계산: 년간에 따라 정해짐
    # 甲己년 → 丙寅월부터 (寅월 천간이 丙)
    # 乙庚년 → 戊寅월부터
    # 丙辛년 → 庚寅월부터
    # 丁壬년 → 壬寅월부터
    # 戊癸년 → 甲寅월부터
    
    year_stem_idx = (year - 1984) % 10
    
    # 월간 시작 인덱스 (寅월 기준)
    month_stem_start = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
    
    # 寅월부터 순서: 寅(2월), 卯(3월), 辰(4월), ..., 子(12월), 丑(1월)
    # 전통적 월 순서로 변환
    TRAD_MONTH_ORDER = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
    branch_hanja = branch.split('(')[1].replace(')', '')
    trad_month_idx = TRAD_MONTH_ORDER.index(branch_hanja)
    
    stem_idx = (month_stem_start[year_stem_idx] + trad_month_idx) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def get_day_pillar(date: datetime) -> Tuple[str, str]:
    """일주 계산 (간지 순환 계산)"""
    # 기준일: 1900년 1월 1일 = 甲戌일
    # 60갑자 순환으로 정확히 계산
    base_date = datetime(1900, 1, 1)
    days_diff = (date - base_date).days
    
    # 1900-01-01 = 甲戌 = 10번째 (0-based index)
    base_index = 10
    jiazi_index = (base_index + days_diff) % 60
    
    stem_idx = jiazi_index % 10
    branch_idx = jiazi_index % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return stem, branch


def get_hour_pillar(date: datetime, day_stem: str) -> Tuple[str, str]:
    """시주 계산"""
    hour = date.hour
    
    # 시지 찾기
    # 23시는 다음날 자시가 아니라 당일 자시로 처리 (야자시 제거)
    branch = '자(子)'  # 기본값
    for (start, end), b in HOUR_BRANCHES.items():
        if start <= hour < end:
            branch = b
            break
        elif start > end:  # 자시(23-01)의 경우
            if hour >= start or hour < end:
                branch = b
                break
    
    # 시간 계산 (일간에 따라 달라짐 - 시두법)
    # 甲己일 → 甲子시부터
    # 乙庚일 → 丙子시부터
    # 丙辛일 → 戊子시부터
    # 丁壬일 → 庚子시부터
    # 戊癸일 → 壬子시부터
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    hour_stem_start = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
    
    # 시지 인덱스 찾기
    branch_idx = EARTHLY_BRANCHES.index(branch)
    stem_idx = (hour_stem_start[day_stem_idx] + branch_idx) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def calculate_four_pillars(birth_date: datetime) -> Dict:
    """사주팔자 계산"""
    year = birth_date.year
    month = birth_date.month
    
    # 연주
    year_stem, year_branch = get_stem_branch(year)
    
    # 월주
    month_stem, month_branch = get_month_pillar(year, month)
    
    # 일주
    day_stem, day_branch = get_day_pillar(birth_date)
    
    # 시주
    hour_stem, hour_branch = get_hour_pillar(birth_date, day_stem)
    
    # 오행 분석
    stems = [year_stem, month_stem, day_stem, hour_stem]
    branches = [year_branch, month_branch, day_branch, hour_branch]
    
    stems_elements = [STEM_ELEMENTS[s] for s in stems]
    branches_elements = [BRANCH_ELEMENTS[b] for b in branches]
    
    # 음양 분석
    stems_yin_yang = [STEM_YIN_YANG[s] for s in stems]
    branches_yin_yang = [BRANCH_YIN_YANG[b] for b in branches]
    
    return {
        'year_pillar': f"{year_stem}{year_branch}",
        'month_pillar': f"{month_stem}{month_branch}",
        'day_pillar': f"{day_stem}{day_branch}",
        'hour_pillar': f"{hour_stem}{hour_branch}",
        'year_stem': year_stem,
        'year_branch': year_branch,
        'month_stem': month_stem,
        'month_branch': month_branch,
        'day_stem': day_stem,
        'day_branch': day_branch,
        'hour_stem': hour_stem,
        'hour_branch': hour_branch,
        'stems_elements': stems_elements,
        'branches_elements': branches_elements,
        'stems_yin_yang': stems_yin_yang,
        'branches_yin_yang': branches_yin_yang,
        'birth_date': birth_date.strftime('%Y년 %m월 %d일 %H시'),
        'year_hanja': f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]}",
        'month_hanja': f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]}",
        'day_hanja': f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]}",
        'hour_hanja': f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]}"
    }


def get_element_count(result: Dict) -> Dict[str, int]:
    """오행 개수 계산"""
    all_elements = result['stems_elements'] + result['branches_elements']
    element_count = {
        '목(木)': 0, '화(火)': 0, '토(土)': 0, '금(金)': 0, '수(水)': 0
    }
    for elem in all_elements:
        element_count[elem] = element_count.get(elem, 0) + 1
    
    return element_count
