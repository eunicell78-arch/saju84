"""
사주팔자 만세력 계산기 with OpenAI ChatGPT 풀이
Streamlit Application for Four Pillars of Destiny Calculator with AI Interpretation
"""

import streamlit as st
from datetime import datetime, time
from saju_calculator import calculate_four_pillars, format_saju_display

# OpenAI import with error handling
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# 페이지 설정
st.set_page_config(
    page_title="사주팔자 만세력 계산기",
    page_icon="🔮",
    layout="centered"
)

# 타이틀
st.title("🔮 사주팔자 만세력 계산기")
st.caption("생년월일시를 입력하면 사주팔자를 계산하고 AI가 풀이해드립니다.")

# 사이드바 정보
with st.sidebar:
    st.header("ℹ️ 사용 방법")
    st.markdown("""
    1. 생년월일과 출생시간을 입력하세요
    2. 성별을 선택하세요
    3. **사주 계산하기** 버튼을 클릭하세요
    4. 결과를 확인한 후 **AI 사주풀이** 버튼으로 상세 해석을 받으세요
    """)
    
    st.header("📌 참고사항")
    st.markdown("""
    - 출생시간은 24시간 형식입니다
    - AI 풀이는 OpenAI GPT를 사용합니다
    - 풀이는 참고용이며 전문가 상담을 대체하지 않습니다
    """)


