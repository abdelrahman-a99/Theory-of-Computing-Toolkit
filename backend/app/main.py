import os
from uuid import uuid4

from flask import Flask, request, jsonify
from flask_cors import CORS

from app.nfa import tokenize, Parser, NFAConstructor, visualize_nfa
from app.cfg import (
    read_grammar,
    build_pda,
    draw as draw_pda,
    accepts as pda_accepts,
    EPS,
    Q1,
    QF,
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
NFA_IMAGES_FOLDER = os.path.join(STATIC_FOLDER, 'nfa_images')

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))

CORS(app)

app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['NFA_IMAGES'] = NFA_IMAGES_FOLDER

os.makedirs(app.config['NFA_IMAGES'], exist_ok=True)

@app.route('/api/convert', methods=['POST'])
def convert_regex():
    data = request.get_json()
    regex = data.get('regex')

    if not regex:
        return jsonify({'error': 'No regex provided'}), 400

    try:
        # Generate NFA
        tokens = tokenize(regex)
        parser = Parser(tokens)
        ast = parser.parse()
        constructor = NFAConstructor()
        nfa = constructor.build_nfa(ast)

        # Generate visualization
        filename = f'nfa_{id(nfa)}'
        image_path = os.path.join(app.config['NFA_IMAGES'], filename)

        visualize_nfa(nfa, image_path)

        # Prepare response
        response = {
            'start_state': nfa.start_state,
            'accept_state': nfa.accept_state,
            'transitions': {
                str(state): {
                    str(symbol): list(states) 
                    for symbol, states in symbols.items()
                } 
                for state, symbols in nfa.transitions.items()
            },
            'image_url': f'/static/nfa_images/{filename}.png'
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


PDA_IMAGES_FOLDER = os.path.join(STATIC_FOLDER, "pda_images")
os.makedirs(PDA_IMAGES_FOLDER, exist_ok=True)


def read_pda_request():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValueError("Send a valid JSON object.")

    grammar = data.get("grammar")

    if not isinstance(grammar, str) or not grammar.strip():
        raise ValueError("Provide a non-empty grammar.")

    if len(grammar) > 8000:
        raise ValueError(
            "Grammar must contain at most 8,000 characters."
        )

    start, terminals, productions = read_grammar(grammar)
    delta = build_pda(start, terminals, productions)

    return data, delta


@app.route("/api/cfg-to-pda", methods=["POST"])
def convert_cfg():
    try:
        _, delta = read_pda_request()

        filename = f"pda_{uuid4().hex}"
        image_path = os.path.join(
            PDA_IMAGES_FOLDER,
            filename,
        )

        draw_pda(
            delta,
            fname=image_path,
            view=False,
        )

        # Remove the generated DOT source; retain the PNG.
        if os.path.isfile(image_path):
            os.remove(image_path)

        states = {Q1, QF}
        transitions = []

        for source in sorted(delta):
            states.add(source)

            for (input_symbol, pop_symbol), targets in sorted(
                delta[source].items()
            ):
                for target, push_symbol in sorted(targets):
                    states.add(target)

                    transitions.append({
                        "from": source,
                        "input": input_symbol or EPS,
                        "pop": pop_symbol or EPS,
                        "to": target,
                        "push": push_symbol or EPS,
                    })

        return jsonify({
            "start_state": Q1,
            "accept_state": QF,
            "states": sorted(states),
            "transitions": transitions,
            "image_url": (
                f"/static/pda_images/{filename}.png"
            ),
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("PDA conversion failed")

        return jsonify({
            "error": (
                "Could not generate the PDA diagram. "
                "Check the backend terminal for details."
            ),
        }), 500


@app.route("/api/cfg-to-pda/test", methods=["POST"])
def test_pda_string():
    try:
        data, delta = read_pda_request()
        word = data.get("word")

        if not isinstance(word, str):
            raise ValueError(
                "Provide a word as a string. "
                "Use an empty string to test epsilon."
            )

        if len(word) > 120:
            raise ValueError(
                "Test strings must contain at most 120 characters."
            )

        try:
            accepted = pda_accepts(delta, word)

        except RuntimeError as error:
            return jsonify({
                "word": word,
                "accepted": None,
                "status": "inconclusive",
                "message": str(error),
            })

        return jsonify({
            "word": word,
            "accepted": accepted,
            "status": (
                "accepted" if accepted else "rejected"
            ),
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        app.logger.exception("PDA string testing failed")

        return jsonify({
            "error": (
                "Could not test the string. "
                "Check the backend terminal for details."
            ),
        }), 500

if __name__ == '__main__':
    app.run(debug=True)