from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404, HttpResponseBadRequest
from .models import Form, Response
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