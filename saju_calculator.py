"""
사주팔자 계산 모듈
Four Pillars (Saju) Calculator Module
"""
from datetime import datetime
from typing import Dict, Tuple

# 음력/양력 변환 라이브러리
try:
    from korean_lunar_calendar import KoreanLunarCalendar
    LUNAR_CALENDAR_AVAILABLE = True
except ImportError:
    LUNAR_CALENDAR_AVAILABLE = False

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

# 시간별 지지
HOUR_BRANCHES = {
    (23, 1): '자(子)', (1, 3): '축(丑)', (3, 5): '인(寅)', (5, 7): '묘(卯)',
    (7, 9): '진(辰)', (9, 11): '사(巳)', (11, 13): '오(午)', (13, 15): '미(未)',
    (15, 17): '신(申)', (17, 19): '유(酉)', (19, 21): '술(戌)', (21, 23): '해(亥)'
}


def lunar_to_solar(year: int, month: int, day: int, is_leap_month: bool = False) -> Dict[str, int]:
    """음력을 양력으로 변환"""
    if not LUNAR_CALENDAR_AVAILABLE:
        raise ImportError("korean_lunar_calendar 라이브러리가 설치되지 않았습니다.")
    
    try:
        calendar = KoreanLunarCalendar()
        calendar.setLunarDate(year, month, day, is_leap_month)
        
        solar_year = calendar.solarYear
        solar_month = calendar.solarMonth
        solar_day = calendar.solarDay
        
        return {
            'year': solar_year,
            'month': solar_month,
            'day': solar_day
        }
    except Exception as e:
        raise ValueError(f"음력 변환 중 오류가 발생했습니다: {str(e)}")


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
    """시주 계산"""
    hour = date.hour
    
    # 시지 찾기
    branch = '자(子)'  # 기본값
    for (start, end), b in HOUR_BRANCHES.items():
        if start <= hour < end:
            branch = b
            break
        elif start > end:  # 자시(23-01)의 경우
            if hour >= start or hour < end:
                branch = b
                break
    
    # 시간 계산 (일간에 따라 달라짐)
    day_stem_idx = HEAVENLY_STEMS.index(day_stem)
    # 갑기일(0,5)은 갑자시, 을경일(1,6)은 병자시...
    hour_stem_start = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
    
    # 시지 인덱스 찾기
    branch_idx = EARTHLY_BRANCHES.index(branch)
    stem_idx = (hour_stem_start[day_stem_idx] + branch_idx) % 10
    stem = HEAVENLY_STEMS[stem_idx]
    
    return stem, branch


def calculate_four_pillars(birth_date: datetime, gender: str = '남') -> Dict:
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
    
    # 한자 변환
    year_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]}"
    month_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]}"
    day_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]}"
    hour_hanja = f"{HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]}{EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]}"
    
    result = {
        'birth_year': year,
        'birth_month': month,
        'birth_day': birth_date.day,
        'birth_hour': birth_date.hour,
        'birth_minute': birth_date.minute,
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
        'year_hanja': year_hanja,
        'month_hanja': month_hanja,
        'day_hanja': day_hanja,
        'hour_hanja': hour_hanja
    }
    
    # 추가 정보 계산 (모듈이 있을 때만)
    if ENHANCED_MODULES_AVAILABLE:
        try:
            # 한자만 추출
            day_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(day_stem)]
            year_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(year_stem)]
            month_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(month_stem)]
            hour_stem_hanja = HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.index(hour_stem)]
            
            year_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(year_branch)]
            month_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(month_branch)]
            day_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(day_branch)]
            hour_branch_hanja = EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.index(hour_branch)]
            
            branches_hanja = [year_branch_hanja, month_branch_hanja, day_branch_hanja, hour_branch_hanja]
            
            # 십신
            result['sipsin'] = {
                'year_stem': get_sipsin(day_stem_hanja, year_stem_hanja),
                'month_stem': get_sipsin(day_stem_hanja, month_stem_hanja),
                'day_stem': '비견(比肩)',  # 일간 자신
                'hour_stem': get_sipsin(day_stem_hanja, hour_stem_hanja),
                'year_branch': get_branch_sipsin(day_stem_hanja, year_branch_hanja),
                'month_branch': get_branch_sipsin(day_stem_hanja, month_branch_hanja),
                'day_branch': get_branch_sipsin(day_stem_hanja, day_branch_hanja),
                'hour_branch': get_branch_sipsin(day_stem_hanja, hour_branch_hanja)
            }
            
            # 12운성
            result['unsung'] = {
                'year': get_twelve_unsung(day_stem_hanja, year_branch_hanja),
                'month': get_twelve_unsung(day_stem_hanja, month_branch_hanja),
                'day': get_twelve_unsung(day_stem_hanja, day_branch_hanja),
                'hour': get_twelve_unsung(day_stem_hanja, hour_branch_hanja)
            }
            
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
            result['napeum'] = {
                'year': get_napeum(year_hanja),
                'month': get_napeum(month_hanja),
                'day': get_napeum(day_hanja),
                'hour': get_napeum(hour_hanja)
            }
            
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


