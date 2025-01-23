from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, F, Q


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Building Manager'),
        ('warehouse_keeper', 'Warehouse Keeper'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='warehouse_keeper')

# Model to represent a construction building or project
class Building(models.Model):
    name = models.CharField(max_length=255)  # Name of the building/project
    location = models.CharField(max_length=255)  # Location of the building
    project_manager = models.CharField(max_length=255)  # Name of the project manager
    date_added = models.DateField()  # Date when the building was added to the system

    def __str__(self):
        return self.name

# Model to represent materials in the inventory
class Material(models.Model):
    MATERIAL_TYPES = [
        ('Admixtures', '1-Admixtures'),
        ('Aggregates', '2-Aggregates'),
        ('Blocks', '3-Blocks'),
        ('Boards and Panels', '4-Boards and Panels'),
        ('Bricks', '5-Bricks'),
        ('Cement - Grey', '6-Cement - Grey'),
        ('Cement - White', '7-Cement - White'),
        ('CI / DI Covers', '8-CI / DI Covers'),
        ('CP Fittings', '9-CP Fittings'),
        ('Door Fittings', '10-Door Fittings'),
        ('Doors and Windows', '11-Doors and Windows'),
        ('Electrical Items', '12-Electrical Items'),
        ('Fabrics', '13-Fabrics'),
        ('Fuels', '14-Fuels'),
        ('Furniture', '15-Furniture'),
        ('Gates and Grills', '16-Gates and Grills'),
        ('GI Covers', '17-GI Covers'),
        ('Granite', '18-Granite'),
        ('Gypsum Vermiculite', '19-Gypsum Vermiculite'),
        ('Hardware', '20-Hardware'),
        ('Heaters and Coolers', '21-Heaters and Coolers'),
        ('Horticulture', '22-Horticulture'),
        ('IT Hardware', '23-IT Hardware'),
        ('IT Software', '24-IT Software'),
        ('Kitchen Equipments', '25-Kitchen Equipments'),
        ('Locks', '26-Locks'),
        ('Marble', '27-Marble'),
        ('Mechanical Spares', '28-Mechanical Spares'),
        ('Medicines', '29-Medicines'),
        ('Mirrors and Glass', '30-Mirrors and Glass'),
        ('General Items', '31-General Items'),
        ('Oils and Lubricants', '32-Oils and Lubricants'),
        ('Paints', '33-Paints'),
        ('Paver Blocks', '34-Paver Blocks'),
        ('Pest Control', '35-Pest Control'),
        ('Pipes/Pipe Fittings', '36-Pipes/Pipe Fittings'),
        ('Plant and Machinery', '37-Plant and Machinery'),
        ('Plumbing Items', '38-Plumbing Items'),
        ('Pre-Cast Items', '39-Pre-Cast Items'),
        ('PVC Cover Blocks', '40-PVC Cover Blocks'),
        ('Safety Equipments', '41-Safety Equipments'),
        ('Sand', '42-Sand'),
        ('Sanitary Wares', '43-Sanitary Wares'),
        ('Sealants/Adhesives', '44-Sealants/Adhesives'),
        ('Shuttering Materials', '45-Shuttering Materials'),
        ('Stationery', '46-Stationery'),
        ('Steel - Re Bars', '47-Steel - Re Bars'),
        ('Stones', '48-Stones'),
        ('Stoneware Pipes', '49-Stoneware Pipes'),
        ('Structural Steel', '50-Structural Steel'),
        ('TDR', '51-TDR'),
        ('Tiles', '52-Tiles'),
        ('Tools', '53-Tools'),
        ('Water', '54-Water'),
        ('Wood and Timber', '55-Wood and Timber'),
        ('Wooden Flooring', '56-Wooden Flooring'),
        ('Scrap Material', '57-Scrap Material'),
        ('BMS Systems', '58-BMS Systems'),
        ('Concrete', '59-Concrete'),
        ('Modular Kitchen', '60-Modular Kitchen'),
        ('Vehicle', '61-Vehicle'),
        ('Flat Re-purchase', '62-Flat Re-purchase'),
        ('White Goods', '63-White Goods'),
        ('Interior Items', '64-Interior Items'),
        ('Hotel', '65-Hotel'),
        ('Travel', '66-Travel'),
        ('Architect Foreign', '501-Architect Foreign'),
        ('Architect Local', '502-Architect Local'),
        ('BMS System', '503-BMS System'),
        ('Cabling Works', '504-Cabling Works'),
        ('Carpentry  Work', '505-Carpentry  Work'),
        ('Civil  Work', '506-Civil  Work'),
        ('D.G.Sets', '507-D.G.Sets'),
        ('Earthwork', '508-Earthwork'), 
        ('Electrical work', '509-Electrical work'),
        ('Elevators', '510-Elevators'),
        ('Fabrication Work', '511-Fabrication Work'),
        ('False Ceiling Work', '512-False Ceiling Work'),
        ('Fire Fighting Sys.', '513-Fire Fighting Sys.'),
        ('Flooring&Dado Tiling', '514-Flooring&Dado Tiling'),
        ('Gas Connection', '515-Gas Connection'),
        ('Glass  Works', '516-Glass  Works'),
        ('H.V.A.C.System', '517-H.V.A.C.System'),
        ('Hydropnuematic Sys.', '518-Hydropnuematic Sys.'),
        ('Infrastructure Works', '519-Infrastructure Works'),
        ('Land  Dev. work', '520-Land  Dev. work'),
        ('LandScape work - Ext', '521-LandScape work - Ext'),
        ('Misc.Labour Work', '522-Misc.Labour Work'),
        ('Painting Work - Exte', '523-Painting Work - Exte'),
        ('Painting Work - Inte', '524-Painting Work - Inte'),
        ('Piling Work', '525-Piling Work'),
        ('Plumb.&Drainage Work', '526-Plumb.&Drainage Work'),
        ('Polishing works', '527-Polishing works'),
        ('Gypsum Plaster Work', '528-Gypsum Plaster Work'),
        ('PVC Doors and Porta', '529-PVC Doors and Porta'),
        ('R&M Building', '530-R&M Building'),
        ('R&M FireFightingSys.', '531-R&M FireFightingSys.'),
        ('R&M HVAC', '532-R&M HVAC'),
        ('R&M Other Asset', '533-R&M Other Asset'),
        ('R&M Plant & M/C', '534-R&M Plant & M/C'),
        ('R.C.C. Consultant', '535-R.C.C. Consultant'),
        ('Rain Water Harvestin', '536-Rain Water Harvestin'),
        ('RMC', '537-RMC'),
        ('Road & Drainage Work', '538-Road & Drainage Work'),
        ('SewageTreatmentPlant', '539-SewageTreatmentPlant'),
        ('Soil Investigation', '540-Soil Investigation'),
        ('Struct. Steel Work', '541-Struct. Steel Work'),
        ('Technical Consultant', '542-Technical Consultant'),
        ('Telecom system', '543-Telecom system'),
        ('Traffic Signal & Sig', '544-Traffic Signal & Sig'),
        ('Transport Services', '545-Transport Services'),
        ('Vigilance CCTV Sys.', '546-Vigilance CCTV Sys.'),
        ('Watermain works', '547-Watermain works'),
        ('Waterproofing Work', '548-Waterproofing Work'),
        ('WaterTreatmentPlant', '549-WaterTreatmentPlant'),
        ('Al. window/str. glaz', '550-Al. window/str. glaz'),
        ('Hiring Charges - equ', '551-Hiring Charges - equ'),
        ('Solar Hot water syst', '552-Solar Hot water syst'),
        ('LandSc.Garden works', '553-LandSc.Garden works'),
        ('Acid Washing', '554-Acid Washing'),
        ('Compound Wall works', '555-Compound Wall works'),
        ('Internal Services', '556-Internal Services'),
        ('Interior Work', '557-Interior Work'),
        ('Security Services', '558-Security Services'),
        ('Project Construction', '559-Project Construction'),
        ('Sales & Marketing', '560-Sales & Marketing'),
        ('Pest Control Work', '561-Pest Control Work'),
        ('Wooden Flooring Work', '562-Wooden Flooring Work'),
        ('Material Testing', '563-Material Testing'),
        ('R&M Vehicle', '564-R&M Vehicle'),
        ('Service Tax', '565-Service Tax'),
        ('Professional Consult', '566-Professional Consult'),
        ('HR', '567-HR'),
        ('Construction Service', '568-Construction Service'),
        ('Earth Filling Work', '569-Earth Filling Work'),
        ('Fencing & Boundary', '570-Fencing & Boundary'),
        ('Rock cutting work', '571-Rock cutting work'),
        ('Air Conditioning Wrk', '572-Air Conditioning Wrk'),
        ('IT Services', '573-IT Services'),
        ('Legal Services', '574-Legal Services'),
        ('Lease material group', '575-Lease material group'),
        ('Lease mat grp LEASE', '576-Lease mat grp LEASE'),
       
    ]
    name = models.CharField(max_length=255, unique=True,null=False)
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPES)  # Type of material
    hsn_code = models.CharField(max_length=15,null=True,blank=True, default=None)
    material_code = models.CharField(max_length=100, unique=True,null=True,blank=True,default=None)

    def __str__(self):
        return self.name

