from flask import Flask, request, jsonify
from g4f.client import Client
import re

app = Flask(__name__)

def generate_report(prompt, count_attempts=3) -> str:
    client = Client()

    for _ in range(count_attempts):
        try:
            response = client.chat.completions.create(
                model="deepseek-r1", 
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.choices[0].message.content.strip()
            if "404" not in answer:
                return answer
        except Exception as _:
            continue

    return "Ошибка: не удалось подключиться к GPT."

def extract_user_id_from_messages(messages):
    return set(message['user'] for message in messages)

def extract_report(generated_text):
    pattern = r'\{\s*\"?user\"?\s*:\s*(\d+)\s*,\s*\"?summary\"?\s*:\s*"([^"]*)"\s*,\s*\"?activity\"?\s*:\s*(\d+)\s*,?\s*\}\s*,?'
    matches = re.findall(pattern, generated_text)

    report = {}
    for match in matches:
        user_id, summary, activity = match
        curr_user = {"summary": summary, "activity": int(activity)}
        report[user_id] = curr_user

    return report

def analyze_messages(messages):
    format_of_summary = ''' 
    { 
        "user" : номер сотрудника,
        "summary" : "краткий анализ работы данного сотрудника",
        "activity" : число от 1 до 10 - оценка работы сотрудника
    }
    '''
    unique_users = extract_user_id_from_messages(messages)

    prompt = f"""
                Ты — умный и опытный менеджер. Проанализируй переписку сотрудников {messages}.
                Проанализируй каждого сотрудника из списка {str(unique_users)[1:-1]}, по отдельности и составь отчет в формате {format_of_summary},
                для каждого сотрудника.  
                Пиши лаконично, объективно и по делу. Отчёт на русском языке.  
            """
    generated_text = generate_report(prompt)
    report = extract_report(generated_text)
    
    return report

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "Нет сообщений для анализа"}), 400

        report = analyze_messages(messages)
        print(report)
        return jsonify({"report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
