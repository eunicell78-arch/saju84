"""
사주팔자 계산 모듈
Four Pillars (Saju) Calculator Module
"""
from datetime import datetime
from typing import Dict, Tuple

# 새로 추가된 모듈들 임포트
try:
    from sipsin import get_sipsin, get_branch_sipsin
    from unsung_12 import get_twelve_unsung
    from sinsal import (get_cheonul_gwiin, get_yeokma, get_dohwa, 
                        get_gongmang, get_wonjin, get_yangin)
    from napeum import get_napeum
    from hyungchunghap import get_chung, get_yukhap, get_samhap, get_hyung
    from daeun import get_daeun_direction, calculate_daeun_start_age, generate_daeun
    from seun import get_current_seun_info, generate_seun
    ENHANCED_MODULES_AVAILABLE = True
except ImportError:
    ENHANCED_MODULES_AVAILABLE = False

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

# 월별 지지 (음력/절기 기준 근사)
# 양력 기준 근사: 2월=寅, 3월=卯, ..., 12월=丑, 1월=寅
# 하지만 절기를 고려하면 12월 중순 이전은 子월, 1월 입춘 이전은 丑월
MONTH_BRANCHES = ['인(寅)', '묘(卯)', '진(辰)', '사(巳)', '오(午)', '미(未)', 
                  '신(申)', '유(酉)', '술(戌)', '해(亥)', '자(子)', '축(丑)']
# 절기 근사 매핑 (양력 월 -> 음력 월지)
# 입춘(2/4경) ~ 경칩 = 寅월, ... , 대설 ~ 소한(1/5경) = 子월, 소한 ~ 입춘 = 丑월
SOLAR_TO_LUNAR_MONTH = {
    1: 11,   # 1월 = 丑월 (소한~입춘)
    2: 0,    # 2월 = 寅월 (입춘~경칩)  
    3: 1,    # 3월 = 卯월
    4: 2,    # 4월 = 辰월
    5: 3,    # 5월 = 巳월
    6: 4,    # 6월 = 午월
    7: 5,    # 7월 = 未월
    8: 6,    # 8월 = 申월
    9: 7,    # 9월 = 酉월
    10: 8,   # 10월 = 戌월
    11: 9,   # 11월 = 亥월
    12: 10   # 12월 = 子월 (대설~소한)
}

# 시간별 지지는 get_hour_pillar 함수 내부에서 계산됨 (30분 기준)


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
    """월주 계산 (절기 기준 근사)"""
    # 월지 결정 (절기 기준 근사)
    lunar_month_idx = SOLAR_TO_LUNAR_MONTH.get(month, 0)
    branch = MONTH_BRANCHES[lunar_month_idx]
    
    # 월간 계산 (연간에 따라 달라짐)
    # 전통 명리학 규칙: 甲己년은 丙寅월부터, 乙庚년은 戊寅월부터, 
    # 丙辛년은 庚寅월부터, 丁壬년은 壬寅월부터, 戊癸년은 甲寅월부터
    # month_stem_start는 寅월(index 0)의 천간 시작 인덱스
    # 0=甲, 2=丙, 4=戊, 6=庚, 8=壬
    year_stem_idx = (year - 1984) % 10
    month_stem_start = {0: 2, 1: 4, 2: 6, 3: 8, 4: 0, 5: 2, 6: 4, 7: 6, 8: 8, 9: 0}
    
    # 寅월(index 0)을 기준으로 계산
    # lunar_month_idx는 MONTH_BRANCHES에서의 인덱스 (寅=0, 卯=1, ..., 丑=11)
    stem_idx = (month_stem_start[year_stem_idx] + lunar_month_idx) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def get_day_pillar(date: datetime) -> Tuple[str, str]:
    """일주 계산 (60갑자 순환)"""
    # 기준일: 1900년 1월 1일 = 甲戌일 (60갑자 index 10)
    # 이 계산은 양력 기준 근사치입니다
    base_date = datetime(1900, 1, 1)
    base_offset = 10  # 甲戌
    
    days_diff = (date - base_date).days
    jiazi_index = (base_offset + days_diff) % 60
    
    stem_idx = jiazi_index % 10
    branch_idx = jiazi_index % 12
    
    stem = HEAVENLY_STEMS[stem_idx]
    branch = EARTHLY_BRANCHES[branch_idx]
    
    return stem, branch


