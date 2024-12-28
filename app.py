import streamlit as st
import openai
import json
import random
from weaviate import Client

# OpenAI APIキーの設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Weaviateクライアントの初期化 (RAG用)
weaviate_client = Client("http://localhost:8080")

# メッセージ履歴の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """
        あなたはDX推進能力を強化するAIコーチです。以下の要素を基にユーザーを支援してください：
        1. 抽象的思考能力の開発
        2. システム思考の実践
        3. データ解析スキルの向上
        4. 仮想プロジェクトシミュレーション
        5. メタ認知の促進
        6. 倫理的思考のトレーニング
        """}
    ]

# RAGによる知識ベース検索

def search_knowledge_base(query):
    try:
        result = weaviate_client.query.get("Philosophy").with_near_text({"concepts": [query]}).do()
        if result["data"]["Get"]["Philosophy"]:
            return result["data"]["Get"]["Philosophy"][0]["content"]
        else:
            return "関連する情報が見つかりませんでした。"
    except Exception as e:
        st.error(f"データベース検索中にエラーが発生しました: {e}")
        return "検索に失敗しました。"

# RAGを利用したシナリオ生成

def generate_scenario_with_rag(category):
    knowledge_base_content = search_knowledge_base(category)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"以下の情報に基づき、ユーザー向けの課題を作成してください：\n\n{knowledge_base_content}"},
                {"role": "user", "content": f"{category}に基づいたシナリオを作成してください。"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"シナリオ生成中にエラーが発生しました: {e}")
        return "シナリオ生成に失敗しました。"

# 動的価値観揺さぶり機能

def generate_value_challenging_question():
    model_prompts = {
        "Bateson": "あなたの行動が無意識的に決まる理由を説明してください。",
        "Bergson": "創造的進化に基づいて、現在の意思決定を再考してください。",
        "Marx": "労働があなたのアイデンティティにどう影響を与えるかを議論してください。",
        "Nishida": "主観と客観の関係を統合する方法について考えてください。"
    }
    selected_model = random.choice(list(model_prompts.keys()))
    return selected_model, model_prompts[selected_model]

# チームダイナミクスシナリオ

def generate_team_dynamics_scenario():
    return """
    あなたはプロジェクトチームのリーダーです。以下のメンバーと協力してDXプロジェクトを進めてください：
    - データアナリスト: データに基づく意思決定を提案。
    - エンジニア: 技術的な実装を担当。
    - マーケティング: 顧客ニーズを分析。
    チームとしての行動計画を提案してください。
    """

# 動的揺らぎを追加したシナリオ生成

def get_random_or_personalized_scenario():
    category = random.choice(["抽象的思考", "システム思考", "データ解析", "プロジェクト管理", "メタ認知", "倫理的思考"])
    return generate_scenario_with_rag(category)

# UI統合
st.header("RAGによる哲学的シナリオ生成")
if st.button("シナリオを生成 (RAG)"):
    category = random.choice(["抽象的思考", "システム思考", "データ解析", "プロジェクト管理", "メタ認知", "倫理的思考"])
    scenario = generate_scenario_with_rag(category)
    st.write(f"生成されたシナリオ:\n\n{scenario}")

st.header("価値観を揺さぶる哲学的質問")
if st.button("価値観を揺さぶる"):
    model, question = generate_value_challenging_question()
    st.write(f"**選択されたモデル**: {model}")
    st.write(f"**生成された質問**: {question}")

st.header("パーソナライズされた学習シナリオ")
if st.button("次の学習ステップを生成"):
    scenario = get_random_or_personalized_scenario()
    st.write(f"生成されたシナリオ:\n\n{scenario}")
