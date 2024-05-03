import subprocess
from mastodon import Mastodon
import mimetypes
from datetime import datetime
import os

# Mastodon インスタンスを設定
mastodon = Mastodon(
    access_token='hogehoge',
    api_base_url='fugafuga'
)

# 現在の日時を取得
now = datetime.now()
formatted_date = now.strftime("%Y/%m/%d")  # ファイル名用
formatted_post_date = now.strftime("%m/%d/%H:%M")  # 投稿コメント用

# 写真を撮影
image_path = f'/home/piine/ine/{formatted_date.replace("/", "-")}.jpg'
subprocess.run(['libcamera-still', '-o', image_path])

# MIMEタイプを特定
mime_type, _ = mimetypes.guess_type(image_path)
if mime_type is None:
    mime_type = 'application/octet-stream'  # 未知のファイルタイプのデフォルト

# Mastodonに画像を投稿
with open(image_path, 'rb') as image:
    media_dict = mastodon.media_post(image, mime_type)
    mastodon.status_post(status=f'{formatted_post_date} の稲の様子です', media_ids=[media_dict['id']])

# 写真を指定された場所に保存（libcamera-still コマンドで既に保存されているため、このステップは省略可能）
