from flask import Flask, render_template, request, jsonify
from main import make_move, check_winner, best_move

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json(force=True, silent=True) or {}
    board = data.get("board")
    position = data.get("position")
    human_symbol = data.get("humanSymbol", "X")
    ai_symbol = data.get("aiSymbol", "O")

    # Basic validation
    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400
    if not isinstance(position, int) or not (0 <= position <= 8):
        return jsonify({"error": "Invalid position"}), 400

    # Apply human move
    if not make_move(board, position, human_symbol):
        return jsonify({"error": "Cell already taken"}), 400

    # Check for terminal state after human move
    winner = check_winner(board)
    if winner is not None:
        return jsonify({
            "board": board,
            "status": "ended",
            "winner": winner,
            "aiMove": None,
        })

    # AI move using best_move (minimax)
    ai_index = best_move(board, ai_symbol)
    make_move(board, ai_index, ai_symbol)

    winner = check_winner(board)
    status = "ended" if winner is not None else "ongoing"

    return jsonify({
        "board": board,
        "status": status,
        "winner": winner,
        "aiMove": ai_index,
    })

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json(force=True, silent=True) or {}
    ai_symbol = data.get("aiSymbol", "O")
    board = [" "] * 9

    if ai_symbol == "X":
        ai_index = best_move(board, ai_symbol)
        make_move(board, ai_index, ai_symbol)
        return jsonify({
            "board": board,
            "aiMove": ai_index,
            "status": "ongoing"
        })
    else:
        return jsonify({
            "board": board,
            "aiMove": None,
            "status": "ongoing"
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


