from django import forms


class WavForms(forms.Form):
    app_id = forms.CharField(label="app_id", max_length=64, required=False)
    session_id = forms.CharField(label="session_id", max_length=64, required=False)
    # download_start = forms.IntegerField(label="download_start", required=False)
    # download_end = forms.IntegerField(label="download_end", required=False)
    # download_all = forms.BooleanField(label="download_all", required=False)
