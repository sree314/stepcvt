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
    print(f"{'Passed' if success else 'Failed'}: {test_name}\nOutput:\n{output}\n")


# defining the tests
tests = {
    "Project Test 1": "stepcvt -j json.js make",  # making the project
    "Project Test 2": "stepcvt -j json.js name test",  # renaming the project from 'stepcvt' to 'test'
    "Project Test 3": "stepcvt -j json.js display",  # show the projects contents so far
    "source test": "stepcvt -j json.js add Stealthburner_Printhead_V6.stp",  # adding the source
    "part test": "stepcvt -j json.js addpart --all",  # adding the parts
    "stl test": "stepcvt -j json.js stlcvt partID --rotation --linearTolerance --angularTolerance",  # adding angular/linear tolerances
    "export test": "stepcvt -j json.js exportstl path",  # exporting the stls
}

# Get test name from command line argument
test_name = sys.argv[1] if len(sys.argv) > 1 else None

# run something like: python cli_test.py "project test" if you only want to look at project test
if test_name:
    if test_name in tests:
        test_command(tests[test_name], test_name)
    else:
        print(f"Test '{test_name}' not found.")
else:
    for name, command in tests.items():
        test_command(command, name)
