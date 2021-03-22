from matplotlib import pyplot as plt

fromNodeIdList = []
toNodeIdList = []
with open(r'Wiki-Vote.txt') as voteFile:
    while True:
        voteLine = voteFile.readline()
        if voteLine == '':
            break
        # The 1-4 lines are comments, so we should remove them
        if voteLine.startswith('#'):
            continue
        voteLineList = voteLine.split("\t")
        voteLineList[1] = voteLineList[1][:-1]
        fromNodeIdList.append(int(voteLineList[0]))
        toNodeIdList.append(int(voteLineList[1]))

# we need to sort these two lists
fromNodeIdList.sort()
toNodeIdList.sort()

# we count the voted numbers of each user
fromNodeIdHashMap = {}
toNodeIdHashMap = {}

for item in fromNodeIdList:
    if fromNodeIdHashMap.get(item) == None:
        fromNodeIdHashMap[item] = 1
    else:
        fromNodeIdHashMap[item] = fromNodeIdHashMap.get(item) + 1

for item in toNodeIdList:
    if toNodeIdHashMap.get(item) == None:
        toNodeIdHashMap[item] = 1
    else:
        toNodeIdHashMap[item] = toNodeIdHashMap.get(item) + 1

# sort the two hashmap by value in descending way
fromNodeIdSortedList = sorted(fromNodeIdHashMap.items(), key = lambda x : x[1], reverse = True)
toNodeIdSortedList = sorted(toNodeIdHashMap.items(), key = lambda x : x[1], reverse = True)

# show the scatter plots
plt.figure()
# solve the problem of Chinese encoding
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.subplot(121)
plt.title("发起投票")
plt.xlabel("编号")
plt.ylabel("投票的数量")
plt.scatter([item[0] for item in fromNodeIdSortedList],  [item[1] for item in fromNodeIdSortedList])
plt.subplot(122)
plt.title("获得投票")
plt.xlabel("编号")
plt.scatter([item[0] for item in toNodeIdSortedList], [item[1] for item in toNodeIdSortedList])
plt.show()
