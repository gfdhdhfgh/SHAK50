from flask import Flask, send_from_directory, request, make_response
import task

app = Flask("SHAK50")

@app.route("/")
def root():
    return send_from_directory("interface", "index.html")

@app.route("/style/<path:path>")
def style(path):
    return send_from_directory("interface", path)

@app.route("/script/<path:path>")
def script(path):
    return send_from_directory("interface", path)

@app.post("/create-task")
def create_task():
    if request.headers.get("IsHuman") == "True":
        return task.add_image(request.get_data())
    else:
        return make_response("NO >:3", 403)


if __name__ == "__main__":
    app.run()