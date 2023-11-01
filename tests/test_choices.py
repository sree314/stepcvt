from stepcvt.choices import *


project_available_choices = Choices([
    SingleChooser('Nevermore Model Version Number', 
                    'NevermoreModel', 
                    [ChoiceValue('V4', 'V4'), 
                        ChoiceValue('V6', 'V6')]),
    MultiChooser('Optional Printer Features', 
                    'PrinterOptions',
                    [ChoiceValue('HEPA Filter', 'Filter'),
                        ChoiceValue('Lights', 'Lights')])
])

user_choices = UserChoices({
        'NevermoreModel': 'V6',
        'PrinterOptions': {
            'Filter',
            'Lights'
        }
    })

choice_expr_v6 = ChoiceExpr('NevermoreModel == \'V6\' and \'Filter\' in PrinterOptions')
choice_expr_v4 = ChoiceExpr('NevermoreModel == \'V4\'')

def test_choice_expr:
    assert choice_expr_v6.vars == ['NevermoreModel', 'PrinterOptions']
    assert choice_expr_v4.vars == ['NevermoreModel']
    assert choice_expr_v6.eval(user_choices)
    assert !choice_expr_v4.eval(user_choices)

def test_selection_effect:
    
