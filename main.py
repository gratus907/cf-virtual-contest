import json, requests

## User registration
userInfoList = []
contestInfoList = []
contestProblemList = []

def register_users():
    global userInfoList
    print("Input user name (A, B, C):")
    handles = input().split()
    for handle in handles:
        print(f"Register {handle} in process...",end=' ')
        r = requests.get(f"https://codeforces.com/api/user.info?handles={handle}")
        response = json.loads(r.text)
        result = response['result'][0]
        userInfoList.append(result)
        print(f"User {result['handle']} with rating {result['rating']} checked")
    print(f"{len(userInfoList)} users registered\n")


def fetch_contests(div=2, maxDuration=7200, minID=1200):
    global contestInfoList
    print("Fetching Contest info...")
    r = requests.get("https://codeforces.com/api/contest.list?gym=false")
    response = json.loads(r.text)
    contests = response['result']
    for contest in contests:
        if contest['phase'] == "BEFORE": continue
        if div==2 and (not "Div. 2" in contest['name']): continue
        if contest['durationSeconds'] > maxDuration: continue
        if contest['id'] < minID: continue
        contestInfoList.append(contest)
    print(f"{len(contestInfoList)} candidate contests\n")


def fetch_problem_list():
    global contestInfoList, contestProblemList
    print("Checking for new contests...")
    prob_list_json = open("prob_list.json", "r")
    cpList = dict(json.load(prob_list_json))
    fetchedRounds = list(cpList.keys())
    prob_list_json.close()
    cnt = 0
    for contest in contestInfoList:
        if str(contest['id']) in fetchedRounds:
            continue
        r = requests.get(f"https://codeforces.com/api/contest.standings?contestId={contest['id']}&from=1&count=1")
        response = json.loads(r.text)
        if response['status'] == 'FAILED': continue
        print(f"Found new contest! {contest['id'], contest['name']}")
        tmp = response['result']['problems']
        pList = []
        for p in tmp:
            pList.append(p['name'])
        cpList[str(contest['id'])] = pList
        cnt += 1
    print(f"{cnt} new contests found\n")
    file_ = open("prob_list.json", "w")
    json.dump(cpList, file_,sort_keys=True, indent=4)


def filter_contests(num=10):
    global userInfoList, contestInfoList, contestProblemList
    prob_list_json = open("prob_list.json", "r")
    cpList = json.load(prob_list_json)
    print("Filtering contests with submissions...")
    triedProblems = set()
    triedContests = set()
    for user in userInfoList:
        r = requests.get(f"https://codeforces.com/api/user.status?handle={user['handle']}")
        response = json.loads(r.text)
        subList = response['result']
        for sub in subList:
            triedContests.add(sub['contestId'])
            triedProblems.add(sub['problem']['name'])
    remainingContests = []
    for contest in contestInfoList:
        if int(contest['id']) in triedContests:
            continue
        pList = cpList[str(contest['id'])]
        flag = False
        for p in pList:
            if p in triedProblems:
                flag = True
        if flag: continue
        remainingContests.append(contest)
    num = min(len(remainingContests), num)
    print(f"{len(remainingContests)} candidates left. Showing recent {num}")
    for i in range(num):
        contest = remainingContests[i]
        print(contest['id'], contest['name'])

register_users()
fetch_contests(maxDuration=9000)
fetch_problem_list()
filter_contests(num=50)