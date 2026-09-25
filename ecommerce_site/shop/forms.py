from django import forms

from .models import Product, Order, Category


# =========================================================
# PRODUCT FORM
# =========================================================

class ProductForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:

        model = Product

        fields = [
            'name',
            'description',
            'price',
            'image',
            'stock',
            'category'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Product Name'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Product Description'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Price',
                    'min': '0',
                    'step': '0.01'
                }
            ),

            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Stock Quantity',
                    'min': '0'
                }
            ),

            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),
        }


# =========================================================
# CHECKOUT FORM
# =========================================================

class CheckoutForm(forms.Form):

    customer_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        )
    )

    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Delivery Address'
            }
        )
    )

    payment_screenshot = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }
        )
    )