
import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート
import speech_recognition as sr # 音声認識の機能をインポート
from bokeh.models.widgets import Button
from bokeh.models import ColumnDataSource,CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# 言語選択と、APIが認識する言語の変換リストを作成
set_language_list = {
    "日本語" :"ja",
    "英語" :"en-US",
}

# デフォルトの言語を設定
set_language = "日本語"

# sr.Recognizer()をｒに代入して省略
r = sr.Recognizer()


# 音声ファイルと音声認識の言語を引数に音声認識をする
def file_speech_to_text(audio_file,set_language):

    # 音声ファイルを読み込み
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source) # r.record(開いた音声ファイル)で認識準備

    try:
        text = r.recognize_google(audio, language=set_language_list[set_language]) #  r.recognize_google(音声データ,言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text # 認識した文字を返す

st.title("文字起こしアプリ") # タイトル
st.write("音声認識する言語を選んでください。") # 案内を表示
set_language = st.selectbox("音声認識する言語を選んでください。",set_language_list.keys()) # 音声認識に使う言語を選択肢として表示
current_language_state = st.empty() # 選択肢を表示するための箱を準備
current_language_state.write("選択中の言語:" + set_language) # 選択肢を表示するための箱に選択した言語を表示
file_upload = st.file_uploader("ここに音声認識したファイルをアップロードしてください。",type=["wav"]) # アップローダーを設定し、wavファイルだけ許可する設定にする

# ファイルアップロードされた場合、file_uploadがNoneではなくなる
if (file_upload !=None):
    
    st.write("音声認識結果:") # 案内表示
    result_text = file_speech_to_text(file_upload,set_language) # アップロードされたファイルと選択した言語を元に音声認識開始
    st.write(result_text) # メソッドから返ってきた値を表示
    st.audio(file_upload) # アップロードした音声をきける形で表示


st.write("マイクでの音声認識はこちらのボタンから") # 案内表示


stt_button = Button(label="音声認識開始",width=123,height=36,margin=0)


if (set_language_list[set_language] == "ja"):
    stt_button.js_on_event("button_click", CustomJS(code="""
                                                    
        

        //音声認識APIの使用
        var speech = new webkitSpeechRecognition();
        speech.lang = "ja";
        speech.start();                                  
                                                    
        speech.addEventListener("result", function (e) {
            // 音声認識で取得した情報を表示
            var text = e.results[0][0].transcript;
            document.dispatchEvent(new CustomEvent("test", {detail: {return_text: text}}))
        });
                                                

        """))
else:
    stt_button.js_on_event("button_click", CustomJS(code="""

        //音声認識APIの使用
        var speech = new webkitSpeechRecognition();
        speech.lang = "en-US";
        speech.start();                                  
                                                    
        speech.addEventListener("result", function (e) {
            // 音声認識で取得した情報を表示
            var text = e.results[0][0].transcript;
            document.dispatchEvent(new CustomEvent("test", {detail: {return_text: text}}))
        });
                                                

        """))

#keysは任意のid
# document.dispatchEventで変数を受け取る
result2 = streamlit_bokeh_events(
    stt_button,
    events="test",
    key="stt",
    refresh_on_update=False,
    override_height=45,
    debounce_time=0)
state = st.empty() # マイク録音中を示す為の箱を準備
if (result2 != None):
    print(result2["test"]["return_text"])
    state.write("音声認識結果:")
    st.write(result2["test"]["return_text"])

