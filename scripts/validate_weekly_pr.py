"""
validate_weekly_pr.py

[목적]
PR에서 코딩 테스트 스터디 제출 형식을 자동 검증한다.
(출석 + 제출 여부 확인용)

[검증 규칙]
✅ weekly/YYYY-WXX/ 아래에서 제출했는가
✅ 한 PR에 한 주차만 제출했는가
✅ weekly/YYYY-WXX/<github-id>/ 구조인가
✅ 한 PR에 한 명만 제출했는가
✅ README.md 존재
✅ p1, p2, p3 폴더 존재
✅ 각 p폴더에 코드 파일 1개 이상 존재

❌ 정답 여부는 검사하지 않음
"""

import os
import subprocess
import sys
from typing import List, Set

# ==============================
# 코드 파일로 인정할 확장자
# ==============================
ALLOWED_CODE_EXT = {
    ".py", ".java", ".kt",
    ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp",
    ".js", ".ts", ".jsx", ".tsx",
    ".go", ".rs", ".cs",
    ".php", ".rb", ".swift",
    ".dart", ".scala", ".lua",
    ".sql",
}


# ==============================
# git 명령 실행
# ==============================
def run_git(args: List[str]) -> str:
    try:
        out = subprocess.check_output(
            ["git"] + args,
            stderr=subprocess.STDOUT
        )
        return out.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        print("❌ Git 명령 실패:", "git " + " ".join(args))
        print(e.output.decode("utf-8", errors="replace"))
        sys.exit(1)


def fail(msg: str):
    print(f"❌ {msg}")
    sys.exit(1)


def ok(msg: str):
    print(f"✅ {msg}")


# ==============================
# PR에서 변경된 파일 목록
# ==============================
def changed_files(base_sha: str, head_sha: str) -> List[str]:
    out = run_git(["diff", "--name-only", f"{base_sha}..{head_sha}"])
    return [f.strip() for f in out.splitlines() if f.strip()]


# ==============================
# 주차 폴더 탐색
# ==============================
def detect_week_folders(files: List[str]) -> Set[str]:
    weeks = set()
    for f in files:
        parts = f.split("/")
        if len(parts) >= 2 and parts[0] == "weekly":
            weeks.add("/".join(parts[:2]))  # weekly/YYYY-WXX
    return weeks


# ==============================
# github-id 탐색
# ==============================
def detect_github_ids(files: List[str], week_folder: str) -> Set[str]:
    ids = set()
    prefix = week_folder + "/"
    for f in files:
        if f.startswith(prefix):
            rest = f[len(prefix):]
            ghid = rest.split("/", 1)[0]
            if ghid and ghid != "problems.md":
                ids.add(ghid)
    return ids


# ==============================
# 코드 파일 존재 검사
# ==============================
def has_code_file(dirpath: str) -> bool:
    if not os.path.isdir(dirpath):
        return False
    for root, _, files in os.walk(dirpath):
        for name in files:
            _, ext = os.path.splitext(name)
            if ext.lower() in ALLOWED_CODE_EXT:
                return True
    return False


# ==============================
# 메인 로직
# ==============================
def main():
    base_sha = os.environ.get("BASE_SHA")
    head_sha = os.environ.get("HEAD_SHA")

    if not base_sha or not head_sha:
        fail("BASE_SHA 또는 HEAD_SHA 환경변수가 없습니다.")

    files = changed_files(base_sha, head_sha)
    if not files:
        fail("PR에 변경된 파일이 없습니다.")

    # 주차 확인
    week_folders = detect_week_folders(files)
    if not week_folders:
        fail("weekly/YYYY-WXX/ 폴더 아래에 제출해야 합니다.")

    if len(week_folders) > 1:
        fail("한 PR에는 한 주차만 제출할 수 있습니다.")

    week_folder = sorted(week_folders)[0]

    # 제출자 확인
    github_ids = detect_github_ids(files, week_folder)
    if not github_ids:
        fail("weekly/YYYY-WXX/<github-id>/ 구조로 제출해야 합니다.")

    if len(github_ids) > 1:
        fail("한 PR에는 한 명만 제출할 수 있습니다.")

    github_id = sorted(github_ids)[0]
    user_dir = os.path.join(week_folder, github_id)

    # README 검사
    readme = os.path.join(user_dir, "README.md")
    if not os.path.isfile(readme):
        fail("README.md가 없습니다.")

    # p1, p2, p3 검사
    missing = []
    for i in (1, 2, 3):
        pdir = os.path.join(user_dir, f"p{i}")
        if not os.path.isdir(pdir):
            missing.append(f"p{i} 폴더")
            continue
        if not has_code_file(pdir):
            missing.append(f"p{i} 코드 파일")

    if missing:
        fail("누락 항목: " + ", ".join(missing))

    ok(f"제출 검증 통과 🎉 ({week_folder}, {github_id})")
    ok("p1/p2/p3 + README 모두 확인됨")


if __name__ == "__main__":
    main()
