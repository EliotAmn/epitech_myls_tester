import os

# Dossier pour effectuer les tests
TEST_DIR = os.path.expanduser("~")

# Profondeur maximale de recherche de sous-dossiers. Plus il est grand, plus le test sera long mais plus il sera complet
MAX_DEPTH = 2

# Arguments à tester (pour en tester plusieurs en une commande, mettre les deux arguments dans un seul élément)
TEST_ARGS = [""]

# Chemin vers le binaire officiel à comparer avec le votre
OFFICIAL_BIN = "/usr/bin/ls"

# Chemin vers votre binaire (sortie de compilation)
STUDENT_BIN = "/usr/bin/ls"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_command_output(cmd):
    try:
        command = os.popen(cmd)
        command_output = command.read()
        command.close()
        return command_output
    except:
        exit(0)
def test_folder(folder_path, student_bin, command_args):
    official_test = get_command_output(OFFICIAL_BIN + " " + command_args + " " + folder_path)
    student_test = get_command_output(student_bin + " " + command_args + " " + folder_path)

    if official_test == student_test:
        return {
            "result": True,
            "command": student_bin + " " + command_args + " " + folder_path,
        }
    else:
        return {
            "result": False,
            "got": student_test.replace("\n", "$\n"),
            "expected": official_test.replace("\n", "$\n"),
            "command": student_bin + " " + command_args + " " + folder_path,
        }


def get_subfolders_rec(folder_path, limit=10):
    subfolders = []
    for subfolder in os.listdir(folder_path):
        subfolder = subfolder.replace(" ", "\\ ")
        if os.path.isdir(os.path.join(folder_path, subfolder)):
            subfolders.append(os.path.join(folder_path, subfolder))
            if limit > 0:
                subfolders += get_subfolders_rec(os.path.join(folder_path, subfolder), limit - 1)
    print(subfolders)
    return subfolders

folders_to_test = get_subfolders_rec(TEST_DIR, MAX_DEPTH)

total_tests = 0
total_passed = 0
max_tests = len(folders_to_test) * len(TEST_ARGS)

for folder in folders_to_test:
    for arg in TEST_ARGS:
        test_result = test_folder(folder, STUDENT_BIN, arg)
        total_tests += 1
        command = test_result["command"]
        if test_result["result"] == True:
            print(f"[{total_tests} / {max_tests}] [{bcolors.OKGREEN}PASSED{bcolors.ENDC}] {command}")
            total_passed += 1
        else:
            print(f"[{bcolors.FAIL}FAILED{bcolors.ENDC}]{command}")
            print(f"{bcolors.FAIL}===== Got =====\n{test_result['got']}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}====== Expected ======\n{test_result['expected']}{bcolors.ENDC}")
            print(f"{bcolors.FAIL}======================={bcolors.ENDC}")
print(f"Total tests: {bcolors.OKCYAN}{total_tests}{bcolors.ENDC}, Passed: {bcolors.OKGREEN}{total_passed}{bcolors.ENDC}, Failed: {bcolors.FAIL}{bcolors.BOLD}{total_tests - total_passed}{bcolors.ENDC}")
print(f"> Score : {bcolors.OKCYAN}" + str((total_passed / total_tests) * 100) + "%")