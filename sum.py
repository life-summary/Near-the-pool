# coding: utf-8

import datetime # 日付や時間データを操作するためのクラスを実装
import csv # CSV形式で書かれたテーブル状のデータを読み書きするためのクラスを実装
import argparse # コマンドライン引数の解析モジュール


def load_inet_data(fname):
    f = open(fname, 'r') # fnameというファイル名のCSVファイルを，fという変数でオープン
    d = csv.reader(f) # CSVの中身を変数dに格納
    data = [] # 空の配列をdataという変数で定義

    for i in d:
        append = str(i[0]) + '/' + str(i[1]) # appendという変数に，iの0個目の要素と1個めの要素を'/'で繋いだ文字列を格納
        t = {'datetime': datetime.datetime.strptime(append, '%Y-%m-%d/%H:%M'), # 辞書に日付，センサ1の状態，センサ2の状態を格納
             'id1': i[2],
             'id2': i[3]}
        data.append(t) # dataにtを追加

    return data


def sensor_data_sum(data):
    data_sum = [] # 空の配列をdata_sumという変数で定義

    cnt1 = 0 # id1の合計を格納する変数
    cnt2 = 0 # id2の合計を格納する変数

    now = data[0]['datetime'] # 日にちを保持
    now -= datetime.timedelta(hours=now.hour, minutes=now.minute) # 時間，分を0に初期化

    for minute in data:
        difference = minute['datetime'] - now # minuteとnowの差をdifferernceに格納

        if difference.days == 1 or minute['datetime'] == data[-1]['datetime']: # 差が1日になる or 一番最後のdataの時，True
            t = {'datetime': now, # 辞書に日付，センサ1の合計，センサ2の合計を格納
                 'id1':      cnt1,
                 'id2':      cnt2}
            data_sum.append(t) # data_sumにtを追加
            now = minute['datetime'] # nowを更新
            cnt1 = 0 # 初期化
            cnt2 = 0 # 初期化

        if minute['id1'] == 'x' or minute['id1'] == 'X': # id1にデータがない時0置換
            minute['id1'] = '0'
        if minute['id2'] == 'x' or minute['id2'] == 'X': # id2にデータがない時0置換
            minute['id2'] = '0'

        cnt1 += int(minute['id1'], 16) # 16進数を10進数に変換し加算
        cnt2 += int(minute['id2'], 16) # 16進数を10進数に変換し加算

    return data_sum


def main():
    # 引数からファイル名を取得
    parser = argparse.ArgumentParser() # コマンドラインの情報を取得
    parser.add_argument("input_csv_file") # コマンドラインの文字列を受け取ってそれをオブジェクトにする
    parser.add_argument("--encoding", default="utf_8") # エンコード
    options = parser.parse_args() # 引数解析
    fname = options.input_csv_file # fnameに引数のCSVファイル名を格納

    print(fname) # ファイル名表示

    data = load_inet_data(fname) # dataにCSVの中身を格納
    data_sum = sensor_data_sum(data) # data_sumに日毎のセンサ合計値を格納

    for day in data_sum: # 表示
        print(day['datetime'], day['id1'], day['id2'])

if __name__ == '__main__':
    main()
