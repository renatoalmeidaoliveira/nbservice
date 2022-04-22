from django.db.models import Q
from utilities.choices import ChoiceSet

OBJETO_ASSIGNMENT_MODELS = Q(
    Q(app_label='dcim', model='device') |
    Q(app_label='circuits', model='circuit') |
    Q(app_label='virtualization', model='virtualmachine') |
    Q(app_label='nb_service', model='application')
)

class PenTestChoices(ChoiceSet):

    APROVED = 1
    REPROVED = 2



    CHOICES = (
        (APROVED, "Approved"),
        (REPROVED, "Reproved"),
    )

class ShapeChoices(ChoiceSet):

    ROUND_EDGES = 1
    STADIUM = 2
    SUBROUTINE = 3
    CYLINDRICAL = 4
    CIRCLE = 5
    ASYMMETRIC = 6
    RHOMBUS = 7
    HEXAGON = 8
    PARALLELOGRAM = 9
    TRAPEZOID = 10
    
    CHOICES = (
        (ROUND_EDGES,  'Round Edges'),
        (STADIUM,  'Stadium Shaped'),
        (SUBROUTINE,  "Subroutine Shape"),
        (CYLINDRICAL,  "Cylindrical Shape"),
        (CIRCLE,  "Circle Shape"),
        (ASYMMETRIC, "asymmetric shape"),
        (RHOMBUS,"rhombus"),
        (HEXAGON,"Hexagon"),
        (PARALLELOGRAM ,"Parallelogram"),
        (TRAPEZOID,"Trapezoid"),
    )

class ConnectorChoices(ChoiceSet):
    ARROW = 1
    OPEN = 2
    DOTTED_ARROW = 3
    DOTTED_OPEN = 4

    CHOICES = (
        (ARROW,  'Arrow'),
        (OPEN,  'Open'),
        (DOTTED_ARROW,  "Dotted Arrow"),
        (DOTTED_OPEN,  "Dotted Open"),
    )