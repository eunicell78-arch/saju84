"""
사주팔자 만세력 계산기 with OpenAI ChatGPT
Saju (Four Pillars) Calculator with AI Interpretation
"""
import streamlit as st
from datetime import datetime, time
from saju_calculator import calculate_four_pillars, get_element_count

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


def get_saju_interpretation(saju_result: dict) -> str:
    """ChatGPT를 이용한 사주 풀이"""
    
    # 오행 개수
    element_count = get_element_count(saju_result)
    element_str = ", ".join([f"{k}: {v}개" for k, v in element_count.items()])
    
    # 십신 분포
    sipsin_str = f"연주: {saju_result['sipsin']['year']}, 월주: {saju_result['sipsin']['month']}, 일주: 일간, 시주: {saju_result['sipsin']['hour']}"
    
    # 12운성 분포
    unsung_str = f"연주: {saju_result['unsung']['year']}, 월주: {saju_result['unsung']['month']}, 일주: {saju_result['unsung']['day']}, 시주: {saju_result['unsung']['hour']}"
    
    # 신살 요약
    sinsal_list = []
    for key, values in saju_result['sinsal'].items():
        if values:
            sinsal_list.extend(values)
    sinsal_str = ', '.join(sinsal_list) if sinsal_list else '없음'
    
    # 형충회합 요약
    hch = saju_result['hyungchunghap']
    hch_str = ""
    if hch['chung']:
        hch_str += f"충: {', '.join(hch['chung'])}\n"
    if hch['yukhap'] or hch['samhap']:
        hch_str += f"합: {', '.join(hch['yukhap'] + hch['samhap'])}\n"
    if hch['hyung']:
        hch_str += f"형: {', '.join(hch['hyung'])}"
    if not hch_str:
        hch_str = "특별한 형충회합 없음"
    
    # 현재 대운
    daeun = saju_result['daeun']
    current_daeun = daeun['list'][0] if daeun['list'] else None
    daeun_str = f"{current_daeun['pillar']} ({current_daeun['age']}~{current_daeun['age']+9}세)" if current_daeun else "계산 불가"
    
    # 현재 세운
    current_seun = [s for s in saju_result['seun'] if s['is_current']]
    seun_str = f"{current_seun[0]['jiazi']} ({current_seun[0]['age']}세)" if current_seun else "계산 불가"
    
    prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다. 
다음 사주팔자를 깊이있고 전문적으로 풀이해주세요.

## 생년월일시
{saju_result['birth_date']} ({saju_result['gender']}성)

## 사주팔자
- 연주(年柱): {saju_result['year_hanja']} (십신: {saju_result['sipsin']['year']}, 12운성: {saju_result['unsung']['year']})
- 월주(月柱): {saju_result['month_hanja']} (십신: {saju_result['sipsin']['month']}, 12운성: {saju_result['unsung']['month']})
- 일주(日柱): {saju_result['day_hanja']} (일간: {saju_result['day_stem_hanja']}, 12운성: {saju_result['unsung']['day']})
- 시주(時柱): {saju_result['hour_hanja']} (십신: {saju_result['sipsin']['hour']}, 12운성: {saju_result['unsung']['hour']})

## 오행 분포
- 천간: {', '.join(saju_result['stems_elements'])}
- 지지: {', '.join(saju_result['branches_elements'])}
- 오행 개수: {element_str}

## 십신 분포
{sipsin_str}

## 12운성
{unsung_str}

## 신살
{sinsal_str}

## 형충회합
{hch_str}

## 대운
방향: {daeun['direction']}, 시작: {daeun['start_age']}세
현재 대운: {daeun_str}

## 세운
현재 년도: {seun_str}

## 풀이 요청사항
다음 항목들을 구조화된 형식으로 풀이해주세요:

### 1. 사주 구조 분석
일간의 강약과 사주 전체 구조를 평가해주세요.

### 2. 용신 선정
이 사주에 필요한 용신(用神)과 희신(喜神)을 선정하고 이유를 설명해주세요.

### 3. 십신으로 본 성격과 적성
십신 배치를 바탕으로 성격과 직업 적성을 분석해주세요.

### 4. 신살의 길흉
주요 신살의 의미와 영향을 설명해주세요.

### 5. 형충회합의 영향
형충회합이 사주에 미치는 영향을 분석해주세요.

### 6. 현재 대운/세운 해석
현재 대운과 세운이 삶에 어떤 영향을 미치는지 설명해주세요.

### 7. 향후 10년 운세
대운과 세운의 흐름을 바탕으로 향후 운세를 전망해주세요.

