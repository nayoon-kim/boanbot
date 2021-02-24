# boanbot

## 설명
> 최신 보안이슈를 볼 수 있는 카카오톡 챗봇 '보안봇'입니다. 
데일리시큐, 보안뉴스와 같은 국내 보안 뉴스 사이트에 들어가지 않고도 보안 뉴스를 접할 수 있으며, wired와 googlezeroprojects와 같은 해외 사이트의 보안 뉴스 또한 접할 수 있습니다.
이 뿐만 아니라, '솔라윈즈'나 '제로데이'와 같은 보안 키워드를 채팅창에 입력하면 해당 키워드에 대한 뉴스 기사만 모아서 볼 수 있습니다.

## 기술 및 구조
> celery 5.05
>
> Django 3.1.5
>
> djangorestframework 3.12.2
>
> gunicorn 20.0.4
>
> docker 4.4.1
>
> nginx
>
> redis

<img src="https://user-images.githubusercontent.com/53392870/108966244-4860c800-76c1-11eb-952a-6749298e42af.png">

## 파일 구조

1. 카카오톡 채팅창에 발화내용(utterance) 입력 시, callApi 함수가 호출되고, 요청값(userRequest)에서 발화내용(utterance)만 추출해서 reply 함수를 호출한다.
```python
# views.py

...

def callApi(request):
    messages = Messages()
    if request.method == 'POST':
        data = JSONParser().parse(request)
        client_utterance = data['userRequest']['utterance'].strip('\n')

        return JsonResponse(messages.reply(client_utterance), status=200)
```

2. reply 함수는 analyze 함수를 호출하고, analyze 함수는 발화내용(utterance)에 따라 실행하는 함수가 달라진다.

```python
# main.py
class Messages:
    hub = Hub()
    templates = KakaoTemplates()

    def reply(self, client_utterance):
        return self.analyze(client_utterance)

    # client_utterance에 따른 templates 해석
    def analyze(self, client_utterance):
        # quickReplies_keywords = ['보안', '안내', '키워드']
        if client_utterance in quickReplies_keywords:
            templates = self.templates.quickReplies()
        # basicCard_keywords = ['주의 이슈', '다크웹', '사건사고', '취약점 경고 및 버그리포트', '주간 핫 뉴스', '최신 보안 뉴스', '올해 보안 전망', '의료 보안', '해외 보안 뉴스(영어)', '구글제로프로젝트', '해외 보안 뉴스(한글)', ]
        elif client_utterance in basicCard_keywords:
            data = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(data)
        # 위의 키워드에 포함되지 않는 경우 검색
        else:
            valid_check = self.hub.distribute(client_utterance)
            templates = self.templates.basicCard(valid_check) if valid_check is not None else self.templates.quickReplies()

        return templates
```

(1) quickReplies_keywords에 속하는 발화내용을 입력할 경우, quickReplies 함수를 호출하게 된다.

  - quickReplies는 바로가기 응답으로, 사용자가 직접 발화를 입력하지 않아도 선택을 통해서 발화를 전달하거나 다른 블록을 호출할 수 있도록 화면에 선택지를 표시합니다. 따라서 카카오톡 챗봇 '바로가기 응답' 포맷에 맞춰서 값을 리턴해준다.

<img src="https://user-images.githubusercontent.com/53392870/108976071-80203d80-76ca-11eb-9900-dccbd11ffc17.png">

(2) basicCard_keywords에 속하는 발화내용을 입력하였을 경우, distribute 함수 호출 후 결과값을 basicCard 함수에 파라미터로 넣어준다.

  - basicCard는 기본 카드형 출력 요소로 뉴스 기사의 제목, 썸네일 이미지, 링크, 작성일자, 기자 이름의 정보를 제공합니다. basicCard의 경우 quickReplies와 달리 발화내용(utterance)에 따라 출력값이 달라져야 하기 때문에 data를 파라미터로 받아 카카오톡 챗봇 '기본 카드형' 포맷에 맞춰 입력한 다음 값을 리턴해준다.

<img src="https://user-images.githubusercontent.com/53392870/108976279-b52c9000-76ca-11eb-8495-04b9df5ca2fc.png">

(3) quickReplies_keywords 혹은 basicCard_keywords가 아닐 경우, 뉴스 사이트에서 해당 발화내용(utterance)로 검색을 진행하게 된다. 

  - 검색 결과가 존재할 경우 -> 발화내용(utterance)를 기반으로 하는 basicCard
  - 검색 결과가 존재하지 않을 경우 -> 바로가기 응답(quickReplies)

