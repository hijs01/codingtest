"""
validate_weekly_pr.py

[목적]
이 스크립트는 GitHub Pull Request(PR)가 올라올 때 자동으로 실행되어,
코딩 테스트 스터디의 "출석 + 제출 규칙"을 지켰는지 검사한다.

[이 스크립트가 확인하는 것]
✅ weekly/YYYY-WXX/ 폴더 아래에서 제출했는가
✅ 한 PR에 한 주차만 제출했는가
✅ 한 PR에 한 사람만 제출했는가
✅ solutions/<github-id>/ 구조를 지켰는가
✅ README.md가 존재하는가
✅ p1, p2, p3 폴더가 모두 존재하는가
✅ 각 p폴더에 코드 파일이 최소 1개 이상 있는가

[이 스크립트가 하지 않는 것]
❌ 문제 정답 여부 확인
❌ 코드 실행 / 채점
❌ 풀이 설명 내용 검사

즉, 이 코드는 "출첵 + 제출 형식 검증" 전용이다.
"""

import os
import re
import subprocess
import sys
from typing import List, Set

# ==============================
# 1. 코드 파일로 인정할 확장자 목록
# ==============================
# 언어가 달라도 상관없게 확장자 화이트리스트 방식 사용
# 필요하면 자유롭게 추가/삭제 가능
ALLOWED_CODE_EXT = {
    ".py", ".java", ".kt",
    ".cpp", ".cc", ".cxx", ".c", ".h", ".hpp",
    ".js", ".ts", ".jsx", ".tsx",
    ".go", ".rs", ".cs",
    ".php", ".rb", ".swift",
    ".dart", ".scala", ".lua",
    ".sql",
}

# (참고용) 주차 경로 패턴
# 현재 코드에서는 직접 사용하지 않지만,
# weekly/2026-W01/solutions/<github-id>/ 형태를 설명하기 위해 남겨둠
WEEK_DIR_PATTERN = re.compile(r"^weekly/\d{4}-W\d{2}/solutions/([^/]+)/")


# ==============================
# 2. git 명령 실행 함수
# ==============================
def run_git(args: List[str]) -> str:
    """
    git 명령어를 실행하고 결과(stdout)를 문자열로 반환한다.

    예:
        run_git(["diff", "--name-only", "BASE..HEAD"])

    git 실행 중 에러가 나면:
    - 에러 메시지를 출력
    - sys.exit(1)로 즉시 실패 처리
    """
    try:
        output = subprocess.check_output(
            ["git"] + args,
            stderr=subprocess.STDOUT
        )
        return output.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError as e:
        print("❌ Git 명령 실행 실패:", "git " + " ".join(args))
        print(e.output.decode("utf-8", errors="replace"))
        sys.exit(1)


# ==============================
# 3. 실패 / 성공 출력 헬퍼
# ==============================
def fail(msg: str) -> None:
    """
    실패 메시지를 출력하고 프로그램 종료.
    GitHub Actions에서는 ❌ 처리됨.
    """
    print(f"❌ {msg}")
    sys.exit(1)


def ok(msg: str) -> None:
    """
    성공 메시지 출력 (프로그램 종료는 안 함)
    """
    print(f"✅ {msg}")


# ==============================
# 4. PR에서 변경된 파일 목록 가져오기
# ==============================
def changed_files(base_sha: str, head_sha: str) -> List[str]:
    """
    PR 기준으로 base → head 사이에서
    변경된 파일 경로 목록을 반환한다.
    """
    diff_output = run_git([
        "diff",
        "--name-only",
        f"{base_sha}..{head_sha}"
    ])
    return [line.strip() for line in diff_output.splitlines() if line.strip()]


# ==============================
# 5. PR에서 건드린 주차 폴더 찾기
# ==============================
def detect_week_folders(files: List[str]) -> Set[str]:
    """
    변경된 파일 목록에서
    weekly/YYYY-WXX 형태의 주차 폴더를 추출한다.

    반환값 예:
        {"weekly/2026-W01"}
    """
    weeks = set()
    for f in files:
        parts = f.split("/")
        if len(parts) >= 2 and parts[0] == "weekly":
            weeks.add("/".join(parts[:2]))
    return weeks


