from django import forms

class inputForm(forms.Form):
    chr = forms.CharField(max_length=20, label='chr', label_suffix="")
    pos = forms.CharField(max_length=20, label='pos', label_suffix="")
    rsid = forms.CharField(max_length=30, label='rsid', label_suffix="",required=False)
    reason = forms.CharField(max_length=30,label='reason', label_suffix="")
    who = forms.CharField(max_length=30, label='who', label_suffix="")