# Model to represent materials in the inventory
class Inward(models.Model):
    
    material = models.ForeignKey(Material,related_name='inward', on_delete=models.CASCADE)
    po_number = models.CharField(max_length=255,null=False)
    supplier = models.CharField(max_length=255)  # Supplier of the material
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Current quantity in stock
    date_inward = models.DateField()
    expiration_date =  models.DateField(null=True, blank=True,default=None)  # Expiry date if applicable
    
    def __str__(self):
        return f"{self.material.name} - {self.quantity} to {self.building.name}"

    # Method to adjust the inventory
    def adjust_quantity(self, quantity_change):
        self.quantity += quantity_change
        self.save()

    # Check if material is expired
    def is_expired(self):
        return self.expiration_date and self.expiration_date < timezone.now().date()

    # Alerts for low stock levels
    def is_low_stock(self, threshold=10):
        return self.quantity <= threshold
    




# Model to represent materials assigned to specific buildings (Many-to-Many relationship)
class BuildingMaterial(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)  # Associated building
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # Associated material
    quantity = models.PositiveIntegerField()  # Quantity of material at the building
    date_added = models.DateTimeField(auto_now_add=True)  # Date when material was assigned

    def __str__(self):
        return f"{self.building.name} - {self.material.name}"

    # Validation for ensuring sufficient material in stock.
    def clean(self):
        if self.quantity is None:
            raise ValidationError("Quantity cannot be empty.")
        
        if self.material and self.material.quantity is None:
            raise ValidationError(f"Material '{self.material.name}' has no stock defined.")
        
        if self.quantity > self.material.quantity:
            raise ValidationError(
                f"Insufficient stock: {self.material.name} only has {self.material.quantity} units available."
            )

    # Save method to perform validation before saving
    def save(self, *args, **kwargs):
        self.clean()  # Call clean() to perform validation before saving
        super().save(*args, **kwargs)


        # Deduct quantity from material stock
        self.material.quantity -= self.quantity
        self.material.save()

