from django.shortcuts import render
from .models import Response, Student, Character
from django.core.paginator import Paginator
from .custom_decorators import decoratorDirect, decoratorDirectError
from student_grade.graphs import pie_chart as custom_pie
from student_grade.graphs import bar_chart as custom_bar
from django.http import JsonResponse
from django.utils.safestring import SafeString
from django.utils import translation
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
import re


def current_view(request):
    pattern = re.compile(r'(?P<scheme>[http|https]+://)(?P<host>[a-zA-Z0-9.]+):(?P<port>[0-9]+)/(?P<lang>[a-z-]+)/(?P<query>[a-zA-Z0-9/-]+)')
    return pattern


def translation_page(request):
    response = render(request, 'base.html')
    try:
        path_rout = current_view(request).match(request.META['HTTP_REFERER']).groupdict().get('query')
    except:
        path_rout = None

    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if path_rout:
                redirect_path = '/' + language + '/' + path_rout
            else:
                redirect_path = '/'

            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = redirect_path
            elif language == settings.LANGUAGE_CODE:
                redirect_path = redirect_path
            else:
                return response
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


def trans(request):
    try:
        current_lang = request.COOKIES.get('language').replace("-", "_")
    except:
        current_lang = settings.LANGUAGE_CODE
    return current_lang


def remove_trailer_character(request):
    specific_char = Student.objects.values_list('gender_'+trans(request), flat=True).distinct()[2]
    return specific_char


@decoratorDirect
def accuracy_analysis(request):
    characters = Character.objects.all().distinct()
    students = Student.objects.all().distinct()
    responses = Response.objects.all().distinct()

    STUDENT_GENDER = list(filter(lambda v: v is not None, list(
        Student.objects.all().exclude(gender=remove_trailer_character(request)).values_list('gender', flat=True).distinct())))
    STUDENT_GRADE = list(filter(lambda v: v is not None, list(
        Student.objects.all().exclude(grade=remove_trailer_character(request)).order_by('grade').values_list('grade', flat=True).distinct())))
    CHARACTER_COMPLEX = list(
        filter(lambda v: v is not None, list(Character.objects.all().values_list('complexity', flat=True).distinct())))

    char, reg, complex, grade, gender = None, None, None, None, None
    rem, err, stud = None, None, None

    character_req = request.GET.get('char')
    regularity_req = request.GET.get('reg')
    complexity_req = request.GET.get('complex')
    grade_req = request.GET.get('grade')
    gender_req = request.GET.get('gender')

    regularity = list(characters.values_list('regularity', flat=True).distinct())

    # specify selected attribute for select input
    if character_req and character_req != 'all':
        char = Character.objects.get(id=int(character_req))

    if regularity_req and regularity_req != 'all':
        reg = regularity_req

    if complexity_req and complexity_req != 'all':
        complex = complexity_req

    if grade_req and grade_req != 'all':
        grade = grade_req

    if gender_req and gender_req != 'all':
        gender = gender_req

    # filter by response_field to get the specific data
    all_char = Character.objects.all()
    resp = Response.objects.all()
    all_student = Student.objects.all()

    if 'char' in request.GET:
        if character_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(id=character_req)
            resp = resp.filter(character__in=all_char)

    if 'reg' in request.GET:
        if regularity_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(regularity=regularity_req)
            reg_list = list(all_char.values_list('regularity', flat=True))
            resp = resp.filter(character__regularity__in=reg_list)

    if 'complex' in request.GET:
        if complexity_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(complexity=complexity_req)
            comp_list = list(all_char.values_list('complexity', flat=True))
            resp = resp.filter(character__complexity__in=comp_list)

    if 'grade' in request.GET:
        if grade_req == 'all':
            all_student = all_student
            resp = resp
        else:
            all_student = all_student.filter(grade=grade_req)
            grade_list = list(all_student.values_list('grade', flat=True))
            resp = resp.filter(student__grade__in=grade_list)

    if 'gender' in request.GET:
        if gender_req == 'all':
            all_student = all_student
            resp = resp
        else:
            all_student = all_student.filter(gender=gender_req)
            gender_list = list(all_student.values_list('gender', flat=True))
            resp = resp.filter(student__gender__in=gender_list)

    all_response = resp
    paginator = Paginator(all_response, 100)
    page_number = request.GET.get('page_number')
    all_response = paginator.get_page(page_number)
    if all_response.has_next():
        next_url = f"{request.get_raw_uri()}&page_number={all_response.next_page_number()}"
    else:
        next_url = ''

    if all_response.has_previous():
        prev_url = f"{request.get_raw_uri()}&page_number={all_response.previous_page_number()}"
    else:
        prev_url = ''

    current_lang = trans(request)

    context = {
        'all_response': all_response,
        'responses': responses,
        'students': students,
        'next_url': next_url,
        'prev_url': prev_url,
        'characters': characters,
        'regularity': regularity,
        'char': char,
        'reg': reg,
        'complex': complex,
        'CHARACTER_COMPLEX': CHARACTER_COMPLEX,
        'STUDENT_GENDER': STUDENT_GENDER,
        'STUDENT_GRADE': STUDENT_GRADE,
        'grade': grade,
        'gender': gender,
        'rem': rem,
        'character_req': character_req,
        'pie_graph': custom_pie.PieChart(current_lang, _('Overall Distribution'), resp).pie_structure('correct'),
        'gender_group': custom_bar.BarChart(current_lang, '', resp, 'correct').gender_group(),
        'grade_group': custom_bar.BarChart(current_lang, '', resp, 'correct').grade_group(),
        'regular_group': custom_bar.BarChart(current_lang, '', resp, 'correct').regular_group(),
        'complex_group': custom_bar.BarChart(current_lang, '', resp, 'correct').complex_group()
    }
    return render(request, 'student_grade/accuracy_response_view.html', context)


