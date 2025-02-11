from flask import Flask, request, jsonify
from g4f.client import Client
import re

app = Flask(__name__)

def make_follow_up_report(business_plan: str, follow_up: str) -> str:
    prompt = f"""
    На основе информации с последней встречи команды и бищнес плана нужно сформировать отчет.

    **Бизнес-план**:
    {business_plan}

    **Информация с последней встречи**:
    {follow_up}

    **Твоя задача**:
    1. Подведи краткие итоги текущего состояния программы.
    2. Определи, какие успехи уже достигнуты.
    3. Укажи проблемные зоны или потенциальные риски.
    4. Дай рекомендации, что можно улучшить для достижения целей.
    5. Предложи шаги для дальнейшего развития и масштабирования программы.

    Дай конкретные и четкие рекомендации, основанные на бизнес-плане и последней встрече команд.
    """
    return prompt.strip()

def generate_report(prompt, count_attempts=3) -> str:
    client = Client()

    for _ in range(count_attempts):
        try:
            response = client.chat.completions.create(
                model="deepseek-r1", 
                messages=[{"role": "user", "content": prompt}],
            )
            answer = response.choices[0].message.content.strip()
            
            answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()

            if "404" not in answer:
                return answer
        except Exception:
            continue

    return "Ошибка: не удалось получить ответ от LLM."

@app.route('/analyze_follow_up', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        business_plan = data.get("business_plan", "").strip()
        follow_up = data.get("follow_up", "").strip()

        if not business_plan or not follow_up:
            return jsonify({"error": "Требуются business_plan и follow_up"}), 400

        prompt = make_follow_up_report(business_plan, follow_up)
        report = generate_report(prompt)
        print(report)

        return jsonify({"report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
