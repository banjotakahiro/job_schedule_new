import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_chatgpt(question, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "あなたはフレンドリーなAIアシスタントです。"},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=6000
    )
    return response.choices[0].message['content'].strip()

# "正しい"に類似するキーワードを追加する関数
def is_valid_response(response):
    keywords = ["正しい", "適切", "妥当", "正確", "正当", "間違いではない", "合っている"]
    return any(keyword in response for keyword in keywords)

# Stateクラスで各手順の状態を保持
class State:
    def __init__(self):
        self.responses = []  # 各手順での結果を保存するリスト
    
    def add_response(self, step, response):
        self.responses.append({"step": step, "response": response})
    
    # display関数の呼び出しを削除またはコメントアウト
    # def display(self):
    #     print("\n=== 各ステップで生成された回答 ===")
    #     for entry in self.responses:
    #         print(f"{entry['step']}の結果: {entry['response']}")
    #     print("==============================\n")

# ChatGPT_1に質問する
def chatgpt_1(question, state):
    answer = ask_chatgpt(question, model="gpt-4")
    if answer:
        state.add_response("ChatGPT_1", answer)  # 状態に保存
    return answer

# ChatGPT_2が回答を検証する
def chatgpt_2(answer, state):
    if answer:
        verification_question =(
    f"以下の疑問に対する回答が正しいか正しくないかを確認してください。\n"
    f"疑問: {question}\n"
    f"回答: {answer}\n"
    f"その際に返答は正しいか正しくないかのどちらかでお願いします。\n"
    f"それに付随する理由や説明などは一切記述しないでください。\n"
    f"してよい返答は正しいか正しくないかのどちらかです。"
    )
        validation = ask_chatgpt(verification_question)
        if validation:
            state.add_response("ChatGPT_2", validation)  # 状態に保存
        return validation
    return None

# ChatGPT_3が再検証する
def chatgpt_3(answer, state):
    if answer:
        final_verification = (
    f"以下の疑問に対する回答正しいか正しくないかを確認してください。\n"
    f"疑問: {question}\n"
    f"回答: {answer}\n"
    f"その際に返答は正しいか正しくないかのどちらかでお願いします。\n"
    f"それに付随する理由や説明などは一切記述しないでください。\n"
    f"してよい返答は正しいか正しくないかのどちらかです。"
    )
        validation = ask_chatgpt(final_verification)
        if validation:
            state.add_response("ChatGPT_3", validation)  # 状態に保存
        return validation
    return None

# メインのロジック
def process_question(question):
    max_attempts = 5
    attempt = 0
    state = State()  # 共通の状態オブジェクトを作成
    
    while attempt < max_attempts:
        attempt += 1
        
        # ChatGPT_1による回答生成
        answer_1 = chatgpt_1(question, state)
        if answer_1 is None:
            print("ChatGPT_1が回答を生成できませんでした。")
            continue

        # ChatGPT_2による回答確認
        validation_2 = chatgpt_2(answer_1, state)
        if validation_2 is None:
            print("ChatGPT_2が回答を検証できませんでした。再試行します。")
            continue
        
        if is_valid_response(validation_2):  # ChatGPT_2が正しいと判定したら
            # ChatGPT_3による最終確認
            validation_3 = chatgpt_3(answer_1, state)
            if validation_3 is None:
                print("ChatGPT_3が再検証できませんでした。再試行します。")
                continue
            print(f"ChatGPT_3の最終確認: {validation_3}")
            
            if is_valid_response(validation_3):
                print("最終的な正しい回答です: ", answer_1)
                # state.display()  # 状態を表示
                return answer_1  # 正しい回答を出力
            else:
                print("ChatGPT_3が回答を間違っていると判断しました。再試行します。")
        else:
            print("ChatGPT_2が回答を間違っていると判断しました。再試行します。")
        
    print("最大試行回数に達しました。正しい回答を得られませんでした。")
    # state.display()  # 状態を表示
    return None

# 質問の入力と処理
if __name__ == "__main__":
    # バイトシフト推理ゲーム (リアリティ重視)
# 誰がどの日にシフトに入っているかを推理してください。

    question = """
    ルール:
    - シフトは月曜日から日曜日までの7日間です。
- バイトは10人（Aさん、Bさん、Cさん、Dさん、Eさん、Fさん、Gさん、Hさん、Iさん、Jさん）がいます。
- 各人が希望したシフトや条件をもとに、誰がどの日に働くかを決定してください。
- シフトは1人につき最大2日までですが、全員が必ず1日はシフトに入ります。

ヒント:
1. Aさんは平日に2日入ることを希望していますが、水曜日と金曜日はNGです。
2. Bさんは土曜日しかシフトに入れないと申告しています。
3. Cさんは週末（土曜日と日曜日）に連続してシフトに入りたいと希望しています。
4. Dさんは月曜日に学校があるため、その日はシフトに入れませんが、火曜日は空いています。
5. Eさんは木曜日と日曜日のどちらか1日しかシフトに入りたくないと伝えています。
6. Fさんは水曜日を絶対に休みたいと伝え、その他の平日であれば調整可能です。
7. Gさんは火曜日と木曜日にシフトに入ることを希望していますが、日曜日は予定があり休みです。
8. Hさんは金曜日と日曜日にシフトに入れると申し出ていますが、月曜日は希望しません。
9. Iさんは土日どちらか1日だけ働きたいと希望しており、日曜日はできれば避けたいと話しています。
10. Jさんは月曜日、火曜日、木曜日のうち1日しかシフトに入れません。

質問:
誰がどの日にシフトに入っているでしょうか？
"""
    # ユーザーから質問を入力
    process_question(question)


