from django import forms
from.models import ShippingAddress


class ShippingForm(forms.ModelForm):

    shipping_full_name=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your full name'}),
        required=True
    )
    shipping_phone=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your phone number'}),
        required=True
    )
    shipping_email=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email address'}),
        required=True
    )
    shipping_address1=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your primary address'}),
        required=True
    )
    shipping_address2=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your secondary address(optional)'}),
        required=False
    )
    shipping_city=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your city'}),
        required=True
    )
    shipping_state=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your state'}),
        required=True
    )
    shipping_zipcode=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your zipcode'}),
        required=True
    )
    shipping_country=forms.CharField(label="",
        
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your country'}),
        required=True
    )


    class Meta:
        model=ShippingAddress
        fields=['shipping_full_name','shipping_email','shipping_phone','shipping_address1','shipping_address2',
        'shipping_city','shipping_state','shipping_zipcode','shipping_country']
        
        exclude=['user',]
