from datetime import datetime
from django import forms
from .models import BuildingMaterial, Inward, IssueMaterial, Material,Loan,Building, MaterialConsumption, MaterialLoan, MaterialRepayment
from django_select2.forms import Select2Widget


class MaterialForm(forms.ModelForm):

    def clean_material_code(self):
        material_code = self.cleaned_data.get('material_code')
        if not material_code.isdigit():
            raise forms.ValidationError("Material code must be exactly 10 digits.")
        return material_code
    
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.TextInput(attrs={'class': 'form-control'}),
            'hsn_code': forms.TextInput(attrs={'class': 'form-control'}),
            'material_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Upload CSV File", widget=forms.FileInput(attrs={'accept': '.csv'}))


class BuildingForm(forms.ModelForm):
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    class Meta:
        model = Building
        fields = ['name','location','project_manager','date_added','company']

class InwardForm(forms.ModelForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        # widget=Select2Widget(attrs={'data-placeholder': 'Search Material...'}),
        widget=forms.HiddenInput()
    )
   
    class Meta:
        model = Inward
        fields = ['material', 'po_number', 'supplier', 'building', 'quantity', 'date_inward', 'expiration_date']
        widgets = {
            'date_inward': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


class BuildingMaterialForm(forms.ModelForm):
    class Meta:
        model = BuildingMaterial
        fields = ['building', 'material', 'quantity']

    def clean_quantity(self):
        """Ensure quantity is valid and doesn't exceed available stock."""
        quantity = self.cleaned_data.get('quantity')
        material = self.cleaned_data.get('material')

        if material is None:
            raise forms.ValidationError("Material must be selected.")

        if quantity is None:
            raise forms.ValidationError("Quantity cannot be empty.")

        if material and quantity > material.quantity:
            raise forms.ValidationError(f"Insufficient stock: {material.name} only has {material.quantity} units available.")

        return quantity

class IssueMaterialForm(forms.ModelForm):
    class Meta:
        model = IssueMaterial
        fields = ['building', 'material', 'quantity', 'remarks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['building'].queryset = Building.objects.all()
        self.fields['material'].queryset = Material.objects.none()  # Initially empty

        if 'building' in self.data:
            try:
                building_id = int(self.data.get('building'))
                self.fields['material'].queryset = Material.objects.filter(inward__building_id=building_id).distinct()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['material'].queryset = Material.objects.filter(inward__building=self.instance.building).distinct()
        
class MaterialConsumptionForm(forms.ModelForm):
    class Meta:
        model = MaterialConsumption
        fields = ['building', 'material', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        material = self.cleaned_data.get('material')

        if material.quantity < quantity:
            raise forms.ValidationError(f"Insufficient stock: Only {material.quantity} units available.")
        return quantity 


#Form to handle inter-building material loans (loan/repayment functionality)
class MaterialLoanForm(forms.ModelForm):
    class Meta:
        model = MaterialLoan
        fields = ['lending_building', 'borrowing_building', 'material', 'quantity']

    def clean_quantity(self):
        """Ensure loan quantity does not exceed available stock."""
        quantity = self.cleaned_data.get('quantity')
        material = self.cleaned_data.get('material')

        if material and quantity > material.quantity:
            raise forms.ValidationError(f"Insufficient stock: Only {material.quantity} units available for loan.")

        return quantity

#Form to handle inter-building material loans (loan/repayment functionality)
class MaterialRepaymentForm(forms.ModelForm):
    class Meta:
        model = MaterialRepayment
        fields = ['loan', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        loan = cleaned_data.get('loan')
        quantity = cleaned_data.get('quantity')

        if loan and quantity > loan.quantity:
            raise forms.ValidationError(f"Cannot repay more than loaned quantity. Remaining loan: {loan.quantity} units.")


