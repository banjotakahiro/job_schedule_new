import openai
import os
# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはフレンドリーなAIアシスタントです。"},
            {"role": "user", "content": user_input}
        ]
    )
    # レスポンスからアシスタントのメッセージを取り出す
    return response['choices'][0]['message']['content']

def main():
    print("ChatGPTボットへようこそ！ 終了するには 'exit' と入力してください。")
    
    while True:
        user_input = input("あなた: ")
        if user_input.lower() == 'exit':
            print("チャットを終了します。")
            break
        
        response = chat_with_gpt(user_input)
        print("ChatGPT: " + response)

if __name__ == "__main__":
    main()
