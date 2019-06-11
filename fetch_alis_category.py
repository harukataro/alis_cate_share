import requests
import json
import datetime
import urllib
from datetime import datetime, timedelta, timezone
from operator import itemgetter

CATEGORY = ['ビューティ', '音楽', 'ALIS', '恋愛・出会い', '神仏', '教育・子育て']
CURR_CATE = [{'jp': 'ビジネス', 'en': 'business'}, {'jp': 'マンガ・アニメ', 'en': 'comic-animation'}, {'jp': 'テクノロジー', 'en':'technology'}, {'jp': 'クリプト', 'en': 'crypto'}, {'jp': 'グルメ', 'en': 'gourmet'}, {'jp': 'トラベル', 'en': 'travel'}, {'jp': 'ゲーム', 'en': 'game'}, {'jp': 'おもしろ', 'en': 'entertainment'}]
cate_num = len(CATEGORY)
curr_cate_num = len(CURR_CATE)


def category_calc(ranked):
    calcs = []
    cate_url = category_url()
    for i in range(cate_num):
        datax = {}
        datax['category'] = CATEGORY[i]
        datax['url'] = cate_url[i]
        datax['article_num'] = 0
        datax['comment_num'] = 0
        datax['like_num'] = 0
        datax['user_num'] = 0
        datax['user_ids'] = []
        calcs.append(datax)

    for s in range(len(ranked)):
        category_much = 0
        cate_num_much = 100
        for i in range(cate_num):
            if CATEGORY[i] in ranked[s]['tags']:
                category_much += 1
                cate_num_much = i
                if category_much == 2:
                    continue
        if category_much == 0:
            continue

        calcs[cate_num_much]['like_num'] += like_num(ranked[s]['article_id'])
        calcs[cate_num_much]['comment_num'] += comment_num(ranked[s]['article_id'])
        calcs[cate_num_much]['article_num'] += 1
        if ranked[s]['user_id'] not in calcs[cate_num_much]['user_ids']:
            calcs[cate_num_much]['user_ids'].append(ranked[s]['user_id'])
            calcs[cate_num_much]['user_num'] += 1
    return calcs


def category_calc_c(ranked):
    calcs = []
    category_url_c()
    for u in range(curr_cate_num):
        datax = {}
        datax['category'] = CURR_CATE[u]['en']
        datax['url'] = CURR_CATE[u]['url']
        datax['article_num'] = 0
        datax['comment_num'] = 0
        datax['like_num'] = 0
        datax['user_num'] = 0
        datax['user_ids'] = []
        calcs.append(datax)

    for s in range(len(ranked)):
        print(s)
        for i in range(curr_cate_num):
            if ranked[s]['category'] == CURR_CATE[i]['en']:
                calcs[i]['article_num'] += 1
                calcs[i]['like_num'] += like_num(ranked[s]['article_id'])
                calcs[i]['comment_num'] += comment_num(ranked[s]['article_id'])

                if ranked[s]['user_id'] not in calcs[i]['user_ids']:
                    calcs[i]['user_ids'].append(ranked[s]['user_id'])
                    calcs[i]['user_num'] += 1
                break
    return calcs


def like_num(article_id):
    num = 0
    api = 'https://alis.to/api/articles/{article_id_label}/likes'
    url = api.format(article_id_label=article_id)
    response = requests.get(url)
    data = json.loads(response.text)
    if 'count' in data:
        num = int(data['count'])
    return num


def comment_num(article_id):
    api = 'https://alis.to/api/articles/{article_id_label}/comments?limit=100'
    url = api.format(article_id_label=article_id)
    response = requests.get(url)
    data = json.loads(response.text)
    if 'Items' in data:
        qa = len(data['Items'])
    else:
        return 0
    for i in range(len(data['Items'])):
        if 'replies' in data['Items'][i]:
            qa += len(data['Items'][i]['replies'])
    return int(qa)


