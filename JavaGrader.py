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
j    #Split name of files
    program=student_response.split("*Codigo")
    #Write all the java files
    problem_names = problem_name["problem_name"].split(",")
    for i in range(len(program)-1):
        program_name = "/edx/Evaluation/{0}".format(problem_names[i])
	source_file = open(program_name, 'w')
        source_file.write(program[i+1])
        source_file.close()
    result = {}
    #Run the External Grader with the parameters in file submissionConf.xml
    p = subprocess.Popen(["java", "-jar", "Evaluation.jar", "submissionConf.xml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.split("Grade :=>>")
    out1 = out[1].split('\n')
    #Inicializate the parameters for the result
    message = out[0]
    score = float(out1[0])/100
    result.update({"score": score, "msg": message})
    result = process_result(result)
    return result

def process_result(result):
    #Define the paramaters for the result
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
    #Extract the information of Json Object
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    problem_name = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    print json_object
    return problem_name, student_response

if __name__ == "__main__":
    #The server listen for ever in his port
    server = BaseHTTPServer.HTTPServer(("localhost", 1710), HTTPHandler)
    print 'Starting JavaGrader server on port 1710...'
    server.serve_forever()

