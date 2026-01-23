from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# 데이터 저장소
todos = [
    {"id": 1, "title": "바닐라 서버 학습", "done": False},
    {"id": 2, "title": "Flask 시작하기", "done": False}
]
next_id = 3

class TodoHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def _send_error_response(self, message, status=400):
        self._send_json_response({"error": message}, status)
    
    def do_GET(self):
        print(f"📥 GET {self.path}")
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == '/todos':
            # 필터링 적용
            result = todos.copy()
            if 'done' in query:
                done_value = query['done'][0].lower() == 'true'
                result = [t for t in result if t['done'] == done_value]
            if 'search' in query:
                search_term = query['search'][0].lower()
                result = [t for t in result if search_term in t['title'].lower()]
            print(f"✅ 조회 결과: {len(result)}개")
            self._send_json_response(result)
            
        elif path.startswith('/todos/'):
            try:
                todo_id = int(path.split('/')[-1])
                todo = next((t for t in todos if t['id'] == todo_id), None)
                if todo:
                    print(f"✅ TODO {todo_id} 조회")
                    self._send_json_response(todo)
                else:
                    print(f"❌ TODO {todo_id} 없음")
                    self._send_error_response("Todo not found", 404)
            except ValueError:
                self._send_error_response("Invalid ID", 400)
        else:
            self._send_error_response("Not Found", 404)
    
    def do_POST(self):
        print(f"📥 POST {self.path}")
        global next_id
        
        if self.path != '/todos':
            self._send_error_response("Not Found", 404)
            return
        
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            print(f"📄 데이터: {body}")
            
            data = json.loads(body)
            if 'title' not in data:
                self._send_error_response("title is required", 400)
                return
            if not data['title'].strip():
                self._send_error_response("title cannot be empty", 422)
                return
            if len(data['title']) > 100:
                self._send_error_response("title too long (max 100)", 422)
                return
            
            new_todo = {
                "id": next_id,
                "title": data['title'],
                "done": data.get('done', False)
            }
            todos.append(new_todo)
            next_id += 1
            print(f"✅ 생성: {new_todo['title']}")
            self._send_json_response(new_todo, 201)
            
        except json.JSONDecodeError:
            print("❌ JSON 파싱 실패")
            self._send_error_response("Invalid JSON", 400)
        except Exception as e:
            print(f"❌ 에러: {e}")
            self._send_error_response("Internal server error", 500)
    
    def do_PATCH(self):
        print(f"📥 PATCH {self.path}")
        if not self.path.startswith('/todos/'):
            self._send_error_response("Not Found", 404)
            return
        
        try:
            todo_id = int(self.path.split('/')[-1])
            todo = next((t for t in todos if t['id'] == todo_id), None)
            if not todo:
                self._send_error_response("Todo not found", 404)
                return
            
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = json.loads(body)
            
            if 'title' in data:
                if len(data['title']) > 100:
                    self._send_error_response("title too long", 422)
                    return
                todo['title'] = data['title']
            if 'done' in data:
                todo['done'] = data['done']
            
            print(f"✅ 수정: TODO {todo_id}")
            self._send_json_response(todo)
            
        except (ValueError, json.JSONDecodeError):
            self._send_error_response("Invalid input", 400)
    
    def do_DELETE(self):
        print(f"📥 DELETE {self.path}")
        if not self.path.startswith('/todos/'):
            self._send_error_response("Not Found", 404)
            return
        
        try:
            todo_id = int(self.path.split('/')[-1])
            global todos
            original_len = len(todos)
            todos = [t for t in todos if t['id'] != todo_id]
            
            if len(todos) == original_len:
                self._send_error_response("Todo not found", 404)
            else:
                print(f"✅ 삭제: TODO {todo_id}")
                self.send_response(204)
                self.end_headers()
        except ValueError:
            self._send_error_response("Invalid ID", 400)

if __name__ == '__main__':
    print("🚀 TODO API 서버 시작!")
    print("📋 http://localhost:8000/todos")
    server = HTTPServer(('localhost', 8000), TodoHandler)
    server.serve_forever()
