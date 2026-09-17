from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from genericglue.forms import GenericForeignKeyField


# No table_exists() check here. Both branches of the old conditional ended up
# equivalent: MODEL_IDS_WITH_PERMALINKS is empty either way, and every consumer
# does `queryset or ContentType.objects.all()`, for which an empty queryset and
# None behave identically. The check only cost a full pg_catalog table listing
# during django.setup().
MODELS_WITH_PERMALINKS = []
MODEL_IDS_WITH_PERMALINKS = []
QUERYSET = None


class WithGenericObjectForm(forms.ModelForm):
    """
    A class for setting up inlines with a generic FK. It assumes the generic
    object is defined by the fields `object_id` and `object_type` on your
    inline model. It needs to be subclassed and the subclass needs to have a
    meta class defined that sets the model that you're inlining::

        class Meta:
            model = YourInlineModel

    By default this class restricts the GFK model drop down just to content
    types that have get_absolute_url methods. To change this restriction
    override the object property. For example to be able to select from all
    content tpyes, you could add a bit like this to your subclass::

        object = GenericForeignKeyField(required=True, queryset=ContentType.objects.all())

    """
    object = GenericForeignKeyField(required=True, queryset=QUERYSET)

    def __init__(self, *args, **kwargs):
        super(WithGenericObjectForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.object_id:
            self.initial['object'] = [self.instance.object_type.id, self.instance.object_id]

    def clean(self):
        self.instance.object_type, self.instance.object_id = self.cleaned_data['object']
        self.cleaned_data['object_id'] = self.instance.object_id
        self.cleaned_data['object_type'] = self.instance.object_type
        return super(WithGenericObjectForm, self).clean()
