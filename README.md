📘 Weekly Coding Test Study

코딩 테스트 실력 향상을 목표로 하는 주 1회 스터디입니다.
매주 정해진 문제를 풀고, Pull Request(PR) 를 통해 출석과 제출을 동시에 관리합니다.

🗓 스터디 운영 방식

주 1회 모임

매주 문제 3개 풀이

Pull Request 1개 제출 = 출석 1회

모임 당일 시작 전까지 PR 제출 필수

프로그래밍 언어 자유

✅ 출석 인정 기준 (중요)

아래 조건을 모두 만족해야 출석으로 인정됩니다.

해당 주차 문제 3개 모두 풀이

지정된 폴더 구조를 지켜서 제출

Pull Request가 모임 시작 전까지 생성

자동 검증(GitHub Actions)을 통과

❌ 모임 시작 이후에 생성된 PR은
풀이가 맞아도 결석 처리됩니다.

🔁 Pull Request(PR)란?

Pull Request(PR) 는
👉 이번 주 문제 풀이를 제출하면서 동시에 출석을 체크하는 방법입니다.

쉽게 말하면:

“이번 주 문제를 다 풀었어요. 확인해 주세요.”
라고 GitHub에 요청하는 버튼입니다.

이 스터디에서는:

PR 1개 = 출석 1회

PR 생성 시간으로 출석 여부를 판단합니다.

✅ 왜 Pull Request로 출석을 하나요?

PR을 사용하면 아래 정보가 자동으로 기록됩니다.

👤 누가 제출했는지 (GitHub 계정)

⏰ 언제 제출했는지 (출석 시간 기준)

📂 무엇을 제출했는지 (문제 풀이 코드)

🤖 제출 조건 충족 여부 (자동 검사)

그래서
“늦었는지”, “문제 다 풀었는지” 같은
애매한 상황이 생기지 않습니다.

📁 폴더 구조 (반드시 지켜주세요)
weekly/
  YYYY-WXX/
    problems.md
    solutions/
      <github-id>/
        p1/
        p2/
        p3/
        README.md

예시
weekly/2026-W01/solutions/hijs01/
  p1/solution.py
  p2/solution.java
  p3/solution.cpp
  README.md

✍️ 제출 방법 (참가자)

이 저장소를 Fork (처음 한 번만)

해당 주차 폴더에 문제 풀이 작성

변경사항 Commit

Pull Request 1개 생성

제출 완료 ✅

👉 매주 PR은 1개만 제출하면 됩니다.

📄 README.md 작성 규칙 (필수)

각자 폴더 안의 README.md에는 아래 내용을 작성해주세요.

# Week XX – 이름(GitHub ID)

## Problem 1
- Approach:
- Time Complexity:
- Space Complexity:

## Problem 2
- Approach:
- Time Complexity:
- Space Complexity:

## Problem 3
- Approach:
- Time Complexity:
- Space Complexity:


언어는 자유

풀이 아이디어는 간단하게라도 반드시 작성

🤖 자동 검증 (GitHub Actions)

Pull Request가 생성되면 자동으로 아래를 검사합니다.

p1, p2, p3 폴더 존재 여부

각 폴더에 코드 파일 존재 여부

README.md 존재 여부

조건을 만족하지 않으면 ❌ PR이 실패하며
출석으로 인정되지 않습니다.

📌 꼭 알아두세요

주당 PR 1개

문제 3개 모두 필수

모임 시작 전 PR 생성이 기준

언어 자유 (Python / Java / C++ / JS 등 모두 가능)