import subprocess
import sys


def run_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT
        ).decode("utf-8")
        return True, result
    except subprocess.CalledProcessError as e:
        return False, e.output.decode("utf-8")


def test_command(command, test_name):
    success, output = run_command(command)
    if not success:
        print(f"Failed: {test_name}\nOutput:\n{output}\n")
        return False
    else:
        print(f"Passed: {test_name}\nOutput:\n{output}\n")
        return True


# defining the tests
tests = {
    "Project Test 1": "python3 ./scripts/stepcvt -j json.js make",  # making the project
    "Project Test 2": "python3 ./scripts/stepcvt -j json.js newProjName test",  # renaming the project from 'stepcvt' to 'test'
    "Project Test 3": "python3 ./scripts/stepcvt -j json.js display",  # show the projects contents so far
    "source add": "python ./scripts/stepcvt -j json.js addstep stealth_burner_head scripts/Stealthburner_Printhead_V6.stp",  # adding the source
    "source list": "python3 ./scripts/stepcvt -j json.js liststep stealth_burner_head",  # lising step parts
    "source remove": "python3 ./scripts/stepcvt -j json.js rmstep stealth_burner_head",  # removing the source
    "source": "python3 ./scripts/stepcvt -j json.js addstep stealth_burner_head scripts/Stealthburner_Printhead_V6.stp",  # adding the source again
    "source add part": "python3 ./scripts/stepcvt -j json.js addpart stealth_burner_head --all",  # adding all the parts to the first source
    "stl test": "python3 ./scripts/stepcvt -j json.js stlconvert partID --rotation 0 0 0 --linearTolerance 0.1 --angularTolerance 0.1",  # adding angular/linear tolerances
    "export test": "python3 ./scripts/stepcvt -j json.js exportstl path",  # exporting the stls
    "choices add test": "python3 ./scripts/stepcvt -j json.js choices add-chooser --type single 'Printer Options' 'options' "
    "'HEPA filter':'Filter' 'Build area lights':'Lights':'version=='V6''",  # Add a single chooser
    "choices edit test": "python3 ./scripts/stepcvt -j json.js choices edit 'options' --choice-value 'Lights' "
    "'Build area lights':'Lights':'version=='V4''",  # rename one of the choice value
    "choices remove test": "python3 ./scripts/stepcvt -j json.js choices remove 'options' --choice-value 'Lights' --cond",  # remove one option value
    "choices apply test": "python3 ./scripts/stepcvt -j json.js choices apply options=Lights,Filter",  # apply a user choice
}

all_tests_passed = True

for name, command in tests.items():
    test_passed = test_command(command, name)
    if not test_passed:
        all_tests_passed = False

if not all_tests_passed:
    sys.exit(1)  # Exit with a non-zero status code if any test failed