def get_hour_pillar(date: datetime, day_stem: str) -> Tuple[str, str]:
    """시주 계산 (자정 기준)
    
    전통 사주학 기준: 각 시(時)는 해당 시간의 30분 전부터 시작
    예: 오시(午時) = 11:30 ~ 13:30
    """
    hour = date.hour
    minute = date.minute
    
    # 시간을 분 단위로 변환 (자정 기준 적용)
    # 예: 13시 5분 = 13 * 60 + 5 = 785분
    total_minutes = hour * 60 + minute
    
    # 각 시는 30분 전부터 시작하므로 30분을 더함
    adjusted_minutes = (total_minutes + 30) % 1440  # 1440분 = 24시간 (60분 * 24시간)
    adjusted_hour = adjusted_minutes // 60
    
    # 시지(時支) 결정
    hour_branch_map = {
        0: '자(子)',   # 23:30 ~ 01:30
        1: '축(丑)',   # 01:30 ~ 03:30
        2: '인(寅)',   # 03:30 ~ 05:30
        3: '묘(卯)',   # 05:30 ~ 07:30
        4: '진(辰)',   # 07:30 ~ 09:30
        5: '사(巳)',   # 09:30 ~ 11:30
        6: '오(午)',   # 11:30 ~ 13:30
        7: '미(未)',   # 13:30 ~ 15:30
        8: '신(申)',   # 15:30 ~ 17:30
        9: '유(酉)',   # 17:30 ~ 19:30
        10: '술(戌)',  # 19:30 ~ 21:30
        11: '해(亥)'   # 21:30 ~ 23:30
    }
    
    branch_index = adjusted_hour // 2  # 2시간 단위로 지지 결정 (자시=0, 축시=1, ...)
    branch = hour_branch_map.get(branch_index, '자(子)')
    
    # 시간(時干) 계산 (일간에 따라 달라짐)
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    hour_stem_start = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
    
    stem_idx = (hour_stem_start[day_stem_idx] + branch_index) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def calculate_four_pillars(birth_date: datetime, gender: str = '남', include_hour: bool = True) -> Dict:
    """사주팔자 계산
    
    Args:
        birth_date: 생년월일시
        gender: 성별
        include_hour: 시주 포함 여부 (False면 3주만 계산)
    """
    year = birth_date.year
    month = birth_date.month
    
    # 연주
    year_stem, year_branch = get_stem_branch(year)
    
    # 월주
    month_stem, month_branch = get_month_pillar(year, month)
    
    # 일주
    day_stem, day_branch = get_day_pillar(birth_date)
    
    # 시주 (시간 모름인 경우 건너뛰기)
    if include_hour:
        hour_stem, hour_branch = get_hour_pillar(birth_date, day_stem)
    else:
        hour_stem, hour_branch = None, None
    
    # 오행 분석
    if include_hour:
        stems = [year_stem, month_stem, day_stem, hour_stem]
        branches = [year_branch, month_branch, day_branch, hour_branch]
    else:
        stems = [year_stem, month_stem, day_stem]
        branches = [year_branch, month_branch, day_branch]
    
    stems_elements = [STEM_ELEMENTS[s] for s in stems]
    branches_elements = [BRANCH_ELEMENTS[b] for b in branches]
    
    # 음양 분석
    stems_yin_yang = [STEM_YIN_YANG[s] for s in stems]
    branches_yin_yang = [BRANCH_YIN_YANG[b] for b in branches]
    
    # 한자 변환
    year_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]}"
    month_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]}"
    day_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]}"
    if include_hour:
        hour_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]}"
    else:
        hour_hanja = "미상"
    
    result = {
        'year_pillar': f"{year_stem}{year_branch}",
        'month_pillar': f"{month_stem}{month_branch}",
        'day_pillar': f"{day_stem}{day_branch}",
        'hour_pillar': f"{hour_stem}{hour_branch}" if include_hour else "미상",
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
        'birth_date': birth_date.strftime('%Y년 %m월 %d일 %H시') if include_hour else birth_date.strftime('%Y년 %m월 %d일'),
        'year_hanja': year_hanja,
        'month_hanja': month_hanja,
        'day_hanja': day_hanja,
        'hour_hanja': hour_hanja,
        'time_unknown': not include_hour
    }
    
    # 추가 정보 계산 (모듈이 있을 때만)
    if ENHANCED_MODULES_AVAILABLE:
        try:
            # 한자만 추출
            day_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]
            year_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]
            month_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]
            
            year_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]
            month_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]
            day_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]
            
            if include_hour:
                hour_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]
                hour_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]
                branches_hanja = [year_branch_hanja, month_branch_hanja, day_branch_hanja, hour_branch_hanja]
            else:
                hour_stem_hanja = None
                hour_branch_hanja = None
                branches_hanja = [year_branch_hanja, month_branch_hanja, day_branch_hanja]
            
            # 십신
            sipsin_data = {
                'year_stem': get_sipsin(day_stem_hanja, year_stem_hanja),
                'month_stem': get_sipsin(day_stem_hanja, month_stem_hanja),
                'day_stem': '비견(比肩)',  # 일간 자신
                'year_branch': get_branch_sipsin(day_stem_hanja, year_branch_hanja),
                'month_branch': get_branch_sipsin(day_stem_hanja, month_branch_hanja),
                'day_branch': get_branch_sipsin(day_stem_hanja, day_branch_hanja),
            }
            if include_hour:
                sipsin_data['hour_stem'] = get_sipsin(day_stem_hanja, hour_stem_hanja)
                sipsin_data['hour_branch'] = get_branch_sipsin(day_stem_hanja, hour_branch_hanja)
            else:
                sipsin_data['hour_stem'] = '미상'
                sipsin_data['hour_branch'] = '미상'
            result['sipsin'] = sipsin_data
            
            # 12운성
            unsung_data = {
                'year': get_twelve_unsung(day_stem_hanja, year_branch_hanja),
                'month': get_twelve_unsung(day_stem_hanja, month_branch_hanja),
                'day': get_twelve_unsung(day_stem_hanja, day_branch_hanja),
            }
            if include_hour:
                unsung_data['hour'] = get_twelve_unsung(day_stem_hanja, hour_branch_hanja)
            else:
                unsung_data['hour'] = '미상'
            result['unsung'] = unsung_data
            
            # 신살
            result['sinsal'] = {
                'cheonul': get_cheonul_gwiin(year_stem_hanja, month_stem_hanja, day_stem_hanja, branches_hanja),
                'yeokma': get_yeokma(branches_hanja),
                'dohwa': get_dohwa(branches_hanja),
                'gongmang': get_gongmang(day_hanja, branches_hanja),
                'wonjin': get_wonjin(branches_hanja),
                'yangin': get_yangin(day_stem_hanja, branches_hanja)
            }
            
            # 납음오행
            napeum_data = {
                'year': get_napeum(year_hanja),
                'month': get_napeum(month_hanja),
                'day': get_napeum(day_hanja),
            }
            if include_hour:
                napeum_data['hour'] = get_napeum(hour_hanja)
            else:
                napeum_data['hour'] = '미상'
            result['napeum'] = napeum_data
            
            # 형충회합
            result['hyungchunghap'] = {
                'chung': get_chung(branches_hanja),
                'yukhap': get_yukhap(branches_hanja),
                'samhap': get_samhap(branches_hanja),
                'hyung': get_hyung(branches_hanja)
            }
            
            # 대운
            direction = get_daeun_direction(gender, year_stem_hanja)
            daeun_age = calculate_daeun_start_age(birth_date, gender, year_stem_hanja, month)
            daeun_list = generate_daeun(year_stem, month_stem, year_branch, month_branch,
                                       gender, daeun_age, day_stem, 10)
            result['daeun'] = {
                'direction': direction,
                'start_age': daeun_age,
                'list': daeun_list
            }
            
            # 세운
            current_year = datetime.now().year
            current_seun = get_current_seun_info(year, current_year)
            seun_list = generate_seun(year, current_year, 5, 10)
            result['seun'] = {
                'current': current_seun,
                'list': seun_list
            }
            
        except Exception as e:
            print(f"추가 정보 계산 중 오류: {e}")
    
    return result


def get_element_count(result: Dict) -> Dict[str, int]:
    """오행 개수 계산"""
    all_elements = result['stems_elements'] + result['branches_elements']
    element_count = {
        '목(木)': 0, '화(火)': 0, '토(土)': 0, '금(金)': 0, '수(水)': 0
    }
    for elem in all_elements:
        element_count[elem] = element_count.get(elem, 0) + 1
    
    return element_count
