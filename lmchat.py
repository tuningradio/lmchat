
# LMstudioとchatする lmchat.py Ver1.0.0(W) by Tuningradio and Microsoft Copilot
# 機能:
# 1)LMstudio serverとチャットする。UIに何の飾りもないところがウリ。
# 2)英語モデルでも安心。googletransで即時日本語に翻訳する。なのでInternet接続しないと使えません。
# 3)経験上元の英文と日本語文の両方を表示したほうがストレスがないのでそうした。
# 4)過去の会話を覚えているので、名前とか話している内容を忘れない。LMstuidioにAPIでアクセスする場合はクライアントに記憶機能が必要なのでつけた。
# 使い方のコツ。 
# 1)ソース内のsystem roleのcontentを好みの名前や性格、目的に変えると、あなた好みのキャラになります。"you are 何々"という感じで 「あなたは何々です」という書き方をします。
# 2)入力は英語モデルに対しては英語です。まず自己紹介をしてください。"hello! my name is Ray"と自己紹介すると、ずっとこちらをレイと呼んでくれますよ。
# 3) LMstudio serverのToken to Generate n_predict:の値がデフォルトの-1だと暴走します。modelにもよりますが、会話には500ぐらい、小説なら3000ぐらいに設定するのが良いです。-1で暴走(同じフレーズを繰り返して生成が止まらなくなる)したら、serverのstopボタンを押すしかないです。
# 元々LMstudioの文字が小さすぎて辛かったのだが設定変更できないので、頭にきて作りましたwww

from openai import OpenAI
from googletrans import Translator

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio") # LMstudio serverがネット上の他のマシンの場合はIPアドレスを書く
translator = Translator()

# Initialize the messages list with the system message
messages = [
    {"role": "system", "content": "your name is Lisa. you are an AI chat friend."},
]

while True:
    user_input = input("user: ")
    
    if not user_input:
        continue

    # Add the user message to the messages list
    messages.append({"role": "user", "content": user_input})

    completion = client.chat.completions.create(
      model="Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF",  # 好きなmodelに設定する。LMStudio serverと一致させる必要あり
      messages=messages,  # Pass the entire conversation history
      temperature=0.7,
    )

    system_message = completion.choices[0].message.content
    system_message = system_message.replace('\n', '')  # Remove newline characters
    print("system: " + system_message)

    # Add the system message to the messages list
    messages.append({"role": "assistant", "content": system_message})

    # Translate the text to Japanese and display
    translated_text = translator.translate(system_message, dest='ja')
    print("system: " + translated_text.text)
