"""
사주팔자 만세력 계산기 with OpenAI ChatGPT
Saju (Four Pillars) Calculator with AI Interpretation
"""
import streamlit as st
import pandas as pd
from datetime import datetime, time
from saju_calculator import calculate_four_pillars, get_element_count
from sipsin import get_sipsin, get_sipsin_for_branch
from sinsal import get_all_sinsal
from unsung_12 import get_unsung, get_unsung_description
from napeum import get_napeum
from hyungchunghap import get_hyungchunghap
from daeun import calculate_daeun
from seun import calculate_seun

# OpenAI 임포트 (선택적)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# 페이지 설정
st.set_page_config(
    page_title="사주팔자 만세력 계산기",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 사주팔자 만세력 계산기")
st.caption("생년월일시를 입력하면 사주팔자를 계산하고 AI가 풀이해드립니다.")


def get_saju_interpretation(saju_result: dict, gender: str, 
                           sipsin_info: dict, sinsal_info: dict,
                           hyungchunghap_info: dict, daeun_info: dict) -> str:
    """ChatGPT를 이용한 사주 풀이"""
    
    # 오행 개수
    element_count = get_element_count(saju_result)
    element_str = ", ".join([f"{k}: {v}개" for k, v in element_count.items()])
    
    # 신살 정리
    sinsal_str = []
    if sinsal_info['cheonul']:
        sinsal_str.append(f"천을귀인: {', '.join(sinsal_info['cheonul'])}")
    if sinsal_info['yeokma']:
        sinsal_str.append(f"역마살: {', '.join(sinsal_info['yeokma'])}")
    if sinsal_info['dohwa']:
        sinsal_str.append(f"도화살: {', '.join(sinsal_info['dohwa'])}")
    
    # 형충회합 정리
    hch_str = []
    if hyungchunghap_info['chung']:
        hch_str.append(f"충: {', '.join(hyungchunghap_info['chung'])}")
    if hyungchunghap_info['hap']:
        hch_str.append(f"합: {', '.join(hyungchunghap_info['hap'])}")
    if hyungchunghap_info['hyung']:
        hch_str.append(f"형: {', '.join(hyungchunghap_info['hyung'])}")
    
    prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다. 
다음 사주팔자를 깊이있고 전문적으로 풀이해주세요.

## 기본 정보
- 성별: {gender}
- 생년월일시: {saju_result['birth_date']}

## 사주팔자
- 연주(年柱): {saju_result['year_hanja']} - 십신: {sipsin_info['year']}, 12운성: {sipsin_info['year_unsung']}
- 월주(月柱): {saju_result['month_hanja']} - 십신: {sipsin_info['month']}, 12운성: {sipsin_info['month_unsung']}
- 일주(日柱): {saju_result['day_hanja']} - 일간(자신), 12운성: {sipsin_info['day_unsung']}
- 시주(時柱): {saju_result['hour_hanja']} - 십신: {sipsin_info['hour']}, 12운성: {sipsin_info['hour_unsung']}

## 오행 분석
- 천간: {', '.join(saju_result['stems_elements'])}
- 지지: {', '.join(saju_result['branches_elements'])}
- 오행 개수: {element_str}

## 신살
{chr(10).join(sinsal_str) if sinsal_str else '주요 신살 없음'}

## 형충회합
{chr(10).join(hch_str) if hch_str else '형충회합 없음'}

## 대운
- 대운 시작: {daeun_info['start_age']}세, {daeun_info['direction']}
- 첫 대운: {daeun_info['first_pillar']}

## 풀이 요청사항
다음 항목들을 구조화된 형식으로 풀이해주세요:

### 1. 사주 전체 구조
사주팔자의 전체적인 구조와 특징을 분석해주세요.

### 2. 일간 강약 판단
일간의 강약을 판단하고, 그 이유를 설명해주세요.

### 3. 용신 선정
이 사주에 필요한 용신(用神)을 선정하고 이유를 설명해주세요.

### 4. 기본 성향
타고난 성격과 기질을 설명해주세요.

### 5. 십신으로 본 성격과 적성
십신 배치를 통해 본 성격과 적합한 직업 분야를 추천해주세요.

### 6. 신살의 길흉
나타난 신살의 의미와 영향을 설명해주세요.

### 7. 재물운
재물에 관한 운세를 설명해주세요.

### 8. 건강
주의해야 할 건강 부분을 알려주세요.

### 9. 대운 해석
현재와 향후 대운의 흐름을 해석해주세요.

### 10. 조언
인생에서 주의할 점과 조언을 해주세요.

한국어로 정중하고 이해하기 쉽게 설명해주세요. 각 섹션은 제목(###)을 포함하여 구분해주세요.
"""
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 전문 사주명리학자입니다. 사주팔자를 깊이있고 정확하게 풀이합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        return response.choices[0].message.content
    
    except openai.AuthenticationError:
        return "❌ OpenAI API 키가 유효하지 않습니다. Streamlit Secrets에서 올바른 API 키를 설정해주세요."
    except openai.RateLimitError:
        return "❌ API 사용량 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
    except Exception as e:
        return f"❌ 풀이 중 오류가 발생했습니다: {str(e)}"


# 메인 UI
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📅 생년월일시 입력")
    
    gender = st.radio("성별", ["남", "여"], horizontal=True)
    
    birth_date = st.date_input(
        "생년월일",
        value=datetime(1990, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    
    birth_time = st.time_input(
        "출생 시간",
        value=time(12, 0)
    )
    
    # datetime 객체 생성
    birth_datetime = datetime.combine(birth_date, birth_time)
    
    if st.button("🔮 사주팔자 계산하기", type="primary", use_container_width=True):
        st.session_state['saju_calculated'] = True
        st.session_state['birth_datetime'] = birth_datetime
        st.session_state['gender'] = gender

with col2:
    st.subheader("ℹ️ 안내사항")
    st.info(
        "**사주팔자란?**\n\n"
        "태어난 년(年), 월(月), 일(日), 시(時)를 "
        "천간(天干)과 지지(地支)로 표현한 것으로, "
        "총 8개의 글자로 구성됩니다.\n\n"
        "**AI 풀이 기능**\n\n"
        "OpenAI ChatGPT를 활용하여 전문적인 사주 해석을 제공합니다."
    )

# 사주 계산 결과 표시
if st.session_state.get('saju_calculated', False):
    birth_datetime = st.session_state['birth_datetime']
    gender = st.session_state.get('gender', '남')
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime)
    
    st.success(f"✅ {result['birth_date']} 출생자의 사주팔자 ({gender})")
    
    # 십신, 12운성, 신살 계산
    day_stem_hanja = result['day_stem_hanja']
    branches_hanja = [result['year_branch_hanja'], result['month_branch_hanja'], 
                      result['day_branch_hanja'], result['hour_branch_hanja']]
    stems_hanja = [result['year_stem_hanja'], result['month_stem_hanja'], 
                   result['day_stem_hanja'], result['hour_stem_hanja']]
    
    # 각 기둥의 십신 계산
    year_sipsin = get_sipsin(day_stem_hanja, result['year_stem_hanja'])
    month_sipsin = get_sipsin(day_stem_hanja, result['month_stem_hanja'])
    day_sipsin = '일간'  # 일간 자신
    hour_sipsin = get_sipsin(day_stem_hanja, result['hour_stem_hanja'])
    
    # 각 기둥의 12운성 계산
    year_unsung = get_unsung(day_stem_hanja, result['year_branch_hanja'])
    month_unsung = get_unsung(day_stem_hanja, result['month_branch_hanja'])
    day_unsung = get_unsung(day_stem_hanja, result['day_branch_hanja'])
    hour_unsung = get_unsung(day_stem_hanja, result['hour_branch_hanja'])
    
    # 납음오행
    year_napeum = get_napeum(result['year_hanja'])
    month_napeum = get_napeum(result['month_hanja'])
    day_napeum = get_napeum(result['day_hanja'])
    hour_napeum = get_napeum(result['hour_hanja'])
    
    # 신살 계산
    sinsal = get_all_sinsal(day_stem_hanja, result['year_branch_hanja'], 
                           result['day_pillar_index'], branches_hanja)
    
    # 사주팔자 표시 (4기둥)
    st.markdown("### 📊 사주팔자 (四柱八字)")
    
    cols = st.columns(4)
    pillars_data = [
        ("시주(時柱)", result['hour_pillar'], result['hour_hanja'], hour_sipsin, hour_unsung, hour_napeum),
        ("일주(日柱)", result['day_pillar'], result['day_hanja'], day_sipsin, day_unsung, day_napeum),
        ("월주(月柱)", result['month_pillar'], result['month_hanja'], month_sipsin, month_unsung, month_napeum),
        ("연주(年柱)", result['year_pillar'], result['year_hanja'], year_sipsin, year_unsung, year_napeum),
    ]
    
    for col, (title, pillar, hanja, sipsin, unsung, napeum) in zip(cols, pillars_data):
        with col:
            st.markdown(f"**{title}**")
            st.markdown(f"# {hanja}")
            st.caption(f"{pillar}")
            st.info(f"**십신**: {sipsin}")
            st.success(f"**12운성**: {unsung}")
            with st.expander("납음오행"):
                st.write(napeum)
    
    # 오행 분석
    st.markdown("### 🌟 오행 분석 (五行)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**천간(天干) 오행:**")
        for i, (stem, element) in enumerate(zip(['연간', '월간', '일간', '시간'], result['stems_elements'])):
            st.write(f"- {stem}: {element}")
    
    with col2:
        st.write("**지지(地支) 오행:**")
        for i, (branch, element) in enumerate(zip(['연지', '월지', '일지', '시지'], result['branches_elements'])):
            st.write(f"- {branch}: {element}")
    
    # 오행 개수 통계
    element_count = get_element_count(result)
    st.write("**오행 개수:**")
    element_cols = st.columns(5)
    for col, (element, count) in zip(element_cols, element_count.items()):
        with col:
            st.metric(label=element, value=f"{count}개")
    
    # 신살 표시
    st.markdown("### ✨ 신살 (神殺)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**길신(吉神)**")
        if sinsal['cheonul']:
            st.success("🌟 " + ", ".join(sinsal['cheonul']))
        else:
            st.info("천을귀인 없음")
    
    with col2:
        st.write("**기타 신살**")
        all_sinsal = []
        if sinsal['yeokma']:
            all_sinsal.extend(sinsal['yeokma'])
        if sinsal['dohwa']:
            all_sinsal.extend(sinsal['dohwa'])
        if sinsal['hwagae']:
            all_sinsal.extend(sinsal['hwagae'])
        if sinsal['gongmang']:
            all_sinsal.extend(sinsal['gongmang'])
        
        if all_sinsal:
            st.warning("⚠️ " + ", ".join(all_sinsal))
        else:
            st.info("기타 신살 없음")
    
    # 형충회합
    st.markdown("### ⚡ 형충회합 (刑沖會合)")
    
    hyungchunghap = get_hyungchunghap(branches_hanja)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**충(沖)**")
        if hyungchunghap['chung']:
            st.error("💥 " + "\n\n💥 ".join(hyungchunghap['chung']))
        else:
            st.info("충 없음")
    
    with col2:
        st.write("**합(合)**")
        if hyungchunghap['hap']:
            st.success("🤝 " + "\n\n🤝 ".join(hyungchunghap['hap']))
        else:
            st.info("합 없음")
    
    with col3:
        st.write("**형(刑)**")
        if hyungchunghap['hyung']:
            st.warning("⚔️ " + "\n\n⚔️ ".join(hyungchunghap['hyung']))
        else:
            st.info("형 없음")
    
    # 대운
    st.markdown("### 🔮 대운 (大運)")
    
    daeun = calculate_daeun(
        birth_datetime, gender,
        result['year_stem_hanja'], result['month_stem_hanja'], 
        result['month_branch_hanja'], result['birth_year']
    )
    
    st.caption(f"{daeun['start_age']}세부터 시작, {daeun['direction']}")
    
    # 대운표 생성
    daeun_data = []
    for pillar in daeun['pillars']:
        stem = pillar['stem']
        branch = pillar['branch']
        age = pillar['age']
        
        # 십신과 12운성 계산
        daeun_sipsin = get_sipsin(day_stem_hanja, stem)
        daeun_unsung = get_unsung(day_stem_hanja, branch)
        
        daeun_data.append({
            '나이': f"{age}-{age+9}세",
            '간지': f"{stem}{branch}",
            '십신': daeun_sipsin,
            '12운성': daeun_unsung
        })
    
    df_daeun = pd.DataFrame(daeun_data)
    st.dataframe(df_daeun, use_container_width=True, hide_index=True)
    
    # 세운
    st.markdown("### 📅 세운 (歲運)")
    
    current_year = datetime.now().year
    seun_list = calculate_seun(result['birth_year'], current_year, past_years=5, future_years=10)
    
    st.caption(f"과거 5년 ~ 미래 10년")
    
    # 세운 표시 (컴팩트하게)
    seun_cols = st.columns(4)
    for i, seun in enumerate(seun_list):
        col_idx = i % 4
        with seun_cols[col_idx]:
            if seun['is_current']:
                st.success(f"**{seun['year']}년** {seun['stem']}{seun['branch']} ({seun['age']}세) ⬅️")
            else:
                st.text(f"{seun['year']}년 {seun['stem']}{seun['branch']} ({seun['age']}세)")
    
    # 음양 분석 (접기)
    with st.expander("☯️ 음양 분석"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**천간 음양:**")
            for stem, yy in zip(['연간', '월간', '일간', '시간'], result['stems_yin_yang']):
                st.write(f"- {stem}: {yy}")
        with col2:
            st.write("**지지 음양:**")
            for branch, yy in zip(['연지', '월지', '일지', '시지'], result['branches_yin_yang']):
                st.write(f"- {branch}: {yy}")
    
    st.divider()
    
    # AI 풀이 버튼
    # API 키 확인
    api_key_available = False
    try:
        if OPENAI_AVAILABLE and "OPENAI_API_KEY" in st.secrets:
            api_key_available = True
    except:
        pass
    
    if not OPENAI_AVAILABLE:
        st.warning("⚠️ OpenAI 라이브러리가 설치되지 않았습니다. `pip install openai`를 실행해주세요.")
    elif not api_key_available:
        st.warning(
            "⚠️ OpenAI API 키가 설정되지 않았습니다.\n\n"
            "Streamlit Cloud에서 배포 시 Settings → Secrets에서 다음과 같이 설정해주세요:\n\n"
            "```toml\n"
            "OPENAI_API_KEY = \"sk-...\"\n"
            "```\n\n"
            "로컬 실행 시 `.streamlit/secrets.toml` 파일을 생성하여 설정하세요."
        )
    else:
        if st.button("🔮 AI 사주풀이 보기", type="primary", use_container_width=True):
            with st.spinner("AI가 사주를 풀이하는 중... (약 20-30초 소요)"):
                # OpenAI 클라이언트 초기화
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                # 십신 정보 준비
                sipsin_info = {
                    'year': year_sipsin,
                    'month': month_sipsin,
                    'day': day_sipsin,
                    'hour': hour_sipsin,
                    'year_unsung': year_unsung,
                    'month_unsung': month_unsung,
                    'day_unsung': day_unsung,
                    'hour_unsung': hour_unsung
                }
                
                # 대운 정보 준비
                daeun_info_for_ai = {
                    'start_age': daeun['start_age'],
                    'direction': daeun['direction'],
                    'first_pillar': f"{daeun['pillars'][0]['stem']}{daeun['pillars'][0]['branch']}"
                }
                
                interpretation = get_saju_interpretation(
                    result, gender, sipsin_info, sinsal, 
                    hyungchunghap, daeun_info_for_ai
                )
                
                st.session_state['interpretation'] = interpretation
        
        # 풀이 결과 표시
        if 'interpretation' in st.session_state:
            st.markdown("### 📖 AI 사주 풀이")
            st.markdown(st.session_state['interpretation'])
            
            # 다운로드 버튼
            download_text = f"""
사주팔자 만세력 계산 결과
==================

성별: {gender}
생년월일시: {result['birth_date']}

사주팔자
-------
- 연주(年柱): {result['year_hanja']} - 십신: {year_sipsin}, 12운성: {year_unsung}
- 월주(月柱): {result['month_hanja']} - 십신: {month_sipsin}, 12운성: {month_unsung}
- 일주(日柱): {result['day_hanja']} - 일간, 12운성: {day_unsung}
- 시주(時柱): {result['hour_hanja']} - 십신: {hour_sipsin}, 12운성: {hour_unsung}

오행 분석
--------
천간: {', '.join(result['stems_elements'])}
지지: {', '.join(result['branches_elements'])}
오행 개수: {", ".join([f"{k}: {v}개" for k, v in element_count.items()])}

대운
----
{daeun['start_age']}세 시작, {daeun['direction']}

AI 사주 풀이
-----------
{st.session_state['interpretation']}

※ 본 풀이는 AI에 의해 자동 생성된 것으로 참고용입니다.
"""
            
            st.download_button(
                label="📥 풀이 결과 다운로드",
                data=download_text.encode('utf-8'),
                file_name=f"사주풀이_{birth_datetime.strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# 푸터
st.divider()
st.caption("💡 본 서비스는 참고용이며, 전문가의 상담을 대체할 수 없습니다.")
st.caption("🤖 AI 풀이는 OpenAI GPT-4를 사용하며, API 비용이 발생할 수 있습니다.")
