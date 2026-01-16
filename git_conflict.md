**"Git 충돌(Conflict) 이슈에 대한 트러블슈팅"**

📂 Vanilla Server Git 연동 및 충돌 해결 정리
1. 중첩된 Git 저장소 문제 해결 🚫
문제: va_server/ 폴더 안에 별도의 .git 설정이 있어 메인 저장소에서 인식을 못함.

원인: 하위 폴더가 독립된 저장소(Submodule 형태)로 간주됨.

해결: 하위 폴더의 .git 폴더를 삭제하여 하나의 프로젝트로 통합.

PowerShell
Remove-Item -Recurse -Force va_server\.git

Remove-Item -Recurse -Force va_server\.git
2. 원격(GitHub)과 로컬 동기화 🔄
문제: GitHub 서버의 내용이 로컬 컴퓨터에 없어 push 거부됨.

해결: rebase 전략을 사용하여 원격의 변경 사항을 가져오고 내 작업을 그 뒤에 이어 붙임.

PowerShell
git pull origin main --rebase

3. 병합 충돌(Merge Conflict) 해결 ⚔️
문제: README.md 파일의 내용이 서버와 로컬에서 서로 달라 자동 합치기 실패.

해결: 1. VS Code에서 README.md를 열어 충돌 표시(<<<<, ====)를 제거하고 최종 내용 확정. 2. 수정된 파일을 스테이징 영역에 추가.

PowerShell
git add README.md

git add README.md
4. 리베이스(Rebase) 마무리 🏁
문제: 커밋 메시지가 비어 있어 rebase --continue가 중단됨.

해결: 직접 커밋 메시지를 생성하여 충돌 해결을 기록하고 나머지 과정을 완료.

PowerShell
git commit -m "README 충돌 해결 및 서버 파일 준비"
git rebase --continue


5. 최종 업로드 🚀
해결: 모든 정리가 끝난 후 GitHub로 코드 전송.

PowerShell
git push origin main
