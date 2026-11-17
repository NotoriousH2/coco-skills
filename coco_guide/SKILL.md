---
name: coco-guide
description: coco 봇 자신의 설정, 스레드 명령, 리로드 범위와 연결 문제를 묻는 질문에 답할 때 사용합니다. 모델, MCP 서버, 스킬, 확장, 시스템 프롬프트, 프로필의 현재 값 확인과 변경 방법 안내를 포함합니다.
metadata:
  type: prompt-bundle
  version: "1.0"
---

## 답변 원칙

- 설명과 확인만 합니다. 설정 파일, 시스템 프롬프트, 스킬과 코드 파일을 `write_file`이나 `run_command`로 수정하지 않습니다.
- 수정을 요청받으면 바꿀 파일, 항목, 값과 반영 방법(리로드 또는 재시작)을 안내합니다. 모델 변경은 `모델` 명령을 안내합니다.
- `.env`의 키와 토큰은 읽거나 출력하지 않습니다. 키와 토큰의 설정 여부는 터미널에서 `python slack_app.py --check`로 확인하도록 안내합니다.
- 현재 값은 추측하지 않고 아래 파일을 `read_file`로 읽어 답합니다. 모델명과 실행 환경은 시스템 지시에도 있습니다.
- 자세한 절차가 필요하면 `slack_setup.md`의 해당 절을 읽고 요약합니다.
- 답변에는 파일 경로, 항목 이름과 반영 방법을 함께 적습니다.

## 파일 구성

경로는 작업 폴더 기준입니다.

| 파일 | 내용 |
| --- | --- |
| `.env` | API 키와 Slack 토큰. 읽지 않습니다 |
| `agent_settings.yaml` | 모델, 로컬 서버 연결, 확장, MCP 선택, 기본 채널, 프로필 |
| `system_prompt.md` | 기본 시스템 프롬프트 |
| `mcp_servers.json` | 연결할 수 있는 MCP 서버 목록과 실행 설정 |
| `skills/<폴더>/SKILL.md` | 스킬 지침. 폴더를 추가하면 스킬이 늘어납니다 |
| `profiles/<이름>/agent.json` | 프로필 봇의 모델, 프롬프트, 도구와 MCP 설정 |
| `slack_setup.md` | Slack 앱 설정, 실행, 명령과 문제 해결 안내 |
| `outputs/slack_mcp_server.log` | 봇이 실행한 Slack MCP 서버의 로그 |

## agent_settings.yaml 항목

`.env`나 환경 변수에 같은 이름이 있으면 그 값이 우선합니다.

| 항목 | 의미 |
| --- | --- |
| `MODEL_PLATFORM` | 대화 모델 플랫폼: `openrouter`, `llamacpp`, `vllm` |
| `OPENROUTER_MODEL_ID` | OpenRouter 대화 모델 |
| `VISION_MODEL_ID` | 이미지 분석 도구의 OpenRouter 모델 |
| `LOCAL_BASE_URL`, `LOCAL_MODEL_ID`, `LOCAL_API_KEY` | llama.cpp 서버 주소, 모델 별칭, 인증 값 |
| `VLLM_BASE_URL`, `VLLM_MODEL_ID` | vLLM 서버 주소와 모델 이름 |
| `SLACK_DEFAULT_CHANNEL_ID` | Slack MCP 도구의 기본 채널. 비어 있으면 Slack 도구가 DRY-RUN 응답을 반환합니다 |
| `AGENT_PROFILE` | 사용할 프로필 폴더. 비어 있으면 기본 구성입니다 |
| `SLACK_AGENT_EXTENSIONS` | 연결할 확장 모듈: `skills`, `context_middleware`, `summarization`, `memory`, `retrieval` |
| `SLACK_MCP_SERVERS` | 연결할 MCP 서버 이름. `mcp_servers.json`에 등록된 이름을 쉼표로 나열합니다 |

## 스레드 명령

| 명령 | 동작 |
| --- | --- |
| `리로드`, `새로고침`, `reload` | 진행 중인 요청이 끝난 뒤 설정, 도구, 확장, 스킬과 프롬프트를 다시 읽습니다 |
| `모델` | 현재 모델을 표시합니다 |
| `모델 <모델명>`, `모델 <플랫폼> [모델명]` | 서버의 모델 목록을 확인한 뒤 `agent_settings.yaml`에 저장하고 리로드합니다 |
| `출력모드 1/2/3` | 이 스레드의 표시 방식을 `final`, `compact`, `verbose`로 바꿉니다 |
| `도움말` | 명령 목록을 표시합니다 |

봇을 실행한 터미널에서는 `R`과 Enter로 리로드하고 `Ctrl+C`로 종료합니다.

## 변경 사항의 반영

| 바꾼 것 | 반영 방법 |
| --- | --- |
| 대화 모델 | `모델` 명령. 프로필 봇은 `agent.json`을 고친 뒤 `리로드` |
| `VISION_MODEL_ID` | 다음 이미지 분석부터 적용 |
| `system_prompt.md`, 스킬 추가와 수정, `SLACK_AGENT_EXTENSIONS`, `tools.py`, 확장 모듈 코드 | `리로드` |
| `SLACK_MCP_SERVERS`, `mcp_servers.json`, `AGENT_PROFILE`, `.env`의 토큰, `slack_app.py` | 봇 재시작: `Ctrl+C` 후 `python slack_app.py` |
| `SLACK_DEFAULT_CHANNEL_ID` | Slack MCP 서버 재시작. 봇이 서버를 실행했다면 봇 재시작 |

대화 기록과 저장된 사용자 메모리는 리로드와 재시작 뒤에도 유지됩니다.

## 확인 절차

- 모델: 시스템 지시의 모델명과 `agent_settings.yaml`의 `MODEL_PLATFORM`, 해당 플랫폼의 모델 항목을 확인합니다.
- MCP 서버: `SLACK_MCP_SERVERS`와 `mcp_servers.json`을 읽습니다. 실제 연결 여부는 봇 시작 요약의 `연결 실패 MCP` 줄이나 `python slack_app.py --check`로 확인합니다.
- 스킬: `list_files`로 `skills` 폴더를 조회합니다.
- 확장과 프로필: `SLACK_AGENT_EXTENSIONS`와 `AGENT_PROFILE`을 읽습니다. 프로필을 지정하면 프로필 폴더의 설정이 확장과 MCP 선택을 대신합니다.

## 연결 문제

먼저 `python slack_app.py --check`를 안내합니다. 실패 항목마다 고칠 방법을 출력합니다.

| 증상 | 확인할 것 |
| --- | --- |
| 멘션에 응답하지 않음 | 봇의 채널 초대, 두 토큰의 종류 |
| Slack 도구가 `DRY-RUN` 응답 | `SLACK_DEFAULT_CHANNEL_ID`와 봇 토큰, Slack MCP 서버 재시작 |
| MCP 서버 연결 실패 | 서버 이름, Node.js 설치(`npx` 서버), `outputs/slack_mcp_server.log` |
| 모델 오류 | 로컬 서버 실행 여부, `*_BASE_URL`과 모델 별칭 |

그 밖의 증상은 `slack_setup.md`의 연결 확인 절을 읽고 안내합니다.
