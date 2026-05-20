"""
Thinking-Enforced AI — UI helpers.

토스 ADS 디자인 시스템 톤으로 정리. Pretendard 폰트, 라운드 16px,
부드러운 그림자, 충분한 여백, 카드 기반 레이아웃.
"""

import streamlit as st


# 토스 ADS 컬러 팔레트
COLORS = {
    "primary": "#3182F6",
    "primary_dark": "#1B64DA",
    "primary_light": "#E8F2FE",
    "bg": "#FFFFFF",
    "bg_subtle": "#F9FAFB",
    "bg_muted": "#F2F4F6",
    "text_primary": "#191F28",
    "text_secondary": "#4E5968",
    "text_tertiary": "#8B95A1",
    "border": "#E5E8EB",
    "border_subtle": "#F2F4F6",
    "success": "#00C896",
    "success_bg": "#E6FAF5",
    "warning": "#FF9500",
    "warning_bg": "#FFF4E5",
    "error": "#F04452",
}


CSS = """
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" as="style" crossorigin
      href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css">
<!-- Material Symbols 폰트 — Streamlit 내부 아이콘이 깨지지 않도록 명시 로드 -->
<link rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0">
<link rel="stylesheet"
      href="https://fonts.googleapis.com/icon?family=Material+Icons|Material+Icons+Outlined">

<style>
/* ============================================================
   Global typography
   - body에만 폰트 지정해서 자식이 자연 상속받게 한다.
   - [class*="st-"] 같은 광범위 selector는 Material Symbols 아이콘
     폰트까지 덮어써서 'keyboard_double_arrow_left' 같은 raw text가
     보이게 만든다. 그래서 selector를 좁힌다.
   - 이모지 fallback도 chain에 추가.
   ============================================================ */
:root {
    --tea-font-sans:
        'Pretendard Variable', Pretendard,
        -apple-system, BlinkMacSystemFont, system-ui, Roboto,
        'Apple SD Gothic Neo', 'Noto Sans KR', 'Segoe UI',
        'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
        'Noto Color Emoji', sans-serif;
}

html, body {
    font-family: var(--tea-font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #191F28;
}

/* Streamlit이 자체 selector로 폰트를 강제하는 텍스트 영역만 명시적으로 덮어쓴다. */
.stApp,
.stMarkdown, .stMarkdown p, .stMarkdown li,
.stChatMessageContent, .stChatInput textarea,
.stTextInput input, .stTextArea textarea, .stSelectbox,
.stButton button, .stDownloadButton button,
[data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"],
[data-testid="stChatMessageContent"] {
    font-family: var(--tea-font-sans);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--tea-font-sans);
    font-weight: 700 !important;
    letter-spacing: -0.022em !important;
    color: #191F28 !important;
}

/* ============================================================
   Material Symbols / Icons — 폰트 보호
   Streamlit 사이드바 collapse 버튼, expander caret, 알림 아이콘 등이
   Material Symbols 폰트를 쓰는데, 폰트가 안 잡히면 아이콘 이름이 raw
   text(예: "keyboard_double_arrow_left")로 노출된다.
   아래 selector들은 그 요소들의 폰트를 보호한다.
   ============================================================ */
.material-icons,
.material-icons-outlined,
.material-symbols-outlined,
.material-symbols-rounded,
.material-symbols-sharp,
span.material-symbols-outlined,
[class*="material-icons"],
[class*="material-symbols"],
[data-testid*="Icon"] svg,
[data-testid*="icon"] svg {
    font-family: 'Material Symbols Outlined', 'Material Symbols Rounded',
                 'Material Icons Outlined', 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    font-size: inherit;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
}

h1 { font-size: 2rem !important; line-height: 1.25 !important; }
h2 { font-size: 1.5rem !important; line-height: 1.3 !important; margin-top: 1.5rem !important; }
h3 { font-size: 1.25rem !important; line-height: 1.4 !important; }

p, li, span, div { letter-spacing: -0.01em; }

/* ============================================================
   Main container — max width + spacious padding
   ============================================================ */
.main .block-container {
    max-width: 880px;
    padding-top: 3rem;
    padding-bottom: 6rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* ============================================================
   Sidebar
   ============================================================ */
section[data-testid="stSidebar"] {
    background-color: #F9FAFB;
    border-right: 1px solid #E5E8EB;
}
section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}
section[data-testid="stSidebar"] hr {
    border: 0;
    border-top: 1px solid #E5E8EB;
    margin: 1.25rem 0;
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: 0.95rem !important;
    color: #4E5968 !important;
    letter-spacing: -0.01em !important;
    text-transform: none;
    margin-bottom: 0.5rem !important;
}

/* ============================================================
   Buttons — Toss style
   ============================================================ */
.stButton > button {
    border-radius: 12px !important;
    border: 1px solid #E5E8EB !important;
    background-color: #FFFFFF !important;
    color: #191F28 !important;
    font-weight: 600 !important;
    padding: 10px 16px !important;
    font-size: 0.9rem !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
.stButton > button:hover {
    background-color: #F2F4F6 !important;
    border-color: #D5D9DC !important;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0);
}
.stButton > button:focus {
    box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.15) !important;
    outline: none !important;
}

.stDownloadButton > button {
    border-radius: 12px !important;
    background-color: #F2F4F6 !important;
    border: 1px solid #F2F4F6 !important;
    color: #4E5968 !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}
.stDownloadButton > button:hover {
    background-color: #E8F2FE !important;
    border-color: #E8F2FE !important;
    color: #3182F6 !important;
}

/* ============================================================
   Inputs / Textareas (일반 입력 — chat input은 별도 처리)
   ============================================================ */
.stTextInput input, .stTextArea textarea {
    border-radius: 12px !important;
    border: 1px solid #E5E8EB !important;
    padding: 10px 14px !important;
    font-size: 0.95rem !important;
    background-color: #FFFFFF !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.12) !important;
    outline: none !important;
}

/* ============================================================
   Chat input — 외곽 컨테이너만 시각적 박스, 모든 자손 wrapper와
   textarea는 완전 투명. 이전엔 깊은 wrapper 단계가 있어 자체
   배경/보더를 유지해 박스 안에 박스가 보였음.
   ============================================================ */

/* 외곽 컨테이너 — 유일하게 시각적 박스 */
div[data-testid="stChatInput"] {
    border: 1px solid #E5E8EB !important;
    border-radius: 16px !important;
    background-color: #FFFFFF !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    position: relative !important;
    padding: 0 !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #3182F6 !important;
    box-shadow: 0 0 0 3px rgba(49, 130, 246, 0.12) !important;
}

/* 모든 자손 wrapper (button/svg/path 제외) — 완전 투명·평탄.
   Streamlit이 emotion으로 만드는 임의 className을 모두 캐치. */
div[data-testid="stChatInput"] div,
div[data-testid="stChatInput"] form,
div[data-testid="stChatInput"] section,
div[data-testid="stChatInput"] label,
div[data-testid="stChatInput"] > *:not(button):not(textarea) {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* textarea 본인 — 시각적으로 완전 평탄, 내용 영역만 가짐.
   우측 padding 56px이 send button 자리. */
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInputTextArea"],
[data-testid="stChatInputTextArea"] {
    border: none !important;
    outline: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 14px 56px 14px 18px !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    min-height: 52px !important;
    resize: none !important;
    border-radius: 0 !important;
    color: #191F28 !important;
}
div[data-testid="stChatInput"] textarea:focus,
div[data-testid="stChatInputTextArea"]:focus,
[data-testid="stChatInputTextArea"]:focus {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Send button — 우측 하단 absolute. 평탄화 룰을 다시 깨고
   자기 시각적 스타일을 명시. */
div[data-testid="stChatInput"] button,
div[data-testid="stChatInputSubmitButton"],
[data-testid="stChatInputSubmitButton"] {
    position: absolute !important;
    right: 8px !important;
    bottom: 8px !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 36px !important;
    height: 36px !important;
    min-width: 36px !important;
    flex-shrink: 0 !important;
    z-index: 2 !important;
    background-color: #3182F6 !important;
    background: #3182F6 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    transition: background-color 0.15s !important;
}
div[data-testid="stChatInput"] button:hover,
div[data-testid="stChatInputSubmitButton"]:hover,
[data-testid="stChatInputSubmitButton"]:hover {
    background-color: #1B64DA !important;
    background: #1B64DA !important;
}
div[data-testid="stChatInput"] button:disabled,
div[data-testid="stChatInputSubmitButton"]:disabled {
    background-color: #D5D9DC !important;
    background: #D5D9DC !important;
    cursor: not-allowed !important;
}
/* Send button 안의 아이콘 흰색 강제 */
div[data-testid="stChatInput"] button svg,
div[data-testid="stChatInputSubmitButton"] svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* ============================================================
   Selectbox / Radio
   ============================================================ */
.stSelectbox > div > div {
    border-radius: 12px !important;
    border: 1px solid #E5E8EB !important;
}

/* ============================================================
   Chat messages
   ============================================================ */
div[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border-radius: 18px !important;
    padding: 12px 18px !important;
    margin-bottom: 8px !important;
    line-height: 1.6;
}
/* Assistant message bubble */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background-color: #F9FAFB !important;
    border: 1px solid #F2F4F6 !important;
}
/* User message bubble — Toss-blue tint */
div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background-color: #E8F2FE !important;
    border: 1px solid #E8F2FE !important;
}

/* Avatar refinement */
div[data-testid="stChatMessage"] img,
div[data-testid="stChatMessage"] svg {
    border-radius: 50%;
}

/* ============================================================
   Expander
   ============================================================ */
div[data-testid="stExpander"] {
    border: 1px solid #F2F4F6 !important;
    border-radius: 14px !important;
    background-color: #F9FAFB !important;
    box-shadow: none !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #4E5968 !important;
    padding: 12px 16px !important;
}
div[data-testid="stExpander"] summary:hover {
    background-color: #F2F4F6 !important;
    border-radius: 14px !important;
}

/* ============================================================
   Progress bar (legacy — we replace with custom stepper)
   ============================================================ */
div[data-testid="stProgress"] > div {
    background-color: #F2F4F6 !important;
    border-radius: 100px !important;
    height: 6px !important;
}
div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #3182F6 0%, #1B64DA 100%) !important;
    border-radius: 100px !important;
    height: 6px !important;
}

/* ============================================================
   Status / Toast
   ============================================================ */
div[data-testid="stStatusWidget"] {
    background-color: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid #E5E8EB !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
}

/* ============================================================
   Code / inline code
   ============================================================ */
code {
    background-color: #F2F4F6 !important;
    padding: 2px 6px !important;
    border-radius: 6px !important;
    font-size: 0.88em !important;
    color: #1B64DA !important;
    font-weight: 500 !important;
}

/* ============================================================
   Caption
   ============================================================ */
.stCaption, p[data-testid="stCaptionContainer"] {
    color: #8B95A1 !important;
    font-size: 0.85rem !important;
}

/* ============================================================
   Alert / Success / Info
   ============================================================ */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 16px !important;
}

/* Success alert (info banner) */
div[data-testid="stAlertContentSuccess"] {
    background-color: #E6FAF5 !important;
    color: #00684D !important;
}
div[data-testid="stAlertContentInfo"] {
    background-color: #E8F2FE !important;
    color: #1B4FB0 !important;
}
div[data-testid="stAlertContentWarning"] {
    background-color: #FFF4E5 !important;
    color: #B85C00 !important;
}

/* ============================================================
   Custom: 5-stage stepper
   ============================================================ */
.tea-stepper {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    width: 100%;
    margin: 0.5rem 0 1.5rem 0;
    padding: 0 0.5rem;
}
.tea-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    position: relative;
}
.tea-step__node {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    z-index: 2;
    background-color: #F2F4F6;
    color: #8B95A1;
    border: 2px solid #F2F4F6;
    transition: all 0.2s;
}
.tea-step__label {
    margin-top: 8px;
    font-size: 0.75rem;
    color: #8B95A1;
    font-weight: 500;
    text-align: center;
    line-height: 1.3;
    letter-spacing: -0.01em;
    white-space: nowrap;
}
/* connector line between steps */
.tea-step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 16px;
    left: calc(50% + 16px);
    right: calc(-50% + 16px);
    height: 2px;
    background-color: #F2F4F6;
    z-index: 1;
}
/* Done state */
.tea-step.is-done .tea-step__node {
    background-color: #3182F6;
    color: #FFFFFF;
    border-color: #3182F6;
}
.tea-step.is-done .tea-step__label {
    color: #4E5968;
}
.tea-step.is-done:not(:last-child)::after {
    background-color: #3182F6;
}
/* Active (current) state */
.tea-step.is-active .tea-step__node {
    background-color: #FFFFFF;
    color: #3182F6;
    border-color: #3182F6;
    box-shadow: 0 0 0 4px rgba(49, 130, 246, 0.18);
}
.tea-step.is-active .tea-step__label {
    color: #191F28;
    font-weight: 700;
}

/* ============================================================
   Custom: Hero header
   ============================================================ */
.tea-hero {
    margin-bottom: 2rem;
}
.tea-hero__eyebrow {
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 600;
    color: #3182F6;
    background-color: #E8F2FE;
    padding: 4px 10px;
    border-radius: 100px;
    letter-spacing: 0;
    margin-bottom: 1rem;
}
.tea-hero__title {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.025em !important;
    line-height: 1.2 !important;
    color: #191F28 !important;
    margin: 0 0 0.5rem 0 !important;
}
.tea-hero__subtitle {
    font-size: 1rem;
    color: #4E5968;
    line-height: 1.6;
    margin: 0;
    letter-spacing: -0.01em;
}

/* ============================================================
   Custom: Stage card (active stage summary above chat)
   ============================================================ */
.tea-stage-card {
    background: linear-gradient(135deg, #3182F6 0%, #1B64DA 100%);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(49, 130, 246, 0.18);
}
.tea-stage-card__label {
    font-size: 0.78rem;
    font-weight: 600;
    opacity: 0.85;
    letter-spacing: 0;
    margin-bottom: 4px;
}
.tea-stage-card__title {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 2px;
}
.tea-stage-card__meta {
    font-size: 0.85rem;
    opacity: 0.85;
}

/* ============================================================
   Custom: Closure check cards (sidebar)
   ============================================================ */
.tea-closure-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    margin-bottom: 6px;
    background-color: #FFFFFF;
    border: 1px solid #F2F4F6;
    border-radius: 12px;
    transition: all 0.15s;
}
.tea-closure-item.is-done {
    background-color: #E6FAF5;
    border-color: #E6FAF5;
}
.tea-closure-item__dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #F2F4F6;
    color: #8B95A1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
}
.tea-closure-item.is-done .tea-closure-item__dot {
    background-color: #00C896;
    color: #FFFFFF;
}
.tea-closure-item__text {
    font-size: 0.85rem;
    color: #4E5968;
    font-weight: 500;
    line-height: 1.3;
}
.tea-closure-item.is-done .tea-closure-item__text {
    color: #006B50;
    font-weight: 600;
}

/* ============================================================
   Custom: Section heading mini
   ============================================================ */
.tea-section-h {
    font-size: 0.78rem;
    font-weight: 700;
    color: #8B95A1;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    margin: 1.25rem 0 0.5rem 0;
}

/* ============================================================
   Synthesis banner (over the synthesis message)
   ============================================================ */
.tea-synth-banner {
    background: linear-gradient(135deg, #E8F2FE 0%, #F0F7FF 100%);
    border: 1px solid #C7DDFA;
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    color: #1B4FB0;
    font-weight: 600;
    font-size: 0.92rem;
}
.tea-synth-banner__icon {
    width: 24px;
    height: 24px;
    background-color: #3182F6;
    color: #FFFFFF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

/* ============================================================
   Footer caption
   ============================================================ */
.tea-footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #F2F4F6;
    font-size: 0.78rem;
    color: #8B95A1;
}

/* Hide Streamlit default chrome we don't need */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

/* Toast tweak */
div[data-baseweb="toast"] {
    border-radius: 12px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08) !important;
}
</style>
"""


