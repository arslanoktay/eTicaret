from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Registeration form
class CreateUserForm(UserCreationForm):  #class içerisine yazdığımızda inherit lemiş oluyoruz

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True    # mail girilmesini mecbur bırakır.


    # Email Validation
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exists():    # eğer girilen mail db de varsa

            raise forms.ValidationError('This email is invalid.')

        if len(email) >= 350:   # üstteki durumu geçtik bu doğru mu ?

            raise forms.ValidationError('Your email is too long.')
        
        return email   # takılmadıysa hiçbirine maili döndür
        

# Login form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())  
    password = forms.CharField(widget=PasswordInput())
        
    

# Update form

class UpdateUserForm(forms.ModelForm):

    password = None  # şifre güncellememize gerek yok o yüzden None yazdık

    class Meta: # Meta verilerimizi tanımlamak için

        model = User

        fields = ['username','email']
        exclude = ['password1','password1']


    # bu def sayesinde email boş bırakarak username güncellenemeyecek.
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True    

    
    # Email Validation
    def clean_email(self):

        email = self.cleaned_data.get("email")

        # tüm mailleri filterele eğer bu mail varsa hata bas eğer (exclude) giriş yapılan maille aynı değilse
        if User.objects.filter(email = email).exclude(pk=self.instance.pk).exists():    # sadece isim değiştirebilir o yüzden exist direk kullanamayız.var diye ismi değiştirtmez o yüzden exclude ile kullanıyoruz

            raise forms.ValidationError('This email is invalid.')

        if len(email) >= 350:   # üstteki durumu geçtik bu doğru mu ?

            raise forms.ValidationError('Your email is too long.')
        
        return email   # takılmadıysa hiçbirine maili döndür
    













    