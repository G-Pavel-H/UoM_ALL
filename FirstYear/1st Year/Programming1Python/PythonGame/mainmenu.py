def load_game():
    load_file = open("save.txt", "r")
    load_line = load_file.readline()
    username = load_line.split(":")[0]
    score = load_line.split(":")[1]
    user = {
    "username" : username,
    "score" : score
    }
    load_content = load_file.read().replace("[",'').replace("]",'').replace("\n",'').split(",")
    print(load_content)
    print(len(load_content))


    load_file.close()
load_game()
