import BaseHTTPServer
import json
import os
import subprocess
import re

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        #Define the post for the result
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response = get_info(body_content)
        result = grade(problem_name, student_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

def grade(problem_name, student_response):
    #Write the file Corrector.java
    program_name = "/edx/Evaluation/{0}/{1}".format(problem_names[0], problem_names[1])
    program_code = student_response.encode('utf-8')
    source_file = open(program_name, 'w')
    source_file.write(program_code)
    source_file.close()
    result = {}
    #Inicializate the parameters for the result
    message = "Ok, File Corrector.java created"
    score=0
    result.update({"score": score, "msg": message})
    result = process_result(result)
    return result

def process_result(result):
    #Define the paramaters for the result
    correct = True
    score = result["score"]
    msg = result["msg"]
    result = {}
    result.update({"correct": correct, "score": score, "msg": msg})
    result = json.dumps(result)
    return result

def get_info(body_content):
    #Extract the information of Json Object
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    problem_name = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    return problem_name, student_response

if __name__ == "__main__":
    #The server listen for ever in his port
    server = BaseHTTPServer.HTTPServer(("localhost", 1720), HTTPHandler)
    print 'Starting Corrector.py Server on port 1720...'
    server.serve_forever()

