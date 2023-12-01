import ast
from functools import reduce
from typing import Dict


class UserChoices:
    """Records a user's choices as a key--value store, where the keys
    are choice variables and value represents the current value of the variable.

    A value may be an single scalar value, or a set of values.


    Examples:
     NevermoreModel = "V6"

     PowerConnector = "2JST"

     PrinterOptions = {"Filter", "Lights"}

    """

    def __init__(self, key_vals: dict):
        self.choices = key_vals


class ChoiceExpr:
    """A logical expression involving a choice variable that evaluates to true or false.

    Example:
      NevermoreModel == "V4" (note the ==)
    """

    ## The syntax for the expression could be a Python expression,
    ## which could then be evaluated using literal_eval or something
    ## like that.

    def __init__(self, expr):
        self.expr = expr

    @staticmethod
    def extract_ast_vars(node: ast.AST) -> [str]:
        """Recursively finds all variables in the given AST
        Currently only supports boolean expressions
        """
        if isinstance(node, ast.Expression):
            return ChoiceExpr.extract_ast_vars(node.body)
        elif isinstance(node, ast.BoolOp):
            return reduce(
                lambda l1, l2: l1 + l2,
                map(ChoiceExpr.extract_ast_vars, node.values),
                [],
            )
        elif isinstance(node, ast.Compare):
            return ChoiceExpr.extract_ast_vars(node.left) + reduce(
                lambda l1, l2: l1 + l2,
                map(ChoiceExpr.extract_ast_vars, node.comparators),
                [],
            )
        elif isinstance(node, ast.Name):
            return [node.id]
        elif isinstance(node, ast.Constant):
            return []
        else:
            raise AttributeError("unexpected ast construct " + node)

    @staticmethod
    def sanitize_ast(node: ast.AST):
        """AST must only contains expressions,
        raise error on potentially unsafe statement and lambda expr"""
        # Only allows explicit expression construct
        # https://docs.python.org/3/library/ast.html#expressions
        if isinstance(node, ast.Expression):
            ChoiceExpr.sanitize_ast(node.body)
        elif isinstance(node, ast.BoolOp):
            map(ChoiceExpr.sanitize_ast, node.values)
        elif isinstance(node, ast.Compare):
            ChoiceExpr.sanitize_ast(node.left)
            map(ChoiceExpr.sanitize_ast, node.comparators)
        elif isinstance(node, ast.UnaryOp):
            ChoiceExpr.sanitize_ast(node.operand)
        elif isinstance(node, ast.BinOp):
            ChoiceExpr.sanitize_ast(node.left)
            ChoiceExpr.sanitize_ast(node.right)
        elif isinstance(node, ast.IfExp):
            ChoiceEffect.sanitize_ast(node.test)
            ChoiceEffect.sanitize_ast(node.body)
            ChoiceEffect.sanitize_ast(node.orelse)
        elif type(node) in {ast.Name, ast.Constant}:
            return
        else:
            raise AttributeError(f"Unsupported expression type: {node}")

    def eval(self, user_choices: UserChoices):
        # sanitize expression string
        ChoiceExpr.sanitize_ast(ast.parse(self.expr, mode="eval"))
        # extract dict items into assignment
        # as scope context for evaluating expr
        scope = "(lambda "
        print(user_choices.choices)
        for key, value in user_choices.choices.items():
            if isinstance(value, str):
                value = f"'{value}'"
            scope += f"{key} = {value}, "
        scope = scope[0:-2] + f": {self.expr})()"
        return eval(scope)  # WARNING: huge security risk

    def vars(self):
        """Returns the variables in the expression"""
        return ChoiceExpr.extract_ast_vars(ast.parse(self.expr, mode="eval"))


class ChoiceEffect:
    """The base class for the effect on a part that is choice-dependent.

    Each subclass of this class is attached to a PartInfo"""

    def __init__(self, cond: ChoiceExpr, *args, **kwargs):
        self.cond = cond


class SelectionEffect(ChoiceEffect):
    """Represents a yes/no choice for a part. If the condition evaluates
    to False, then the part is not selected

    """

    pass


class RelativeCountEffect(ChoiceEffect):
    """Changes the count for a part depending on a choice. This models an
    additive or subractive count.

    """

    def __init__(self, cond: ChoiceExpr, count_delta, *args, **kwargs):
        self.count_delta = count_delta
        super().__init__(cond, *args, **kwargs)