def calculate_jijanggan(result: Dict) -> str:
    """지장간 계산"""
    JIJANGGAN_TABLE = {
        '子': ['癸(10일)'],
        '丑': ['己(9일)', '癸(3일)', '辛(18일)'],
        '寅': ['戊(7일)', '丙(7일)', '甲(16일)'],
        '卯': ['乙(10일)'],
        '辰': ['戊(9일)', '乙(3일)', '癸(18일)'],
        '巳': ['戊(5일)', '庚(9일)', '丙(16일)'],
        '午': ['己(10일)', '丁(20일)'],
        '未': ['己(9일)', '丁(3일)', '乙(18일)'],
        '申': ['戊(7일)', '壬(3일)', '庚(20일)'],
        '酉': ['辛(10일)'],
        '戌': ['戊(9일)', '辛(3일)', '丁(18일)'],
        '亥': ['戊(7일)', '甲(5일)', '壬(18일)']
    }
    
    year_hanja = result.get('year_hanja', '')
    month_hanja = result.get('month_hanja', '')
    day_hanja = result.get('day_hanja', '')
    hour_hanja = result.get('hour_hanja', '')
    
    branches = [
        year_hanja[1] if len(year_hanja) > 1 else '',
        month_hanja[1] if len(month_hanja) > 1 else '',
        day_hanja[1] if len(day_hanja) > 1 else '',
        hour_hanja[1] if len(hour_hanja) > 1 else ''
    ]
    
    jijanggan_str = ""
    for i, branch_name in enumerate(['년지', '월지', '일지', '시지']):
        hanja = branches[i]
        if hanja:
            jijanggan = JIJANGGAN_TABLE.get(hanja, [])
            jijanggan_str += f"- {branch_name} {hanja}: {', '.join(jijanggan)}\n"
    
    return jijanggan_str


def format_sipsin_distribution(result: Dict) -> str:
    """십신 분포 포맷팅"""
    sipsin_data = result.get('sipsin', {})
    return f"""
- 년주: {sipsin_data.get('year_stem', '미상')}
- 월주: {sipsin_data.get('month_stem', '미상')}
- 일주: 일간 (본인)
- 시주: {sipsin_data.get('hour_stem', '미상')}
"""


def format_current_daeun(result: Dict) -> str:
    """현재 대운 포맷팅"""
    if 'daeun' not in result or not result['daeun'].get('list'):
        return "- 현재 대운 정보 없음"
    
    # 현재 나이 계산
    birth_year = result.get('birth_year', 0)
    current_year = datetime.now().year
    current_age = current_year - birth_year + 1
    
    daeun_list = result['daeun']['list']
    current_daeun = None
    
    # 현재 대운 찾기
    for daeun in daeun_list:
        start_age = daeun.get('나이', 0)
        end_age = start_age + 10
        if start_age <= current_age < end_age:
            current_daeun = daeun
            break
    
    if not current_daeun:
        current_daeun = daeun_list[0]
    
    return f"""
- 대운 간지: {current_daeun.get('간지', '미상')}
- 시작 나이: {current_daeun.get('나이', '미상')}세
- 십신: {current_daeun.get('십신', '미상')}
- 12운성: {current_daeun.get('12운성', '미상')}
"""


def format_daeun_table(result: Dict) -> str:
    """대운표 포맷팅"""
    daeun_list = result.get('daeun', {}).get('list', [])
    if not daeun_list:
        return "대운 정보 없음"
    
    table_str = "| 나이 | 간지 | 십신 | 12운성 |\n"
    table_str += "|------|------|------|--------|\n"
    for daeun in daeun_list[:10]:  # 10개 대운
        age = daeun.get('나이', '?')
        ganji = daeun.get('간지', '?')
        sipsin = daeun.get('십신', '?')
        unsung = daeun.get('12운성', '?')
        table_str += f"| {age}세 | {ganji} | {sipsin} | {unsung} |\n"
    return table_str


def format_gwiin_list(result: Dict) -> str:
    """귀인 목록 포맷팅"""
    sinsal = result.get('sinsal', {})
    gwiin_list = []
    
    if sinsal.get('cheonul'):
        gwiin_list.append(f"천을귀인: {', '.join(sinsal['cheonul'])}")
    
    if gwiin_list:
        return "\n".join([f"- {g}" for g in gwiin_list])
    return "- 특별한 귀인 없음"


def format_sal_list(result: Dict) -> str:
    """살 목록 포맷팅"""
    sinsal = result.get('sinsal', {})
    sal_list = []
    
    if sinsal.get('yeokma'):
        sal_list.append(f"역마살: {', '.join(sinsal['yeokma'])}")
    if sinsal.get('dohwa'):
        sal_list.append(f"도화살: {', '.join(sinsal['dohwa'])}")
    if sinsal.get('gongmang'):
        sal_list.append(f"공망: {', '.join(sinsal['gongmang'])}")
    if sinsal.get('wonjin'):
        sal_list.append(f"원진: {', '.join(sinsal['wonjin'])}")
    if sinsal.get('yangin'):
        sal_list.append(f"양인: {', '.join(sinsal['yangin'])}")
    
    if sal_list:
        return "\n".join([f"- {s}" for s in sal_list])
    return "- 특별한 살 없음"
