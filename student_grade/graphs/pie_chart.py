import plotly.offline as opy
import plotly.graph_objs as go
from django.db.models import Count
from student_grade.models import Response, Student, Character
from django.utils.translation import ugettext as _


class MainStructure:

    def __init__(self, request_cookie, text, objects):
        self.request_cookie = request_cookie
        self.text = text
        self.objects = objects
        self.STUDENT_GENDER = list(filter(lambda v: v is not None, list(Student.objects.all().values_list('gender_'+request_cookie, flat=True).distinct())))
        self.STUDENT_GRADE = list(filter(lambda v: v is not None, list(Student.objects.all().order_by('grade').values_list('grade', flat=True).distinct())))
        self.CHARACTER_REGULAR = list(filter(lambda v: v is not None, list(Character.objects.all().values_list('regularity_'+request_cookie, flat=True).distinct())))
        self.CHARACTER_COMPLEX = list(filter(lambda v: v is not None, list(Character.objects.all().values_list('complexity_'+request_cookie, flat=True).distinct())))
        self.CORRECT_LIST = list(filter(lambda v: v is not None, list(Response.objects.values_list('correct', flat=True).distinct())))
        self.ERROR_NUMBER_LIST = list(filter(lambda v: v is not None, list(Response.objects.values_list('error_number_'+request_cookie, flat=True).distinct())))
        self.ERROR_CLASS_LIST = list(filter(lambda v: v is not None, list(Response.objects.values_list('error_class_'+request_cookie, flat=True).distinct())))
        self.ERROR_UNIT_LIST = list(filter(lambda v: v is not None, list(Response.objects.values_list('error_unit_'+request_cookie, flat=True).distinct())))
        self.ERROR_TYPE_LIST = list(filter(lambda v: v is not None, list(Response.objects.values_list('error_type_'+request_cookie, flat=True).distinct())))

    def remove_tail_character(self):
        specific_char = Student.objects.values_list('gender_'+self.request_cookie, flat=True).distinct()[2]
        return specific_char
'''
    pseudocode:-
    MainStructure(request_cookie, 'Overall Distribution', resp, 'pie').pie_structure('error_number')
'''
class PieChart(MainStructure):
    def __init__(self, request_cookie, text, objects):
        super(PieChart, self).__init__(request_cookie, text, objects)

    def pie_val(self, obj_filter):
        values_list = []
        main_filter = str(obj_filter)

        if main_filter == 'error_number':
            for chars in self.ERROR_NUMBER_LIST:
                values_list.append(self.objects.filter(error_number=chars).aggregate(char=Count(main_filter))['char'])
        elif main_filter == 'correct':
            for chars in self.CORRECT_LIST:
                values_list.append(self.objects.filter(correct=chars).aggregate(correct=Count(main_filter))['correct'])
        elif main_filter == "error_class":
            for chars in self.ERROR_CLASS_LIST:
                values_list.append(self.objects.filter(error_class=chars).aggregate(char=Count(main_filter))['char'])
        elif main_filter == "error_unit":
            for chars in self.ERROR_UNIT_LIST:
                values_list.append(self.objects.filter(error_unit=chars).aggregate(char=Count(main_filter))['char'])
        elif main_filter == "error_type":
            for chars in self.ERROR_TYPE_LIST:
                values_list.append(self.objects.filter(error_type=chars).aggregate(char=Count(main_filter))['char'])
        else:
            pass
        return values_list

    def pie_label(self, obj_filter):
        labels_list = []
        main_filter = str(obj_filter)

        if main_filter == 'error_number':
            for chars in self.ERROR_NUMBER_LIST:
                labels_list.append(chars)
        elif main_filter == 'correct':
            for chars in self.CORRECT_LIST:
                labels_list.append(chars)

            for e, labels in enumerate(labels_list):
                if labels == 0:
                    labels_list[e] = _("Correct")
                elif labels == 1:
                    labels_list[e] = _("Incorrect")
                else:
                    labels_list[e] = _("Blank")
        elif main_filter == "error_class":
            for chars in self.ERROR_CLASS_LIST:
                labels_list.append(chars)
        elif main_filter == "error_unit":
            for chars in self.ERROR_UNIT_LIST:
                labels_list.append(chars)
        elif main_filter == "error_type":
            for chars in self.ERROR_TYPE_LIST:
                labels_list.append(chars)
        else:
            pass
        return labels_list

    def pie_structure(self, object_filter):
        trace = go.Pie({'labels': self.pie_label(object_filter), 'values': self.pie_val(object_filter)},
        marker={
            'colors': ["#2f855a", "#c53030", "#2b6cb0", "#2b5a10", "#22acb0", "#DC143C", "#B22222", "#FF4500", "#006400"],
            "line": {"width": 2, "color": "#FFF"}
        },
       hovertemplate="%{label}" + "</br></br>" + "%{percent}",
       texttemplate=["", "", ""])

        data = go.Data([trace])
        layout = go.Layout(
            width=400,
            title={
                'text': str(self.text),
                'font': {
                    'size': 18,
                    'color': "#4a5568",
                },
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            showlegend=True,
            legend={
                "orientation": "v",
            },
        )
        figure = go.Figure(data, layout)
        figure.update_traces(hoverinfo='label+percent', textinfo='value', name="")
        div = opy.plot(figure, auto_open=False, output_type='div', config=dict(displayModeBar=False))
        return div