class IssueMaterial(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='issued_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='issued')
    quantity = models.PositiveIntegerField()
    remarks = models.TextField(blank=True, null=True)
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.material.name} issued to {self.building.name}"

#Model to represent material consumption by a building
class MaterialConsumption(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="consumptions")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="consumptions")
    quantity = models.PositiveIntegerField()
    remarks = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.building.name} - {self.material.name} - {self.quantity} units"

    # Method to adjust material quantities based on consumption
    def adjust_inventory(self):
        self.material.quantity -= self.quantity
        self.material.save()
    
    # Save method to perform validation before saving
    def save(self, *args, **kwargs):
        self.clean()  # Call clean() to perform validation before saving
        super().save(*args, **kwargs)


#Model to handle inter-building material loans (loan/repayment functionality)
class MaterialLoan(models.Model):
    lending_building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE, 
        related_name='material_loans_given'
    )
    borrowing_building = models.ForeignKey(
        Building, 
        on_delete=models.CASCADE, 
        related_name='material_loans_received'
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50, 
        choices=[('Pending', 'Pending'), ('Returned', 'Returned')], 
        default='Pending'
    )

    def clean(self):
        """Validate that the loan quantity does not exceed available stock."""
        if self.quantity > self.material.quantity:
            raise ValidationError(f"Insufficient stock: Only {self.material.quantity} units available for loan.")
    
    def save(self, *args, **kwargs):
        # Call clean to perform validation before saving
        self.clean()
        super().save(*args, **kwargs)

        # Deduct loaned quantity from material stock
        self.material.quantity -= self.quantity
        self.material.save()

    def __str__(self):
        return f"{self.material.name} loaned from {self.lending_building.name} to {self.borrowing_building.name}"
    
