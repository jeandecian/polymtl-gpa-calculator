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

retake = df[['Code', 'Credit', 'Grade']].copy()
grades = pd.DataFrame({'Expected': list(grade_values.keys())})

retake['key'] = 0
grades['key'] = 0

retake = retake.merge(grades, how = 'left', on = 'key')
retake.drop('key', 1, inplace = True)
retake['Difference GPA'] = round(retake['Credit'] * (retake['Expected'].map(grade_values) - retake['Grade'].map(grade_values)) / sum_credit, 2)
retake['New GPA'] = gpa + retake['Difference GPA']

excluded_courses = ['INF1995', 'INF3005', 'INF3005A', 'INF3005I', 'INF3995', 'LOG2990']
retake_mask = (retake['Difference GPA'] > 0) & ~retake['Code'].isin(excluded_courses) & ~retake['Expected'].isin(['A*'])

print(retake[retake_mask].sort_values(by = ['New GPA'], ascending = False).to_string())