from buggyController import BuggyController

bc = BuggyController()

bc.magnetoSetup()

while True:
    print(bc.get_current_direction())