def alis_format(calcs):
    cate_num =len(calcs)
    JST = timezone(timedelta(hours=+9), 'JST')
    nowx = datetime.now(JST)
    mid_contents = mid_contents + str(nowx.month) + '月' + str(nowx.day) + '日' + str(nowx.hour) + '時 更新<br>\n'

    mid_contents += '<h2>記事数集計</h2>\n'
    calcs = sorted(calcs, key=itemgetter('article_num'), reverse=True)
    for i in range(cate_num):
        if calcs[i]['article_num'] == 0:
            break
        mid_contents = mid_contents + calcs[i]['url'] + ': ' + str(calcs[i]['article_num']) + '<br>\n'
    mid_contents += '<br>'

    mid_contents += '<h2>いいね数集計</h2>\n'
    calcs = sorted(calcs, key=itemgetter('like_num'), reverse=True)
    for i in range(cate_num):
        if calcs[i]['like_num'] == 0:
            break
        mid_contents = mid_contents + calcs[i]['url'] + ': ' + str(calcs[i]['like_num']) + '<br>\n'
    mid_contents += '<br>'

    mid_contents += '<h2>コメント数集計</h2>\n'
    calcs = sorted(calcs, key=itemgetter('comment_num'), reverse=True)
    for i in range(cate_num):
        if calcs[i]['comment_num'] == 0:
            break
        mid_contents = mid_contents + calcs[i]['url'] + ': ' + str(calcs[i]['comment_num']) + '<br>\n'
    mid_contents += '<br>'

    mid_contents += '<h2>ユニークユーザー数集計</h2>\n'
    calcs = sorted(calcs, key=itemgetter('user_num'), reverse=True)
    for i in range(cate_num):
        if calcs[i]['user_num'] == 0:
            break
        mid_contents = mid_contents + calcs[i]['url'] + ': ' + str(calcs[i]['user_num']) + '<br>\n'
    mid_contents += '<br>'

    file = open('alis-category-alis.html', 'w')
    file.write(mid_contents)
    file.close()


def category_url():
    url = [''] * cate_num
    for i in range(cate_num):
        url[i] = '<a href="https://alis.to/tag/' + urllib.parse.quote(CATEGORY[i]) + '">' + CATEGORY[i] + '</a>'
    return url


def category_url_c():
    for i in range(curr_cate_num):
        CURR_CATE[i]['url'] = CURR_CATE[i]['jp']
    return 0


def contest_calc():
    api = 'https://alis.to/api/articles/recent?limit=100&page={page}'
    PAGE_NUM = 50
    ranked = []
    limit_dt = datetime(2019, 5, 15, 15, 0)
    oldest_dt = datetime(2019, 5, 16)
    fetch_stop_dt = datetime(2019, 5, 10)

    for i in range(PAGE_NUM):
        url = api.format(page=str(i + 1))
        response = requests.get(url)
        data = json.loads(response.text)

        for s in range(len(data['Items'])):
            d_new = {}
            date_created = datetime.fromtimestamp(data['Items'][s]['published_at'])
            d_new['user_id'] = data['Items'][s]['user_id']
            if date_created < limit_dt or d_new['user_id'] == 'ALIS-official':
                continue
            d_new['article_id'] = data['Items'][s]['article_id']
            d_new['tags'] = data['Items'][s]['tags']
            ranked.append(d_new)

            oldest_dt = min(oldest_dt, date_created)
        if oldest_dt < fetch_stop_dt:
            print("fetch page end by ", i)
            break
    if len(ranked) > 1:
        print(oldest_dt)
    return ranked


def regacy_calc():
    api = 'https://alis.to/api/articles/recent?topic={category}&limit=100&page={page}'
    PAGE_NUM = 60
    ranked = []
    limit_dt = datetime(2019, 5, 15, 15, 0)
    fetch_stop_dt = datetime(2019, 5, 10)

    for u in range(curr_cate_num):
        print(CURR_CATE[u]['jp'])
        oldest_dt = datetime(2019, 5, 16)
        for i in range(PAGE_NUM):
            url = api.format(category=CURR_CATE[u]['en'], page=str(i + 1))
            response = requests.get(url)
            data = json.loads(response.text)

            for s in range(len(data['Items'])):
                d_new = {}
                date_created = datetime.fromtimestamp(data['Items'][s]['published_at'])
                d_new['user_id'] = data['Items'][s]['user_id']
                d_new['article_id'] = data['Items'][s]['article_id']
                d_new['category'] = CURR_CATE[u]['en']

                oldest_dt = min(oldest_dt, date_created)
                if date_created < limit_dt:
                    continue
                ranked.append(d_new)
            if oldest_dt < fetch_stop_dt:
                print("fetch page end by ", i)
                print(oldest_dt)
                break
    return ranked


if __name__ == '__main__':
    print("get information from ALIS")
    ranked = contest_calc()
    ranked_c = regacy_calc()

    print('calculate new category articles')
    calcs = category_calc(ranked)
    print('calculate exiting category articles')
    calcs_c = category_calc_c(ranked_c)
    calcs.extend(calcs_c)

    print('make form for alis')
    alis_format(calcs)
