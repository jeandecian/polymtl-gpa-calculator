import pandas as pd

def get_course_title(course_code):
    try:
        return courses.get(course_code).get('title')
    except:
        print(course_code + ' doesn\'t exist. Please verify the entry or contact the developer.')
        return 'TITLE NOT FOUND ERROR'

def get_course_credit(course_code):
    try:
        return courses.get(course_code).get('credit')
    except:
        print(course_code + ' doesn\'t exist. Please verify the entry or contact the developer.')
        return 9999

courses = {}

for course in list(open("data/courses_credit.txt", "r")):
    course_arr = course.split(" ", 2)
    courses[course_arr[0]] = {
        'title': course_arr[2].rstrip(),
        'credit': int(course_arr[1].rstrip())
    }

grade_values = {}

for grade in list(open("data/grade_values.txt", "r")):
    grade_arr = grade.split(" ")
    grade_values[grade_arr[0]] = float(grade_arr[1].rstrip())

df = pd.read_csv('grade_report.csv')

df['Title'] = df['Code'].apply(get_course_title)
df['Credit'] = df['Code'].apply(get_course_credit)
df['Value'] = df['Grade'].map(grade_values)
df['Grade Points'] = df['Credit'] * df['Value']

df = df[['Trimester', 'Code', 'Title', 'Credit', 'Grade', 'Value', 'Grade Points']]

print(df.sort_values(by = ['Grade Points'], ascending = False))

sum_credit = df['Credit'].sum()
sum_grade_points = df['Grade Points'].sum()
gpa = round(sum_grade_points / sum_credit, 2)
summary = {'Credits': [sum_credit], 'Grade Points':  [sum_grade_points], 'GPA': [gpa]}

print(pd.DataFrame(data = summary))