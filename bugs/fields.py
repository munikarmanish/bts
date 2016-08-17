from django.forms.models import ModelChoiceField


class UserChoiceField(ModelChoiceField):
    """Multiple choice field to select a user by displaying
    name and email."""

    def label_from_instance(self, obj):
        return "{} <{}>".format(obj.get_full_name(), obj.email)
