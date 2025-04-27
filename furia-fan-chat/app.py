from flask import Flask, render_template, request, jsonify
import random
from functions import teste_de_funcao, elenco_furia

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/send", methods=["POST"])
def send():
    user_message = request.json["message"]
    bot_response = generate_bot_response(user_message)
    return jsonify({"response": bot_response})


# Perguntas e respostas do quiz
quiz_questions = {
    "Quem é o capitão do time de CS da FURIA?": "arT",
    "Qual país a FURIA representa?": "Brasil",
    "Quantos jogadores tem um time de CS:GO?": "5",
    "Qual é o mascote da FURIA?": "pantera",
    "Em que ano a FURIA foi fundada?": "2017",
}

current_quiz_question = None
score = 0
total_questions = 0


def generate_bot_response(message):
    global current_quiz_question, score, total_questions

    message = message.lower()

    if current_quiz_question:
        correct_answer = quiz_questions[current_quiz_question].lower()
        total_questions += 1
        if correct_answer in message:
            score += 1
            response = (
                f"✅ Resposta correta! Pontuação atual: {score}/{total_questions}"
            )
        else:
            response = f"❌ Errado! A resposta correta era: {quiz_questions[current_quiz_question]}. Pontuação atual: {score}/{total_questions}"
        current_quiz_question = None
        return response

    if "próximo jogo" in message or "proximo jogo" in message:
        # return "aqui vai uma função que busca os próximos jogos"
        return teste_de_funcao()
    elif "status" in message or "ao vivo" in message:
        return "aqui vai uma função que busca status em tempo real caso um jogo esteja acontecendo"
    elif "resultado" in message or "ultimos jogos" in message:
        return "aqui vai uma função que busca os resultados dos últimos jogos"
    elif "elenco" in message or "time da furia" in message:
        return elenco_furia()
    elif "quiz" in message:
        # Escolhe uma pergunta aleatória
        current_quiz_question = random.choice(list(quiz_questions.keys()))
        return f"🧠 QUIZ TIME!\n{current_quiz_question}\n(Dica: responda com uma palavra ou número!)"
    elif "pontuação" in message:
        return f"🏆 Sua pontuação atual é {score}/{total_questions}."
    else:
        return "🤔 Não entendi, mas vamos FURIAAAA!"


if __name__ == "__main__":
    app.run(debug=True)