@decoratorDirectError
def error_analysis(request):
    characters = Character.objects.all().distinct()
    students = Student.objects.all().distinct()
    responses = Response.objects.all().distinct()
    STUDENT_GENDER = list(filter(lambda v: v is not None, list(
        Student.objects.all().exclude(gender=remove_trailer_character(request)).values_list('gender',
                                                                                            flat=True).distinct())))
    STUDENT_GRADE = list(filter(lambda v: v is not None, list(
        Student.objects.all().exclude(grade='未填写').order_by('grade').values_list('grade', flat=True).distinct())))
    CHARACTER_COMPLEX = list(
        filter(lambda v: v is not None, list(Character.objects.all().values_list('complexity', flat=True).distinct())))
    CHARACTER_REGULAR = list(
        filter(lambda v: v is not None, list(Character.objects.all().values_list('regularity', flat=True).distinct())))

    char, reg, complex, grade, gender, correct, err_class, err_number = None, None, None, None, None, None, None, None
    err_unit, err_type, rem, err, stud = None, None, None, None, None

    character_req = request.GET.get('char')
    regularity_req = request.GET.get('reg')
    complexity_req = request.GET.get('complex')
    grade_req = request.GET.get('grade')
    gender_req = request.GET.get('gender')
    correct_req = request.GET.get('correct')
    errorClass_req = request.GET.get('error_class')
    errorNumber_req = request.GET.get('error_number')
    errorUnit_req = request.GET.get('error_unit')
    errorType_req = request.GET.get('error_type')

    error_class = list(responses.values_list('error_class', flat=True).distinct())
    error_number = list(responses.values_list('error_number', flat=True).distinct())
    error_unit = list(responses.values_list('error_unit', flat=True).distinct())
    error_type = list(responses.values_list('error_type', flat=True).distinct())
    regularity = list(characters.values_list('regularity', flat=True).distinct())

    # specify selected attribute for select input
    if character_req and character_req != 'all':
        char = Character.objects.get(id=int(character_req))

    if regularity_req and regularity_req != 'all':
        reg = regularity_req

    if complexity_req and complexity_req != 'all':
        complex = complexity_req

    if grade_req and grade_req != 'all':
        grade = grade_req

    if gender_req and gender_req != 'all':
        gender = gender_req

    if correct_req and correct_req != 'all':
        correct = correct_req

    if errorClass_req and errorClass_req != 'all':
        err_class = errorClass_req

    if errorType_req and errorType_req != 'all':
        err_type = errorType_req

    if errorUnit_req and errorUnit_req != 'all':
        err_unit = errorUnit_req

    if errorNumber_req and errorNumber_req != 'all':
        err_number = errorNumber_req

    # filter by response_field to get the specific data
    all_char = Character.objects.all()
    resp = Response.objects.all().filter(correct=1)
    all_student = Student.objects.all()

    if 'char' in request.GET:
        if character_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(id=character_req)
            resp = resp.filter(character__in=all_char)

    if 'reg' in request.GET:
        if regularity_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(regularity=regularity_req)
            reg_list = list(all_char.values_list('regularity', flat=True))
            resp = resp.filter(character__regularity__in=reg_list)

    if 'complex' in request.GET:
        if complexity_req == 'all':
            all_char = all_char
            resp = resp
        else:
            all_char = all_char.filter(complexity=complexity_req)
            comp_list = list(all_char.values_list('complexity', flat=True))
            resp = resp.filter(character__complexity__in=comp_list)

    if 'grade' in request.GET:
        if grade_req == 'all':
            all_student = all_student
            resp = resp
        else:
            all_student = all_student.filter(grade=grade_req)
            grade_list = list(all_student.values_list('grade', flat=True))
            resp = resp.filter(student__grade__in=grade_list)

    if 'gender' in request.GET:
        if gender_req == 'all':
            all_student = all_student
            resp = resp
        else:
            all_student = all_student.filter(gender=gender_req)
            gender_list = list(all_student.values_list('gender', flat=True))
            resp = resp.filter(student__gender__in=gender_list)

    if 'error_class' in request.GET:
        if errorClass_req == 'all':
            resp = resp
        else:
            resp = resp.filter(error_class=errorClass_req)

    if 'error_number' in request.GET:
        if errorNumber_req == 'all':
            resp = resp
        else:
            resp = resp.filter(error_number=errorNumber_req)

    if 'error_type' in request.GET:
        if errorType_req == 'all':
            resp = resp
        else:
            resp = resp.filter(error_type=errorType_req)

    if 'error_unit' in request.GET:
        if errorUnit_req == 'all':
            resp = resp
        else:
            resp = resp.filter(error_unit=errorUnit_req)

    all_response = resp
    paginator = Paginator(all_response, 50)
    page_number = request.GET.get('page_number')
    all_response = paginator.get_page(page_number)

    if all_response.has_next():
        next_url = f"{request.get_raw_uri()}&page_number={all_response.next_page_number()}"
    else:
        next_url = ''

    if all_response.has_previous():
        prev_url = f"{request.get_raw_uri()}&page_number={all_response.previous_page_number()}"
    else:
        prev_url = ''

    current_lang = trans(request)
    pick_specific_error = list(filter(lambda v: v is not None, list(
        Response.objects.all().values_list('error_number_' + trans(request), flat=True).distinct())))[1]
    pick_specific_error_sec = list(filter(lambda v: v is not None, list(
        Response.objects.all().values_list('error_number_' + trans(request), flat=True).distinct())))[0]
    error_number_unique = resp.exclude(error_number__isnull=True).values_list('error_number', flat=True).distinct()

    context = {
        'all_response': all_response,
        'responses': responses,
        'students': students,
        'next_url': next_url,
        'prev_url': prev_url,
        'characters': characters,
        'error_class': error_class,
        'error_number': error_number,
        'error_unit': error_unit,
        'error_type': error_type,
        'regularity': regularity,
        'STUDENT_GENDER': STUDENT_GENDER,
        'STUDENT_GRADE': STUDENT_GRADE,
        'CHARACTER_COMPLEX': CHARACTER_COMPLEX,
        'CHARACTER_REGULAR': CHARACTER_REGULAR,
        'char': char,
        'reg': reg,
        'complex': complex,
        'grade': grade,
        'gender': gender,
        'correct': correct,
        'err_class': err_class,
        'err_unit': err_unit,
        'err_number': err_number,
        'err_type': err_type,
        'rem': rem,
        'character_req': character_req,
        'pick_specific_error': pick_specific_error,
        'pick_specific_error_sec': pick_specific_error_sec,
        'error_number_unique': error_number_unique
    }

    from django.urls import reverse
    from django.shortcuts import redirect

    # set context data based on particular character => "单一"
    if err_number != pick_specific_error:
        if request.GET.get('distribution') == 'overall' or 'distribution' not in request.GET:
            try:
                gender_group = custom_bar.BarChart(current_lang, '', resp, 'error_number').gender_group()
            except ZeroDivisionError:
                sub_language = request.get_full_path('/').split('/')[1]
                sub_language = request.get_full_path('/').replace(sub_language, request.COOKIES.get('language'))
                return redirect(sub_language)


            new_context = {
                'all_response': all_response,
                'pie_graph': custom_pie.PieChart(current_lang, _('Overall Distribution'), resp).pie_structure(
                    'error_number'),
                'gender_group': gender_group,
                'grade_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').grade_group(),
                'regular_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').regular_group(),
                'complex_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').complex_group(),
            }
            context.update(new_context)
        elif request.GET.get('distribution') == 'gender':

            if request.method == 'GET':
                if 'data' in request.GET:
                    context_data = {
                        'student': SafeString(resp.get(id=int(request.GET.get('data'))).student.student),
                        'grades': resp.get(id=int(request.GET.get('data'))).student.grade,
                        'gender': SafeString(resp.get(id=int(request.GET.get('data'))).student.gender),
                        'character': SafeString(resp.get(id=int(request.GET.get('data'))).character.character),
                        'regularity': SafeString(resp.get(id=int(request.GET.get('data'))).character.regularity),
                        'complexity': SafeString(resp.get(id=int(request.GET.get('data'))).character.complexity),
                        'error_class': SafeString(resp.get(id=int(request.GET.get('data'))).error_class),
                        'error_unit': SafeString(resp.get(id=int(request.GET.get('data'))).error_unit),
                        'error_number': SafeString(resp.get(id=int(request.GET.get('data'))).error_number),
                        'error_type': SafeString(resp.get(id=int(request.GET.get('data'))).error_type)
                    }
                    return JsonResponse(context_data, safe=True, status=200)

            new_context = {
                'gender_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').gender_group(),
                'resp': resp,
                'error_number_unique': resp.values_list('error_number', flat=True).distinct()
            }
            context.update(new_context)
        elif request.GET.get('distribution') == 'grade':

            if request.method == 'GET':
                if 'data' in request.GET:
                    context_data = {
                        'student': SafeString(resp.get(id=int(request.GET.get('data'))).student.student),
                        'grades': resp.get(id=int(request.GET.get('data'))).student.grade,
                        'gender': SafeString(resp.get(id=int(request.GET.get('data'))).student.gender),
                        'character': SafeString(resp.get(id=int(request.GET.get('data'))).character.character),
                        'regularity': SafeString(resp.get(id=int(request.GET.get('data'))).character.regularity),
                        'complexity': SafeString(resp.get(id=int(request.GET.get('data'))).character.complexity),
                        'error_class': SafeString(resp.get(id=int(request.GET.get('data'))).error_class),
                        'error_unit': SafeString(resp.get(id=int(request.GET.get('data'))).error_unit),
                        'error_number': SafeString(resp.get(id=int(request.GET.get('data'))).error_number),
                        'error_type': SafeString(resp.get(id=int(request.GET.get('data'))).error_type)
                    }
                    return JsonResponse(context_data, safe=True, status=200)
            new_context = {
                'grade_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').grade_group(),
                'resp': resp,
                'error_number_unique': resp.values_list('error_number', flat=True).distinct()
            }
            context.update(new_context)
        elif request.GET.get('distribution') == 'regular':

            if request.method == 'GET':
                if 'data' in request.GET:
                    context_data = {
                        'student': SafeString(resp.get(id=int(request.GET.get('data'))).student.student),
                        'grades': SafeString(resp.get(id=int(request.GET.get('data'))).student.grade),
                        'gender': SafeString(resp.get(id=int(request.GET.get('data'))).student.gender),
                        'character': SafeString(resp.get(id=int(request.GET.get('data'))).character.character),
                        'regularity': SafeString(resp.get(id=int(request.GET.get('data'))).character.regularity),
                        'complexity': SafeString(resp.get(id=int(request.GET.get('data'))).character.complexity),
                        'error_class': SafeString(resp.get(id=int(request.GET.get('data'))).error_class),
                        'error_unit': SafeString(resp.get(id=int(request.GET.get('data'))).error_unit),
                        'error_number': SafeString(resp.get(id=int(request.GET.get('data'))).error_number),
                        'error_type': SafeString(resp.get(id=int(request.GET.get('data'))).error_type)
                    }
                    return JsonResponse(context_data, safe=True, status=200)
            new_context = {
                'regular_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').regular_group(),
                'resp': resp,
                'error_number_unique': resp.values_list('error_number', flat=True).distinct()
            }
            context.update(new_context)
        elif request.GET.get('distribution') == 'complex':

            if request.method == 'GET':
                if 'data' in request.GET:
                    context_data = {
                        'student': SafeString(resp.get(id=int(request.GET.get('data'))).student.student),
                        'grades': resp.get(id=int(request.GET.get('data'))).student.grade,
                        'gender': SafeString(resp.get(id=int(request.GET.get('data'))).student.gender),
                        'character': SafeString(resp.get(id=int(request.GET.get('data'))).character.character),
                        'regularity': SafeString(resp.get(id=int(request.GET.get('data'))).character.regularity),
                        'complexity': SafeString(resp.get(id=int(request.GET.get('data'))).character.complexity),
                        'error_class': SafeString(resp.get(id=int(request.GET.get('data'))).error_class),
                        'error_unit': SafeString(resp.get(id=int(request.GET.get('data'))).error_unit),
                        'error_number': SafeString(resp.get(id=int(request.GET.get('data'))).error_number),
                        'error_type': SafeString(resp.get(id=int(request.GET.get('data'))).error_type)
                    }
                    return JsonResponse(context_data, safe=True, status=200)
            new_context = {
                'complex_group': custom_bar.BarChart(current_lang, '', resp, 'error_number').complex_group(),
                'resp': resp,
                'error_number_unique': resp.values_list('error_number', flat=True).distinct()
            }
            context.update(new_context)
    url_error = request.GET.get('error')

    if err_number == pick_specific_error:
        if url_error == "errorClass":
            new_context = {
                'pie_graph': custom_pie.PieChart(current_lang, _('Error Class Distribution'), resp).pie_structure(
                    'error_class'),
                'gender_group': custom_bar.BarChart(current_lang, '', resp, 'error_class').gender_group(),
                'grade_group': custom_bar.BarChart(current_lang, '', resp, 'error_class').grade_group(),
                'regular_group': custom_bar.BarChart(current_lang, '', resp, 'error_class').regular_group(),
                'complex_group': custom_bar.BarChart(current_lang, '', resp, 'error_class').complex_group(),
            }
            context.update(new_context)
        elif url_error == "errorUnit":
            new_context = {
                'pie_graph': custom_pie.PieChart(current_lang, _('Error Unit Distribution'), resp).pie_structure(
                    'error_unit'),
                'gender_group': custom_bar.BarChart(current_lang, '', resp, 'error_unit').gender_group(),
                'grade_group': custom_bar.BarChart(current_lang, '', resp, 'error_unit').grade_group(),
                'regular_group': custom_bar.BarChart(current_lang, '', resp, 'error_unit').regular_group(),
                'complex_group': custom_bar.BarChart(current_lang, '', resp, 'error_unit').complex_group(),
            }
            context.update(new_context)
        elif url_error == "errorType":
            new_context = {
                'pie_graph': custom_pie.PieChart(current_lang, _('Error Type Distribution'), resp).pie_structure(
                    'error_type'),
                'gender_group': custom_bar.BarChart(current_lang, '', resp, 'error_type').gender_group(),
                'grade_group': custom_bar.BarChart(current_lang, '', resp, 'error_type').grade_group(),
                'regular_group': custom_bar.BarChart(current_lang, '', resp, 'error_type').regular_group(),
                'complex_group': custom_bar.BarChart(current_lang, '', resp, 'error_type').complex_group(),
            }
            context.update(new_context)
    return render(request, 'student_grade/error_response_view.html', context)
