from human_cupid.cupid import Cupid
from human_cupid.sub import SubprofileAnalyzer
from human_cupid.super import SuperprofileAnalyzer

Alex_Mom = [
    {"sender": "alex", "content": "hey mom, just wanted to check in"},
    {"sender": "mom", "content": "Hi honey! How are you feeling today?"},
    {"sender": "alex", "content": "honestly pretty stressed about work stuff"},
    {"sender": "mom", "content": "What's going on? You can tell me"},
    {"sender": "alex", "content": "my manager keeps piling on coding projects and I don't want to disappoint anyone"},
    {"sender": "mom", "content": "You're such a hard worker, but don't forget to take care of yourself"},
    {"sender": "alex", "content": "I know, I know. just want to make you proud"},
    {"sender": "mom", "content": "I'm already proud of you! Always remember that"},
    {"sender": "alex", "content": "thanks mom ❤️ that helps"},
    # {"sender": "mom", "content": "Have you been eating enough? And sleeping?"},
    # {"sender": "alex", "content": "um... define enough? 😅"},
    # {"sender": "mom", "content": "Alex! You need to take better care of yourself"},
    # {"sender": "alex", "content": "okay okay I'll try to do better. promise"},
    # {"sender": "mom", "content": "Good. I worry about you working so hard"},
    # {"sender": "alex", "content": "I appreciate you caring so much"},
    # {"sender": "mom", "content": "That's what mothers are for"},
    # {"sender": "alex", "content": "speaking of which, how's dad doing?"},
    # {"sender": "mom", "content": "He's good! Still complaining about his back though"},
    # {"sender": "alex", "content": "tell him to actually do the physical therapy exercises lol"},
    # {"sender": "mom", "content": "I've been trying! He's as stubborn as you"},
    # {"sender": "alex", "content": "hey! I'm not stubborn, I'm... persistent 😏"},
    # {"sender": "mom", "content": "Uh huh, sure honey"},
    # {"sender": "alex", "content": "anyway I should probably get back to work"},
    # {"sender": "mom", "content": "Okay, but remember what we talked about - take breaks!"},
    # {"sender": "alex", "content": "will do. love you mom"},
    # {"sender": "mom", "content": "Love you too sweetie. Talk soon!"}
]

Amanda_Jane = [
    {"sender": "amanda", "content": "hey Jane, did you finish the reading for econ?"},
    {"sender": "jane", "content": "lol not even close, that chapter is brutal"},
    {"sender": "amanda", "content": "right?? I read the first 10 pages and my brain shut down"},
    {"sender": "jane", "content": "at least the prof said the quiz will be open notes"},
    {"sender": "amanda", "content": "true but my notes are basically just doodles at this point 😅"},
    {"sender": "jane", "content": "haha same. want to study together tomorrow?"},
    {"sender": "amanda", "content": "yes please, I retain stuff way better when we talk it out"},
    {"sender": "jane", "content": "cool, library at 3?"},
    {"sender": "amanda", "content": "works for me. also did you see the group project email?"},
    {"sender": "jane", "content": "ugh don't remind me..."},
    {"sender": "amanda", "content": "lol same, but at least we got paired with Emma, she actually does work"},
    {"sender": "jane", "content": "bless Emma 🙌"},
    {"sender": "amanda", "content": "ok so library tomorrow and we’ll make a game plan"},
    {"sender": "jane", "content": "deal. bring caffeine"}
]

def main():
    pass
    # with open("amanda_jane_subprofile.md", "r") as f:
    #     alex_mom_profile = f.read()
    #     # a = SubprofileAnalyzer("alex", Alex_Mom, alex_mom_profile).run()

    #     sp = SuperprofileAnalyzer("amanda", [alex_mom_profile]).run()
        
    #     if sp:
    #         with open("amanda.md", "w") as f:
    #             f.write(sp)

    # file1_path = "alex.md"
    # file2_path = "amanda.md"

    # with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
    #     content1 = file1.read()
    #     content2 = file2.read()

    #     b = Cupid([content1, content2], ["alex", "amanda"]).run()

    #     print(b)