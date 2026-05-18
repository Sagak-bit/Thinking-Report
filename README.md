# Thinking-Enforced AI

> "AI를 막는 것이 아니라, 인간의 사고 과정을 보존한다."
>
> 청소년 사용자가 AI에 정답을 외주하지 않고 스스로 사고하도록 강제하는 AI 사고 코치.
> 기반 문서: `Want_to_Implement.pdf`

## 핵심 컨셉

기존 생성형 AI는 **빠른 정답 제공** 중심입니다. 사용자가 "보고서 써줘" 하면 곧바로 결과물을 토해냅니다.
Thinking-Enforced AI는 그 반대입니다:

1. **Problem Framing** — "당신이 진짜 해결하려는 문제는 뭔가요?"
2. **Exploration** — 반대 사례, 다른 관점, 관련 개념을 제시 (답은 X)
3. **Thinking Construction** — "당신의 가설은? 근거는? 예상 반론은?"
4. **Reflective Feedback** — 사고 과정 자체에 피드백
5. **Synthesis** — 4가지 Cognitive Closure 조건 충족 시 비로소 종합 답변

매 턴마다 별도의 **평가자 LLM**이 사용자가 다음 4조건을 충족했는지 JSON으로 판단합니다:
- Problem Framing Complete
- Hypothesis Formation
- Counter Perspective Exposure
- Reflective Revision

조건이 충족되면 자동으로 다음 단계로 진행하고, 4조건이 모두 충족되면 Synthesis 단계로 점프합니다.
모든 사고 과정은 `thinking_data/` 에 JSON으로 누적 저장됩니다.

## 빠른 시작

### 1. Python 환경

Python 3.9+ 권장.

```powershell
# 가상환경 (선택)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2. OpenAI API 키 설정 — 다음 두 방법 중 하나를 선택

**방법 A. 화면에서 직접 입력 (가장 간단)**

앱을 실행하면 왼쪽 사이드바에 `OpenAI API Key` 입력란이 나옵니다. 거기에 `sk-...` 키를 붙여넣으면 끝.
이 키는 브라우저 세션에만 머물고 저장되지 않습니다.

**방법 B. `.env` 파일로 자동 로드 (편함)**

1. 이 폴더에 있는 `.env.example` 파일을 복사해 이름을 `.env` 로 바꿉니다.
2. `.env` 파일을 열어 다음 줄의 값을 본인 키로 교체합니다:

```env
OPENAI_API_KEY=sk-여기에-당신의-키를-붙여넣으세요
```

저장하고 닫으면, 앱 실행 시 자동으로 불러옵니다.

> 키 발급: https://platform.openai.com/api-keys

### 3. 실행

```powershell
streamlit run app.py
```

브라우저가 자동으로 열립니다 (보통 `http://localhost:8501`).

## 사용 방법

1. 사이드바에서 **모델** 선택 (gpt-4o-mini 추천 / 더 정교한 반례를 원하면 gpt-4o)
2. **과목·사고 프레임** 선택 (일반/수학/과학/역사/국어·문학/사회)
3. 본문에서 다루고 싶은 문제 입력
4. AI가 답을 주지 않고 질문·반례·관점을 제시 → 응답 → 평가자가 단계 통과 여부 판단
5. 5단계를 모두 통과하면 비로소 종합 답변 제공
6. 사이드바에서 **Thinking Data 다운로드** 버튼으로 JSON 저장

## 시연용 예시

**일반 모드에서 "보고서 써줘" 라고 입력해 보세요.**

기존 AI: 즉시 보고서 작성 시작.
이 AI: "어떤 문제를 다루려는 거예요? 그 문제가 왜 중요한지, 당신의 초기 가정은 뭔지부터 들려주세요."

## 파일 구조

```
yjj_assignment/
├── app.py              # Streamlit 메인
├── prompts.py          # 핵심 원칙 + 5단계 프롬프트 + 평가자 프롬프트
├── subjects.py         # 과목별 사고 프레임
├── requirements.txt
├── .env.example        # API 키 템플릿
├── .env                # (직접 생성, gitignore 권장)
├── README.md
├── Want_to_Implement.pdf
└── thinking_data/      # 세션별 JSON 로그 (자동 생성)
```

## 커스터마이즈 포인트

