quickReplies_keywords = ['보안', '안내', '키워드']
basicCard_keywords = ["보안뉴스", "데일리시큐", "와이어드", "구글제로프로젝트", "주의 이슈", "다크웹", "사건사고", "취약점 경고 및 버그리포트", "주간 핫 뉴스", "올해 보안 전망", "의료 보안", "해외 보안 뉴스", ]

def dateFormat(date):
    date_str, time = date.split()
    year, mon, day = date_str.split("-")

    return year + "년 "+ mon + "월 " + day + "일 " + time