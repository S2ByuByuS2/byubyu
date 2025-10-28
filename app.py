from flask import Flask, request, jsonify
import pandas as pd
import difflib

app = Flask(__name__)

# CSV 파일 읽기
data = pd.read_csv('mabinogi_runes.csv')
data['keyword_clean'] = data['keyword'].astype(str).str.replace(' ', '').str.lower()

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        user_text = request.json.get('userRequest', {}).get('utterance', '').strip()
    except:
        user_text = ''

    # 테스트용 상태 응답
    if not user_text:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": "뷰뷰 봇 서버가 정상적으로 작동 중입니다 💫"}}
                ]
            }
        })

    keyword = user_text.replace('?', '').strip().lower().replace(' ', '')
    row = data[data['keyword_clean'].str.contains(keyword, na=False)]

    # 오타나 부분 검색 보정
    if row.empty:
        close = difflib.get_close_matches(keyword, data['keyword_clean'], n=1, cutoff=0.5)
        if close:
            row = data[data['keyword_clean'] == close[0]]

    if not row.empty:
        response = row.iloc[0]['response']
    else:
        response = f"'{user_text}'에 대한 정보를 찾을 수 없어요."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": response}}
            ]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
