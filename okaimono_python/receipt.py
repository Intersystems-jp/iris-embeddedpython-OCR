import os
json_path="/okaimono_python/*******.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_path # json_pathは、サービスアカウントキーのパス

import io
from google.cloud import vision
import receiptIRIS

def call_visionAPI(input_file):
  #input_file="C:\\WorkSpace\\EmbeddedPython-onlinelearning\\data\\img\\OK6.jpg"
  client = vision.ImageAnnotatorClient()
  with io.open(input_file, 'rb') as image_file:
      content = image_file.read()
  image = vision.Image(content=content)
  response = client.document_text_detection(image=image)
  print("***** googleのVisionAPIからの回答 *****")
  print(response.text_annotations[0].description)
  return response

#OCRで取得したテキストを位置に合わせてソートする
def get_sorted_lines(response):
    document = response.full_text_annotation
    bounds = []
    for page in document.pages:
      for block in page.blocks:
        for paragraph in block.paragraphs:
          for word in paragraph.words:
            for symbol in word.symbols:
              x = symbol.bounding_box.vertices[0].x
              y = symbol.bounding_box.vertices[0].y
              text = symbol.text
              bounds.append([x, y, text, symbol.bounding_box])
    bounds.sort(key=lambda x: x[1])
    old_y = -1
    line = []
    lines = []
    threshold = 1
    for bound in bounds:
      x = bound[0]
      y = bound[1]
      if old_y == -1:
        old_y = y
      elif old_y-threshold <= y <= old_y+threshold:
        old_y = y
      else:
        old_y = -1
        line.sort(key=lambda x: x[0])
        lines.append(line)
        line = []
      line.append(bound)
    line.sort(key=lambda x: x[0])
    lines.append(line)
    return lines


import re
import datetime

def get_matched_string(pattern, string):
    prog = re.compile(pattern)
    result = prog.search(string)
    if result:
        return result.group()
    else:
        return False


def getOCRData(input_file):
  response=call_visionAPI(input_file)
  lines = get_sorted_lines(response)
  
  #lineから各行がどの情報か取り出すための正規表現
  pattern_dict = {}
  pattern_dict['datetime'] = r'[12]\d{3}[/\-年](0?[1-9]|1[0-2])[/\-月](0?[1-9]|[12][0-9]|3[01])[/\-日](0?\([月火水木金土日]\))((0?|1)[0-9]|2[0-3])[:時][0-5][0-9]分?'
  #pattern_dict['tel'] = '0\d{1,3}-\d{1,4}-\d{4}'
  pattern_dict['total_price'] = r'^合計.*'
  pattern_dict['discount'] = r'^-(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3}))'
  pattern_dict['storename']=r'オーケー.+店'
  pattern_dict['itemname']=r'F.+'
  pattern_dict['itemprice']=r'(¥|#)(0|[1-9]\d*|[1-9]\d{0,2}(,\d{3})+)$'

  #OCRから戻ってきたテキストを後で確認できるようにするため一旦ファイルに出力（入力ファイルと同じ場所に置く）
  #入力ファイル名を取得して、拡張子.txtを付与
  filename=os.path.basename(input_file).split(".",1)[0]+".txt"
  #OCRから読み取った文字列を出力するファイルを置く
  dir=os.path.dirname(input_file)
  txtfile=os.path.join(dir,filename)
  f = open(txtfile, 'w', encoding='UTF-8')

  #IRISに登録したいデータ格納用リスト作成
  savedata=[]
  for line in lines:
    texts = [i[2] for i in line]
    texts = ''.join(texts)
    for key, pattern in pattern_dict.items():
      matched_string = get_matched_string(pattern, texts)
      if matched_string:
          # どうも¥が環境依存文字の方で、r"\\|,"　では消せないようす。
          if key == 'itemprice':
              matched_string=re.sub(r"¥|#|,","",matched_string)
          if key == 'datetime':
              #曜日が入ってるので削除
              matched_string=re.sub(r'(\([月火水木金土日]\))',"",matched_string)
          
          print(key, matched_string)
          #タブ区切りでファイル出力
          f.write(key+"\t"+ matched_string + "\n")
          savedata.append([key,matched_string])

  f.close()
  
  receiptIRIS.save(savedata)
  
  #テキストファイルの情報を利用してIRIS登録を試す場合
  #receiptIRIS.savefromfile(txtfile)
