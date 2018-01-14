import urllib.request, sys,base64,json,os,time,baiduSearch
from PIL import Image
from aip import AipOcr
from analyse_answer import Ai

start = time.time()
os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png") 
os.system("adb pull /sdcard/screenshot.png ./screenshot.png")
'''
汉王ocr 涨价涨价了。。
host = 'http://text.aliapi.hanvon.com'
path = '/rt/ws/v1/ocr/text/recg'
method = 'POST'
appcode = 'a962e94260ee4043b824d2f40c126d8e'    #汉王识别appcode（填你自己的）
querys = 'code=74e51a88-41ec-413e-b162-bd031fe0407e'
bodys = {}
url = host + path + '?' + querys
'''
""" （百度ocr）你的 APPID AK SK """
APP_ID = '10684531'
API_KEY = 'FqRvrpPwhSNXt2FhT6d3dXfc'
SECRET_KEY = 'UIu2qOPHXENScjr1yzAyXQgNkLQzkcdc'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

im = Image.open(r"./screenshot.png")   

img_size = im.size
w = im.size[0]
h = im.size[1]
print("屏幕尺寸:{}".format(img_size))

""" 读取图片函数 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
""" 获取最大的数字函数 """
def biggest(a,b,c,d):  
         if a>b:
             maxnum = a
         else:
             maxnum = b
         if c>maxnum:
             maxnum=c
             if  d > maxnum:
                   maxnum = d
         return maxnum

""" 截取问题图片 """
question  = im.crop((130, 600, w-130, 880)) # mi6
question.save(r"./crop_test1.png")

""" 获取问题文本 """
question_image = get_file_content(r"./crop_test1.png")
#用完500次后可改respon = client.basicAccurate(question_image) 
respon = client.basicAccurate(question_image)  
titles = respon['words_result']
ans = ''
for title in titles:
      ans = ans +title['words']
#打印问题（黑色）
print("\033[30m", ans) 

""" 截取答案图片 """
answer1 = im.crop((250, 950 , 880, 1110)) 
answer1.save(r"./crop_answer1.png")
answer2 = im.crop((250, 1150 , 880, 1310)) 
answer2.save(r"./crop_answer2.png")
answer3 = im.crop((250, 1350 , 880, 1510)) 
answer3.save(r"./crop_answer3.png")
answer4 = im.crop((250, 1550 , 880, 1710)) 
answer4.save(r"./crop_answer4.png")
""" 获取答案文本 """
# 答案1
ans1_img = get_file_content(r"./crop_answer1.png")
ans1_respon = client.basicAccurate(ans1_img) 
ans1_result = ans1_respon['words_result'] 
ans1_words = ''
for title1 in ans1_result:
      ans1_words = ans1_words +title1['words']
# 答案2
ans2_img = get_file_content(r"./crop_answer2.png")
ans2_respon = client.basicAccurate(ans2_img) 
ans2_result = ans2_respon['words_result'] 
ans2_words = ''
for title2 in ans2_result:
      ans2_words = ans2_words +title2['words']
# 答案3
ans3_img = get_file_content(r"./crop_answer3.png")
ans3_respon = client.basicAccurate(ans3_img) 
ans3_result = ans3_respon['words_result'] 
ans3_words = ''
for title3 in ans3_result:
      ans3_words = ans3_words +title3['words']
# 答案4
ans4_img = get_file_content(r"./crop_answer4.png")
ans4_respon = client.basicAccurate(ans4_img) 
ans4_result = ans4_respon['words_result'] 
ans4_words = ''
for title4 in ans4_result:
      ans4_words = ans4_words +title4['words']
# 打印答案（蓝色） 
print("\033[34m", ans1_words, ans2_words, ans3_words, ans4_words)

keyword = ans 
convey = 'n'
if convey == 'y' or convey == 'Y':
    results = baiduSearch.search(keyword, convey=True)
elif convey == 'n' or convey == 'N' or not convey:
    results = baiduSearch.search(keyword)
else:
    print('输入错误')
    exit(0)
count = 0

# 获取搜索结果 
result_final = ''
for result in results:
    # print('{0} {1} {2} {3} {4}'.format(result.index, result.title, result.abstract, result.show_url, result.url))  # 此处应有格式化输出
	# print("\033[31m", '{0}'.format(result.abstract))  # 此处应有格式化输出
      result_final = result_final + '{0}'.format(result.abstract)
      count=count+1
      if(count == 2): #这里限制了只显示2条结果，可以自己设置
            break
# 打印搜索结果（红色） 
print("\033[31m", result_final)

""" 分析答案（统计答案在结果中的出现次数） """
a = result_final.count(ans1_words)
b = result_final.count(ans2_words)
c = result_final.count(ans3_words)
d = result_final.count(ans4_words)
dict={a: ans1_words, b: ans2_words, c: ans3_words, d: ans4_words}
print("\036[35m", '推荐答案：' + dict[biggest(a,b,c,d)])


end = time.time()
print('程序用时：'+str(end-start)+'秒')