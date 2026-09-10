def NameOfStudent():
    print("Enter the name of student:")
    Name = input()
    return Name


def StudentScore():
    print("Enter the score:")
    score = int(input())

    if score < 0:
        print("Please enter a valid number.")
        grade = "Invalid"
    elif score >= 50:
        grade = "Pass"
    else:
        grade = "Fail"

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