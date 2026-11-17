"""coco-guide 스킬이 과정 프로젝트의 실제 설정 항목, 명령과 파일에 맞는지 검사합니다.

사용법: python scripts/check_coco_guide.py <과정 프로젝트 폴더>
"""

import ast
from pathlib import Path
import re
import sys

import yaml

SKILL = Path(__file__).resolve().parent.parent / "coco_guide" / "SKILL.md"


def constant_sets(path, names):
    """모듈 최상위의 집합 상수를 읽습니다."""
    values = {}
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names:
            values[node.targets[0].id] = set(ast.literal_eval(node.value))
    return values


def main(project):
    project = Path(project).resolve()
    text = SKILL.read_text(encoding="utf-8")
    front, body = text.split("---", 2)[1:]
    metadata = yaml.safe_load(front)
    errors = []
    if metadata.get("name") != "coco-guide" or not metadata.get("description"):
        errors.append("frontmatter의 name과 description을 확인하세요.")

    settings = set(yaml.safe_load((project / "agent_settings.yaml").read_text(encoding="utf-8")))
    for key in sorted(set(re.findall(r"`([A-Z][A-Z_]+_[A-Z_]+)`", body))):
        if key not in settings:
            errors.append(f"agent_settings.yaml에 없는 항목: {key}")
    missing = settings - set(re.findall(r"`([A-Z][A-Z_]+)`", body))
    if missing:
        errors.append("스킬에 설명하지 않은 설정 항목: " + ", ".join(sorted(missing)))

    commands = constant_sets(project / "agent_lib/slack_commands.py", {"RELOAD_COMMANDS", "MODEL_COMMANDS"})
    for name in ("RELOAD_COMMANDS", "MODEL_COMMANDS"):
        for command in commands.get(name, set()) - {"model"}:
            if f"`{command}" not in body:
                errors.append(f"스킬에 없는 스레드 명령: {command}")
    handler = (project / "agent_lib/slack_commands.py").read_text(encoding="utf-8")
    for command in ("출력모드", "도움말"):
        if f'"{command}"' not in handler:
            errors.append(f"봇 코드에 없는 명령: {command}")

    for path in ("agent_settings.yaml", "system_prompt.md", "mcp_servers.json", "slack_setup.md", "slack_app.py",
                 "tools.py", "skills", "profiles"):
        if not (project / path).exists():
            errors.append(f"프로젝트에 없는 경로: {path}")
    servers = yaml.safe_load((project / "mcp_servers.json").read_text(encoding="utf-8"))["mcpServers"]
    for module in ("skills", "context_middleware", "summarization", "memory", "retrieval"):
        if not (project / f"{module}.py").is_file():
            errors.append(f"프로젝트에 없는 확장 모듈: {module}")
    if "slack" not in servers:
        errors.append("mcp_servers.json에 slack 서버가 없습니다.")

    if errors:
        print("\n".join(errors))
        return 1
    print("coco-guide 검사를 통과했습니다.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
