from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .models import Form, Response
from django.core.serializers import serialize
import json

def get_forms(request):
    forms_data = []

    for form in Form.objects.all():
        fields = form.fields.all().values(
            'label', 'type', 'required', 'regex_validation', 'placeholder'
        )
        forms_data.append({
            'id': form.id,
            'title': form.title,
            'created_on': form.created_on,
            'fields': list(fields)
        })

    return JsonResponse(forms_data, safe=False)

def get_form(request, form_id):
    try:
        form = Form.objects.get(pk=form_id)
    except Form.DoesNotExist:
        raise Http404("Form not found")

    fields = form.fields.all().values(
        'id', 'label', 'type', 'required', 'regex_validation', 'placeholder'
    )

    data = {
        'id': form.id,
        'title': form.title,
        'created_on': form.created_on,
        'fields': list(fields),
    }

    return JsonResponse(data)

from django.http import JsonResponse, HttpResponseBadRequest

def get_form_responses(request, form_id):
    try:
        # Retrieve the form object
        cur_form = Form.objects.get(id=form_id)
        # Retrieve responses related to the form (use filter() for multiple responses)
        responses = Response.objects.filter(form=cur_form)
        
        # Serialize the queryset of responses
        response_data = []
        for response in responses:
            response_data.append(
                response.response
            )

        # Return a JsonResponse with serialized data
        return JsonResponse(response_data, safe=False)

    except Form.DoesNotExist:
        return HttpResponseBadRequest("Form not found")


@csrf_exempt
def post_response(request, form_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body)
        # For example, you can save it or print it
        print("Received response:", data)

        # Optionally, save to DB here
        selectedForm = Form.objects.get(id=form_id)
        Response.objects.create(form=selectedForm, response=data)

        return JsonResponse({'message': 'Form submitted successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)