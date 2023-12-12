from google.cloud import vision
import google.cloud.vision_v1.types as types
from PIL import Image
from PIL import ImageOps
import os
import random
import shutil

images_dir_path='./img/後藤ひとり_コスプレ'
train_dir_path='./ds/train'
test_dir_path='./ds/test'

image_size=(128,128)

def detect_face(image_path):
    client=vision.ImageAnnotatorClient()
    #コードブロックが終わったら自動でfileが閉じる
    #メモリの効率化
    #引数で取ったiamge_pathを'rb'バイナリファイルを読み込む
    with open(image_path, 'rb') as file:
        #読み込んだバイナリファイルを画像形式に変換している        
        image=types.Image(content=file.read())
        #GCV APIのface_detection()を使って画像内の顔を検出する
        #そのうち、顔の情報を含むface_annotationsオブジェクトを返す
        annotations=client.face_detection(image=image).face_annotations
    
    face_boxes=[]

    for annotation in annotations:
        #annotation(顔の情報)の境界ボックス(bounding_poly)の座標情報(vertices)を取得
        #リスト内包表記で、うちx座標のみをリストに格納
        x_s=[vertex.x for vertex in annotation.bounding_poly.vertices]
        y_s=[vertex.y for vertex in annotation.bounding_poly.vertices]
        face_boxes.append((min(x_s),min(y_s),max(x_s),max(y_s)))
    return face_boxes

def splist_dataset(images_dir_path):
    file_list=os.listdir(images_dir_path)
    random.shuffle(file_list)

    train_size=int(len(file_list)*0.8)

    if not os.path.exists('./ds'):
        os.mkdir('./ds')
    if not os.path.exists(train_dir_path):
        os.mkdir(train_dir_path)
    
    if not os.path.exists(test_dir_path):
        os.mkdir(test_dir_path)
    
    #enumerate()とすることで、引数のリストとかから、インデックスと要素のペアを返してくれる
    for i, file in enumerate(file_list):
        if i < train_size:
            shutil.copy(os.path.join(images_dir_path, file), os.path.join(train_dir_path, file))
        else:
            shutil.copy(os.path.join(images_dir_path, file), os.path.join(test_dir_path, file))
#顔周辺(マージン)を切り取る
#後で
max_margin=0.2

file_list=os.listdir(images_dir_path)

for img in file_list:
    new_img=os.path.join(images_dir_path,img)
    target_name=images_dir_path.split('/')[-1]
    print(new_img)

    if img.endswith('.jpg') or img.endswith('.png') or img.endswith('.jpeg'):
        #faces=img+'_face'
        faces=detect_face(new_img)

        if len(faces)>0:
            #PILライブラリのImage.open()で画像を開く
            image=Image.open(new_img).convert('RGB')

            x1,y1,x2,y2=faces[0]
            w=x2-x1
            h=y2-y1

            spaces_x = min(x1, image.width - x2, int(float(w) * max_margin))
            spaces_y = min(y1,image.height-y2,int(float(h)*max_margin))
            margin=min(spaces_x,spaces_y)

            cropped_img=image.crop((
                x1-margin,
                y1-margin,
                x2+margin,
                y2+margin
            ))
            #ImageOps:切り取り
            cropped_img=ImageOps.contain(cropped_img,image_size)

            directory='face_cropped'
            new_directory=os.path.join('./img',directory,target_name)
            if not os.path.exists(new_directory):
                os.mkdir(new_directory)

            cropped_img.save(os.path.join(new_directory,f'cropped_{img}'))

splist_dataset(os.path.join('./img','face_cropped','後藤ひとり_コスプレ'))