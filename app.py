from flask import Flask
from flask import render_template
from flask import request
import subprocess
app = Flask(__name__, static_url_path='/static')

# Machine info
arch = subprocess.check_output(["uname", "-m"]).decode("utf-8")

@app.route("/")
def hello():
    name = subprocess.check_output("hostname").decode("utf-8").strip()
    return render_template('index.html', name=name)

@app.route("/cmd", methods=['GET'])
def exec_cmd():
    command = request.args["command"]
    implemented_commands = {
        "shutdown" : ["sudo", "shutdown", "-h", "now"],
        "reboot"   : ["sudo", "shutdown", "-r", "now"],
        "uptime"   : ["uptime"]}
    if command:
        if command in implemented_commands:
            output = subprocess.check_output(implemented_commands[command])
        else:
            output = "Unimplemented/Invalid Command"
    else:
        output = "Empty Command"
    return output

@app.route("/temp", methods=["GET"])
def get_temp():
    if ("arm" in arch):
        temp_output = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
    else:
        temp_output = "NA"
    return temp_output

if __name__ == "__main__":
    app.run()
