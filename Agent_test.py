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
    question = "1=1.2ということは正しいですか？"
    process_question(question)