def get_saju_interpretation(saju_result: dict) -> str:
    """
    ChatGPT를 이용한 사주 풀이
    
    Args:
        saju_result: 사주팔자 계산 결과 딕셔너리
    
    Returns:
        AI가 생성한 사주 풀이 텍스트
    """
    # API 키 확인
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        st.error("⚠️ OpenAI API 키가 설정되지 않았습니다.")
        st.info("""
        **Streamlit Cloud 배포 시:**
        1. Streamlit Cloud 대시보드에서 앱 선택
        2. Settings → Secrets 메뉴 선택
        3. 다음 형식으로 API 키 입력:
        ```
        OPENAI_API_KEY = "sk-your-api-key-here"
        ```
        
        **로컬 테스트 시:**
        `.streamlit/secrets.toml` 파일을 생성하고 위 내용을 추가하세요.
        """)
        st.stop()
    
    try:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=api_key)
        
        # 프롬프트 생성
        element_summary = "\n".join([f"  - {k}: {v}개" for k, v in saju_result['element_count'].items()])
        
        prompt = f"""
당신은 30년 경력의 전문 사주명리학자입니다. 
다음 사주팔자를 깊이있고 전문적으로 풀이해주세요.

## 기본 정보
- 생년월일시: {saju_result['birth_date']}
- 성별: {saju_result['gender']}

## 사주팔자
- 연주(年柱): {saju_result['year_pillar']} ({saju_result['year_hanja']})
- 월주(月柱): {saju_result['month_pillar']} ({saju_result['month_hanja']})
- 일주(日柱): {saju_result['day_pillar']} ({saju_result['day_hanja']})
- 시주(時柱): {saju_result['hour_pillar']} ({saju_result['hour_hanja']})

## 오행 분석
- 천간: {' → '.join(saju_result['stems_elements'])}
- 지지: {' → '.join(saju_result['branches_elements'])}
- 일간(본인): {saju_result['day_stem']} ({saju_result['day_stem_element']})

## 오행 분포
{element_summary}

## 풀이 요청사항
다음 항목들을 체계적으로 풀이해주세요:

1. **기본 성향**: 타고난 성격과 기질, 장점과 단점
2. **오행 균형**: 오행의 강약과 조화, 부족하거나 과한 오행
3. **길흉 판단**: 사주의 전반적인 길흉과 운세의 흐름
4. **직업운**: 적합한 직업 분야와 특성
5. **재물운**: 재물에 관한 운세와 재테크 성향
6. **건강운**: 주의해야 할 건강 부분
7. **대인관계**: 인간관계의 특징과 주의사항
8. **인생 조언**: 인생에서 주의할 점과 발전을 위한 조언

한국어로 정중하고 이해하기 쉽게 설명해주세요.
각 항목은 명확하게 구분하여 작성해주시고, 
구체적이고 실용적인 조언을 포함해주세요.
"""
        
        # ChatGPT API 호출
        with st.spinner("🔮 AI가 사주를 풀이하는 중입니다... (약 10-20초 소요)"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # 또는 "gpt-4"
                messages=[
                    {"role": "system", "content": "당신은 30년 경력의 전문 사주명리학자입니다. 사주팔자를 깊이있고 전문적으로 풀이하되, 일반인도 이해하기 쉽게 설명합니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
        
        return response.choices[0].message.content
    
    except Exception as e:
        st.error(f"❌ 풀이 중 오류가 발생했습니다: {str(e)}")
        st.info("""
        **일반적인 오류 원인:**
        - API 키가 올바르지 않음
        - API 사용 한도 초과
        - 네트워크 연결 문제
        - API 키에 충분한 크레딧이 없음
        
        OpenAI 대시보드에서 API 키와 사용량을 확인해주세요.
        """)
        return None


# 메인 UI
st.header("📝 생년월일 정보 입력")

# 입력 폼
col1, col2 = st.columns(2)

with col1:
    birth_date = st.date_input(
        "생년월일",
        value=datetime(1990, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now(),
        format="YYYY-MM-DD"
    )

with col2:
    birth_time = st.time_input(
        "출생 시간",
        value=time(12, 0),
        help="출생 시간을 정확히 알 수 없다면 12시(오정)를 선택하세요"
    )

gender = st.radio(
    "성별",
    options=["남", "여"],
    horizontal=True
)

# 사주 계산 버튼
if st.button("🎯 사주 계산하기", type="primary", use_container_width=True):
    # 사주 계산
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day
    hour = birth_time.hour
    
    try:
        result = calculate_four_pillars(year, month, day, hour, gender)
        
        # 세션 스테이트에 저장
        st.session_state['saju_result'] = result
        
        # 결과 표시
        st.success("✅ 사주 계산이 완료되었습니다!")
        
    except Exception as e:
        st.error(f"❌ 계산 중 오류가 발생했습니다: {str(e)}")
        st.stop()

# 사주 결과 표시
if 'saju_result' in st.session_state:
    result = st.session_state['saju_result']
    
    st.markdown("---")
    st.header("📊 사주팔자 계산 결과")
    
    # 사주팔자 테이블
    st.markdown("### 四柱八字 (사주팔자)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**時柱 (시주)**")
        st.markdown(f"### {result['hour_hanja']}")
        st.caption(result['hour_pillar'])
    
    with col2:
        st.markdown("**日柱 (일주)**")
        st.markdown(f"### {result['day_hanja']}")
        st.caption(result['day_pillar'])
    
    with col3:
        st.markdown("**月柱 (월주)**")
        st.markdown(f"### {result['month_hanja']}")
        st.caption(result['month_pillar'])
    
    with col4:
        st.markdown("**年柱 (연주)**")
        st.markdown(f"### {result['year_hanja']}")
        st.caption(result['year_pillar'])
    
    # 오행 분석
    st.markdown("---")
    st.markdown("### 五行 (오행) 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**천간(天干)**")
        for i, elem in enumerate(result['stems_elements']):
            pillar_names = ["연간", "월간", "일간", "시간"]
            st.write(f"- {pillar_names[i]}: {elem}")
    
    with col2:
        st.markdown("**지지(地支)**")
        for i, elem in enumerate(result['branches_elements']):
            pillar_names = ["연지", "월지", "일지", "시지"]
            st.write(f"- {pillar_names[i]}: {elem}")
    
    # 오행 분포 차트
    st.markdown("**오행 분포**")
    element_colors = {
        "목": "🟢",
        "화": "🔴", 
        "토": "🟡",
        "금": "⚪",
        "수": "🔵"
    }
    
    for element, count in result['element_count'].items():
        bar = "■" * count + "□" * (8 - count)
        emoji = element_colors.get(element, "⚫")
        st.write(f"{emoji} **{element}**: {bar} ({count})")
    
    # 일간 정보
    st.info(f"**일간(日干)**: {result['day_stem']} - {result['day_stem_element']} (본인을 나타내는 기둥)")
    
    # AI 풀이 버튼
    st.markdown("---")
    
    # Check if secrets exist and have the API key
    has_api_key = False
    try:
        has_api_key = "OPENAI_API_KEY" in st.secrets
    except Exception:
        has_api_key = False
    
    if not OPENAI_AVAILABLE:
        st.warning("⚠️ OpenAI 라이브러리가 설치되지 않았습니다. `pip install openai`를 실행하세요.")
    elif not has_api_key:
        st.warning("⚠️ OpenAI API 키가 설정되지 않았습니다. Secrets 설정이 필요합니다.")
        with st.expander("API 키 설정 방법 보기"):
            st.markdown("""
            **Streamlit Cloud에서:**
            1. 앱 대시보드 → Settings → Secrets
            2. 다음 형식으로 입력:
            ```
            OPENAI_API_KEY = "sk-your-api-key-here"
            ```
            
            **로컬 개발 시:**
            1. `.streamlit/secrets.toml` 파일 생성
            2. 위와 동일한 형식으로 입력
            """)
    else:
        if st.button("🔮 AI 사주풀이 보기", type="primary", use_container_width=True):
            interpretation = get_saju_interpretation(result)
            
            if interpretation:
                st.markdown("---")
                st.header("📖 AI 사주 풀이")
                st.markdown(interpretation)
                
                # 다운로드 버튼
                st.markdown("---")
                
                # 전체 결과를 텍스트로 구성
                full_text = format_saju_display(result)
                full_text += "\n\n" + "=" * 50
                full_text += "\n\n【 AI 사주 풀이 】\n\n"
                full_text += interpretation
                
                st.download_button(
                    label="📥 풀이 결과 다운로드 (TXT)",
                    data=full_text.encode('utf-8'),
                    file_name=f"사주풀이_{result['birth_date'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

# 푸터
st.markdown("---")
st.caption("""
💡 **참고사항**: 이 사주 풀이는 AI가 생성한 것으로 참고용입니다. 
정확한 감정을 원하시면 전문 명리학자와 상담하시기 바랍니다.
""")
