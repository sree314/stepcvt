class UserChoices:
    """Records a user's choices as a key--value store, where the keys
    are choice variables and value represents the current value of the variable.

    A value may be an single scalar value, or a set of values.


    Examples:
     NevermoreModel = "V6"

     PowerConnector = "2JST"

     PrinterOptions = {"Filter", "Lights"}

    """

    pass


class ChoiceExpr:
    """A logical expression involving a choice variable that evaluates to true or false.

    Example:
      NevermoreModel == "V4" (note the ==)
    """

    ## The syntax for the expression could be a Python expression,
    ## which could then be evaluated using literal_eval or something
    ## like that.

    def eval(self, choices: UserChoices):
        """Evaluates the condition based on the choices"""
        pass

    def vars(self):
        """Returns the variables in the expression"""
        pass


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

    pass


class AbsoluteCountEffect(ChoiceEffect):
    """Changes the count for a part depending on a choice. This models an
    absolute count.

    """

    pass


class ScaleEffect(ChoiceEffect):
    """Transforms the scale of an object depending on a choice.

    Example: change the length of an STL object based on size of
    the printer.
    """

    pass


class Chooser:
    """Base class for a choice. This also corresponds to the UI shown for
    a choice"""

    pass


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
        self.text = text  # human-readable text
        self.varname = varname  # variable name
        self.values = values


class MultiChooser(Chooser):
    """Represents a choice where multiple values can be selected from a
    list of choices.

    Example: PrinterMods \in {"Lights", "Filter", "FridgeDoor"}
    """

    def __init__(self, text: str, varname: str, values: [ChoiceValue]):
        self.text = text
        self.varname = varname
        self.values = values


class BooleanChoice(Chooser):
    """Represents a yes/no choice. Usually rendered as a checkbox"""

    def __init__(
        self,
        text: str,
        varname: str,
        sel_value: ChoiceValue,  # value when selected
        unsel_value: ChoiceValue = None,
    ):  # value when not selected
        self.text = text
        self.varname = varname
        self.sel_value = sel_value
        self.unsel_value = unsel_value


class Choices:
    """A collection of choices available in a project."""

    def __init__(self, choices: [Chooser]):
        self.choices = choices

    def toposort(self):
        # returns a topological ordering of choices
        # for choices at the same level, return choices in the order that they
        # were passed in choices

        # each level of choices depends on choices made in the previous levels

        # circular dependencies are prohibited
        pass
