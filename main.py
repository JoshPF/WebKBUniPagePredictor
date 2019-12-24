import sys
import os
import nltk
from construct_dataset import calculate_freq_dist, find_keywords, calculate_weights
from os.path import dirname

def usage():
    print("Usage: python main.py <Number of Keywords> <University to Predict pages for>")
    print("       Number of Keywords must be a valid integer that is greater than 0.")
    print("       University Options: \"cornell\", \"texas\", \"washington\", \"wisconsin\" or leave blank for Miscellaneous")
    exit(1)

simple_pred = False
num_keywords = 0
valid_univs = ['cornell', 'misc', 'texas', 'washington', 'wisconsin']

# Read in Command Line arguments
try:
    if len(sys.argv) < 2:
        usage()
    elif len(sys.argv) == 2:
        num_keywords = int(sys.argv[1])
        pred_univ = 'misc'
    elif len(sys.argv) == 3:
        num_keywords = int(sys.argv[1])
        pred_univ = sys.argv[2].lower()
    else:
        usage()

    if (num_keywords <= 0) or (pred_univ not in valid_univs):
        usage()

except Exception as e:
    print(str(e))
    usage()

# Find keywords and their weights
course_keywords, course_weights = calculate_freq_dist('webkb/course/', pred_univ, num_keywords)
department_keywords, department_weights = calculate_freq_dist('webkb/department/', pred_univ, num_keywords)
faculty_keywords, faculty_weights = calculate_freq_dist('webkb/faculty/', pred_univ, num_keywords)
other_keywords, other_weights = calculate_freq_dist('webkb/other/', pred_univ, num_keywords)
project_keywords, project_weights = calculate_freq_dist('webkb/project/', pred_univ, num_keywords)
staff_keywords, staff_weights = calculate_freq_dist('webkb/staff/', pred_univ, num_keywords)
student_keywords, student_weights = calculate_freq_dist('webkb/student/', pred_univ, num_keywords)

def get_highest_val_from_dict(d):
    highest_val = 0
    highest_key = None
    for (key, value) in d.items():
        if value > highest_val:
            highest_val = value
            highest_key = key
    return highest_key

def predict(testing_weights):
    categories = {'course': 0, 'department': 0, 'faculty': 0, 'other': 0, 'project': 0, 'staff': 0, 'student': 0}

    for tup in testing_weights:
        word = tup[0].lower()
        freq = tup[1]
        for cmp_tup in course_weights:
            if word == cmp_tup[0].lower():
                categories['course'] += (freq + cmp_tup[1])
                break
        for cmp_tup in department_weights:
            if word == cmp_tup[0].lower():
                categories['department'] += (freq + cmp_tup[1])
                break
        for cmp_tup in faculty_weights:
            if word == cmp_tup[0].lower():
                categories['faculty'] += (freq + cmp_tup[1])
                break
        for cmp_tup in other_weights:
            if word == cmp_tup[0].lower():
                categories['other'] += (freq + cmp_tup[1])
                break
        for cmp_tup in project_weights:
            if word == cmp_tup[0].lower():
                categories['project'] += (freq + cmp_tup[1])
                break
        for cmp_tup in staff_weights:
            if word == cmp_tup[0].lower():
                categories['staff'] += (freq + cmp_tup[1])
                break
        for cmp_tup in student_weights:
            if word == cmp_tup[0].lower():
                categories['student'] += (freq + cmp_tup[1])
                break

    return get_highest_val_from_dict(categories)
 
# Begin Predictions
correct_count = total_count = 0
category_accuracies = {'course': 0, 'department': 0, 'faculty': 0, 'other': 0, 'project': 0, 'staff': 0, 'student': 0}
other_correct = other_total = 0
for category in os.listdir('webkb'):
    actual = category
    file_path = 'webkb/' + category + '/' + pred_univ
    category_correct_count = category_total_count = 0
    for filename in os.listdir(file_path):
        category_total_count += 1
        total_count += 1
        full_path = file_path + '/' + filename
        testing_keywords = find_keywords(full_path)
        predicted = None
        freq_dist = nltk.FreqDist(testing_keywords)
        freq_dist = freq_dist.most_common(int(num_keywords))
        freq_dist = calculate_weights(freq_dist)
        predicted = predict(freq_dist)
        print('%s:\n    Predicted: %s; Actual: %s' % (full_path, predicted, actual))
        if predicted == actual:
            correct_count += 1
            category_correct_count += 1
            
    category_accuracies[category] = category_correct_count / category_total_count

    if category == 'other':
        other_correct = category_correct_count
        other_total = category_total_count

print('\n\nProgram Accuracy\n==========================')
for category in category_accuracies:
    print('%s Accuracy: %.3f' % (category, category_accuracies[category]))

print('--------------------------\nTotal Accuracy: %.3f' % ( (correct_count - other_correct) / (total_count - other_total) ))
print('Total Accuracy (Including Other Category): %.3f' % (float(correct_count) / float(total_count)))