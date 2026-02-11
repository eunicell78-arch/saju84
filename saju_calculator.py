"""
사주팔자 계산 모듈
Four Pillars (Saju) Calculator Module
"""
from datetime import datetime, timedelta
from typing import Dict, Tuple

# 천간 (Heavenly Stems) - 10개
HEAVENLY_STEMS = ['갑(甲)', '을(乙)', '병(丙)', '정(丁)', '무(戊)', '기(己)', '경(庚)', '신(辛)', '임(壬)', '계(癸)']
HEAVENLY_STEMS_HANJA = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 지지 (Earthly Branches) - 12개
EARTHLY_BRANCHES = ['자(子)', '축(丑)', '인(寅)', '묘(卯)', '진(辰)', '사(巳)', '오(午)', '미(未)', '신(申)', '유(酉)', '술(戌)', '해(亥)']
EARTHLY_BRANCHES_HANJA = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 60갑자 (60 Jiazi Cycle)
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

# 절기별 월지 (Solar Terms - approximate dates)
# 입춘(立春) 2월 4일경, 경칩(驚蟄) 3월 6일경...
SOLAR_TERMS = [
    # (month, day_start, branch_index) - 입춘부터 시작
    (2, 4, 2),   # 입춘 - 寅 (인월)
    (3, 6, 3),   # 경칩 - 卯 (묘월)
    (4, 5, 4),   # 청명 - 辰 (진월)
    (5, 6, 5),   # 입하 - 巳 (사월)
    (6, 6, 6),   # 망종 - 午 (오월)
    (7, 7, 7),   # 소서 - 未 (미월)
    (8, 8, 8),   # 입추 - 申 (신월)
    (9, 8, 9),   # 백로 - 酉 (유월)
    (10, 8, 10), # 한로 - 戌 (술월)
    (11, 7, 11), # 입동 - 亥 (해월)
    (12, 7, 0),  # 대설 - 子 (자월)
    (1, 6, 1),   # 소한 - 丑 (축월)
]

# 시간별 지지 (24시간 기준)
def get_hour_branch_index(hour: int) -> int:
    """시간을 지지 인덱스로 변환 (자시=0)"""
    # 23-01시: 子, 01-03시: 丑, 03-05시: 寅...
    if 23 <= hour or hour < 1:
        return 0  # 子
    elif 1 <= hour < 3:
        return 1  # 丑
    elif 3 <= hour < 5:
        return 2  # 寅
    elif 5 <= hour < 7:
        return 3  # 卯
    elif 7 <= hour < 9:
        return 4  # 辰
    elif 9 <= hour < 11:
        return 5  # 巳
    elif 11 <= hour < 13:
        return 6  # 午
    elif 13 <= hour < 15:
        return 7  # 未
    elif 15 <= hour < 17:
        return 8  # 申
    elif 17 <= hour < 19:
        return 9  # 酉
    elif 19 <= hour < 21:
        return 10 # 戌
    else:  # 21 <= hour < 23
        return 11 # 亥


def get_stem_branch(year: int) -> Tuple[str, str]:
    """연도를 천간지지로 변환 (60갑자 순환)"""
    # 1984년 = 甲子년 기준
    base_year = 1984
    offset = (year - base_year) % 60
    
    stem_hanja, branch_hanja = SIXTY_JIAZI[offset]
    
    # 한글 변환
    stem = HEAVENLY_STEMS[HEAVENLY_STEMS_HANJA.index(stem_hanja)]
    branch = EARTHLY_BRANCHES[EARTHLY_BRANCHES_HANJA.index(branch_hanja)]
    
    return stem, branch


def get_month_branch(month: int, day: int) -> int:
    """절기를 고려한 월지 계산 (간략화)"""
    # 절기 기준으로 월을 결정 (대략적인 날짜 사용)
    for term_month, term_day, branch_idx in SOLAR_TERMS:
        if month == term_month:
            if day >= term_day:
                return branch_idx
            else:
                # 이전 절기
                prev_idx = SOLAR_TERMS.index((term_month, term_day, branch_idx)) - 1
                if prev_idx >= 0:
                    return SOLAR_TERMS[prev_idx][2]
                else:
                    return SOLAR_TERMS[-1][2]
    
    # 해당 월에 절기가 없으면 이전 절기 찾기
    for i, (term_month, term_day, branch_idx) in enumerate(SOLAR_TERMS):
        if term_month > month or (term_month == month and term_day > day):
            # 이전 절기 사용
            if i > 0:
                return SOLAR_TERMS[i-1][2]
            else:
                return SOLAR_TERMS[-1][2]
    
    # 기본값: 마지막 절기
    return SOLAR_TERMS[-1][2]