- **새 과목 추가**: `subjects.py`의 `SUBJECT_FRAMEWORKS` dict에 항목 추가
- **단계 흐름 변경**: `prompts.py`의 `STAGE_PROMPTS` 수정
- **사고 코치 톤 조정**: `prompts.py`의 `CORE_PRINCIPLES` 수정
- **Cognitive Closure 조건**: `prompts.py`의 `EVALUATOR_PROMPT` + `app.py`의 `CLOSURE_LABELS`

## 비용 가이드

- gpt-4o-mini: 한 턴(코치+평가자 2회 호출) 당 약 $0.0005~0.002. 30턴 대화 ≈ $0.05.
- gpt-4o: 약 10배. 30턴 대화 ≈ $0.5.

## 알려진 한계

- 평가자가 매 턴 LLM 호출이라 응답 약 1.5~3초 추가됨.
- 사용자가 의도적으로 "예/아니오"만 답하며 단계를 통과하려 하면, 평가자가 적절히 false 판정해야 함. 보수적 평가 기준이 프롬프트에 포함돼 있지만 완벽하지는 않음.
- 현재 단일 사용자 로컬 데모. 다중 사용자 운영은 별도 백엔드 필요.

## Streamlit Community Cloud 배포

운영자(=배포자) 키를 Streamlit Secrets에 보관하고, 접속자는 키 입력 없이 바로 쓰는 구조입니다.
앱 사이드바에는 "내 키 직접 사용" 토글이 자동 노출되어 BYOK도 가능합니다.

### 1) GitHub 레포 만들기

GitHub에서 새 public(또는 private) 레포 생성 후, 로컬에서:

```powershell
git init
git add .
git commit -m "Initial commit: Thinking-Enforced AI"
git branch -M main
git remote add origin https://github.com/<YOUR_GH_ID>/<REPO_NAME>.git
git push -u origin main
```

> `.gitignore` 가 이미 `.env`, `.streamlit/secrets.toml`, `thinking_data/` 를 제외합니다.
> 혹시라도 키가 들어간 파일을 커밋하지 않도록 push 전 `git status` 로 한 번 더 확인하세요.

### 2) Streamlit Community Cloud 연결

1. https://share.streamlit.io 접속 후 GitHub로 로그인
2. **New app** → 방금 만든 레포 선택
3. Branch: `main`, Main file path: `app.py`
4. **Advanced settings**:
   - Python version: `3.12` (3.14는 미지원이므로 명시적으로 선택)
   - **Secrets** 칸에 아래 내용 붙여넣기:
     ```toml
     OPENAI_API_KEY = "sk-여기에-당신의-키를-붙여넣으세요"
     ```
5. **Deploy!** 클릭

배포 후 URL이 `https://<your-app>.streamlit.app` 형태로 나옵니다.

### 3) 배포 후 동작

- 사이드바 상단에 "🔐 API Key가 자동으로 로드되었습니다" 메시지가 보이면 정상.
- 접속자가 자기 키를 쓰고 싶다면 "내 OpenAI API Key 직접 사용" 체크박스 활용.
- 로컬 파일 저장은 비활성화됩니다 — `thinking_data/` 는 컨테이너 재시작 시 사라지므로,
  **사이드바의 "⬇️ Thinking Data 다운로드" 버튼**을 사용해 JSON을 받아두세요.

### 4) 비용 가드 (운영자 키 사용 시 권장)

- URL을 공개로 공유하면 누구나 무료로 호출할 수 있습니다 → 비용 폭주 가능.
  친구·시연 대상에게만 비공개로 URL 공유하는 것을 강력 권장.
- 더 안전하게는 OpenAI 대시보드에서 **사용 한도(Usage limit)** 를 월 단위로 걸어두세요:
  https://platform.openai.com/account/limits
- 평가자 LLM이 매 턴 별도 호출되므로, 한 턴 ≈ 2회 호출입니다.
  - gpt-4o-mini 기준 30턴 대화 ≈ $0.05
  - gpt-4o 기준 30턴 대화 ≈ $0.5

### 5) 키 회전 / 비활성

운영 중 키를 바꾸려면:
- Streamlit Cloud → 앱의 **Settings → Secrets** 에서 값 수정 후 저장 → 자동 재시작
- 또는 OpenAI 대시보드에서 기존 키 revoke

---

PDF 기반 컨셉 구현 — 추가 기능(예: Thinking Data 시각화 대시보드, 사고 데이터 비교, B2B 학교용 다중 학생 관리)은 요청 시 확장 가능.
