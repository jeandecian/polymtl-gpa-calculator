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

def is_course_acquired(grade):
    try:
        return 0 if (grade == 'P') else 1
    except:
        print(grade + ' doesn\'t exist. Please verify the entry or contact the developer.')
        return 0

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
df['Credit Acquired'] = df['Credit'] * df['Grade'].apply(is_course_acquired)
df['Value'] = df['Grade'].map(grade_values)
df['Grade Points'] = df['Credit'] * df['Value']

df = df[['Trimester', 'Code', 'Title', 'Credit', 'Credit Acquired', 'Grade', 'Value', 'Grade Points']]

print(df.sort_values(by = ['Grade Points'], ascending = False))

sum_credit = df['Credit'].sum()
sum_credit_acquired = df['Credit Acquired'].sum()
sum_grade_points = df['Grade Points'].sum()
gpa = round(sum_grade_points / sum_credit_acquired, 2)
summary = {'Credits': [sum_credit], 'Credits Acquired': [sum_credit_acquired], 'Grade Points':  [sum_grade_points], 'GPA': [gpa]}

print(pd.DataFrame(data = summary))

retake = df[['Code', 'Credit', 'Grade']].copy()
grades = pd.DataFrame({'Expected': list(grade_values.keys())})

retake['key'] = 0
grades['key'] = 0

retake = retake.merge(grades, how = 'left', on = 'key')
retake.drop('key', 1, inplace = True)
retake['Difference GPA'] = round(retake['Credit'] * (retake['Expected'].map(grade_values) - retake['Grade'].map(grade_values)) / sum_credit_acquired, 2)
retake['New GPA'] = gpa + retake['Difference GPA']

excluded_courses = ['INF1995', 'INF3005', 'INF3005A', 'INF3005I', 'INF3995', 'LOG2990', 'INF3995']
retake = retake[(retake['Difference GPA'] > 0) & ~retake['Code'].isin(excluded_courses) & ~retake['Expected'].isin(['A*'])]

print(retake.sort_values(by = ['New GPA'], ascending = False).head(15))

retake_one = retake.copy()
retake_one.drop('New GPA', 1, inplace = True)
retake_one = retake_one.rename(columns={'Code': 'Code 1', 'Credit': 'Credit 1', 'Grade': 'Grade 1', 'Expected': 'Expected 1', 'Difference GPA': 'Difference GPA 1'})

retake_two = retake.copy()
retake_two.drop('New GPA', 1, inplace = True)
retake_two = retake_two.rename(columns={'Code': 'Code 2', 'Credit': 'Credit 2', 'Grade': 'Grade 2', 'Expected': 'Expected 2', 'Difference GPA': 'Difference GPA 2'})

retake_one['key'] = 0
retake_two['key'] = 0

retake_new = retake_one.merge(retake_two, how = 'left', on = 'key')
retake_new = retake_new[retake_new['Code 1'] < retake_new['Code 2']]
retake_new['New GPA'] = gpa + retake_new['Difference GPA 1'] + retake_new['Difference GPA 2']

print(retake_new.sort_values(by = ['New GPA'], ascending = False).head(15))

for grade in grade_values:
    if grade not in ('P'):
        expected_gpa = round((sum_grade_points + (120 - sum_credit) * grade_values[grade]) / (120 - (sum_credit - sum_credit_acquired)), 2)
        gpa_comparison = "+" if expected_gpa > gpa else "-"
        print("GPA if only " + grade + " : " + str(expected_gpa) + " (" + gpa_comparison + ")")