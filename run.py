from flask import Flask, render_template, request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from luke import SentenceLukeJapanese  # luke.py から SentenceLukeJapanese クラスをインポート
import numpy as np

app = Flask(__name__)

# --- モデルとデータの準備 ---
# アプリケーション起動時に一度だけモデルとデータを読み込む
print("LUKEモデルを読み込んでいます...")
MODEL_NAME = "sonoisa/sentence-luke-japanese-base-lite"
model = SentenceLukeJapanese(MODEL_NAME)
print("モデルの読み込みが完了しました。")

# ワインデータを読み込む
print("ワインデータを読み込んでいます...")
wine_df = pd.read_csv("wine_data.csv")
print(wine_df)

# 全ワインの説明文をベクトル化する（これも起動時に一度だけ）
print("全ワインのベクトルを計算しています...")
wine_vectors = model.encode(wine_df['description'].tolist())
print("ベクトル計算が完了しました。")
# --------------------


@app.route('/', methods=['GET', 'POST'])
def index():
    # POSTリクエスト（フォームが送信された）の場合
    if request.method == 'POST':
        # フォームから'user_text'という名前のデータを取得
        user_preference_text = request.form.get('user_text')
        
        # テキストが空でなければ、おすすめを検索
        if user_preference_text:

            # 表示したいおすすめの件数
            TOP_N = 3

            # 1. ユーザーの好みをベクトル化
            user_vector = model.encode([user_preference_text])
            
            # 2. 全ワインのベクトルとコサイン類似度を計算
            similarities = cosine_similarity(user_vector, wine_vectors)
            print(similarities)
            
            # 3. 類似度スコアを元に、上位N件のインデックスを取得
            # np.argsortはスコアを小さい順に並べた時の「インデックス」を返す
            # [-TOP_N:]で末尾からN件を取得し、[::-1]で降順に並べ替える
            top_n_indices = np.argsort(similarities[0])[-TOP_N:][::-1]
            
            # 4. 上位N件のワインの情報をDataFrameとして取得
            recommended_wines_df = wine_df.iloc[top_n_indices]
            
            # 5. DataFrameを辞書のリストに変換してテンプレートに渡す
            recommended_wines = recommended_wines_df.to_dict('records')
            
            return render_template('result.html', wines=recommended_wines)
            

            

    # GETリクエスト（最初にページにアクセスした）の場合は入力ページを表示
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)