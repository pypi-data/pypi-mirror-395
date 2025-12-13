from django.forms import HiddenInput
from django.utils.html import format_html


class JsonEditorField(HiddenInput):    
    def __init__(self, *args, **kwargs):      
        super(JsonEditorField, self).__init__(*args, **kwargs)

    class Media:
        js = (                       
            'https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js',
            'hslayers/js/json-editor-field.js',
        )

    def render(self, name, value, attrs=None, renderer=None):        
        input_id = attrs.get("id")

        return format_html(
            '<input type="hidden" class="json-editor-id" value="{}" />' +
            '{}' +
            '<div class="map-tools-container" id="{}"></div>',            
            input_id,            
            super(JsonEditorField, self).render(name, value, attrs, renderer),
            input_id + '-editor',
        )


class MapCompositionSelect(HiddenInput):
    def __init__(self, *args, **kwargs):      
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):

        return format_html(
            '<select id="{}"></select>' +
            '{}',
            attrs.get("id") + '-select',
            super().render(name, value, attrs, renderer),
        )


class MapProjectionSelect(HiddenInput):
    def __init__(self, *args, **kwargs):      
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):

        return format_html(
            '<select id="{}"></select>' +
            '{}',
            attrs.get("id") + '-select',
            super().render(name, value, attrs, renderer),
        )
