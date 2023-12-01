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
    "Project Test 1": "python ./scripts/stepcvt -j json.js make",  # making the project
    "Project Test 2": "python ./scripts/stepcvt -j json.js name test",  # renaming the project from 'stepcvt' to 'test'
    "Project Test 3": "python ./scripts/stepcvt -j json.js display",  # show the projects contents so far
    "source test": "python ./scripts/stepcvt -j json.js addstep scripts\Stealthburner_Printhead_V6.stp",  # adding the source
    "source list": "python ./scripts/stepcvt -j json.js liststep scripts\Stealthburner_Printhead_V6.stp",  # lising step parts
    "part test": "python ./scripts/stepcvt -j json.js addpart --all",  # adding the parts
    "stl test": "python ./scripts/stepcvt -j json.js stlcvt partID --rotation --linearTolerance --angularTolerance",  # adding angular/linear tolerances
    "export test": "python ./scripts/stepcvt -j json.js exportstl path",  # exporting the stls
    "choices add test": "python ./scripts/stepcvt -j json.js choices add-chooser --choice-type single 'Printer Options' 'options' "
    "--values 'HEPA filter':'Filter' 'Build area lights':'Lights':'version=='V6''",  # Add a single chooser
    "choices edit test": "python ./scripts/stepcvt choices edit 'options' --choice-value 'Lights' "
    "'Build area lights':'Lights':'version==''V4''",  # rename one of the choice value
    "choices remove test": "python ./scripts/stepcvt choices remove 'options' --choice-value 'Lights' --cond",  # remove one option value
    "choices apply test": "python ./scripts/stepcvt choices apply Version=v6 Options=Lights,Filter",  # apply a user choice
}

all_tests_passed = True

for name, command in tests.items():
    test_passed = test_command(command, name)
    if not test_passed:
        all_tests_passed = False

if not all_tests_passed:
    sys.exit(1)  # Exit with a non-zero status code if any test failed
