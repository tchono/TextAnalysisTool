import streamlit as st
import japanize_matplotlib
import matplotlib.pyplot as plt
import random

def predict_category(text):
    probabilities = {
        "長い修飾"    : round(random.uniform(0.5, 1.0), 2),
        "てにをは不正": round(random.uniform(0, 1.0), 2),
        "意味不明"    : round(random.uniform(0, 1.0), 2),
        "係り受け"    : round(random.uniform(0, 1.0), 2),
        "主語なし"    : round(random.uniform(0, 1.0), 2),
    }

    return probabilities

def plot_results(categories, probabilities, threshold):
    plt.figure(figsize=(10, 4))
    plt.bar(categories, probabilities)
    plt.axhline(y=threshold, color='r', linestyle='-')
    plt.ylim(0, 1)
    plt.xlabel('カテゴリー')
    plt.ylabel('確率')
    plt.title('テキスト解析結果')
    st.pyplot(plt)

def main():
    user_input = st.text_area("解析する文章を入力してください")
    analyze_button = st.button('解析')

    if analyze_button and user_input:
        # セッションステートのクリア
        for key in list(st.session_state.keys()):
            if key.startswith('categories_') or key.startswith('probabilities_'):
                del st.session_state[key]

        lines = user_input.split('\n')
        for i, line in enumerate(lines):
            if line:  # 空の行は無視
                results = predict_category(line)
                st.session_state[f'text_{i}'] = line
                st.session_state[f'categories_{i}'] = list(results.keys())
                st.session_state[f'probabilities_{i}'] = list(results.values())

    threshold = st.slider("閾値を設定", 0.0, 1.0, 0.5, 0.01)

    # 水平線を挿入してセクションを区切る
    st.markdown("---")
    st.markdown("### 解析結果")


    # 解析結果の表示のために、キーをソート
    text_keys = sorted([key for key in st.session_state.keys() if key.startswith('text_')], key=lambda x: int(x.split('_')[1]))

    for key in text_keys:
        i = int(key.split('_')[1])
        line = st.session_state[key]
        if f'probabilities_{i}' in st.session_state:
            probabilities = st.session_state[f'probabilities_{i}']

            # 列を作成
            col1, col2, col3 = st.columns([6, 3, 1])
            with col1:
                st.write(line)
            with col2:
                if any(prob >= threshold for prob in probabilities):
                    # 検出された異常の種類をリストアップ
                    detected_anomalies = [category for category, prob in zip(st.session_state[f'categories_{i}'], probabilities) if prob >= threshold]
                    # 異常のリストを文字列に変換
                    anomalies_str = ', '.join(detected_anomalies)
                    # メッセージに異常のリストを含める
                    st.markdown(f"<span style='color: red;'>{anomalies_str}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: blue;'>正常です</span>", unsafe_allow_html=True)
            with col3:
                if f'categories_{i}' in st.session_state:
                    plot_results(st.session_state[f'categories_{i}'], st.session_state[f'probabilities_{i}'], threshold)


if __name__ == '__main__':
    main()