def inject_css():
    """페이지 첫머리에 한 번만 호출 — 모든 컴포넌트가 그 다음에 그려져야 함."""
    st.markdown(CSS, unsafe_allow_html=True)


def render_hero():
    """페이지 상단 큰 헤더."""
    st.markdown(
        """
        <div class="tea-hero">
          <span class="tea-hero__eyebrow">Thinking-Enforced AI</span>
          <h1 class="tea-hero__title">정답이 아니라 사고 과정을 같이 만드는 AI</h1>
          <p class="tea-hero__subtitle">
            탐색 · 질문 · 검증 · 수정 · 성찰의 5단계를 거쳐
            당신의 사고로 결과물을 완성합니다.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stepper(stages: list, stage_labels: dict, current_stage: str):
    """5단계 stepper 컴포넌트.

    stages: 단계 키 리스트 (순서대로)
    stage_labels: {key: 짧은 한국어 라벨}
    current_stage: 현재 단계 키
    """
    try:
        cur_idx = stages.index(current_stage)
    except ValueError:
        cur_idx = 0

    parts = ['<div class="tea-stepper">']
    for i, key in enumerate(stages):
        if i < cur_idx:
            state_class = "is-done"
            inner = "✓"
        elif i == cur_idx:
            state_class = "is-active"
            inner = str(i + 1)
        else:
            state_class = ""
            inner = str(i + 1)
        label = stage_labels.get(key, key)
        parts.append(
            f'<div class="tea-step {state_class}">'
            f'<div class="tea-step__node">{inner}</div>'
            f'<div class="tea-step__label">{label}</div>'
            f"</div>"
        )
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_stage_card(stage_full_name: str, turns_label: str | None = None):
    """현재 단계 강조 카드 (그라데이션 블루)."""
    meta = f'<div class="tea-stage-card__meta">{turns_label}</div>' if turns_label else ""
    st.markdown(
        f"""
        <div class="tea-stage-card">
          <div class="tea-stage-card__label">현재 단계</div>
          <div class="tea-stage-card__title">{stage_full_name}</div>
          {meta}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_closure_grid(closure_labels: dict, closure_state: dict):
    """사이드바 closure 4조건 카드 그리드."""
    rows = []
    for key, label in closure_labels.items():
        done = closure_state.get(key, False)
        state = "is-done" if done else ""
        dot = "✓" if done else "·"
        rows.append(
            f'<div class="tea-closure-item {state}">'
            f'<div class="tea-closure-item__dot">{dot}</div>'
            f'<div class="tea-closure-item__text">{label}</div>'
            f"</div>"
        )
    st.markdown("".join(rows), unsafe_allow_html=True)


def render_section_heading(text: str):
    """사이드바·메인 안에서 작은 대문자 섹션 헤딩."""
    st.markdown(f'<div class="tea-section-h">{text}</div>', unsafe_allow_html=True)


def render_synthesis_banner():
    """합성 메시지 위 강조 배너."""
    st.markdown(
        """
        <div class="tea-synth-banner">
          <div class="tea-synth-banner__icon">✨</div>
          <div>사고 종합 보고서 — 당신이 거친 사고 과정의 결과물입니다</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
