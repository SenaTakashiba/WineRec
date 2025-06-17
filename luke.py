import pandas as pd
from transformers import MLukeTokenizer, LukeModel
import torch
import scipy.spatial

class SentenceLukeJapanese:
    def __init__(self, model_name_or_path, device=None):
        self.tokenizer = MLukeTokenizer.from_pretrained(model_name_or_path)
        self.model = LukeModel.from_pretrained(model_name_or_path)
        self.model.eval()  # モデルを評価モードに設定

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        self.model.to(self.device)

    def _mean_pooling(self, model_output, attention_mask):
        # model_output[0] には全てのトークンの埋め込みが含まれています
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    @torch.no_grad() # 推論のために勾配計算を無効化
    def encode(self, sentences, batch_size=8):
        all_embeddings = []
        iterator = range(0, len(sentences), batch_size)
        for batch_idx in iterator:
            batch = sentences[batch_idx:batch_idx + batch_size]
            
            encoded_input = self.tokenizer.batch_encode_plus(
                batch,
                padding="longest",        # バッチ内で最も長いシーケンスにパディング
                truncation=True,          # モデルの最大長を超えるシーケンスを切り捨て
                return_tensors="pt"       # PyTorchテンソルを返す
            ).to(self.device)
            
            model_output = self.model(**encoded_input)
            sentence_embeddings = self._mean_pooling(model_output, encoded_input["attention_mask"]).to('cpu')
            all_embeddings.extend(sentence_embeddings)
            
        return torch.stack(all_embeddings)

if __name__=='__main__':
    # モデルの読み込み
    MODEL_NAME = "sonoisa/sentence-luke-japanese-base-lite"
    model = SentenceLukeJapanese(MODEL_NAME)

    # CSV読み込み
    csv_file_path = 'C:\\Users\\kz211\\geeksalon\\wine_sele\\output\\wine_data.csv'
    data = pd.read_csv(csv_file_path)

    # ワイン名リスト
    sentences = data['name'].tolist()

    # クエリ入力（理想のワインのイメージ）
    query = input("理想のワインのイメージを文章で入力してください: ")
    sentences.append(query)

    # エンコード（ベクトル化）
    sentence_embeddings = model.encode(sentences, batch_size=8)

    # 類似度計算（コサイン距離）
    distances = scipy.spatial.distance.cdist(
        [sentence_embeddings[-1]], sentence_embeddings[:-1], metric="cosine"
    )[0]

    # 最も近いワインのインデックスを取得
    closest_idx = distances.argmin()

    # 結果表示
    print("\n\n======================\n")
    print("あなたの理想:", query)
    print("\nおすすめのワイン：")
    print(f"ワイン名: {data.iloc[closest_idx]['name']}")
    print(f"説明: {data.iloc[closest_idx]['description']}")
    print(f"URL: {data.iloc[closest_idx]['page_url']}")