def get_month_pillar(year: int, month: int, day: int) -> Tuple[str, str]:
    """월주 계산 (절기 기준)"""
    # 월지 계산
    branch_idx = get_month_branch(month, day)
    branch = EARTHLY_BRANCHES[branch_idx]
    
    # 월간 계산 (연간에 따라 달라짐)
    year_stem_idx = (year - 1984) % 10
    
    # 월간 기시법 (연간에 따른 월간 시작점)
    # 甲己년: 丙寅월부터, 乙庚년: 戊寅월부터, 丙辛년: 庚寅월부터, 丁壬년: 壬寅월부터, 戊癸년: 甲寅월부터
    month_stem_start = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
    
    # 寅월(인월, index=2)이 기준이므로, 寅월부터의 차이를 계산
    # branch_idx가 월지 인덱스
    # 寅=2가 첫 달이므로
    months_from_yin = (branch_idx - 2) % 12
    stem_idx = (month_stem_start[year_stem_idx] + months_from_yin) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def get_day_pillar(date: datetime) -> Tuple[str, str]:
    """일주 계산 (60갑자 순환)"""
    # 기준일: 2000년 1월 1일 = 戊午일 (verified)
    base_date = datetime(2000, 1, 1)
    base_jiazi_index = 54  # 戊午 (SIXTY_JIAZI에서 54번째)
    
    days_diff = (date.date() - base_date.date()).days
    jiazi_index = (base_jiazi_index + days_diff) % 60
    
    stem_hanja, branch_hanja = SIXTY_JIAZI[jiazi_index]
    
    # 한글 변환
    stem = HEAVENLY_STEMS[HEAVENLY_STEMS_HANJA.index(stem_hanja)]
    branch = EARTHLY_BRANCHES[EARTHLY_BRANCHES_HANJA.index(branch_hanja)]
    
    return stem, branch


def get_hour_pillar(date: datetime, day_stem: str) -> Tuple[str, str]:
    """시주 계산 (시두법 적용)"""
    hour = date.hour
    
    # 시지 계산 (23시도 당일 자시로 처리, 야자시 제거)
    branch_idx = get_hour_branch_index(hour)
    branch = EARTHLY_BRANCHES[branch_idx]
    
    # 시간 계산 (일간에 따라 달라짐 - 시두법)
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    
    # 일간별 시작 시간 천간 (甲己日 갑자시, 乙庚日 병자시, 丙辛日 무자시, 丁壬日 경자시, 戊癸日 임자시)
    hour_stem_start = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
    
    # 子시(branch_idx=0)부터 시작하는 천간
    stem_idx = (hour_stem_start[day_stem_idx] + branch_idx) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def calculate_four_pillars(birth_date: datetime) -> Dict:
    """사주팔자 계산"""
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    
    # 연주
    year_stem, year_branch = get_stem_branch(year)
    
    # 월주 (절기 고려)
    month_stem, month_branch = get_month_pillar(year, month, day)
    
    # 일주
    day_stem, day_branch = get_day_pillar(birth_date)
    
    # 일주 60갑자 인덱스 계산 (공망 등에 필요)
    base_date = datetime(2000, 1, 1)
    base_jiazi_index = 54  # 戊午
    days_diff = (birth_date.date() - base_date.date()).days
    day_pillar_index = (base_jiazi_index + days_diff) % 60
    
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
    
    # 한자만 추출
    year_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]
    year_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]
    month_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]
    month_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]
    day_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]
    day_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]
    hour_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]
    hour_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]
    
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
        'birth_date': birth_date.strftime('%Y년 %m월 %d일 %H시 %M분'),
        'birth_year': year,
        'year_hanja': f"{year_stem_hanja}{year_branch_hanja}",
        'month_hanja': f"{month_stem_hanja}{month_branch_hanja}",
        'day_hanja': f"{day_stem_hanja}{day_branch_hanja}",
        'hour_hanja': f"{hour_stem_hanja}{hour_branch_hanja}",
        'year_stem_hanja': year_stem_hanja,
        'year_branch_hanja': year_branch_hanja,
        'month_stem_hanja': month_stem_hanja,
        'month_branch_hanja': month_branch_hanja,
        'day_stem_hanja': day_stem_hanja,
        'day_branch_hanja': day_branch_hanja,
        'hour_stem_hanja': hour_stem_hanja,
        'hour_branch_hanja': hour_branch_hanja,
        'day_pillar_index': day_pillar_index
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
