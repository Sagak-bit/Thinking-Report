"""
Thinking-Enforced AI - Streamlit 앱.

실행:
    streamlit run app.py

사이드바에서 OpenAI API Key를 입력하거나, .env 파일에 OPENAI_API_KEY를 설정하세요.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from openai import OpenAI

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from prompts import CORE_PRINCIPLES, STAGE_PROMPTS, EVALUATOR_PROMPT
from subjects import SUBJECT_FRAMEWORKS


# ============================================================
# 상수
# ============================================================
STAGES = [
    "problem_framing",
    "exploration",
    "thinking_construction",
    "reflective_feedback",
    "synthesis",
]

STAGE_NAMES_KO = {
    "problem_framing": "1단계: Problem Framing (문제 재정의)",
    "exploration": "2단계: Exploration (탐색)",
    "thinking_construction": "3단계: Thinking Construction (가설 구축)",
    "reflective_feedback": "4단계: Reflective Feedback (성찰 피드백)",
    "synthesis": "5단계: Synthesis (종합)",
}

CLOSURE_LABELS = {
    "problem_framing_complete": "문제 재정의 (Problem Framing)",
    "hypothesis_formation": "가설 형성 (Hypothesis Formation)",
    "counter_perspective_exposure": "반대 관점 검토 (Counter Perspective)",
    "reflective_revision": "사고 수정/강화 (Reflective Revision)",
}

DATA_DIR = Path("thinking_data")

# Streamlit Cloud 등 컨테이너 환경 감지 (filesystem이 ephemeral 함)
IS_CLOUD = bool(os.getenv("STREAMLIT_RUNTIME_CLOUD") or os.getenv("HOSTNAME", "").startswith("streamlit"))


def get_api_key_from_secrets() -> str:
    """st.secrets에서 OPENAI_API_KEY를 읽되, 없으면 빈 문자열."""
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return ""


# ============================================================
# 세션 상태 초기화
# ============================================================
def init_session():
    defaults = {
        "messages": [],
        "current_stage": "problem_framing",
        "closure": {k: False for k in CLOSURE_LABELS},
        "thinking_data": [],
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "started_at": datetime.now().isoformat(),
        "subject": "일반",
        "last_eval": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ============================================================
# Thinking Data 저장
# ============================================================
def save_session():
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"session_{st.session_state.session_id}.json"
    data = {
        "session_id": st.session_state.session_id,
        "started_at": st.session_state.started_at,
        "saved_at": datetime.now().isoformat(),
        "subject": st.session_state.subject,
        "current_stage": st.session_state.current_stage,
        "closure": st.session_state.closure,
        "messages": st.session_state.messages,
        "thinking_data": st.session_state.thinking_data,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def reset_session():
    save_session()
    for k in [
        "messages",
        "current_stage",
        "closure",
        "thinking_data",
        "session_id",
        "started_at",
        "last_eval",
    ]:
        if k in st.session_state:
            del st.session_state[k]
    init_session()


# ============================================================
# 시스템 프롬프트 빌더
# ============================================================
def build_system_prompt(subject: str, stage: str) -> str:
    subj = SUBJECT_FRAMEWORKS[subject]
    stage_prompt = STAGE_PROMPTS[stage]
    stage_hint = subj["stage_hints"].get(stage, "")
    closure_status = "\n".join(
        f"- {CLOSURE_LABELS[k]}: {'✓' if v else '✗'}"
        for k, v in st.session_state.closure.items()
    )
    return f"""{CORE_PRINCIPLES}

【현재 과목·사고 프레임: {subject}】
- 사고 초점: {subj['thinking_focus']}
- 권장 흐름: {subj['flow']}
- 활용 가능한 질문 예시: {' / '.join(subj['key_questions'])}
- 이 단계에서의 과목별 힌트: {stage_hint}

{stage_prompt}

【지금까지의 Cognitive Closure 충족 현황】
{closure_status}