3. distrbute 함수는 레디스(redis)에 발화내용(category)이 존재하는지 확인한다.

```python
class Hub:
    category_in_boannews = {"최신 보안 뉴스" : "/media/t_list.asp", "올해 보안 전망": "/search/news_total.asp?search=title&find=2021%B3%E2%BA%B8%BE%C8%C0%FC%B8%C1", "다크웹": "/search/news_total.asp?search=title&find=%B4%D9%C5%A9%C0%A5", "사건사고":"/search/news_total.asp?search=key_word&find=%BB%E7%B0%C7%BB%E7%B0%ED", "취약점 경고 및 버그리포트":"/media/s_list.asp?skind=5", "주간 핫 뉴스":"/media/o_list.asp", "query": "/search/news_total.asp"}
    category_in_dailysecu = {"의료 보안": "/news/articleList.html?sc_serial_code=SRN5&view_type=sm", "해외 보안 뉴스(한글)":"/news/articleList.html?sc_serial_code=SRN4&view_type=sm", "주의 이슈": "/news/articleList.html?sc_serial_code=SRN2&view_type=sm", "query": "/news/articleList.html"}
    category_in_wired = {"해외 보안 뉴스(영어)": "/category/security/"}
    category_in_googlezeroprojects = {"구글제로프로젝트": ""}
    query_site = "보안뉴스"

    crawler = Crawler()
    redis = Redis()

    def distribute(self, category):
        result = self.diverge(category) if not self.redis.get(category) else json.loads(self.redis.get(category))

        if not self.redis.get(category): self.redis.set(category, result)

        return result

    def diverge(self, category):
        result = ""
        if category in self.category_in_boannews:
            result = self.crawler.boannews(self.category_in_boannews[category])
        elif category in self.category_in_dailysecu:
            result = self.crawler.dailysecu(self.category_in_dailysecu[category])
        elif category in self.category_in_wired:
            result = self.crawler.wired(self.category_in_wired[category])
        elif category in self.category_in_googlezeroprojects:
            result = self.crawler.googlezeroprojects(self.category_in_googlezeroprojects[category])
        else:
            if self.query_site == "보안뉴스":
                result = self.crawler.boannews(self.crawler.query_path("보안뉴스", self.category_in_boannews["query"], category))
            elif self.query_site == "데일리시큐":
                result = self.crawler.dailysecu(self.crawler.query_path("데일리시큐", self.category_in_dailysecu["query"], category))
        return result
```

  - 레디스(redis)에 해당 발화내용(category)의 값이 있으면 반환
  
  - 레디스(redis)에 해당 발화내용(category)의 값이 없으면 diverge 함수 호출 후 값 반환 시, 레디스(redis)에 반환 값 저장
  
  (1) diverge 함수는 발화내용(category)를 가지고 다시 분기한다. 어느 뉴스 사이트(보안뉴스, 데일리시큐, wired, 구글제로프로젝트)에서 크롤링해와야하는지를 파악해야하므로 위와 같이 구성했다.
  
  (2) 해당하는 뉴스 사이트가 없는 경우는 발화내용(category)를 가지고 검색을 하는 경우인데, 위에서 query_site를 "보안뉴스"로 정의하였다. 정의된 query_site에서 검색을 진행한다.
  
  4. 발화내용(category)로 "최신 보안 뉴스"를 입력했다고 하면, boannews 함수가 호출되고 해당하는 사이트에 들어가 크롤링을 한 후, 값을 반환한다.
  
  ```python
  class Crawler:
      ...
      def boannews(self, params):
        webpage = requests.get(self.boannews_path(params))
        soup = BeautifulSoup(webpage.text, "html.parser")

        news = soup.select('div.news_list')
        print(self.boannews_path(params))
        result = list()
        for n in news:
            result.append({
                "title": n.select("span.news_txt")[0].text,
                "link": self.boannews_path(n.find("a")['href']),
                "img": self.boannews_path(n.find("img")["src"] if n.find("img") is not None else ""),
                "author": n.select("span.news_writer")[0].text.split(' | ')[0],
                "date": n.select("span.news_writer")[0].text.split(' | ')[1]
            })

        return result
     ...
  ```
  <img src="https://user-images.githubusercontent.com/53392870/108976468-e1e0a780-76ca-11eb-9db3-c2cae8b9f02d.png">
 
 ## 유튜브 영상
 
 
  
