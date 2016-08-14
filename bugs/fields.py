from django.forms.models import ModelChoiceField


class UserChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return "{} <{}>".format(obj.get_full_name(), obj.email)
