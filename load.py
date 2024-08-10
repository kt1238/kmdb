# Load data from .csv file into sqlite db
# This is just for testing in future version will make use of mysql server
# 
# !=========================================IMPORTANT==============================================!
# Run this from django shell when loading movies from csv
import csv
from demo.models import Movie

def loadcsvfile():
    with open(file='C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movies.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        reader.__next__() # Skips over header
        for row in reader:
            if row[2] == '':
                row[2] = None
            Movie.objects.update_or_create(
                name = row[1],
                release_year = row[2],
                language = row[3],
                genre_1 = row[4],
                watched = row[5],
                priority = row[6],
                extra_info = row[7]
            )