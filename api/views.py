from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.http import require_POST, require_GET
from django.core.files.base import ContentFile
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Printer, Check
import django_rq
import requests
import base64
import json
import os


def render_check_worker(check):
    url = 'http://wkhtmltopdf:80/'
    context = {
        'check': check.order
    }
    if check.type == 'client':
        data = {
            'contents': base64.b64encode(render(None, 'client_check.html', context).content).decode('utf-8'),
        }
    else:
        data = {
            'contents': base64.b64encode(render(None, 'kitchen_check.html', context).content).decode('utf-8'),
        }
    headers = {
        'Content-Type': 'application/json',  # This is important
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Save the response contents to a file

    check.status = 'rendered'
    # check.pdf_file = File(codecs.open('{}_{}.pdf'.format(check.order['id'], check.type), 'r',
    #                                   encoding='utf-8', errors='ignore'))

    check.pdf_file.save('{}_{}.pdf'.format(check.order['id'], check.type), ContentFile(response.content))

    with open(check.pdf_file.path, 'wb') as f:
        f.write(response.content)
        f.close()

    check.save()


@require_POST
def create_checks(request):
    data_json = json.loads(request.body.decode('utf-8'))
    try:
        Check.objects.get(order__id=data_json['id'])
    except ObjectDoesNotExist:
        no_kitchen = False
        no_client = False
        try:
            kitchen_printer = Printer.objects.filter(point_id=data_json["point_id"]).get(
                check_type='kitchen')
            kitchen_check = kitchen_printer.check_set.create(type='kitchen',
                                                             order=data_json)
            django_rq.enqueue(render_check_worker, kitchen_check)
        except ObjectDoesNotExist:
            no_kitchen = True
        try:
            client_printer = Printer.objects.filter(point_id=data_json["point_id"]).get(
                check_type='client')
            client_check = client_printer.check_set.create(type='client',
                                                           order=data_json)
            django_rq.enqueue(render_check_worker, client_check)
        except ObjectDoesNotExist:
            no_client = True
        if no_kitchen and no_client:
            response = {
                'error': 'Для данной точки не настроено ни одного принтера'
            }
            return JsonResponse(response, status=400)
        else:
            response = {
                'ok': 'Чеки успешно созданы'
            }
            return JsonResponse(response)
    except MultipleObjectsReturned:
        response = {
            'error': 'Для данного заказа уже созданы чеки'
        }
        return JsonResponse(response, status=400)
    else:
        response = {
            'ok': 'Для данного заказа уже созданы чеки'
        }
        return JsonResponse(response, status=400)


@require_GET
def new_checks(request, api_key):
    try:
        printer = Printer.objects.get(api_key=api_key)
        response = {}
        checks_items = printer.check_set.filter(status='rendered')
        response["checks"] = [check.id for check in checks_items]
        return JsonResponse(response)
    except ObjectDoesNotExist:
        response = {
            'error': 'Ошибка авторизации'
        }
        return JsonResponse(response, status=401)


@require_GET
def check(request, api_key, check_id):
    try:
        printer = Printer.objects.get(api_key=api_key)
    except ObjectDoesNotExist:
        response = {
            'error': 'Ошибка авторизации'
        }
        return JsonResponse(response, status=401)
    try:
        check = printer.check_set.get(id=check_id)
        if check.status == 'new':
            response = {
                'error': 'Для данного чека не сгенерирован PDF файл'
            }
            return JsonResponse(response, status=400)
        file = open(check.pdf_file.path, 'rb')
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file.name)}'
        check.status = 'printed'
        check.save()
        return response
    except ObjectDoesNotExist:
        response = {
            'error': 'Данного чека не существует'
        }
        return JsonResponse(response, status=400)
