import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import copy

driver=webdriver.Chrome("/Users/sayqu/Desktop/은령/과제/3-1/웹파/TermProject/chromedriver")
driver.get('https://play.google.com/store/apps/collection/cluster?clp=SnsKGgoUdG9wc2VsbGluZ19mcmVlX0dBTUUQBxgDEgRHQU1FGlcKUW5ld19ob21lX2RldmljZV9mZWF0dXJlZF9yZWNzMl90b3BpY192MV9sYXVuY2hfR0FNRV90b3BzZWxsaW5nX2ZyZWVfR0FNRV8zLTctMy03NBAMGAM%3D:S:ANO1ljLGqtA&gsr=Cn1KewoaChR0b3BzZWxsaW5nX2ZyZWVfR0FNRRAHGAMSBEdBTUUaVwpRbmV3X2hvbWVfZGV2aWNlX2ZlYXR1cmVkX3JlY3MyX3RvcGljX3YxX2xhdW5jaF9HQU1FX3RvcHNlbGxpbmdfZnJlZV9HQU1FXzMtNy0zLTc0EAwYAw%3D%3D:S:ANO1ljIhiZQ')


for i in range(4): # 3번 스크롤을 내리면 전체 랭킹 순위가 다 나오게 됨
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # 스크롤을 내려 로딩한 값까지 긁어오기 위해서 3초 대기

urlList=[]
details=driver.find_elements_by_class_name('JC71ub')
for item in details:
    url=item.get_attribute("href")
    urlList.append(url)

starDic={}
onlyStarDic={}
path_1='//*[@id="fcxH9b"]/div[4]/c-wiz/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/div['
path_2=']/c-wiz/div/div/div[2]/div/div/div[2]/div/div/div/div'
for i in range(1, 51):
    stars=driver.find_element_by_xpath(path_1+str(i)+path_2)
    star = stars.get_attribute("aria-label")
    starDic[i]=float(star[10:13])+10-((i-1)*0.025) # 1~50위
    onlyStarDic[i]=float(star[10:13])

path_1='//*[@id="fcxH9b"]/div[4]/c-wiz/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/c-wiz['
path_2=']/div/div/div[2]/div/div/div[2]/div/div[1]/div/div'
for i in range(1, 151):
    stars=driver.find_element_by_xpath(path_1+str(i)+path_2)
    star = stars.get_attribute("aria-label")
    starDic[50+i]=float(star[10:13])+10-((50+i-1)*0.025) # 51~200위
    onlyStarDic[50+i] = float(star[10:13])
sorted_starDic=sorted(starDic.items(), key=lambda x:x[1], reverse=True)
sorted_onlyStarDic=sorted(onlyStarDic.items(), key=lambda x:x[1], reverse=True)

ranks=driver.find_elements_by_class_name("kCSSQe")
rank_dictionary={}
for item in ranks:
    if(item.text!=''):
        rankList=item.text.split('\n')
        rank_dictionary[rankList[0]] = rankList[1]
    # rankList에다가 게임 이름과 회사를 각각 0과 1 인덱스에 저장
    # 그 후 rank_dictionary에 추가 (게임 이름이 key, 회사가 value)

games=[]
count=1
for k, v in rank_dictionary.items():
    newList=[count, k, v]
    games.append(newList) # rank_dictionary의 items를 list로 만들어줌
    count+=1

with open('Game_Rank_List.csv', 'w', encoding='UTF8') as fileWrite:
    myWriter=csv.writer(fileWrite)
    for i in range(len(games)):
        myWriter.writerow(games[i])

upperList=[]
lowerList=[]
for i in range(len(sorted_starDic)):
    find=sorted_starDic[i][0]-1
    if(i<20): # 상위 10퍼센트에 속한다면
        new=copy.copy(games[find])
        new.append(urlList[find]) # url 값까지 넣어줌
        upperList.append(new) # upperList에 순위, 게임 이름, 회사 이름, url 순서로 들어감
    elif(i>=len(sorted_starDic)-20): # 하위 10퍼센트에 속한다면
        new = copy.copy(games[find])
        new.append(urlList[find])  # url 값까지 넣어줌
        lowerList.append(new) # lowerList에 upperList와 같은 순서로 들어감

with open('Game_Rank_upperList.csv', 'w', encoding='UTF8') as fileWrite:
    myWriter=csv.writer(fileWrite)
    for i in range(len(upperList)):
        myWriter.writerow(upperList[i])

with open('Game_Rank_lowerList.csv', 'w', encoding='UTF8') as fileWrite:
    myWriter=csv.writer(fileWrite)
    for i in range(len(lowerList)-1, -1, -1):
        myWriter.writerow(lowerList[i])


star_upperList=[]
star_lowerList=[]
for i in range(len(sorted_onlyStarDic)):
    find=sorted_onlyStarDic[i][0]-1 # x위는 games의 x-1번째에 위치하기 때문
    if(i<20): # 상위 10퍼센트에 속한다면
        new=copy.copy(games[find])
        new.append(sorted_onlyStarDic[i][1])
        new.append(urlList[find]) # url 값까지 넣어줌
        star_upperList.append(new) # upperList에 순위, 게임 이름, 회사 이름, url 순서로 들어감
    elif(i>=len(sorted_onlyStarDic)-20): # 하위 10퍼센트에 속한다면
        new = copy.copy(games[find])
        new.append(sorted_onlyStarDic[i][1])
        new.append(urlList[find])  # url 값까지 넣어줌
        star_lowerList.append(new) # lowerList에 upperList와 같은 순서로 들어감


with open('Game_Rank_Star_upperList.csv', 'w', encoding='UTF8') as fileWrite:
    myWriter=csv.writer(fileWrite)
    for i in range(len(star_upperList)):
        myWriter.writerow(star_upperList[i])

with open('Game_Rank_Star_lowerList.csv', 'w', encoding='UTF8') as fileWrite:
    myWriter=csv.writer(fileWrite)
    for i in range(len(star_lowerList)-1, -1, -1):
        myWriter.writerow(star_lowerList[i])