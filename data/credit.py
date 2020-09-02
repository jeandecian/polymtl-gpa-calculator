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

courses = {}

for course in list(open("courses_credit.txt", "r")):
    course_arr = course.split(" ", 2)
    courses[course_arr[0]] = {
        'title': course_arr[2].rstrip(),
        'credit': int(course_arr[1].rstrip())
    }

for course in list(open("courses.txt", "r")):
    course_arr = course.split(" ", 1)
    code = course_arr[0]
    if code not in courses:
        courses[code] = {
            'title': course_arr[1].rstrip(),
            'credit': int(get_credits(code).rstrip())
        }
        print(course_arr)

with open("courses_credit.txt", "w") as courses_credit_file:
    for code in sorted(courses):
        course = courses[code]
        courses_credit_file.write(code + " " + str(course['credit']) + " " + course['title'] + "\n")