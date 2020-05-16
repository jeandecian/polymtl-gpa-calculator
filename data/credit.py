from urllib.request import Request, urlopen

headers = {'User-Agent': 'Mozilla/5.0'}

def trim_html(html, start, end):
    return html[html.index(start):html.index(end)]

def get_html(url):
    return urlopen(Request(url, headers = headers)).read().decode("utf8")

def get_credits(course_code):
    html = get_html('https://www.polymtl.ca/etudes/cours/recherche/%2A?sigle=' + course_code)

    trim = trim_html(html, '<tbody>', '</table>')
    trim = trim_html(trim, course_code + '<', '</tbody>')
    sub_url = trim_html(trim, 'https', '">')

    sub_html = get_html(sub_url)

    trim = trim_html(sub_html, '<span class="tooltip triplet">', '<span class="tooltiptext">')
    trim = trim_html(trim, '</strong>', ' (')
    credit = trim[-1]

    return credit

with open("courses_credit.txt", "w") as courses_credit_file:
    for course in list(open("courses.txt", "r")):
        course_arr = course.split(" ", 1)
        course_arr.insert(1, get_credits(course_arr[0]))
        print(course_arr)
        courses_credit_file.write(" ".join(course_arr))

    for course in list(open("old_courses.txt", "r")):
        courses_credit_file.write(course)