위 정보를 바탕으로, 사용자의 사고를 한 단계 더 깊게 끌고 가는 응답을 작성하세요.
응답은 한국어로, 2~5문장 또는 짧은 질문 형식으로 작성합니다.
"""


# ============================================================
# OpenAI 호출
# ============================================================
def call_chat(client: OpenAI, model: str, system_prompt: str, messages: list) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.7,
    )
    return resp.choices[0].message.content


def call_evaluator(client: OpenAI, model: str, conv_history: str, stage: str, subject: str):
    eval_prompt = EVALUATOR_PROMPT.format(
        conversation_history=conv_history,
        current_stage=stage,
        subject=subject,
    )
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0,
            response_format={"type": "json_object"},
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        return {"_error": str(e)}


# ============================================================
# 사이드바
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.title("⚙️ 설정")

        # 1) Streamlit Secrets > 2) 환경변수 > 3) 사용자 직접 입력
        secret_key = get_api_key_from_secrets()
        env_key = os.getenv("OPENAI_API_KEY", "")
        preset_key = secret_key or env_key

        if preset_key:
            st.success("🔐 API Key가 자동으로 로드되었습니다.")
            override = st.checkbox(
                "내 OpenAI API Key 직접 사용",
                value=False,
                help="체크하면 운영자 키 대신 본인의 키를 사용합니다.",
            )
            if override:
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    value="",
                    help="sk-... 로 시작하는 키. 브라우저 세션에만 저장됩니다.",
                )
            else:
                api_key = preset_key
        else:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value="",
                help="sk-... 로 시작하는 키. 브라우저 세션에만 저장됩니다.",
            )

        model = st.radio(
            "모델 선택",
            ["gpt-4o-mini", "gpt-4o"],
            index=0,
            help="gpt-4o-mini: 저렴하고 빠름 / gpt-4o: 반례·메타인지 피드백 품질이 더 좋음",
        )

        subject = st.selectbox(
            "과목 / 사고 프레임",
            list(SUBJECT_FRAMEWORKS.keys()),
            index=list(SUBJECT_FRAMEWORKS.keys()).index(st.session_state.subject),
        )
        st.session_state.subject = subject

        st.divider()
        st.subheader("🧠 Cognitive Closure")
        st.caption("4조건이 모두 충족되면 Synthesis 단계로 자동 진입")
        for k, label in CLOSURE_LABELS.items():
            mark = "✅" if st.session_state.closure[k] else "⬜"
            st.markdown(f"{mark} {label}")

        st.divider()
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 새 세션", use_container_width=True):
                reset_session()
                st.rerun()
        with col_b:
            save_label = "⬇️ JSON" if IS_CLOUD else "💾 저장"
            if st.button(save_label, use_container_width=True, disabled=IS_CLOUD):
                path = save_session()
                st.success(f"저장: {path.name}")

        if IS_CLOUD:
            st.caption("☁️ 클라우드 환경 — 로컬 저장은 비활성. 아래 다운로드를 사용하세요.")

        if st.session_state.messages:
            data_bytes = json.dumps(
                {
                    "session_id": st.session_state.session_id,
                    "started_at": st.session_state.started_at,
                    "subject": st.session_state.subject,
                    "current_stage": st.session_state.current_stage,
                    "closure": st.session_state.closure,
                    "messages": st.session_state.messages,
                    "thinking_data": st.session_state.thinking_data,
                },
                ensure_ascii=False,
                indent=2,
            ).encode("utf-8")
            st.download_button(
                "⬇️ Thinking Data 다운로드 (JSON)",
                data=data_bytes,
                file_name=f"thinking_{st.session_state.session_id}.json",
                mime="application/json",
                use_container_width=True,
            )

        st.divider()
        st.caption("Thinking-Enforced AI · v0.1")
        st.caption("기반: Want_to_Implement.pdf")

    return api_key, model, subject


# ============================================================
# 메인 영역
# ============================================================
def render_progress():
    idx = STAGES.index(st.session_state.current_stage)
    progress = (idx + 1) / len(STAGES)
    st.progress(progress, text=STAGE_NAMES_KO[st.session_state.current_stage])


def render_subject_panel(subject: str):
    subj = SUBJECT_FRAMEWORKS[subject]
    with st.expander(f"📚 {subject} 사고 프레임", expanded=False):
        st.markdown(f"**사고 초점**: {subj['thinking_focus']}")
        st.markdown(f"**흐름**: {subj['flow']}")
        st.markdown("**예시 질문**")
        for q in subj["key_questions"]:
            st.markdown(f"- {q}")


def render_chat_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def update_closure_and_stage(eval_result: dict):
    """평가 결과로 closure 상태를 누적 갱신하고 단계 진행 결정."""
    if not eval_result or "_error" in eval_result:
        return

    # 누적 갱신 — 한 번 true가 된 조건은 유지
    for k in st.session_state.closure:
        if eval_result.get(k):
            st.session_state.closure[k] = True

    # thinking_data 기록
    if "thinking_data" in eval_result:
        st.session_state.thinking_data.append(
            {
                "timestamp": datetime.now().isoformat(),
                "stage_at_eval": st.session_state.current_stage,
                "closure_snapshot": dict(st.session_state.closure),
                "evaluator_reason": eval_result.get("reason", ""),
                "data": eval_result["thinking_data"],
            }
        )

    st.session_state.last_eval = eval_result

    # 단계 진행 — 평가자 권고 + 안전 가드
    cur_idx = STAGES.index(st.session_state.current_stage)
    if cur_idx >= len(STAGES) - 1:
        return  # 이미 마지막

    advance = eval_result.get("stage_advance_recommended", False)

    # 4조건 모두 충족되면 무조건 synthesis로 점프
    if all(st.session_state.closure.values()):
        st.session_state.current_stage = "synthesis"
        st.toast("🎉 Cognitive Closure 4조건 충족 — Synthesis 단계로 진입")
        return

    if advance:
        st.session_state.current_stage = STAGES[cur_idx + 1]
        st.toast(f"➡️ 다음 단계: {STAGE_NAMES_KO[st.session_state.current_stage]}")


def render_chat(api_key: str, model: str, subject: str):
    user_input = st.chat_input(
        "다루고 싶은 문제나 응답을 입력하세요…",
        disabled=not api_key,
    )

    if not api_key:
        st.info("👈 사이드바에서 OpenAI API Key를 입력해주세요.")
        return

    if not user_input:
        return

    client = OpenAI(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # 사고 코치 응답
    stage = st.session_state.current_stage
    system_prompt = build_system_prompt(subject, stage)

    with st.chat_message("assistant"):
        with st.spinner("사고 코치가 응답 중…"):
            try:
                reply = call_chat(client, model, system_prompt, st.session_state.messages)
            except Exception as e:
                st.error(f"API 호출 오류: {e}")
                return
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Cognitive Closure 평가
    # Synthesis 단계에서는 평가/진행 X
    if stage != "synthesis":
        conv = "\n".join(
            f"[{m['role']}] {m['content']}" for m in st.session_state.messages[-8:]
        )
        with st.spinner("사고 과정 평가 중…"):
            eval_result = call_evaluator(client, model, conv, stage, subject)
        update_closure_and_stage(eval_result)

    st.rerun()


def render_last_eval_panel():
    if not st.session_state.last_eval:
        return
    ev = st.session_state.last_eval
    if "_error" in ev:
        return
    with st.expander("🔍 최근 사고 과정 평가 보기", expanded=False):
        st.markdown(f"**평가자 판단**: {ev.get('reason', '-')}")
        td = ev.get("thinking_data", {})
        if td:
            st.markdown("**Thinking Data**")
            for k, v in td.items():
                st.markdown(f"- `{k}`: {v}")


# ============================================================
# 메인
# ============================================================
def main():
    st.set_page_config(
        page_title="Thinking-Enforced AI",
        page_icon="🧠",
        layout="wide",
    )

    init_session()
    api_key, model, subject = render_sidebar()

    st.title("🧠 Thinking-Enforced AI")
    st.caption(
        "AI를 막는 것이 아니라, 인간의 사고 과정을 보존한다 — "
        "**탐색 → 질문 → 검증 → 수정 → 성찰**"
    )

    render_progress()
    render_subject_panel(subject)
    render_chat_history()
    render_last_eval_panel()
    render_chat(api_key, model, subject)


if __name__ == "__main__":
    main()
