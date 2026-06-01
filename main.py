from flask import Flask, render_template, request, redirect, url_for, make_response
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/createnote", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        
        with open("data.txt", "a") as file:
            file.write(f"Title: {title}\n")
            file.write(f"Content: {content}\n")
            file.write(f"---\n")

        return redirect(url_for("index"))
    return render_template("createnote.html")

@app.route("/displaynote", methods=["GET"])
def display_note():
    notes = []
    with open("data.txt", "r") as file:
        content = file.read()
        entries = content.split("---\n")
        for entry in entries:
            if entry.strip():
                lines = entry.strip().split("\n")
                title = lines[0].replace("Title: ", "")
                body = lines[1].replace("Content: ", "")
                notes.append({"title": title, "content": body}) 
    return render_template("displayNote.html", notes=notes)


@app.route("/delete/<int:index>", methods=["POST"])
def delete_note(index):
    notes = []

    # read all notes first
    with open("data.txt", "r") as file:
        content = file.read()

    entries = content.split("---\n")

    for entry in entries:
        if entry.strip():
            lines = entry.strip().split("\n")
            title = lines[0].replace("Title: ", "")
            body = lines[1].replace("Content: ", "")
            notes.append({"title": title, "content": body})

    # remove the specific note by index
    notes.pop(index)

    # rewrite data.txt without deleted note
    with open("data.txt", "w") as file:
        for note in notes:
            file.write(f"Title: {note['title']}\n")
            file.write(f"Content: {note['content']}\n")
            file.write("---\n")

    return redirect(url_for("display_note"), 303)



if __name__ == "__main__":
    app.run(debug=True)