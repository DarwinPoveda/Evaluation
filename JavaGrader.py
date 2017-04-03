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
    program=student_response.split("*CODIGO")
    #Write all the java files
    for i in range(len(program)-1):
        problem_names = problem_name["problem_name"].split(",")
        program_name = "/edx/java-grader/{0}/{1}".format(problem_names[0], problem_names[i+1])
	source_file = open(program_name, 'w')
        source_file.write(program[i+1])
        source_file.close()
    result = {}
    p = subprocess.Popen(["java", "-jar", "Evaluation.jar", "submissionConf.xml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.split("Grade :=>>")
    out2 = re.split('\n', out[0])
    out1 = re.split('\n', out[1])
    correct = True
    message = out2[0]
    score=float(out1[0])/100
    result.update({"score": score, "msg": message})
    result = process_result(result)

    #remove student's program from disk
    #for i in range(len(program)-1):
    #    program_name = "/edx/java-grader/{0}/{1}".format(problem_names[0], problem_names[i+1])
    #    os.remove(program_name)
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

    server = BaseHTTPServer.HTTPServer(("localhost", 1710), HTTPHandler)
    print 'Starting server on port 1710...'
    server.serve_forever()

