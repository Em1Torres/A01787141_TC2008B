import numpy
x =  ["scissors","rock","paper","paper",
"rock","scissors","rock","paper","paper"];
x.append("scissors")

def gamerule(a,b):
    if a == b:
         return 0; # draw no one is winning
    if a == "rock":
        match b:
            case "scissors":
                return 1
            case "paper":
                return -1
    if a == "scissors":
        match b:
            case "paper":
                return 1
            case "rock":
                return -1
    if a == "paper":
        match b:
            case "rock":
                return 1
            case "scissors":
                return -1


for i in range(len(x)):
    a = input("Enter my turn: ")
    if i % 2 == 0:
        b = numpy.random.choice(x,1)[0]
    else:
        b = x[i]
    result=gamerule(a,b)
    print("My turn: %s \t Agent's: %s" %(a,b))
    print(result)