### 8. 개선 방향 조언
오행 조화를 위한 실천적 조언을 해주세요.

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
            max_tokens=2000
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
    
    # 성별 선택 추가
    gender = st.radio(
        "성별",
        options=['남', '여'],
        horizontal=True,
        index=1  # 기본값: 여
    )
    
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
    gender = st.session_state.get('gender', '여')
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime, gender)
    
    st.success(f"✅ {result['birth_date']} 출생, {gender}성의 사주팔자")
    
    # 사주팔자 표시 (가로로 4기둥)
    st.subheader("📊 사주팔자 (四柱八字)")
    
    cols = st.columns(4)
    pillars = [
        ("시주(時柱)", result['hour_pillar'], result['hour_hanja'], 'hour'),
        ("일주(日柱)", result['day_pillar'], result['day_hanja'], 'day'),
        ("월주(月柱)", result['month_pillar'], result['month_hanja'], 'month'),
        ("연주(年柱)", result['year_pillar'], result['year_hanja'], 'year')
    ]
    
    for col, (title, pillar, hanja, pos) in zip(cols, pillars):
        with col:
            st.markdown(f"**{title}**")
            st.markdown(f"### {hanja}")
            st.caption(f"한글: {pillar}")
            
            # 십신 표시
            if pos == 'day':
                st.info(f"**일간** ({result['day_stem_hanja']})")
            else:
                st.info(f"**십신**: {result['sipsin'][pos]}")
            
            # 12운성 표시
            st.success(f"**12운성**: {result['unsung'][pos]}")
            
            # 납음오행 표시
            st.caption(f"납음: {result['napeum'][pos]}")
    
    st.divider()
    
    # 오행 분석
    st.subheader("🌟 오행 분석 (五行)")
    
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
    
    st.divider()
    
    # 신살 표시
    st.subheader("✨ 신살 (神殺)")
    
    sinsal_cols = st.columns(2)
    with sinsal_cols[0]:
        if result['sinsal']['cheonul']:
            st.success(f"**천을귀인**: {', '.join(result['sinsal']['cheonul'])}")
        if result['sinsal']['yeokma']:
            st.info(f"**역마살**: {', '.join(result['sinsal']['yeokma'])}")
        if result['sinsal']['dohwa']:
            st.warning(f"**도화살**: {', '.join(result['sinsal']['dohwa'])}")
    
    with sinsal_cols[1]:
        if result['sinsal']['gongmang']:
            st.error(f"**공망**: {', '.join(result['sinsal']['gongmang'])}")
        if result['sinsal']['wonjin']:
            st.warning(f"**원진**: {', '.join(result['sinsal']['wonjin'])}")
    
    st.divider()
    
    # 형충회합 표시
    st.subheader("⚡ 형충회합 (刑沖會合)")
    
    hch = result['hyungchunghap']
    hch_cols = st.columns(3)
    
    with hch_cols[0]:
        if hch['chung']:
            st.error(f"**충(沖)**: {', '.join(hch['chung'])}")
        else:
            st.caption("충(沖): 없음")
    
    with hch_cols[1]:
        if hch['yukhap']:
            st.success(f"**육합**: {', '.join(hch['yukhap'])}")
        if hch['samhap']:
            st.success(f"**삼합**: {', '.join(hch['samhap'])}")
        if hch['banghap']:
            st.success(f"**방합**: {', '.join(hch['banghap'])}")
        if not (hch['yukhap'] or hch['samhap'] or hch['banghap']):
            st.caption("합(合): 없음")
    
    with hch_cols[2]:
        if hch['hyung']:
            st.warning(f"**형(刑)**: {', '.join(hch['hyung'])}")
        else:
            st.caption("형(刑): 없음")
    
    st.divider()
    
    # 대운 표시
    st.subheader("🔮 대운 (大運)")
    
    daeun = result['daeun']
    st.caption(f"**{daeun['start_age']}세부터 시작**, {daeun['direction']}")
    
    # 대운표를 DataFrame으로 표시
    import pandas as pd
    
    daeun_data = []
    for d in daeun['list']:
        daeun_data.append({
            '나이': f"{d['age']}~{d['age']+9}세",
            '간지': d['pillar'],
            '천간': d['stem'],
            '지지': d['branch']
        })
    
    df_daeun = pd.DataFrame(daeun_data)
    st.dataframe(df_daeun, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # 세운 표시
    st.subheader("📅 세운 (歲運)")
    
    seun = result['seun']
    
    # 현재 년도를 강조하여 표시
    seun_cols = st.columns(4)
    for i, s in enumerate(seun):
        col_idx = i % 4
        with seun_cols[col_idx]:
            if s['is_current']:
                st.success(f"**{s['year']}년**\n{s['jiazi']}\n({s['age']}세) ⭐")
            else:
                st.text(f"{s['year']}년\n{s['jiazi']}\n({s['age']}세)")
    
    # 음양 분석
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
            with st.spinner("AI가 사주를 풀이하는 중... (약 10-20초 소요)"):
                # OpenAI 클라이언트 초기화
                openai.api_key = st.secrets["OPENAI_API_KEY"]
                
                interpretation = get_saju_interpretation(result)
                
                st.session_state['interpretation'] = interpretation
        
        # 풀이 결과 표시
        if 'interpretation' in st.session_state:
            st.markdown("### 📖 AI 사주 풀이")
            st.markdown(st.session_state['interpretation'])
            
            # 다운로드 버튼
            download_text = f"""
사주팔자 만세력 계산 결과
==================

생년월일시: {result['birth_date']}

사주팔자
-------
- 연주(年柱): {result['year_pillar']} ({result['year_hanja']})
- 월주(月柱): {result['month_pillar']} ({result['month_hanja']})
- 일주(日柱): {result['day_pillar']} ({result['day_hanja']})
- 시주(時柱): {result['hour_pillar']} ({result['hour_hanja']})

오행 분석
--------
천간: {', '.join(result['stems_elements'])}
지지: {', '.join(result['branches_elements'])}

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
