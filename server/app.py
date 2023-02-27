from flask import Flask, render_template, request, jsonify
from Models import db, game_states
from logging import exception

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\sergi\\OneDrive\\Desktop\\TestBBDD\\database\\game_states.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///D:\\PyCharm\\Projects\\TotalBotWar\\Database\\game_states.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/", methods = ["GET"])
def Index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            print("archivo subido exitosamente")
            file.save(file.filename)
            return 'archivo subido exitosamente'
    else:
        return render_template('uploader.html')

@app.route("/api/game_states", methods = ["GET"])
def get_data():
    try:
        gss = game_states.query.all()
        toReturn = [gs.serialize() for gs in gss]
        print("Succes on get GET request")
        return jsonify(toReturn), 200
    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un error"}), 500

@app.route("/api/last", methods = ["GET"])
def get_last_game_state():
    try:
        gss = [db.session.query(game_states).order_by(game_states.rowid.desc()).first()]
        print("Succes on get GET request")
        return jsonify([gs.serialize() for gs in gss]), 200
    except Exception:
        exception("[SERVER]: Error ->")
        return jsonify({"msg": "Ha ocurrido un error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=4000)