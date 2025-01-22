import csv
from datetime import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Building, Inward, Material, MaterialConsumption, MaterialLoan, MaterialRepayment
from .forms import BuildingForm, BuildingMaterialForm, CSVUploadForm, InwardForm, IssueMaterialForm, MaterialConsumptionForm, MaterialForm, MaterialLoanForm, MaterialRepaymentForm  # Form to handle material creation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Prefetch
from .permissions import IsAdmin, IsBuildingManager, IsWarehouseKeeper
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import messages
from django.db.models import Sum
from warehouse import models
from django.db.models import Q,F

class AdminView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "   , Admin! You have full access."})

class BuildingManagerView(APIView):
    permission_classes = [IsBuildingManager]

    def get(self, request):
        return Response({"message": "Welcome, Building Manager! You can request loans and manage your buildings."})

class WarehouseKeeperView(APIView):
    permission_classes = [IsWarehouseKeeper]

    def get(self, request):
        return Response({"message": "Welcome, Warehouse Keeper! You can manage materials and assign them to buildings."})

#Login View
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate and log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the homepage after login
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'warehouse/login.html', {'form': form})


#Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

#Dashboard View
@login_required  # Ensure that only authenticated users can access this page
def dashboard(request):
    user = request.user  # Get the logged-in user
    # You can also fetch any data related to the user (e.g., inventory, projects)
    
    context = {
        'user': user,
        'welcome_message': f"Welcome, {user.username}!",  # Personalized greeting
    }
    
    return render(request, 'warehouse/dashboard.html', context)