class AbsoluteCountEffect(ChoiceEffect):
    """Changes the count for a part depending on a choice. This models an
    absolute count.

    """

    def __init__(self, cond: ChoiceExpr, count, *args, **kwargs):
        self.count = count
        super().__init__(cond, *args, **kwargs)


class ScaleEffect(ChoiceEffect):
    """Transforms the scale of an object depending on a choice.

    Example: change the length of an STL object based on size of
    the printer.
    """

    def __init__(self, cond: ChoiceExpr, scale, *args, **kwargs):
        self.scale = scale
        super().__init__(cond, *args, **kwargs)


class Chooser:
    """Base class for a choice. This also corresponds to the UI shown for
    a choice"""

    def __init__(self, text: str, varname: str) -> None:
        self.text = text  # human-readable text
        self.varname = varname  # variable name


class ChoiceValue:
    """Represents a value available for a choice."""

    def __init__(self, text: str, value: str, cond: ChoiceExpr = None):
        self.text = text
        self.value = value

        # if this is not None, then it represents a value
        # which is only available if the condition is true.
        self.cond = cond


class SingleChooser(Chooser):
    """Represents a choice where only one value can be selected from a
    list of multiple choices.

    May be rendered as a list or a bunch of radio buttons.

    Example: NevermoreModel \in {V4, V5, V6}
    """

    def __init__(self, text: str, varname: str, values: [ChoiceValue]):
        self.values = values
        super().__init__(text, varname)


class MultiChooser(Chooser):
    """Represents a choice where multiple values can be selected from a
    list of choices.

    Example: PrinterMods \in {"Lights", "Filter", "FridgeDoor"}
    """

    def __init__(self, text: str, varname: str, values: [ChoiceValue]):
        self.values = values
        super().__init__(text, varname)


class BooleanChooser(Chooser):
    """Represents a yes/no choice. Usually rendered as a checkbox"""

    def __init__(
        self,
        text: str,
        varname: str,
        sel_value: ChoiceValue,  # value when selected
        unsel_value: ChoiceValue = None,
    ):  # value when not selected
        self.sel_value = sel_value
        self.unsel_value = unsel_value
        super().__init__(text, varname)


class Choices:
    """A collection of choices available in a project."""

    def __init__(self, choices: [Chooser]):
        self.choices = choices

    def validate(self, user_choices: UserChoices):
        """Test validity of user choices input"""
        avail_choices_dict = self.to_simple_dict()
        valid_user_choices = UserChoices(dict())
        for key, val in user_choices.choices.items():
            # test valid option
            if key not in avail_choices_dict:
                raise AttributeError(f"Unidentified option key '{key}'")
            val_set = set(val) if type(val) is list or type(val) is set else {val}
            if not val_set <= avail_choices_dict[key]:
                raise AttributeError(f"Unidentified options '{val}' in '{key}'")

            # test valid precondition
            valid_user_choices.choices[key] = val
            # get the chooser we just corresponding to the new user choice key val pair
            chooser = next(
                filter(
                    lambda ch, key=key: ch.varname == key,
                    self.choices,
                )
            )
            # get the set of values that appeared in the user choice
            values = (
                {chooser.sel_value, chooser.unsel_value}
                if type(chooser) is BooleanChooser
                else set(chooser.values)
            )
            values = filter(lambda v, val=val: v.value in val, values)
            # test if all preconditions for values in such set are satisfied
            for value in values:
                print(value.value)
                if value.cond is not None and not value.cond.eval(valid_user_choices):
                    raise AttributeError(
                        f"Precondition for '{value.value}' not satisfied"
                    )

    def to_simple_dict(self) -> Dict[str, set]:
        """Serialize simplified available choices as dict,
        list is converted to set for better membership testing"""
        d = dict()
        for chooser in self.toposort():
            d[chooser.varname] = (
                {chooser.sel_value.value, chooser.unsel_value.value}
                if type(chooser) is BooleanChooser
                else set(ch_v.value for ch_v in chooser.values)
            )
        return d

    def to_dict(self) -> [dict]:
        """Differs from to_simple_dict in that this method returns the full serialization"""
        return [c.to_dict() for c in self.choices]

    def toposort(self):
        # returns a topological ordering of choices
        # for choices at the same level, return choices in the order that they
        # were passed in choices

        # each level of choices depends on choices made in the previous levels

        # circular dependencies are prohibited
        # TODO: make this real toposort
        return self.choices
