import random
random.seed(0xDEADBEEF)
def get_user_agent():
    with open("user_agents","r") as f:
        return f.read().split("\n")[random.randint(0,7137)]
