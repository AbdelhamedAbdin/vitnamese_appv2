from .models import History as history_model
from ipware import get_client_ip
import geoip2.database
from pathlib import Path
import os
from django.utils.deprecation import MiddlewareMixin

BASE_DIR = Path(__file__).resolve().parent.parent

# IP: '197.52.228.207'


class History(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'is_visitor'):
            request.is_visitor = 'visitor'
        try:
            try:
                user_ip = get_client_ip(request)[0]
            except:
                user_ip = 'Unknown'
            with geoip2.database.Reader(os.path.join(BASE_DIR, 'GeoLite2-Country_20210608/GeoLite2-Country.mmdb')) as reader:
                try:
                    country_ip = reader.country(user_ip)
                except:
                    country_ip = 'Unknown'
                else:
                    country_ip = country_ip.country.names['en']

            with geoip2.database.Reader(os.path.join(BASE_DIR, 'GeoLite2-City_20210608/GeoLite2-City.mmdb')) as reader:
                try:
                    city_ip = reader.city(user_ip)
                except:
                    city_ip = 'Unknown'
                else:
                    city_ip = city_ip.city.names['en']
            if request.is_visitor == 'visitor' and 'filtering' not in request.GET:
                request.is_visitor = 'visitor'
            else:
                query_list = ['char', 'reg', 'complex', 'grade', 'gender', 'correct',
                              'error_class', 'error_type', 'error_unit', 'error_number', 'remark']
                check_list = []
                for q in query_list:
                    if q in request.GET:
                        check_list.append(str(request.GET[q]))
                if check_list.count('all') == len(check_list):
                    request.is_visitor = 'visitor'
                else:
                    request.is_visitor = 'make filter'
            history_model.objects.get_or_create(
                user_ip=user_ip,
                action=request.is_visitor,
                country_ip=country_ip,
                city_ip=city_ip
            )
        except Exception as msg:
            raise msg
            pass
