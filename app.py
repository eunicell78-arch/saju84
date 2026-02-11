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
    
    prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다. 
다음 사주팔자를 깊이있고 전문적으로 풀이해주세요.

## 생년월일시
{saju_result['birth_date']}

## 사주팔자
- 연주(年柱): {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주(月柱): {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주(日柱): {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주(時柱): {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행 분석
- 천간: {', '.join(saju_result['stems_elements'])}
- 지지: {', '.join(saju_result['branches_elements'])}
- 오행 개수: {element_str}

## 음양 분석
- 천간: {', '.join(saju_result['stems_yin_yang'])}
- 지지: {', '.join(saju_result['branches_yin_yang'])}

## 풀이 요청사항
다음 항목들을 구조화된 형식으로 풀이해주세요:

### 1. 기본 성향
타고난 성격과 기질을 설명해주세요.

### 2. 오행 균형
오행의 강약과 조화를 분석해주세요. 어떤 오행이 강하고 약한지, 그것이 어떤 의미인지 설명해주세요.

### 3. 길흉 판단
사주의 전반적인 길흉을 평가해주세요.

### 4. 직업운
이 사주에 적합한 직업 분야를 추천해주세요.

### 5. 재물운
재물에 관한 운세를 설명해주세요.

### 6. 건강
주의해야 할 건강 부분을 알려주세요.

### 7. 조언
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
    
    with st.spinner("사주팔자를 계산하는 중..."):
        result = calculate_four_pillars(birth_datetime)
    
    st.success(f"✅ {result['birth_date']} 출생자의 사주팔자")
    
    # 사주팔자 표시
    st.subheader("📊 사주팔자 (四柱八字)")
    
    cols = st.columns(4)
    pillars = [
        ("연주(年柱)", result['year_pillar'], result['year_hanja']),
        ("월주(月柱)", result['month_pillar'], result['month_hanja']),
        ("일주(日柱)", result['day_pillar'], result['day_hanja']),
        ("시주(時柱)", result['hour_pillar'], result['hour_hanja'])
    ]
    
    for col, (title, pillar, hanja) in zip(cols, pillars):
        with col:
            st.metric(label=title, value=pillar)
            st.caption(f"한자: {hanja}")
    
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
    if not OPENAI_AVAILABLE:
        st.warning("⚠️ OpenAI 라이브러리가 설치되지 않았습니다. `pip install openai`를 실행해주세요.")
    elif "OPENAI_API_KEY" not in st.secrets:
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
