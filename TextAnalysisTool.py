import streamlit as st
import japanize_matplotlib
import matplotlib.pyplot as plt

def predict_category(text):
    probabilities = {
        "長い修飾"    :0.9,
        "てにをは不正":0.1,
        "意味不明"    :0.2,
        "係り受け"    :0.1,
        "主語なし"    :0.01,
    }

    return probabilities

def plot_results(categories, probabilities, threshold):
    plt.figure(figsize=(10, 4))
    plt.bar(categories, probabilities)
    plt.axhline(y=threshold, color='r', linestyle='-')
    plt.xlabel('カテゴリー')
    plt.ylabel('確率')
    plt.title('テキスト解析結果')
    st.pyplot(plt)

def main():
    st.write('テキスト解析ツール')

    user_input = st.text_area("テキストを入力してください")
    analyze_button = st.button('解析')

    if analyze_button and user_input:
        results = predict_category(user_input)
        categories = list(results.keys())
        probabilities = list(results.values())

        # 解析結果をセッションステートに保存
        st.session_state['categories'] = categories
        st.session_state['probabilities'] = probabilities

    threshold = st.slider("閾値を設定", 0.0, 1.0, 0.5, 0.01)

    # グラフと閾値判定を表示
    if 'categories' in st.session_state and 'probabilities' in st.session_state:
        plot_results(st.session_state['categories'], st.session_state['probabilities'], threshold)

        threshold_exceeded = False
        for category, probability in zip(st.session_state['categories'], st.session_state['probabilities']):
            if probability >= threshold:
                st.write(f"{category}: {probability} (閾値を超えています)")
                threshold_exceeded = True

        if not threshold_exceeded:
            st.write("この文章は正常です。")

    elif analyze_button and not user_input:
        st.write("テキストを入力して解析ボタンを押してください。")

if __name__ == '__main__':
    main()