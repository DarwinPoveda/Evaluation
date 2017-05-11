import BaseHTTPServer
import json
import os
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

    #Create name of files
    program=student_response.split("*Codigo")
    #Write all the java files
    for i in range(len(program)-1):
        program_name = "/edx/Evaluation/{0}".format(problem_name["problem_name"])
	source_file = open(program_name, 'w')
        source_file.write(program[i+1])
        source_file.close()
    result = {}
    p = subprocess.Popen(["java", "-jar", "Evaluation.jar", "submissionConf.xml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.split("Grade :=>>")
    out2 = out[0].split('\n')
    out1 = out[1].split('\n')
    #message = "".join(out2).encode('utf-8')
    message=out[0].encode('utf-8')
    score = float(out1[0])/100
    print message, score 
    result.update({"score": score, "msg": message})
    result = process_result(result)

    #remove student's program from disk
    #for i in range(len(program)-1):
    #    program_name = "{0}".format(problem_name["problem_name"])
    #    os.remove(program_name)
    #return result

def process_result(result):
    score = result["score"]
    if score == 1 :
        correct = True
    else:
        correct = False
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

    server = BaseHTTPServer.HTTPServer(("localhost", 1710), HTTPHandler)
    print 'Starting JavaGrader server on port 1710...'
    server.serve_forever()

