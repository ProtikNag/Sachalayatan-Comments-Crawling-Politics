import csv


def create_csv(ret):
    with open(r'Comments.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(ret)
