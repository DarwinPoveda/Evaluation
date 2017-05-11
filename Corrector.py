import BaseHTTPServer
import json
import subprocess
import re

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response = get_info(body_content)
        result = grade(problem_name, student_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

def grade(problem_name, student_response):
    
    #Write the file Corrector.java
    program_name = problem_name["problem_name"]
    source_file = open(program_name, 'w')
    source_file.write(student_response)
    source_file.close()
    result = {}
    message = "Ok, File Corrector.java created"
    score=0
    result.update({"score": score, "msg": message})
    result = process_result(result)
    return result

def process_result(result):
    correct = True
    score = result["score"]
    msg = result["msg"]
    result = {}
    result.update({"correct": correct, "score": score, "msg": msg})
    result = json.dumps(result)
    return result

def get_info(body_content):
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    problem_name = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    return problem_name, student_response

if __name__ == "__main__":

    server = BaseHTTPServer.HTTPServer(("localhost", 1720), HTTPHandler)
    print 'Starting Corrector.py Server on port 1720...'
    server.serve_forever()

