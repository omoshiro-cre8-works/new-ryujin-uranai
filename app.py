import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="龍神鑑定所", page_icon="🐉")
st.title("🐉 龍神鑑定所 - 真・開山")

# ポート番号の取得（Google Cloud環境用）
port = int(os.environ.get("PORT", 8501))

# APIキーの取得
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("APIキーが設定されていません。StreamlitのSecretsを確認してください。")
else:
    try:
        # 通信の「道」を最新（v1）に固定し、接続方式をRESTに強制します
        genai.configure(api_key=api_key, transport='rest')
        
        # 最も安定しているモデル名を指定
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.write("龍神様がお悩みを聞く準備を整えられました。")
        user_input = st.text_input("今、心にあるお悩みを一行で記してください。")
        
        if st.button("鑑定を仰ぐ"):
            if user_input:
                with st.spinner("龍神様と交信中..."):
                    # 鑑定実行（system_instructionを使わない最も安全な形式）
                    prompt = f"あなたは慈愛に満ちた龍神です。以下の悩みに短く、力強く答えてください：{user_input}"
                    response = model.generate_content(prompt)
                    
                    st.subheader("【龍神からのお告げ】")
                    st.write(response.text)
            else:
                st.warning("お悩みをご記入ください。")
                
    except Exception as e:
        st.error(f"龍神様との通信に不具合が生じました。管理者にお伝えください。")
        st.info(f"技術詳細: {e}")