#Model to handle inter-building material loans (loan/repayment functionality)
class MaterialRepayment(models.Model):
    loan = models.ForeignKey(MaterialLoan, on_delete=models.CASCADE, related_name='repayments')
    quantity = models.PositiveIntegerField()
    repayment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units of {self.loan.material.name} repaid"




# Model to handle inter-building material loans (loan/repayment functionality)
class Loan(models.Model):
    from_building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='loans_given')  # Lending building
    to_building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='loans_received')  # Borrowing building
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # Loaned material
    quantity = models.PositiveIntegerField()  # Quantity loaned
    loan_date = models.DateTimeField(auto_now_add=True)  # Date of loan
    repayment_date = models.DateTimeField(null=True, blank=True)  # Repayment date

    def __str__(self):
        return f"Loan of {self.material.name} from {self.from_building.name} to {self.to_building.name}"

    # Repay the loan and update inventory
    def repay_loan(self):
        if self.repayment_date:
            return "Already repaid"
        self.repayment_date = timezone.now()
        self.save()
        # Adjust inventories of both buildings
        self.material.adjust_quantity(self.quantity)
        building_material_from = BuildingMaterial.objects.get(building=self.from_building, material=self.material)
        building_material_to = BuildingMaterial.objects.get(building=self.to_building, material=self.material)
        
        building_material_from.adjust_quantity(self.quantity)  # Add back to lending building
        building_material_to.adjust_quantity(-self.quantity)  # Subtract from borrowing building
        return "Loan repaid successfully"

    # Check if the loan is due for repayment
    def is_due_for_repayment(self):
        return self.repayment_date is None and (timezone.now() - self.loan_date).days > 30  # 30 days overdue


# Model to represent inventory transactions (addition, consumption, transfer)
class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Add', 'Add'),
        ('Consume', 'Consume'),
        ('Loan', 'Loan'),
        ('Repayment', 'Repayment'),
    ]
    
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES)  # Type of transaction
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # Material being transacted
    building = models.ForeignKey(Building, on_delete=models.CASCADE)  # Building involved in the transaction
    quantity = models.PositiveIntegerField()  # Quantity involved in the transaction
    date = models.DateTimeField(auto_now_add=True)  # Date of the transaction

    def __str__(self):
        return f"{self.transaction_type} - {self.material.name} at {self.building.name} ({self.quantity})"

    # Method to adjust material quantities based on transaction type
    def adjust_inventory(self):
        if self.transaction_type == 'Add':
            self.material.adjust_quantity(self.quantity)
        elif self.transaction_type == 'Consume':
            self.material.adjust_quantity(-self.quantity)
        elif self.transaction_type == 'Loan':
            self.material.adjust_quantity(-self.quantity)
        elif self.transaction_type == 'Repayment':
            self.material.adjust_quantity(self.quantity)
        else:
            raise ValueError("Invalid transaction type")

# Model to represent stock alerts for low stock levels
class StockAlert(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)  # Material being monitored
    threshold = models.PositiveIntegerField()  # Threshold for low stock alert
    alert_date = models.DateTimeField(auto_now_add=True)  # Date when the alert was triggered

    def __str__(self):
        return f"Low Stock Alert: {self.material.name} below {self.threshold} units"

    # Check if an alert is needed for low stock
    def check_for_alert(self):
        if self.material.quantity <= self.threshold:
            return True
        return False

# Model to store building-specific reports (e.g., usage or cost reports)
class BuildingReport(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)  # Associated building
    report_type = models.CharField(max_length=50)  # Type of report (e.g., Usage, Cost)
    generated_on = models.DateTimeField(auto_now_add=True)  # Date when the report was generated
    content = models.TextField()  # Content of the report (e.g., summary of materials used or costs incurred)

    def __str__(self):
        return f"Report for {self.building.name} - {self.report_type} ({self.generated_on})"
