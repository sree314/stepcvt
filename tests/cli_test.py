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
    "project": "stepcvt -j json.js make test",  # making the project
    "source": "stepcvt -j json.js add Stealthburner_Printhead_V6.stp",  # adding the source
    "part": "stepcvt -j json.js addpart --all",  # adding the parts
    "stl": "stepcvt -j json.js stlcvt partID --rotation --linearTolerance --angularTolerance",  # adding angular/linear tolerances
    "export": "stepcvt -j json.js exportstl path",  # exporting the stls
}

# Get test name from command line argument
test_name = sys.argv[1] if len(sys.argv) > 1 else None

# run something like: python cli_test.py project if you only want to look at project test
if test_name:
    if test_name in tests:
        test_command(tests[test_name], test_name)
    else:
        print(f"Test '{test_name}' not found.")
else:
    for name, command in tests.items():
        test_command(command, name)
