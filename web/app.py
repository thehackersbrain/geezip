from flask import Flask, render_template, request, session, send_file, render_template_string
import os
import subprocess
import gzip
import hashlib
import urllib
from time import strftime


# app configuration
app = Flask(__name__, static_url_path="/static")
app.secret_key = os.urandom(32)

counter = 0


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/compress', methods=['GET', 'POST'])
def compress():
    global counter

    if (request.method == "GET"):
        return render_template("compress.html")
    else:
        if (counter >= 10):
            os.system("/bin/rm /tmp/*.gz")
            counter = 0

        # filename = request.form["filename"] if "filename" in request.form else ""
        filename = ""
        contents = ""
        if ("filename" in request.form):
            filename = request.form["filename"]
            if ("contents" in request.form):
                contents = request.form["contents"]

        reqData = ["filename", "contents"]

        for i in reqData:
            if (not request.form[i]):
                return "{} field is empty...".format(str(i))

        if (not filename.endswith(".gz")):
            return "filename must end with '.gz' extension..."

        with gzip.open("/tmp/{}".format(filename), "wb") as fh:
            fh.write(contents.encode("utf-8"))

        sha = hashlib.sha256()
        with open("/tmp/{}".format(filename), "rb") as fp:
            sha.update(fp.read())

        shahash = sha.hexdigest()

        prs = subprocess.Popen("zgrep . *gz", shell=True,
                               cwd="/tmp/", stdout=subprocess.PIPE)
        results = prs.stdout.read().decode("utf-8")

        counter += 1

        # return "Files or Data compressed successfully..."
        generate_logs(filename)
        return render_template_string("<p>{}</p><br/><br/><p>{}</p>".format(results, shahash))


def generate_logs(filename):
    with open("/usr/src/logs/file.log", "a") as logfile:
        logfile.write("[+] Filename: {} Time: {}\n".format(filename, strftime("%H:%M:%S"))


@ app.route("/download/<filename>")
def download(filename):
    # To-do: Explain the workerbee request process
    # include docs on urllib.request.urlopen(destination)
    if (os.path.exists("/tmp/%s" % filename)):
        return send_file("/tmp/{}".format(filename), as_attachment=True, download_name=filename)
    else:
        return "Woops! That file doesn't exists..."


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
