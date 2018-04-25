# Guangxu Chen
import os
import json
from PIL import Image
import oss2

PATH_TO_images_DIR = 'D:\\Downloads\\images\\painting'
filenames = os.listdir(PATH_TO_images_DIR)
images_PATHS = [ os.path.join(PATH_TO_images_DIR, i) for i in filenames ]
url_base = 'https://cs6242project.oss-us-east-1.aliyuncs.com/'
types = ['', 'angle', 'arch', 'building', 'child', 'cross', 'horse', 'man', 'rock', 'ship', 'tree', 'vase', 'woman']
tag_map = {}

for i in types:
	tag_map[i] = []
color_map = {}
color_map['white'] = 1
color_map['silver'] = 2
color_map['gray'] = 3
color_map['aqua'] = 4
color_map['olive'] = 5
color_map['green'] = 6
color_map['skyblue'] = 7
color_map['darkblue'] = 8
color_map['wheat'] = 9
color_map['khaki'] = 10
color_map['brown'] = 11
color_map['black'] = 12

color_tag_map = {}
for line in open('D:\\Downloads\\color_recog.csv', 'r'):
	line = line.strip()
	#print line
	l = line.split(',')
	color_tag_map[l[0]] = l[1]
	
#print color_tag_map[filenames[10]]

for line in open('D:\\tensorflow\\6675\\result.txt', 'r'):
	line = line.strip()
	l = line.split(',')
	for i in range(0, len(types)):
		if l[i] != '0':
			tag_map[types[i]].append(l[0])
			
#print tag_map['tree']

json_list = []

for i in range(0, len(filenames)):
	filename = filenames[i]
	print(filename)
	json_dic = {}
	json_dic["thumbnail"] = url_base + filename
	json_dic["enlarged"] = json_dic["thumbnail"]
	tmp_list = filename.split('.')
	json_dic["title"] = tmp_list[0]
	tmp_str = ""
	for j in range(1, len(types)):
		if filename in tag_map[types[j]]:
			if tmp_str == "":
				tmp_str = tmp_str + types[j]
			else:
				tmp_str = tmp_str + ',' + types[j]
	json_dic["tag"] = tmp_str
	tmp_list2 = []
	tmp_dic = {}
	color = color_tag_map[filename]
	id = color_map[color]
	tmp_dic["id"] = id
	tmp_dic["color"] = color
	tmp_list2.append(tmp_dic)
	json_dic["categories"] = tmp_list2
	im = Image.open(images_PATHS[i])
	width, height = im.size
	json_dic["tWidth"] = width
	json_dic["tHeight"] = height
	json_dic["eWidth"] = width
	json_dic["eHeight"] = height
	json_list.append(json_dic)
	
#print json_list[0]
json_str = json.dumps(json_list)
#print json_str

with open('paintings.json', 'w') as f:
	f.write(json_str)