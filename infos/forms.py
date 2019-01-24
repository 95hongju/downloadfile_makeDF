from django import forms

class inputForm(forms.Form):
    rack_num=forms.CharField(max_length=20, label='rack_num', label_suffix="")
    box_num=forms.CharField(max_length=30, label='box_num', label_suffix="")
    barcode_num=forms.CharField(max_length=30,label='barcode_num', label_suffix="")
    well_num=forms.CharField(max_length=10, label='well_num', label_suffix="")
    freezer_num=forms.CharField(max_length=20,label='freezer_num', label_suffix="")
