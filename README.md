## 🧭 스터디 제출 & 출석 방법

### 한 줄 요약
문제 3개 풀고 PR 1개 올리면 출석 완료  
(README 제출 ❌ 필요 없음)

---

### 1. 이번 주 문제 확인
weekly/YYYY-WXX/problems.md

yaml
Copy code

---

### 2. 레포 Fork (처음 한 번만)
- 스터디 레포 오른쪽 위 **Fork** 클릭
- 내 GitHub 계정으로 fork 생성

---

### 3. VS Code에서 내 fork 열기
1. VS Code 실행
2. `Git: Clone`
3. 내 fork 레포 주소 붙여넣기
4. 폴더 열기

---

### 4. 새 브랜치 만들기 (중요)
- VS Code 왼쪽 아래 `master` 클릭
- **Create new branch**
- 이름 예:
2026-W01-내GitHubID

yaml
Copy code

---

### 5. 문제 풀이 파일 만들기
아래 구조를 그대로 만들기:

weekly/YYYY-WXX/
내GitHubID/
p1/
p2/
p3/

markdown
Copy code

- `p1 / p2 / p3` 모두 필수
- 각 폴더에 코드 파일 1개 이상
- 언어 자유 (Python / Java / C++ 등)
- `.txt` ❌ (자동검증 실패)

**예시**
weekly/2026-W01/
hijs01/
p1/solution.py
p2/solution.java
p3/solution.cpp

yaml
Copy code

---

### 6. Commit & Push
1. VS Code 왼쪽 **Source Control**
2. Commit 메시지 작성
3. **Commit → Push**

---

### 7. Pull Request(PR) 만들기
- Push 후 뜨는 **Create Pull Request** 클릭  
- 또는 GitHub에서 PR 생성

**PR 1개 = 출석 1회**

---

### 8. 자동검증 확인
PR 페이지에서 **Checks** 확인:
- ✅ 통과 → 출석 인정
- ❌ 실패 → 수정 후 다시 push (PR 새로 안 만들어도 됨)

---

### 자주 하는 실수
- p1/p2/p3 중 하나 빠짐  
- 코드 파일 없이 폴더만 있음  
- PR 안 올림  

---

### 핵심 요약
**p1 · p2 · p3 다 올리고 PR만 만들면 끝.**