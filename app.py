from flask import Flask
from flask import render_template
from flask import request
import subprocess

from player import Player

app = Flask(__name__, static_url_path='/static')
omx_player = Player()

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

@app.route("/temp_sensor", methods=["GET"])
def get_temp_sensor():
    temp_output = subprocess.check_output(["head", "-n", "1", "/home/pi/code/tempd/tempdb"])
    return temp_output

@app.route("/play_link", methods=["POST"])
def play_link():
    if omx_player.nowplaying == True:
        try:
            omx_player.stop()
        except:
            print("exception occured")
            omx_player.reset()
    link = request.form["link"]
    omx_player.decode_url(link)
    omx_player.play()
    return "Now playing"

@app.route("/control", methods=["POST"])
def control_player():
    if omx_player.nowplaying:
        output = omx_player.control_omx_proc("pause_toggle")
    else:
        output = "No player playing"
    return output

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
