# coco 봇 전용 스킬

과정 실습 배포본에는 넣지 않는 coco Slack 봇용 스킬입니다.

| 폴더 | 스킬 | 내용 |
| --- | --- | --- |
| `coco_guide` | `coco-guide` | 봇 자신의 설정, 스레드 명령, 리로드 범위와 연결 문제 안내. 설정을 확인하고 설명만 하며 파일은 수정하지 않습니다 |

## 설치

과정 프로젝트의 `skills/` 아래에 폴더를 복사하고, `agent_settings.yaml`의 `SLACK_AGENT_EXTENSIONS`에 `skills`가 있는지 확인한 뒤 Slack 스레드에서 `리로드`를 입력합니다.

```bash
cp -r coco_guide <과정 프로젝트>/skills/
```

프로필을 지정한 봇(`AGENT_PROFILE`)은 프로필 폴더의 스킬을 사용하므로 이 스킬이 연결되지 않습니다.

## 검사

과정 프로젝트의 설정 항목, 스레드 명령과 파일이 스킬 내용과 맞는지 확인합니다. 과정 저장소를 바꾼 뒤 실행합니다.

```bash
python scripts/check_coco_guide.py <과정 프로젝트>
```
