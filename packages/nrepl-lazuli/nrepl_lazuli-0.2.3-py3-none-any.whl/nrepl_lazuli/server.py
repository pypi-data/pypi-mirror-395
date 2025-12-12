import socket
import threading
import random
import sys
import ast
import json
import time
import re
import inspect
import os
import builtins

from .bencode import Bencode, Decoder

class NREPL:
    def __init__(self, host='127.0.0.1', port=7889, debug=False, frame=None, root_dir=None, pwd=os.getcwd()):
        self.host = host
        self.port = port
        self.debug = debug
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = False
        self.watches = {}
        self.watches_by_id = {}
        if frame: self._save_trace_info(frame, "NREPL::Start")
        self._connections = set()
        self._pwd = pwd
        self._root_dir = root_dir

    @staticmethod
    def bind(frame, host='127.0.0.1', port=7889, debug=False, root_dir=None, pwd=os.getcwd()):
        NREPL(host, port, debug, frame, root_dir, pwd).start()

    @staticmethod
    def spawn(host='127.0.0.1', port=7889, debug=False, frame=None, root_dir=None, pwd=os.getcwd()):
        server = []
        def start(server):
            server.append(NREPL(host, port, debug, frame, root_dir, pwd))
            server[0].start()
        repl_handler = threading.Thread(target=start, args=(server,))
        repl_handler.start()
        time.sleep(0.5)
        server[0]._start_trace(sys.setprofile)
        return server[0]

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.is_running = True
        print(f"Server listening on {self.host}:{self.port}")

        self._start_trace(threading.setprofile)
        try:
            with open(".nrepl-port", "w") as f: f.write(str(self.port)+"\n")
            while True:
                client_socket, addr = self.server_socket.accept()
                if(self.debug): print(f"Accepted connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
                self._connections.add(client_socket)
        finally:
            os.remove(".nrepl-port")
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                decoder = Decoder(client_socket)

                request = decoder.decode()
                if(not request): continue
                if(self.debug): print(f"Handling {request}")

                request['__original_file'] = request.get("file")
                if self._root_dir and request.get("file"):
                    request['file'] = request['file'].replace(self._root_dir, self._pwd, 1)

                if 'op' in request:
                    operation = request['op']

                    if operation == 'eval':
                        self.handle_eval(client_socket, request)
                    elif operation == 'clone':
                        self.handle_clone(client_socket, request)
                    elif operation == 'get_watches':
                        self.handle_get_watches(client_socket, request)
                    elif operation == 'unwatch':
                        self.unwatch(client_socket, request)
                    elif operation == 'complete':
                        self.complete(client_socket, request)
                    elif operation == 'find_definition':
                        self.find_definition(client_socket, request)
                    else:
                        self.response_to(client_socket, request, {
                            'op': request['op'],
                            'status': ['done', 'error'],
                            'error': f"unknown operation: {repr(request['op'])}"
                        })
        except (BrokenPipeError, OSError):
            pass
        finally:
            client_socket.close()
            self._connections.remove(client_socket)

    def _need_to_run_as_exec(self, __lazuli__last__code):
        return not isinstance(__lazuli__last__code, ast.Expr)

    def _need_to_run_as_import(self, code, request):
        return request.get('file') and ( isinstance(code, ast.Import) or isinstance(code, ast.ImportFrom) )

    def handle_eval(self, client_socket, request):
        try:
            code = "\n" * request.get("line", 0) + request['code']
            __lazuli__file__name = request.get('file', '<EVAL>')
            __lazuli__file__row = request.get('line', 0)
            __lazuli__parsed__code = ast.parse(code)
            __lazuli__last__code = __lazuli__parsed__code.body.pop()
            __lazuli__locals__vars, __lazuli__globals__vars, __lazuli__watch__path = self.find_watch_point(request.get('file'), request.get('line'), request.get('watch_id'))
            for __lazuli__code in __lazuli__parsed__code.body:
                __lazuli__placeholder__row = "\n" * __lazuli__file__row
                __lazuli__file__row += 1
                exec(compile(__lazuli__placeholder__row + ast.unparse(__lazuli__code), __lazuli__file__name, 'exec'), __lazuli__globals__vars, __lazuli__locals__vars)
            __lazuli__placeholder__row = "\n" * __lazuli__file__row
            if self._need_to_run_as_import(__lazuli__last__code, request):
                exec(compile(__lazuli__placeholder__row + ast.unparse(__lazuli__last__code), __lazuli__file__name, 'exec'), __lazuli__globals__vars, __lazuli__locals__vars)
                response = self._update_watch_points(__lazuli__last__code, request['__original_file'], __lazuli__locals__vars)
                self.response_to(client_socket, request, {
                    'value': json.dumps(response),
                    'status': ['done']
                })
                return
            elif self._need_to_run_as_exec(__lazuli__last__code):
                exec(compile(__lazuli__placeholder__row + ast.unparse(__lazuli__last__code), __lazuli__file__name, 'exec'), __lazuli__globals__vars, __lazuli__locals__vars)
                result = self.return_something_from_exec(__lazuli__last__code, __lazuli__locals__vars)
            else:
                result = eval(compile(__lazuli__placeholder__row + ast.unparse(__lazuli__last__code), __lazuli__file__name, 'eval'), __lazuli__globals__vars, __lazuli__locals__vars)

            if(__lazuli__watch__path):
                self.watches[__lazuli__watch__path[0]][__lazuli__watch__path[1]][__lazuli__watch__path[2]] = {
                    "globals": __lazuli__globals__vars,
                    "locals": __lazuli__locals__vars
                }
            # Execute the code and capture the result
            self.response_to(client_socket, request, {
                'value': json.dumps(self._repr(result)),
                'status': ['done']
            })
        except Exception as e:
            self.response_to(client_socket, request, {
                'ex': json.dumps(self._repr(e)),
                'status': ['done', 'error']
            })

    def return_something_from_exec(self, last_code, locals):
        if isinstance(last_code, ast.Assign):
            vals = []
            for t in last_code.targets:
                if isinstance(t, ast.Attribute):
                    vals.append(locals.get(t.attr))
                else:
                    vals.append(locals.get(t.id))

            if len(vals) > 1:
                return vals
            else:
                return vals[0]
        elif isinstance(last_code, ast.FunctionDef) or isinstance(last_code, ast.ClassDef):
            return locals[last_code.name]
        else:
            # print(f"LAST {type(last_code)}")
            # print(f"LOCALS {locals}")
            return None

    def _repr(self, result, level=0):
        sub_level = level + 1
        t = type(result)
        if level >= 5:
            return ["...", repr(result)]
        elif isinstance(result, BaseException):
            tb = result.__traceback__
            code = tb.tb_frame.f_code
            filename = code.co_filename
            if self._root_dir: filename = filename.replace(self._pwd, self._root_dir, 1)
            stack = [[filename, tb.tb_lineno, None, code.co_qualname]]
            while(tb := tb.tb_next):
                code = tb.tb_frame.f_code
                filename = code.co_filename
                if self._root_dir: filename = filename.replace(self._pwd, self._root_dir, 1)
                stack.append([filename, tb.tb_lineno, None, code.co_qualname])
            stack.reverse()
            return ["exception", ["literal", repr(result)], stack]
        elif t == str:
            return ["string", result]
        elif t == float or t == int:
            return ["number", repr(result)]
        elif t == list:
            return ["coll", "list", "[", ", ", "]", [self._repr(i, sub_level) for i in result]]
        elif t == tuple:
            return ["coll", "list", "(", ", ", ")", [self._repr(i, sub_level) for i in result]]
        elif t == dict:
            return ["map", "dict", "{", ": ", ", ", "}", [[self._repr(i, sub_level), self._repr(result[i], sub_level)] for i in result]]
        elif hasattr(result, "__dict__"):
            attrs = []
            fields = vars(result)
            for field in fields:
                attrs.append([["literal", field], self._repr(fields[field], sub_level)])
            return ["object", repr(t), repr(result), attrs]
        else:
            obj = repr(result)
            fields_in_repr = re.findall(r"([\w\d_]+)=", obj)
            if fields_in_repr:
                attrs = []
                for field in fields_in_repr:
                    if hasattr(result, field):
                        attrs.append([["literal", field], self._repr(getattr(result, field), sub_level)])

                # for tuple in inspect.getmembers(result):
                #     if tuple[0] in fields_in_repr:
                #         attrs.append([["literal", tuple[0]], self._repr(tuple[1], sub_level)])
                return ["object", repr(t), obj, attrs]
            else:
                return ["literal", obj]

    def _update_watch_points(self, code, file, locals):
        names = [n.name for n in code.names]
        file_watches = self.watches.get(file, {})
        for row in file_watches:
            row_watches = file_watches[row]
            for id in row_watches:
                value = row_watches[id]
                if not isinstance(value, dict):
                    value = {"globals": value.f_globals}
                for name in names:
                    value['globals'][name] = locals[name]
        return ["literal", f"imported: {', '.join(names)}"]

    def find_watch_point(self, file, row, watch_id):
        if(watch_id):
            [file, row] = self.watches_by_id.get(watch_id, [None, None])

        if(file != None and row != None):
            file_watches = self.watches.get(file)
            if(not file_watches): return {}, {}, None
            for i in range(row, -1, -1):
                row_watches = file_watches.get(i)
                if(row_watches):
                    first_key = next(iter(row_watches), None)
                    path = [file, i, first_key]
                    first_value = row_watches.get(first_key)
                    if(not first_value):
                        return {}, {}, None
                    elif(isinstance(first_value, dict)):
                        return first_value["locals"], first_value["globals"], path
                    else:
                        return first_value.f_locals, first_value.f_globals, path
            return {}, {}, None
        else:
            return {}, {}, None

    def handle_clone(self, client_socket, request):
        random_number = random.randint(0, 4294967086)
        hex_string = hex(random_number)[2:]
        response = {
            'new_session': hex_string,
            'status': ['done']
        }
        self.response_to(client_socket, request, response)

    def handle_get_watches(self, client_socket, request):
        file = request.get('file')
        original_file = request.get('__original_file')
        file_watches = self.watches.get(file, {})
        results = []
        for row, watch in file_watches.items():
            for id in iter(watch):
                results.append({
                    "file": original_file,
                    "line": row,
                    "id": id
                })
        self.response_to(client_socket, request, {
            'status': ['done'],
            'watches': sorted(results, key=lambda w: w['line']),
            'op': 'get_watches'
        })

    def unwatch(self, client_socket, request):
        watch_id = request.get('watch_id')
        path = self.watches_by_id.get(watch_id)
        if(not path): return
        [file, row] = path
        file_watches = self.watches.get(file)
        if(not file): return
        row_watches = file_watches.get(row)
        if(not row_watches): return
        if(not row_watches[watch_id]): return

        row_watches.pop(watch_id)
        if(not row_watches): file_watches.pop(row)
        if(not file_watches): self.watches.pop(file)
        self.watches_by_id.pop(watch_id)
        self.response_to(client_socket, request, { 'status': ['done'] })

    def complete(self, client_socket, request):
        regex = re.compile(re.escape(request['prefix']).replace(r"", ".*"))
        __lazuli__locals__vars, __lazuli__globals__vars, __lazuli__watch__path = self.find_watch_point(request.get('file'), request.get('line'), request.get('watch_id'))
        result = []

        if context := request.get('context'):
            r = self._safe_eval(request, context)
            for k in dir(r):
                if regex.match(k):
                    value = getattr(r, k)
                    result.append({"candidate": k, "type": self._complete_type(value, 'property')})
        else:
            for k in __lazuli__locals__vars:
                if regex.match(k): result.append({"candidate": k, "type": "local"})
            for k in dir(builtins):
                if regex.match(k):
                    value = getattr(builtins, k)
                    result.append({"candidate": k, "type": self._complete_type(value, 'var')})
            for k in __lazuli__globals__vars:
                if regex.match(k):
                    result.append({"candidate": k, "type": self._complete_type(__lazuli__globals__vars[k], 'var')})
        self.response_to(client_socket, request, { 'completions': result, 'status': ['done'] })

    def _complete_type(self, value, default):
        if isinstance(value, type):
            return 'constant'
        elif inspect.ismethod(value):
            return 'method/public'
        elif inspect.isfunction(value):
            return 'function'
        else:
            return default

    def find_definition(self, client_socket, request):
        try:
            r = self._safe_eval(request, request.get('symbol', ''))
            file = inspect.getfile(r)
            try:
                line = inspect.getsourcelines(r)[1] - 1
                self.response_to(client_socket, request, {
                    'file': file,
                    'line': line,
                    'status': ['done'] }
                )
            except:
                self.response_to(client_socket, request, {
                    'file': file,
                    'line': 0,
                    'status': ['done'] }
                )
        except Exception as e:
            self.response_to(client_socket, request, {
                'status': ['done', 'notfound']
            })

    def _safe_eval(self, request, code):
        __lazuli__locals__vars, __lazuli__globals__vars, __lazuli__watch__path = self.find_watch_point(request.get('file'), request.get('line'), request.get('watch_id'))
        try:
            return eval(code, __lazuli__globals__vars, __lazuli__locals__vars)
        except Exception as e:
            return []

    def response_to(self, client_socket, request, response):
        answer = {'id': request.get('id', 'some_id')} | response
        if(self.debug): print(f"Responding with {answer}")
        response_data = Bencode.encode(answer)
        client_socket.sendall(response_data)

    def stop(self):
        self.is_running = False
        for s in self._connections:
            s.shutdown(socket.SHUT_RDWR)
            s.close()

        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()
        print("nREPL server stopped")

    def _start_trace(self, trace_fun):
        def trace_calls(frame, event, _arg):
            if event == "call":
                self._save_trace_info(frame)
                code = frame.f_code
                file = code.co_filename
                if file.startswith(self._pwd) and '.venv' not in file:
                    params = {
                        'op': 'hit_auto_watch',
                        'file': file,
                        '__original_file': file,
                        'line': frame.f_lineno-1,
                        'status': ['done']
                    }
                    if self._root_dir:
                        params['file'] = file.replace(self._pwd, self._root_dir, 1)
                    for socket in [*self._connections]:
                        self.response_to(socket, {}, params)
        trace_fun(trace_calls)

    def _save_trace_info(self, frame, id=None):
        code = frame.f_code
        func_filename = code.co_filename
        func_lineno = frame.f_lineno - 1
        file_watches = self.watches.get(func_filename)

        if(not file_watches):
            file_watches = {}
            self.watches[func_filename] = file_watches

        row_watches = file_watches.get(func_lineno)
        if(not row_watches):
            row_watches = {}
            file_watches[func_lineno] = row_watches

        if not id:
            id_filename = func_filename
            if self._root_dir:
                id_filename = func_filename.replace(self._pwd, self._root_dir, 1)
            id = f"{id_filename}:{func_lineno + 1}"
        row_watches[id] = frame
        self.watches_by_id[id] = [func_filename, func_lineno]