# ==============================
# 6. PR에서 제출한 GitHub ID 추출
# ==============================
def detect_github_ids(files: List[str], week_folder: str) -> Set[str]:
    """
    weekly/YYYY-WXX/solutions/<github-id>/ 구조에서
    <github-id>를 추출한다.
    """
    ids = set()
    prefix = week_folder + "/solutions/"

    for f in files:
        if f.startswith(prefix):
            rest = f[len(prefix):]
            github_id = rest.split("/", 1)[0]
            if github_id:
                ids.add(github_id)

    return ids


# ==============================
# 7. 특정 폴더 안에 코드 파일이 있는지 검사
# ==============================
def has_code_file_in_dir(dirpath: str) -> bool:
    """
    폴더 내부(하위 폴더 포함)에
    허용된 확장자의 코드 파일이 하나라도 있으면 True
    """
    if not os.path.isdir(dirpath):
        return False

    for root, _, files in os.walk(dirpath):
        for name in files:
            _, ext = os.path.splitext(name)
            if ext.lower() in ALLOWED_CODE_EXT:
                return True

    return False


# ==============================
# 8. 메인 검증 로직
# ==============================
def main() -> None:
    # GitHub Actions에서 전달한 PR 기준 SHA
    base_sha = os.environ.get("BASE_SHA")
    head_sha = os.environ.get("HEAD_SHA")

    if not base_sha or not head_sha:
        fail("BASE_SHA 또는 HEAD_SHA 환경 변수가 없습니다.")

    # PR에서 변경된 파일 목록
    files = changed_files(base_sha, head_sha)
    if not files:
        fail("이 PR에는 변경된 파일이 없습니다.")

    # weekly 폴더 제출 여부 확인
    week_folders = detect_week_folders(files)
    if not week_folders:
        fail("weekly/ 폴더 아래에 제출해야 합니다.")

    # 한 PR에 한 주차만 허용
    if len(week_folders) > 1:
        fail(
            "한 PR에는 한 주차만 제출할 수 있습니다: "
            + ", ".join(sorted(week_folders))
        )

    week_folder = sorted(week_folders)[0]
    solutions_root = os.path.join(week_folder, "solutions")

    if not os.path.isdir(solutions_root):
        fail(f"{week_folder}/solutions 폴더가 없습니다.")

    # 제출한 GitHub ID 확인
    github_ids = detect_github_ids(files, week_folder)
    if not github_ids:
        fail("solutions/<github-id>/ 구조로 제출해야 합니다.")

    # 한 PR에 한 사람만 허용
    if len(github_ids) > 1:
        fail(
            "한 PR에는 한 명만 제출할 수 있습니다: "
            + ", ".join(sorted(github_ids))
        )

    github_id = sorted(github_ids)[0]
    user_dir = os.path.join(week_folder, "solutions", github_id)

    # README.md 필수
    readme_path = os.path.join(user_dir, "README.md")
    if not os.path.isfile(readme_path):
        fail(f"README.md가 없습니다: {readme_path}")

    # p1, p2, p3 폴더 및 코드 파일 검사
    missing = []
    for i in (1, 2, 3):
        pdir = os.path.join(user_dir, f"p{i}")
        if not os.path.isdir(pdir):
            missing.append(f"p{i} 폴더")
            continue
        if not has_code_file_in_dir(pdir):
            missing.append(f"p{i} 코드 파일")

    if missing:
        fail(
            "제출이 완전하지 않습니다. 누락 항목: "
            + ", ".join(missing)
        )

    # 모든 검사 통과
    ok(f"제출 검증 통과 🎉 (주차: {week_folder}, 제출자: {github_id})")
    ok("p1, p2, p3 및 README.md 모두 확인됨")


# ==============================
# 9. 실행 진입점
# ==============================
if __name__ == "__main__":
    main()
