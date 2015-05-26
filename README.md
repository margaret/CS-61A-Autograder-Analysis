# CS-61A-Autograder-Analysis
Exploratory analysis of autograder logs (for project 1 in Spring 2015)

CS 61A students test their projects using the autograder program ok, which was written by the 61A staff and is hosted at https://github.com/Cal-CS-61A-Staff/ok-client. The autograder has different features, which can be called with various arguments (for example, students must first unlock tests before being able to run them, so there is an unlock mode). We examing the results of the grading protocol, which tells which problems were submitted for grading, and how many tests for those problems were unlocked, passed, and failed. Here is the data-munging code.

Scripts assume you are in a directory containing

/hog
    /<id>
        backups.pkl
    /<id>
        backups.pkl
    ...

Must use Python 3 because logs were pickled in Python 3.