#View All Inventory View
@login_required
def view_all_inventory(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')

    # Fetch inventory items
    inventory = Inward.objects.select_related('material', 'building').all()

    # Apply search filter
    if search_query:
        inventory = inventory.filter(
            Q(material__name__icontains=search_query) |
            Q(material__material_type__icontains=search_query) |
            Q(building__name__icontains=search_query) |
            Q(supplier__icontains=search_query)
        )

    # Apply sorting
    if sort_by:
        inventory = inventory.order_by(sort_by)
        
    inventory = inventory.annotate(
        inward_quantity=Sum('quantity'),
        issued_quantity=Sum('material__consumptions__quantity'),  # Adjust if the related_name is different
        available_quantity=F('quantity') - Sum('material__consumptions__quantity')
        ) 
    
    # Paginate results
    paginator = Paginator(inventory, 25)  # 25 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'warehouse/view_all_inventory.html', {'page_obj': page_obj})

#Add Material View


@login_required
def add_material(request):
    material_types = ['Acid Washing', 'Admixtures', 
                      'Aggregates', 'Air Conditioning Wrk', 'Al. window/str. glaz', 'Architect Foreign', 'Architect Local', 'BMS System', 'BMS Systems', 'Blocks', 'Boards and Panels', 'Bricks', 'Cabling Works', 'Carpentry Work', 'Cement - Grey', 'Cement - White', 'CI / DI Covers', 'Civil Work', 'Compound Wall works', 'Concrete', 'Construction Service', 'CP Fittings', 'D.G.Sets', 'Doors and Windows', 'Door Fittings', 'Earth Filling Work', 'Earthwork', 'Electrical Items', 'Electrical work', 'Elevators', 'Fabrication Work', 'Fabrics', 'False Ceiling Work', 'Fencing & Boundary', 'Fire Fighting Sys.', 'Flat Re-purchase', 'Flooring&Dado Tiling', 'Fuels', 'Furniture', 'Gates and Grills', 'General Items', 'GI Covers', 'Glass Works', 'Granite', 'Gypsum Plaster Work', 'Gypsum Vermiculite', 'Hardware', 'Heaters and Coolers', 'Hiring Charges - equ', 'Horticulture', 'Hotel', 'HR', 'H.V.A.C.System', 'Hydropnuematic Sys.', 'Infrastructure Works', 'Interior Items', 'Interior Work', 'Internal Services', 'IT Hardware', 'IT Services', 'IT Software', 'Kitchen Equipments', 'Land Dev. work', 'LandSc.Garden works', 
                      'LandScape work - Ext', 'Lease mat grp LEASE', 'Lease material group', 'Legal Services', 'Locks', 'Marble', 'Material Testing', 'Mechanical Spares', 'Medicines', 'Misc.Labour Work', 'Mirrors and Glass', 'Modular Kitchen', 'Oils and Lubricants', 'Painting Work - Exte', 'Painting Work - Inte', 'Paints', 'Paver Blocks', 'Pest Control', 'Pest Control Work', 'Piling Work', 'Plant and Machinery', 'Plumb.&Drainage Work', 'Plumbing Items', 'Polishing works', 'Pre-Cast Items', 'Professional Consult', 'Project Construction', 'PVC Cover Blocks', 'PVC Doors and Porta', 'Rain Water Harvestin', 'R.C.C. Consultant', 'R&M Building', 'R&M FireFightingSys.', 'R&M HVAC', 'R&M Other Asset', 'R&M Plant & M/C', 'R&M Vehicle', 'RMC', 'Road & Drainage Work', 'Rock cutting work', 'Safety Equipments', 'Sales & Marketing', 'Sand', 'Sanitary Wares', 'Scrap Material', 'Sealants/Adhesives', 'Security Services', 'Service Tax', 'SewageTreatmentPlant', 'Shuttering Materials', 'Soil Investigation', 'Solar Hot water syst', 'Stainless Steel', 'Stationery', 'Steel - Re Bars', 'Stoneware Pipes', 'Stones', 'Struct. Steel Work', 'Structural Steel', 'Technical Consultant', 'Telecom system', 'TDR', 'Tiles', 'Tools', 'Traffic Signal & Sig', 'Transport Services', 'Travel', 'Vigilance CCTV Sys.', 'Vehicle', 'Water', 'Watermain works', 'Waterproofing Work', 'WaterTreatmentPlant', 'White Goods', 'Wood and Timber', 'Wooden Flooring', 'Wooden Flooring Work']
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            # Save the new material to the database
            material = form.save()
            material_name = material.name  # Get the material name
            

            if request.POST.get('action') == 'save_add_another':
                messages.success(request, f"Material '{material.name}' added successfully!")
                return redirect('add_material')  # Redirect to the same page to add another material
            else:
                messages.success(request, f"Material '{material_name}' added successfully!")
                return redirect('view_all_inventory')  # Redirect to inventory list after saving
        else:
            # Show an error message if the form is invalid
            messages.error(request, "There was an error with the form.")
    else:
        form = MaterialForm()

    return render(request, 'warehouse/add_material.html', {
            'form': form,
            'material_types' : material_types
        })

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Ensure the file is a CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Invalid file format. Please upload a CSV file.")
                return redirect('upload_csv')

            try:
                # Decode the file and read it
                data = csv_file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(data)
                
                for row in reader:
                    Material.objects.update_or_create(
                        name=row['name'],
                        defaults={
                            'material_type': row['material_type'],
                            'hsn_code': row['hsn_code'],
                            'material_code': row['material_code']
                        }
                    )
                messages.success(request, "Materials successfully uploaded and added.")
                return redirect('upload_csv')

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('upload_csv')

    else:
        form = CSVUploadForm()

    return render(request, 'warehouse/upload_csv.html', {'form': form})
    #Add Building View
@login_required
def add_building(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Building added successfully!')
            return redirect('dashboard')  # Change to the desired redirect URL
    else:
        form = BuildingForm()
    
    return render(request, 'warehouse/add_building.html', {'form': form})

#Assign Material View
@login_required
def assign_material(request):
    if request.method == 'POST':
        form = BuildingMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material assigned successfully!')
            return redirect('building_material_list')  # Redirect to the list of assigned materials
        else:
            messages.error(request, 'There was an error assigning the material.')
    else:
        form = BuildingMaterialForm()

    return render(request, 'warehouse/assign_material.html', {'form': form})

def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'warehouse/building_list.html', {'buildings': buildings})


#List of Assigned Materials
def building_material_list(request, building_name):
    # Fetch the building by its name
    building = get_object_or_404(Building, name=building_name)
    
    # Retrieve all materials related to this building from the Inward table
    materials = Inward.objects.filter(building=building)
    
    # Pass both the building and materials to the template
    context = {
        'building': building,
        'materials': materials,
    }
    
    return render(request, 'warehouse/building_material_list.html', context)

#Get Material Details
def get_material_details(request):
    material_id = request.GET.get('material_id')  # Fetch material ID from request
    if material_id:
        try:
            material = Material.objects.get(id=material_id)
            return JsonResponse({
                'material_type': material.material_type,
                'hsn_code': material.hsn_code,
                'material_code': material.material_code
            })
        except Material.DoesNotExist:
            return JsonResponse({'error': 'Material not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)




def search_materials(request):
    term = request.GET.get('term', '')
    materials = Material.objects.filter(name__icontains=term).values('id', 'name')[:10]
    return JsonResponse(list(materials), safe=False)

def inward_material(request):
    material_types = ['Acid Washing', 'Admixtures', 
                      'Aggregates', 'Air Conditioning Wrk', 'Al. window/str. glaz', 'Architect Foreign', 'Architect Local', 'BMS System', 'BMS Systems', 'Blocks', 'Boards and Panels', 'Bricks', 'Cabling Works', 'Carpentry Work', 'Cement - Grey', 'Cement - White', 'CI / DI Covers', 'Civil Work', 'Compound Wall works', 'Concrete', 'Construction Service', 'CP Fittings', 'D.G.Sets', 'Doors and Windows', 'Door Fittings', 'Earth Filling Work', 'Earthwork', 'Electrical Items', 'Electrical work', 'Elevators', 'Fabrication Work', 'Fabrics', 'False Ceiling Work', 'Fencing & Boundary', 'Fire Fighting Sys.', 'Flat Re-purchase', 'Flooring&Dado Tiling', 'Fuels', 'Furniture', 'Gates and Grills', 'General Items', 'GI Covers', 'Glass Works', 'Granite', 'Gypsum Plaster Work', 'Gypsum Vermiculite', 'Hardware', 'Heaters and Coolers', 'Hiring Charges - equ', 'Horticulture', 'Hotel', 'HR', 'H.V.A.C.System', 'Hydropnuematic Sys.', 'Infrastructure Works', 'Interior Items', 'Interior Work', 'Internal Services', 'IT Hardware', 'IT Services', 'IT Software', 'Kitchen Equipments', 'Land Dev. work', 'LandSc.Garden works', 
                      'LandScape work - Ext', 'Lease mat grp LEASE', 'Lease material group', 'Legal Services', 'Locks', 'Marble', 'Material Testing', 'Mechanical Spares', 'Medicines', 'Misc.Labour Work', 'Mirrors and Glass', 'Modular Kitchen', 'Oils and Lubricants', 'Painting Work - Exte', 'Painting Work - Inte', 'Paints', 'Paver Blocks', 'Pest Control', 'Pest Control Work', 'Piling Work', 'Plant and Machinery', 'Plumb.&Drainage Work', 'Plumbing Items', 'Polishing works', 'Pre-Cast Items', 'Professional Consult', 'Project Construction', 'PVC Cover Blocks', 'PVC Doors and Porta', 'Rain Water Harvestin', 'R.C.C. Consultant', 'R&M Building', 'R&M FireFightingSys.', 'R&M HVAC', 'R&M Other Asset', 'R&M Plant & M/C', 'R&M Vehicle', 'RMC', 'Road & Drainage Work', 'Rock cutting work', 'Safety Equipments', 'Sales & Marketing', 'Sand', 'Sanitary Wares', 'Scrap Material', 'Sealants/Adhesives', 'Security Services', 'Service Tax', 'SewageTreatmentPlant', 'Shuttering Materials', 'Soil Investigation', 'Solar Hot water syst', 'Stainless Steel', 'Stationery', 'Steel - Re Bars', 'Stoneware Pipes', 'Stones', 'Struct. Steel Work', 'Structural Steel', 'Technical Consultant', 'Telecom system', 'TDR', 'Tiles', 'Tools', 'Traffic Signal & Sig', 'Transport Services', 'Travel', 'Vigilance CCTV Sys.', 'Vehicle', 'Water', 'Watermain works', 'Waterproofing Work', 'WaterTreatmentPlant', 'White Goods', 'Wood and Timber', 'Wooden Flooring', 'Wooden Flooring Work']

    if request.method == 'POST':
        form = InwardForm(request.POST)
        if form.is_valid():
            print("Form is valid.")
            form.save()

            # Assign material to the building
            building = form.cleaned_data['building']
            material = form.cleaned_data['material']
            messages.success(request, f'{material.name} has been assigned to {building.name}.')

            # Redirect based on user action
            if request.POST.get('action') == 'record_another':
                return redirect('inward_material')
            else:
                return redirect('view_all_inventory')
        else:
            print("Form is invalid.")
            print(form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InwardForm()

    return render(request, 'warehouse/inward.html', {'form': form, 'form_errors': form.errors,'material_types' : material_types})
    


#View for handling ISSUE of material 
def issue_material(request):
    if request.method == 'POST':
        form = IssueMaterialForm(request.POST)
        if form.is_valid():
            issued_material = form.save(commit=False)
            building = issued_material.building
            material = issued_material.material
            quantity = issued_material.quantity
            remarks = form.cleaned_data.get('remarks')

            # Check stock availability
            total_quantity = (
                Inward.objects.filter(building=building, material=material)
                .aggregate(Sum('quantity'))['quantity__sum'] or 0
            )

            if quantity > total_quantity:
                messages.error(request, f"Insufficient stock for {material.name} in {building.name}.")
            else:
                # Deduct from stock
                remaining_quantity = quantity
                for inward in Inward.objects.filter(building=building, material=material).order_by('date_inward'):
                    if remaining_quantity <= 0:
                        break
                    if inward.quantity >= remaining_quantity:
                        inward.quantity -= remaining_quantity
                        inward.save()
                        remaining_quantity = 0
                    else:
                        remaining_quantity -= inward.quantity
                        inward.quantity = 0
                        inward.save()

                # Save consumption record
                MaterialConsumption.objects.create(
                    building=building,
                    material=material,
                    quantity=quantity,
                    date=issued_material.issue_date,
                    remarks=remarks
                )

                # Save issued material
                issued_material.save()
                messages.success(request, f"{quantity} units of {material.name} issued to {building.name}.")
                return redirect('issue_material')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = IssueMaterialForm()

    return render(request, 'warehouse/issue_material.html', {'form': form})

def get_material_quantity(request):
    material_id = request.GET.get('material_id')
    building_id = request.GET.get('building_id')

    if material_id and building_id:
        # Calculate total available quantity of the material for the building
        total_quantity = Inward.objects.filter(
            material_id=material_id,
            building_id=building_id
        ).aggregate(total=models.Sum('quantity'))['total'] or 0

        return JsonResponse({'quantity': total_quantity})
    else:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)
    
def record_consumption(request):
    if request.method == 'POST':
        form = MaterialConsumptionForm(request.POST)
        if form.is_valid():
            consumption = form.save()
            
            # Deduct consumed quantity from material stock
            material = consumption.material
            material.quantity -= consumption.quantity
            material.save()

            messages.success(request, 'Material issued successfully!')
            return redirect('consumption_report')
    else:
        form = MaterialConsumptionForm()

    return render(request, 'warehouse/record_consumption.html', {'form': form})

#API for get materials as per building selection
def get_materials_for_building(request, building_id):
    materials = Inward.objects.filter(building_id=building_id).select_related('material').values(
        'material__id', 'material__name'
    )
    return JsonResponse({'materials': list(materials)})

def get_building_materials(request):
    building_id = request.GET.get('building_id')
    materials = (
        Inward.objects
        .filter(building_id=building_id)
        .values('material_id', 'material__name')
        .annotate(total_quantity=Sum('quantity'))
        .distinct()
    )
    response_data = [
        {
            'id': material['material_id'],
            'name': material['material__name'],
            'total_quantity': material['total_quantity']
        }
        for material in materials
    ]
    return JsonResponse({'materials': response_data})

def consumption_report(request):
    # Fetching material consumptions with related building and material
    consumptions = MaterialConsumption.objects.select_related('building', 'material').all().order_by('-date')
    building_labels = list(consumptions.values_list('building__name', flat=True).distinct())
    material_quantities = [
        consumptions.filter(building__name=label).aggregate(total=Sum('quantity'))['total'] or 0
        for label in building_labels
    ]

    return render(request, 'warehouse/consumption_report.html', {
        'consumptions': consumptions,
        'building_labels': building_labels,
        'material_quantities': material_quantities,
    })


#Loan Material View
def loan_material(request):
    if request.method == 'POST':
        form = MaterialLoanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material loan recorded successfully.')
            return redirect('loan_list')
        else:
            messages.error(request, 'Error: Unable to process the loan.')
    else:
        form = MaterialLoanForm()

    return render(request, 'warehouse/loan_material.html', {'form': form})

#Repay Material View
def repay_material(request):
    if request.method == 'POST':
        form = MaterialRepaymentForm(request.POST)
        if form.is_valid():
            repayment = form.save()

            # Update loan status and stock
            loan = repayment.loan
            loan.quantity -= repayment.quantity
            if loan.quantity == 0:
                loan.status = 'Returned'
            loan.save()

            # Add repaid quantity back to lending building's stock
            material = loan.material
            material.quantity += repayment.quantity
            material.save()

            messages.success(request, 'Material repayment recorded successfully.')
            return redirect('loan_list')
    else:
        form = MaterialRepaymentForm()

    return render(request, 'warehouse/repay_material.html', {'form': form})

#Total Inventory Usage View
def total_inventory_usage(request):
    # Aggregate total quantity consumed by each building
    usage_data = Building.objects.annotate(
        total_consumption=Sum('consumptions__quantity')
    ).order_by('-total_consumption')

    return render(request, 'warehouse/total_inventory_usage.html', {'usage_data': usage_data})

#Loan Repayment History View
def loan_repayment_history(request):
    loans = MaterialLoan.objects.all().order_by('-loan_date')
    repayments = MaterialRepayment.objects.all().order_by('-repayment_date')

    return render(request, 'warehouse/loan_repayment_history.html', {
        'loans': loans,
        'repayments': repayments
    })

#Loan List View
def loan_list(request):
    loans = MaterialLoan.objects.select_related('lending_building', 'borrowing_building', 'material')
    return render(request, 'warehouse/loan_list.html', {'loans': loans})



@login_required
def create_loan_request(request, from_building_id, to_building_id):
    if request.method == 'POST':
        # Handle loan request creation
        pass
    return render(request, 'warehouse/loan_request.html')

@login_required
def approve_loan(request, loan_id):
    loan = MaterialLoan.objects.get(id=loan_id)
    if request.method == 'POST':
        # Handle loan approval logic
        pass
    return render(request, 'warehouse/approve_loan.html', {'loan': loan})

@login_required
def repay_loan(request, loan_id):
    loan = MaterialLoan.objects.get(id=loan_id)
    if request.method == 'POST':
        # Handle loan repayment logic
        pass
    return render(request, 'warehouse/repay_loan.html', {'loan': loan})
