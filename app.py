import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="なんでもカウントくん", layout="centered")

st.title("🔢 なんでもカウント保存")

# データの保持（リロードするまで有効）
if 'master_count_list' not in st.session_state:
    st.session_state.master_count_list = []

# --- 1. カウント入力エリア ---
st.header("📝 入力フォーム")

# 名前は自由記述
target_name = st.text_input("数えるものの名前", placeholder="例：A倉庫の段ボール、赤いボールなど")

# 写真のアップロード（記録用）
uploaded_photo = st.file_uploader("写真を記録（任意）", type=["jpg", "png", "jpeg"])

# カウンター機能
st.write("### 個数をカウント")
if 'current_num' not in st.session_state:
    st.session_state.current_num = 0

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("➖", use_container_width=True):
        st.session_state.current_num -= 1
with col2:
    # 直接入力も可能
    count_val = st.number_input("個数", value=st.session_state.current_num, step=1, label_visibility="collapsed")
    st.session_state.current_num = count_val
with col3:
    if st.button("➕", use_container_width=True):
        st.session_state.current_num += 1

# メモ欄
note = st.text_area("メモ", placeholder="状態や場所など（例：少し破れている、3番棚）", height=70)

# 登録ボタン
if st.button("✅ この内容でリストに追加", use_container_width=True):
    if not target_name:
        st.error("「名前」を入力してください！")
    else:
        new_entry = {
            "日時": datetime.now().strftime("%H:%M:%S"),
            "名前": target_name,
            "個数": count_val,
            "メモ": note
        }
        st.session_state.master_count_list.append(new_entry)
        # 登録後にリセット
        st.session_state.current_num = 0
        st.success(f"「{target_name}」を保存しました！")
        st.balloons()

st.divider()

# --- 2. 一覧表示エリア ---
st.header("📋 今日の集計リスト")

if st.session_state.master_count_list:
    df = pd.DataFrame(st.session_state.master_count_list)
    
    # スマホで見やすいようにインデックスなしで表示
    st.table(df)
    
    # CSV保存
    csv = df.to_csv(index=False).encode('utf_8_sig')
    st.download_button(
        label="📥 全データをCSVでダウンロード",
        data=csv,
        file_name=f'count_log_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    if st.button("リストを全削除"):
        st.session_state.master_count_list = []
        st.rerun()
else:
    st.info("まだデータがありません。上のフォームから登録してください。")
