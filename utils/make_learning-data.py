import PySimpleGUI as sg
import os
import subprocess
import webbrowser
import time

# ウィンドウのテーマ
sg.theme('SystemDefault')

# 実行するコマンド
def run_bat():
    train_name = r"train-data\train-"+values[0]+".hcpe"
    test_name  = r"train-data\test-"+values[0]+".hcpe"
    min_rating = "--min_rating " + str(int(values[1]))
    max_rating = "--max_rating " + str(int(values[2]))
    years_str = "--get_years "
    if values[3] == True: years_str += "2015."
    if values[4] == True: years_str += "2016."
    if values[5] == True: years_str += "2017."
    if values[6] == True: years_str += "2018."
    if values[7] == True: years_str += "2019."
    if values[8] == True: years_str += "2020."
    if years_str == "--get_years ": years_str += "0000."
    years_str = years_str[:-1]  # 最後の一文字「.」を削る。
    
    run_str = r"python utils\csa_to_hcpe.py ..\wdoor-csa " \
              + train_name +" "+ test_name +" " \
              + min_rating +" "+ max_rating +" "+ years_str 
    sg.popup("学習データを作成するので、OK押して待ってね。", font=(None,14), title = "")
    # 実行するコマンドを出力する。
    with open(r"train-data\output_cmd.txt", mode='w') as f:
        f.write(run_str)
    subprocess.run(run_str)

# ウィンドウに配置するコンポーネント
txt_str1  = "作成する「train-***.hcpe」と「test-***.hcpe」ファイルの\n"
txt_str1 += "***は何にする？"

layout = [
    [sg.Text(txt_str1, font=(None,14) )],
    [sg.InputText()],
    [sg.Text('')],
    [sg.Text('最低ratingは？', font=(None,14)), sg.Slider(range=(0,5000), default_value=3500, resolution=100, orientation='h', font=(None,14))],
    [sg.Text('')],
    [sg.Text('最高ratingは？', font=(None,14)), sg.Slider(range=(0,5000), default_value=5000, resolution=100, orientation='h', font=(None,14))],
    [sg.Text('')],
    [sg.Text('何年度のfloodgateの棋譜を使う？（1～2年分がオススメ）', font=(None,14) )],
    [sg.Checkbox('2015年', font=(None,14)), sg.Checkbox('2016年', font=(None,14)), sg.Checkbox('2017年', font=(None,14))],
    [sg.Checkbox('2018年', font=(None,14)), sg.Checkbox('2019年', font=(None,14)), sg.Checkbox('2020年', font=(None,14), default=True)],
    [sg.Text('')],
    [sg.Button('学習データを作成する', font=(None,14))],
    [sg.Text('')],
    [sg.Button('このウインドウを終了する', font=(None,14))]
     ]

# ウィンドウの生成
window = sg.Window('将棋AI学習データ作成ツール', layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'このウインドウを終了する':
        break
    elif event == '学習データを作成する':
        """if    values[3] == False \
          and values[4] == False \
          and values[5] == False \
          and values[6] == False \
          and values[7] == False \
          and values[8] == False:
            sg.popup("年度を選んでほしい。", font=(None,14), title = "")
            continue"""
            
        run_bat()
        popup_str  = "学習データを作成したよ。\n"
        popup_str += "OKを押すとフォルダーを開けるね。"
        sg.popup(popup_str, font=(None,14), title = "")
        # フォルダを開く
        subprocess.Popen(["explorer",  r"train-data"], shell=True)
        
        # 1秒間を空ける。
        time.sleep(1)
        popup_str  = "OKを押した後に表示されるGoogleColaboratoryに\n"
        popup_str += "書かれている内容に沿って、\n"
        popup_str += "作成した学習データで学習させてね。"
        # エクスプローラに隠れないように前面表示
        sg.popup(popup_str, font=(None,14), title = "", keep_on_top=True)

        # Webページを開く
        #webbrowser.open(r"https://colab.research.google.com/drive/1XwKtPMPGJqR54xjXYQKlUsRjNsJD8Ej7?usp=sharing")
        
        # Windowを閉じるときは、breakを有効にする。
        #break

# キャンセル時ウィンドウ終了処理
window.close()
