

def classify_question(question):
    if ("how much" in question):
        question_type = "how much"

    elif ("how many" in question) or \
    ("how large" in question) or \
    ("how big" in question) or \
    ("how tall" in question) or \
    ("how high" in question) or \
    ("how long" in question) or \
    ("how often" in question) or \
    ("how old" in question) or \
    ("how far" in question) or \
    ("how deep" in question):
        question_type = "how numerical"
            
    elif ("when" in question) or \
    ("what time" in question) or \
    ("which time" in question) or \
    ("what year" in question) or \
    ("which year" in question) or \
    ("what month" in question) or \
    ("which month" in question) or \
    ("what day" in question) or \
    ("which day" in question):
        question_type = "when"
        
    elif ("where" in question) or \
    ("what location" in question) or \
    ("which location" in question) or \
    ("what place" in question) or \
    ("which place" in question) or \
    ("what address" in question) or \
    ("which address" in question):
        question_type = "where"

    elif ("what" in question) or ("which" in question):
        question_type = "what"

    elif ("who" in question):
        question_type = "who"

    elif (" how " in question) or (question[0:4] == "how "):
        question_type = "how"
    
    else:
        question_type = "others"

    return question_type

if __name__ == "__main__":


    train_question_filename = "train_question.txt"
    train_questions = open(train_question_filename, 'r',encoding="utf8").readlines()

    test_question_filename = "test_question.txt"
    test_questions = open(test_question_filename, 'r',encoding="utf8").readlines()

    for question in train_questions:
        index = question.split(":")[0].split(" ")[1]
        question = question.strip('\n').split(":")[1].strip().lower()
        
        question_type = classify_question(question)

        print(str(index)+","+str(question)+","+str(question_type))

    for question in test_questions:
        index = int(question.split(":")[0].split(" ")[1]) + 238
        question = question.strip('\n').split(":")[1].strip().lower()
        
        question_type = classify_question(question)

        print(str(index)+","+str(question)+","+str(question_type))