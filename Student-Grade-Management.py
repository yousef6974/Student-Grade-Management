def NameOfStudent():
    print("Enter the name of student:")
    Name = input()
    return Name


def StudentScore():
    print("Enter the score:")
    score = int(input())

    if  score < 0 or score > 100:
        print("Please enter a valid number between 0 and 100.")
        grade = "Invalid"
    elif 0 == score < 50 :
        grade = "F"
    elif 50 <= score < 60:
        grade = "D"
    elif 60 <= score < 70:
        grade = "C"
    elif 70 <= score < 80:
        grade = "C+"
    elif 80 <= score < 85:
        grade = "B"
    elif 85 <= score < 90:
        grade = "B+"
    elif 90 <= score < 95:
        grade = "A"
    elif 95 <= score <= 100:
        grade = "A+"
        
    return score, grade


def Result(Name, score, grade):
    print(f"{Name} {score} {grade}")
    return grade


while True:

    Name = NameOfStudent()

    score, grade = StudentScore()

    Result(Name, score, grade)

    choice = input("Do you want to enter another student? (Y/N): ")

    if choice.upper() != "Y":
        break
