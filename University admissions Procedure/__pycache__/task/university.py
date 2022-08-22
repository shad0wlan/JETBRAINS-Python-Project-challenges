# write your code here
import numpy as np
from copy import deepcopy
from collections import defaultdict
total_number_applicants = int(input())

file = './test/applicants.txt'

applicants = []  # This will hold all applicants with all values from the file
lesson_names = ["Engineering", "Biotech", "Chemistry", "Physics", "Mathematics"]
with open(file) as f:
    for line in f:
        full_names = " ".join(line.strip().split()[0:2])
        remains = line.strip().split()[2:]
        remains.insert(0, full_names)
        final_line = remains
        applicants.append(final_line)

applicants_main_info = np.array(applicants)  # Constructing a numpy array to do the sorting stuff

applicant_names = list(applicants_main_info[:, 0])  # Getting only the fullnames

dept_results = defaultdict(list)  # dict to hold succeeded candidates for each lesson
lesson_results = defaultdict(list)

#  Function to construct the above dictionary and sort each value. The capacity is the maximum capacity of each lesson


def grade_sort(app_names, arr, capacity, column=6):
    arr_to_sort = []
    column_grade_index = None
    extra_index = None
    rows_to_remove = []
    students = deepcopy(app_names)
    applicants_info = deepcopy(arr)

    if column == 9:
        return True
    if len(students) == 0:
        return True

    for j in applicants_info[:, :]:
        if "Physics" == j[column]:
            column_grade_index = 1
            extra_index = 3
        if "Chemistry" == j[column]:
            column_grade_index = 2
            extra_index = 2
        if "Mathematics" == j[column]:
            column_grade_index = 3
            extra_index = 3
        if "Biotech" == j[column]:
            column_grade_index = 2
            extra_index = 1
        if "Engineering" == j[column]:
            column_grade_index = 4
            extra_index = 3
        if j[0] in students:
            if float(j[5]) > (int(j[column_grade_index]) + int(j[extra_index])) / 2:
                arr_to_sort.append([j[0], float(j[5]), j[column]])
            else:
                arr_to_sort.append([j[0], (int(j[column_grade_index]) + int(j[extra_index])) / 2, j[column]])

            # arr_to_sort.append([j[0],float(j[column_grade_index]),j[column]])
    for i in sorted(arr_to_sort, key=lambda x: (-x[1], x[0])):
        if len(lesson_results[i[2]]) < capacity:
            lesson_results[i[2]] += [[i[0], i[1]]]
            students.remove(i[0])
            rows_to_remove.append(i)
        else:
            continue
    for i in lesson_results:
        lesson_results[i].sort(key= lambda x: (-x[1], x[0]))

    if len(students) > 0:
        rows_to_remove.clear()
        grade_sort(students, applicants_info, capacity, column + 1)


def gpa_sort(app_names, arr, capacity, column=2):
    rows_to_remove = []
    students = deepcopy(app_names)
    applicants_info = deepcopy(arr)

    if column == 5:
        return True
    if len(students) == 0:
        return True

    for i in sorted(lesson_names):
        # Getting lesson based values per column of priorities, 2nd column is 1st priority, 3rd second. etc.
        lesson = applicants_info[applicants_info[:, column] == i, :]

        # Sorting all the values per GPA(float) first and if GPAS are same we do Full name sorting
        arr_to_sort = lesson[np.lexsort((lesson[:, 0], -lesson[:, 1].astype(dtype=float)))]
        if arr_to_sort[:capacity, [0, 1, column]].size > 0:  # Making sure it's not empty to avoid empty arrays
            if len(dept_results[i]) == capacity:  # Making sure that we avoid appending to already filled lesson
                continue
            else:
                dept_results[i] += list(arr_to_sort[:capacity, [0, 1]])  # Appending full name and GPA

                # Reconstructing to sort again new values because we might have appended higher GPAs
                dept_results[i] = np.array(dept_results[i])
                dept_results[i] = dept_results[i][np.lexsort((dept_results[i][:, 0], -dept_results[i][:, 1].astype(dtype=float)))]

                #  Converting to list again, so we can append again with +=
                dept_results[i] = list(dept_results[i][:capacity])
        try:
            for student in arr_to_sort[:capacity, 0]:
                students.remove(student)  # We remove all the students that we registered in lesson
        except ValueError:
            continue
        x = np.where((applicants_info == arr_to_sort[:capacity, None]).all(-1))[1]  # We get all the index of rows that we used
        rows_to_remove += list(x)

    rows_to_remove.sort()
    applicants_info = np.delete(applicants_info, rows_to_remove, axis=0)  # We remove all the rows that we used

    #  Recursion till we reach the capacity of each class
    if len(students) > 0:
        rows_to_remove.clear()
        gpa_sort(students, applicants_info, capacity, column + 1)



def results_printer(**departments):
    values = []
    for i, j in sorted(departments.items()):
        values.append(i + '\n' + '\n'.join(map(str, j)).replace(" [", "").replace("[", "").replace("'","")
                      .replace("]", '').replace(",","") + '\n')
        with open(i + ".txt", 'w+') as f:
            f.write('\n'.join(map(str, j)).replace(" [", "").replace("[", "").replace("'","")
                      .replace("]", '').replace(",","") + '\n')
    return "\n".join(map(str, values))


grade_sort(applicant_names, applicants_main_info, total_number_applicants)
print(results_printer(**lesson_results))

