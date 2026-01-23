from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 데이터 저장소
todos = [
    {"id": 1, "title": "바닐라 서버 학습", "done": False},
    {"id": 2, "title": "Flask 시작하기", "done": False}
]

class TodoHandler(BaseHTTPRequestHandler):
    
    def _send_json_response(self, data, status=200):
        """JSON 응답 헬퍼 함수"""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
def do_GET(self):
    print(f"📥 GET 요청: {self.path}")
    
    # /todos - 전체 목록
    if self.path == '/todos':
        print("✅ 전체 TODO 목록 반환")
        self._send_json_response(todos)
    
    # /todos/1 - 특정 TODO 조회 (새로 추가)
    elif self.path.startswith('/todos/'):
        try:
            # URL에서 ID 추출
            todo_id = int(self.path.split('/')[-1])
            print(f"🔍 TODO 검색: ID={todo_id}")
            
            # ID로 TODO 찾기
            todo = next((t for t in todos if t['id'] == todo_id), None)
            
            if todo:
                print(f"✅ TODO 발견: {todo['title']}")
                self._send_json_response(todo)
            else:
                print(f"❌ TODO 없음: ID={todo_id}")
                self._send_json_response({"error": "Todo not found"}, 404)
        
        except ValueError:
            print("❌ 잘못된 ID 형식")
            self._send_json_response({"error": "Invalid ID"}, 400)
    
    else:
        print("❌ 경로를 찾을 수 없음")
        self._send_json_response({"error": "Not Found"}, 404)

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), TodoHandler)
    print('🚀 서버 시작: http://localhost:8000')
    print('📝 테스트: http://localhost:8000/todos')
    server.serve_forever()