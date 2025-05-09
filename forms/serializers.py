from rest_framework import serializers
from .models import Form, Field

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['label', 'type', 'choices', 'is_required', 'regex_validation', 'placeholder']

class FormSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'title', 'created_on', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        user = self.context['request'].user  # Get the current logged-in user
        form = Form.objects.create(creator=user, **validated_data)
        for field_data in fields_data:
            Field.objects.create(form=form, **field_data)
        form.owners.add(user)  # Add the creator to the owners of the form
        return form
