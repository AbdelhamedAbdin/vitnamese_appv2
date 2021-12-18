from student_grade.graphs.pie_chart import MainStructure
import plotly.offline as opy
import plotly.graph_objs as go
from django.db.models import Count
from django.utils.translation import ugettext as _


'''
    pseudocode:-
    BarChar(request_cookie, 'Distribution by gender', resp, 'correct').gender_group()
    Note:
    the text that exists in class will be ignored but will replaced by text in bar_structure function
    instead
'''
class BarChart(MainStructure):

    def __init__(self, request_cookie, text, objects, filter_type):
        super().__init__(request_cookie, text, objects)
        self.filter_type = filter_type

    def gender(self, num_or_obj):
        gender_type = []
        if self.filter_type == "correct":
            for gender in self.objects.exclude(student__gender=self.remove_tail_character()).values('student__gender_%s'%self.request_cookie).annotate(count=Count('student__gender_%s'%self.request_cookie)):
                if gender.get('student__gender_en',0) != None:
                    gender_type.append((self.objects.exclude(student__gender=self.remove_tail_character()).filter(student__gender=gender['student__gender_%s'%self.request_cookie]).filter(correct=num_or_obj).count() / gender['count']) * 100)

        elif self.filter_type == "error_number":
            for gender in self.objects.exclude(student__gender=self.remove_tail_character()).values('student__gender_%s'%self.request_cookie).annotate(count=Count('student__gender_%s'%self.request_cookie)):
                if gender.get('student__gender_en',0) != None:
                    gender_type.append((self.objects.exclude(student__gender=self.remove_tail_character()).filter(student__gender=gender['student__gender_%s'%self.request_cookie]).filter(error_number=num_or_obj).count() / gender['count']) * 100)

        elif self.filter_type == "error_class":
            for gender in self.objects.exclude(student__gender=self.remove_tail_character()).values('student__gender_%s'%self.request_cookie).annotate(count=Count('student__gender_%s'%self.request_cookie)):
                if gender.get('student__gender_en',0) != None:
                    gender_type.append((self.objects.exclude(student__gender=self.remove_tail_character()).filter(student__gender=gender['student__gender_%s'%self.request_cookie]).filter(error_class=num_or_obj).count() / gender['count']) * 100)

        elif self.filter_type == "error_unit":
            for gender in self.objects.exclude(student__gender=self.remove_tail_character()).values('student__gender_%s'%self.request_cookie).annotate(count=Count('student__gender_%s'%self.request_cookie)):
                if gender.get('student__gender_en',0) != None:
                    gender_type.append((self.objects.exclude(student__gender=self.remove_tail_character()).filter(student__gender=gender['student__gender_%s'%self.request_cookie]).filter(error_unit=num_or_obj).count() / gender['count']) * 100)

        elif self.filter_type == "error_type":
            for gender in self.objects.exclude(student__gender=self.remove_tail_character()).values('student__gender_%s'%self.request_cookie).annotate(count=Count('student__gender_%s'%self.request_cookie)):
                if gender.get('student__gender_en',0) != None:
                    gender_type.append((self.objects.exclude(student__gender=self.remove_tail_character()).filter(student__gender=gender['student__gender_%s'%self.request_cookie]).filter(error_type=num_or_obj).count() / gender['count']) * 100)
        return gender_type

    def grade(self, num_or_obj):
        grade_type = []

        if self.filter_type == "correct":
            for grade in self.objects.exclude(student__grade='未填写').values('student__grade').order_by('student__grade').annotate(count=Count('student__grade')):
                grade_type.append((self.objects.filter(student__grade=grade['student__grade']).exclude(student__grade='未填写')
                                   .filter(correct=num_or_obj).count() / grade['count']) * 100)

        elif self.filter_type == "error_number":
            for grade in self.objects.exclude(student__grade='未填写').values('student__grade').order_by('student__grade').annotate(count=Count('student__grade')):
                grade_type.append((self.objects.filter(student__grade=grade['student__grade']).exclude(student__grade='未填写')
                                   .filter(error_number=num_or_obj).count() / grade['count']) * 100)

        elif self.filter_type == "error_class":
            for grade in self.objects.exclude(student__grade='未填写').values('student__grade').order_by('student__grade').annotate(count=Count('student__grade')):
                grade_type.append((self.objects.filter(student__grade=grade['student__grade']).exclude(student__grade='未填写')
                                   .filter(error_class=num_or_obj).count() / grade['count']) * 100)

        elif self.filter_type == "error_unit":
            for grade in self.objects.exclude(student__grade='未填写').values('student__grade').order_by('student__grade').annotate(count=Count('student__grade')):
                grade_type.append((self.objects.filter(student__grade=grade['student__grade']).exclude(student__grade='未填写')
                                   .filter(error_unit=num_or_obj).count() / grade['count']) * 100)

        elif self.filter_type == "error_type":
            for grade in self.objects.exclude(student__grade='未填写').values('student__grade').order_by('student__grade').annotate(count=Count('student__grade')):
                grade_type.append((self.objects.filter(student__grade=grade['student__grade']).exclude(student__grade='未填写')
                                   .filter(error_type=num_or_obj).count() / grade['count']) * 100)
        return grade_type

    def regular(self, num_or_obj):
        reg_type = []

        if self.filter_type == "correct":
            for reg in self.objects.values('character__regularity_%s'%self.request_cookie).annotate(count=Count('character__regularity_%s'%self.request_cookie)):
                reg_type.append((self.objects.filter(character__regularity=reg['character__regularity_%s'%self.request_cookie]).filter(correct=num_or_obj).count() / reg['count']) * 100)

        elif self.filter_type == "error_number":
            for reg in self.objects.values('character__regularity_%s'%self.request_cookie).annotate(count=Count('character__regularity_%s'%self.request_cookie)):
                reg_type.append((self.objects.filter(character__regularity=reg['character__regularity_%s'%self.request_cookie]).filter(error_number=num_or_obj).count() / reg['count']) * 100)

        elif self.filter_type == "error_class":
            for reg in self.objects.values('character__regularity_%s'%self.request_cookie).annotate(count=Count('character__regularity_%s'%self.request_cookie)):
                reg_type.append((self.objects.filter(character__regularity=reg['character__regularity_%s'%self.request_cookie]).filter(error_class=num_or_obj).count() / reg['count']) * 100)

        elif self.filter_type == "error_unit":
            for reg in self.objects.values('character__regularity_%s'%self.request_cookie).annotate(count=Count('character__regularity_%s'%self.request_cookie)):
                reg_type.append((self.objects.filter(character__regularity=reg['character__regularity_%s'%self.request_cookie]).filter(error_unit=num_or_obj).count() / reg['count']) * 100)

        elif self.filter_type == "error_type":
            for reg in self.objects.values('character__regularity_%s'%self.request_cookie).annotate(count=Count('character__regularity_%s'%self.request_cookie)):
                reg_type.append((self.objects.filter(character__regularity=reg['character__regularity_%s'%self.request_cookie]).filter(error_type=num_or_obj).count() / reg['count']) * 100)
        return reg_type

    def complexity(self, num_or_obj):
        complex_type = []

        if self.filter_type == "correct":
            for c in self.objects.values('character__complexity_%s'%self.request_cookie).annotate(count=Count('character__complexity_%s'%self.request_cookie)):
                complex_type.append((self.objects.filter(character__complexity=c['character__complexity_%s'%self.request_cookie]).filter(correct=num_or_obj).count() / c['count']) * 100)

        elif self.filter_type == "error_number":
            for c in self.objects.values('character__complexity_%s'%self.request_cookie).annotate(count=Count('character__complexity_%s'%self.request_cookie)):
                complex_type.append((self.objects.filter(character__complexity=c['character__complexity_%s'%self.request_cookie]).filter(error_number=num_or_obj).count() / c['count']) * 100)

        elif self.filter_type == "error_class":
            for c in self.objects.values('character__complexity_%s'%self.request_cookie).annotate(count=Count('character__complexity_%s'%self.request_cookie)):
                complex_type.append((self.objects.filter(character__complexity=c['character__complexity_%s'%self.request_cookie]).filter(error_class=num_or_obj).count() / c['count']) * 100)

        elif self.filter_type == "error_unit":
            for c in self.objects.values('character__complexity_%s'%self.request_cookie).annotate(count=Count('character__complexity_%s'%self.request_cookie)):
                complex_type.append((self.objects.filter(character__complexity=c['character__complexity_%s'%self.request_cookie]).filter(error_unit=num_or_obj).count() / c['count']) * 100)

        elif self.filter_type == "error_type":
            for c in self.objects.values('character__complexity_%s'%self.request_cookie).annotate(count=Count('character__complexity_%s'%self.request_cookie)):
                complex_type.append((self.objects.filter(character__complexity=c['character__complexity_%s'%self.request_cookie]).filter(error_type=num_or_obj).count() / c['count']) * 100)
        return complex_type

    # add list of names based on trace you would like to add
    def trace_name(self, name):
        if name == "correct":
            return self.CORRECT_LIST
        elif name == "error_number":
            return self.ERROR_NUMBER_LIST
        elif name == "error_class":
            return self.ERROR_CLASS_LIST
        elif name == "error_unit":
            return self.ERROR_UNIT_LIST
        else:
            return self.ERROR_TYPE_LIST

    # main structure for bar chart
    def bar_structure(self, label, texts, title_x, *args):
        labels = label
        layout = go.Layout(
            barmode='stack',
            height=500,
            title={
                'text': texts,
                'font': {'size': 18, 'color': "#4a5568"},
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            showlegend=True,
            legend={"orientation": "v", "yanchor": "top", "xanchor": "left"},
            xaxis={'title': title_x},
            yaxis={'title': _('Percentages')+' (%)', 'hoverformat': '.2f', 'ticksuffix': ' %'})
        figure = go.Figure(layout=layout)

        colors = ["#2f855a", "#c53030", "#2b6cb0", "#2b5a10", "#22acb0", "#DC143C", "#B22222", "#FF4500", "#006400"]
        names = []
        # Add a real name of trace
        if self.filter_type == "correct":
            for trace in self.trace_name(self.filter_type):
                if trace == 0:
                    names.append(_("Correct"))
                elif trace == 1:
                    names.append(_("Incorrect"))
                else:
                    names.append(_("Blank"))
        else:
            for trace in self.trace_name(self.filter_type):
                names.append(trace)

        for n, arg in enumerate(args):
            figure.add_trace(go.Bar(x=labels, y=arg,
                    name=names[n],
                    marker={'color': colors[n]},
                    hovertemplate='%{y}'
                ))
        figure.update_layout(
            autosize=True,
            yaxis=dict(
                titlefont=dict(size=18),
                zeroline=True,
                fixedrange=True,
                showgrid=True
            ),
            xaxis=dict(
                titlefont=dict(size=18),
                fixedrange=True
            ),
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1
        )
        figure.update_yaxes(automargin=True)
        return figure

    def gender_group(self):
        list_of_lists = []
        for o in self.trace_name(self.filter_type):
            list_of_lists.append(self.gender(o))
        figure = self.bar_structure(self.STUDENT_GENDER, _('Distribution by Gender'), _('Gender'), *list_of_lists)
        div = opy.plot(figure, auto_open=False, output_type='div', config=dict(displayModeBar=False))
        return div

    def grade_group(self):
        list_of_lists = []
        for o in self.trace_name(self.filter_type):
            list_of_lists.append(self.grade(o))
        figure = self.bar_structure(self.STUDENT_GRADE, _('Distribution by Grade'), _('Grade'), *list_of_lists)
        div = opy.plot(figure, auto_open=False, output_type='div', config=dict(displayModeBar=False))
        return div

    def regular_group(self):
        list_of_lists = []
        for o in self.trace_name(self.filter_type):
            list_of_lists.append(self.regular(o))
        figure = self.bar_structure(self.CHARACTER_REGULAR, _('Distribution by Regularity'), _('Regularity'), *list_of_lists)
        div = opy.plot(figure, auto_open=False, output_type='div', config=dict(displayModeBar=False))
        return div

    def complex_group(self):
        list_of_lists = []
        for o in self.trace_name(self.filter_type):
            list_of_lists.append(self.complexity(o))
        figure = self.bar_structure(self.CHARACTER_COMPLEX, _('Distribution by Complexity'), _('Complexity'), *list_of_lists)
        div = opy.plot(figure, auto_open=False, output_type='div', config=dict(displayModeBar=False))
        return div
