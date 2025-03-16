#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Form 1040 PDF Filler
Fills ALL fields in a Form 1040 PDF with realistic sample data for a single person filing.
Uses descriptive variable names for each field to make customization easy.
"""
import pdfrw
import os

def decode_field_name(field):
    """
    Remove enclosing angle brackets (if present) and decode a field name from hex (UTF-16) if needed.
    If decoding fails or it's not in hex, return the original string.
    """
    # Remove enclosing angle brackets if they exist
    if field.startswith("<") and field.endswith(">"):
        field = field[1:-1]
    try:
        if field.startswith("FEFF"):
            return bytes.fromhex(field).decode("utf-16")
    except Exception:
        pass
    return field

def fill_form1040_with_sample_data(pdf_path, output_path):
    """
    Fill Form 1040 PDF with comprehensive, realistic sample data for a single filer
    """
    # Enable debugging to see field names as they're processed
    debug_mode = True
    # PERSONAL INFORMATION
    personal_info = {
        "f1_01[0]": "January",           # Beginning month
        "f1_02[0]": "December",          # Ending month
        "f1_03[0]": "24",                # Year
        "f1_04[0]": "John C",            # First name and middle initial
        "f1_05[0]": "Doe",               # Last name
        "f1_06[0]": "222222222",         # Your SSN
        "f1_07[0]": "Mary",              # Spouse first name and MI
        "f1_08[0]": "Jane",              # Spouse last name
        "f1_09[0]": "111111111",         # Spouse SSN
        "f1_10[0]": "123 Main St",       # Street address
        "f1_11[0]": "Apt A",             # Apartment number
        "f1_12[0]": "Anytown",           # City/town
        "f1_13[0]": "CA",                # State
        "f1_14[0]": "90210",             # ZIP code
        "f1_15[0]": "Saudi Arabia",      # Foreign country name
        "f1_16[0]": "Riyadh",            # Foreign province
        "f1_17[0]": "69696",             # Foreign postal code
        "f1_18[0]": "Mary Jane",         # Name for MFS/HOH/QSS
        "f1_19[0]": "Mary Jane",         # Name for nonresident alien spouse
    }

    # DEPENDENTS
    dependents = {
        "f1_20[0]": "Emma Doe",          # Dependent 1 first and last name
        "f1_21[0]": "987-65-4321",       # Dependent 1 SSN
        "f1_22[0]": "Daughter",          # Dependent 1 relationship to you
        "f1_23[0]": "Liam Doe",          # Dependent 2 first and last name
        "f1_24[0]": "876-54-3210",       # Dependent 2 SSN
        "f1_25[0]": "Son",               # Dependent 2 relationship to you
        "f1_26[0]": "Olivia Doe",        # Dependent 3 first and last name
        "f1_27[0]": "765-43-2109",       # Dependent 3 SSN
        "f1_28[0]": "Daughter",          # Dependent 3 relationship to you
        "f1_29[0]": "Noah Doe",          # Dependent 4 first and last name
        "f1_30[0]": "654-32-1098",       # Dependent 4 SSN
        "f1_31[0]": "Son",               # Dependent 4 relationship to you
    }
    
    ###!!!!!!!!!Jacked up
    # RELATIONSHIP INFO FOR DEPENDENTS - Using field names that match actual form
    dependent_relationship = {
        # Try different potential field name patterns for dependent relationships
        "f3_1[0]": "Daughter",                # Dependent 1 relationship 
        "f3_2[0]": "Son",                     # Dependent 2 relationship
        "f3_3[0]": "",                        # Dependent 3 relationship (blank)
        "f3_4[0]": "",                        # Dependent 4 relationship (blank)
        
        # Alternative field names
        "f1_67[0]": "Daughter",               # Dependent 1 relationship (alternate)
        "f1_68[0]": "Son",                    # Dependent 2 relationship (alternate)
        "f1_69[0]": "",                       # Dependent 3 relationship (alternate)
        "f1_70[0]": "",                       # Dependent 4 relationship (alternate)
    }

    
    # INCOME SECTION
    # Define income values
    w2_income = 65000.00
    household_wages = 0.00
    tip_income = 1200.00
    medicaid_payments = 0.00
    dependent_care = 0.00
    adoption_benefits = 0.00
    form_8919_wages = 0.00
    other_earned = 500.00
    nontaxable_combat = 0.00
    
    # Calculate total wages
    total_wages = w2_income + household_wages + tip_income + medicaid_payments + dependent_care + adoption_benefits + form_8919_wages + other_earned
    
    # Define other income
    tax_exempt_interest = 50.00
    taxable_interest = 750.00
    qualified_dividends = 1200.00
    ordinary_dividends = 1500.00
    ira_distributions = 0.00
    taxable_ira = 0.00
    pensions = 0.00
    taxable_pensions = 0.00
    social_security = 0.00
    taxable_ss = 0.00
    capital_gain = 2500.00
    additional_income = 1000.00
    
    # Calculate total income
    total_income = total_wages + taxable_interest + ordinary_dividends + taxable_ira + taxable_pensions + taxable_ss + capital_gain + additional_income
    
    # Calculate adjusted gross income
    adjustments = 3500.00
    agi = total_income - adjustments
    
    # Calculate taxable income
    std_deduction = 14600.00
    qbi_deduction = 0.00
    total_deductions = std_deduction + qbi_deduction
    taxable_income = max(0, agi - total_deductions)
    
    # INCOME SECTION
    income_data = {
        "f1_32[0]": str(w2_income),            # Total amount from Form(s) W-2, box 1
        "f1_33[0]": str(household_wages),      # Household employee wages not reported on W-2
        "f1_34[0]": str(tip_income),           # Tip income not reported on line 1a
        "f1_35[0]": str(medicaid_payments),    # Medicaid waiver payments not reported on W-2
        "f1_36[0]": str(dependent_care),       # Taxable dependent care benefits
        "f1_37[0]": str(adoption_benefits),    # Employer-provided adoption benefits
        "f1_38[0]": str(form_8919_wages),      # Wages from Form 8919, line 6
        "f1_39[0]": str(other_earned),         # Other earned income
        "f1_40[0]": str(nontaxable_combat),    # Nontaxable combat pay election
        "f1_41[0]": str(total_wages),          # Add lines 1a through 1h
        "f1_42[0]": str(tax_exempt_interest),  # Tax-exempt interest
        "f1_43[0]": str(taxable_interest),     # Taxable interest
        "f1_44[0]": str(qualified_dividends),  # Qualified dividends
        "f1_45[0]": str(ordinary_dividends),   # Ordinary dividends
        "f1_46[0]": str(ira_distributions),    # IRA distributions
        "f1_47[0]": str(taxable_ira),          # Taxable amount of IRA distributions
        "f1_48[0]": str(pensions),             # Pensions and annuities
        "f1_49[0]": str(taxable_pensions),     # Taxable amount of pensions
        "f1_50[0]": str(social_security),      # Social security benefits
        "f1_51[0]": str(taxable_ss),           # Taxable amount of social security
        "f1_52[0]": str(capital_gain),         # Capital gain or (loss)
        "f1_53[0]": str(additional_income),    # Additional income from Schedule 1
        "f1_54[0]": str(total_income),         # Total income
        "f1_55[0]": str(adjustments),          # Adjustments to income
        "f1_56[0]": str(agi),                  # Adjusted gross income
        "f1_57[0]": str(std_deduction),        # Standard deduction or itemized deductions
        "f1_58[0]": str(qbi_deduction),        # Qualified business income deduction
        "f1_59[0]": str(total_deductions),     # Add lines 12 and 13
        "f1_60[0]": str(taxable_income),       # Taxable income
    }

    # PAGE 2 - TAX AND CREDITS
    tax_and_credits = {
        "f2_02[0]": "6140.00",                # Line 16: Tax
        "f2_03[0]": "0.00",                   # Line 17: Amount from Schedule 2
        "f2_04[0]": "6140.00",                # Line 18: Add lines 16 and 17
        "f2_05[0]": "4000.00",                # Line 19: Child tax credit
        "f2_06[0]": "0.00",                   # Line 20: Amount from Schedule 3
        "f2_07[0]": "4000.00",                # Line 21: Add lines 19 and 20
        "f2_08[0]": "2140.00",                # Line 22: Subtract line 21 from 18
        "f2_09[0]": "0.00",                   # Line 23: Other taxes
        "f2_10[0]": "2140.00",                # Line 24: Total tax
    }

    # PAYMENTS
    payments = {
        "f2_11[0]": "7560.00",                # Line 25a: Federal income tax withheld W-2
        "f2_12[0]": "300.00",                 # Line 25b: Federal income tax withheld 1099
        "f2_13[0]": "0.00",                   # Line 25c: Federal income tax withheld other forms
        "f2_14[0]": "7860.00",                # Line 25d: Total federal income tax withheld
        "f2_15[0]": "0.00",                   # Line 26: Estimated tax payments
        "f2_16[0]": "0.00",                   # Line 27: Earned income credit
        "f2_17[0]": "0.00",                   # Line 28: Additional child tax credit
        "f2_18[0]": "0.00",                   # Line 29: American opportunity credit
        "f2_19[0]": "",                       # Line 30: Reserved for future use
        "f2_20[0]": "0.00",                   # Line 31: Amount from Schedule 3
        "f2_21[0]": "0.00",                   # Line 32: Total other payments and refundable credits
        "f2_22[0]": "7860.00",                # Line 33: Total payments
        "f2_23[0]": "5720.00",                # Line 34: Overpaid amount
        "f2_24[0]": "3720.00",                # Line 35a: Amount to be refunded
    }

    # BANK ACCOUNT INFO FOR DIRECT DEPOSIT
    bank_info = {
        "f2_25[0]": "0",                      # Line 35b: Routing number (first character)
        "f2_26[0]": "1",                      # Line 35b: Routing number (second character)
        "f2_27[0]": "2",                      # Line 35b: Routing number (third character)
        "f2_28[0]": "3",                      # Line 35b: Routing number (fourth character)
        "f2_29[0]": "4",                      # Line 35b: Routing number (fifth character)
        "f2_30[0]": "5",                      # Line 35b: Routing number (sixth character)
        "f2_31[0]": "6",                      # Line 35b: Routing number (seventh character)
        "f2_32[0]": "7",                      # Line 35b: Routing number (eighth character)
        "f2_33[0]": "8",                      # Line 35b: Routing number (ninth character)
        "f2_34[0]": "1",                      # Line 35d: Account number (first character)
        "f2_35[0]": "2",                      # Line 35d: Account number (second character)
        "f2_36[0]": "3",                      # Line 35d: Account number (third character)
        "f2_37[0]": "4",                      # Line 35d: Account number (fourth character)
        "f2_38[0]": "5",                      # Line 35d: Account number (fifth character)
        "f2_39[0]": "6",                      # Line 35d: Account number (sixth character)
        "f2_40[0]": "7",                      # Line 35d: Account number (seventh character)
        "f2_41[0]": "8",                      # Line 35d: Account number (eighth character)
        "f2_42[0]": "9",                      # Line 35d: Account number (ninth character)
        "f2_43[0]": "0",                      # Line 35d: Account number (tenth character)
        "f2_44[0]": "1",                      # Line 35d: Account number (eleventh character)
        "f2_45[0]": "2",                      # Line 35d: Account number (twelfth character)
        "f2_46[0]": "3",                      # Line 35d: Account number (thirteenth character)
        "f2_47[0]": "4",                      # Line 35d: Account number (fourteenth character)
        "f2_48[0]": "5",                      # Line 35d: Account number (fifteenth character)
        "f2_49[0]": "6",                      # Line 35d: Account number (sixteenth character)
        "f2_50[0]": "7",                      # Line 35d: Account number (seventeenth character)
    }

    # REMAINING FIELDS
    remaining_fields = {
        "f2_51[0]": "2000.00",                # Line 36: Estimated tax to be applied
        "f2_52[0]": "0.00",                   # Line 37: Amount you owe
        "f2_53[0]": "0.00",                   # Line 38: Estimated tax penalty
    }

    # THIRD PARTY DESIGNEE
    third_party = {
        "f2_54[0]": "Jane Smith",             # Designee name
        "f2_55[0]": "555-123-4567",           # Designee phone
        "f2_56[0]": "12345",                  # Designee PIN
    }

    # SIGNATURE INFORMATION
    signature_info = {
        "f2_57[0]": "Software Engineer",      # Your occupation
        "f2_58[0]": "",                       # Spouse occupation (blank for single filer)
        "f2_59[0]": "555-987-6543",           # Phone number
        "f2_60[0]": "john.doe@email.com",     # Email address
    }

    # PAID PREPARER
    preparer_info = {
        "f2_61[0]": "Mary Johnson",           # Preparer name
        "f2_62[0]": "P12345678",              # PTIN
        "f2_63[0]": "Tax Experts LLC",        # Firm name
        "f2_64[0]": "555-567-8901",           # Phone number
        "f2_65[0]": "789 Tax Blvd, Suite 101, Anytown, CA 90210", # Firm address
        "f2_66[0]": "98-7654321",             # Firm EIN
    }

    # RELATIONSHIP INFO FOR DEPENDENTS
    dependent_relationship = {
        "f1_67[0]": "Daughter",               # Dependent 1 relationship
        "f1_68[0]": "Son",                    # Dependent 2 relationship
        "f1_69[0]": "",                       # Dependent 3 relationship (blank)
        "f1_70[0]": "",                       # Dependent 4 relationship (blank)
    }

    # Define specific field mappings based on the filled form images
    specific_field_mappings = {
        # Dependent relationship fields - from the image, these appear to be different
        "(3) Relationship to you_1": "Daughter",   # First dependent relationship
        "(3) Relationship to you_2": "Son",        # Second dependent relationship
        
        # Social Security Numbers with specific formatting
        "(2) Social security number_1": "987-65-4321",  # First dependent SSN
        "(2) Social security number_2": "876-54-3210",  # Second dependent SSN
        
        # Credit fields for children - checkboxes handled separately
        "(4) Check the box if qualifies for (see instructions):_1": "",  # First dependent
        "(4) Check the box if qualifies for (see instructions):_2": "",  # Second dependent
    }
    
    # Combine all data dictionaries
    all_field_data = {**personal_info, **dependents, **income_data, **tax_and_credits, 
                     **payments, **bank_info, **remaining_fields, **third_party, 
                     **signature_info, **preparer_info, **dependent_relationship,
                     **specific_field_mappings}

    # CHECKBOXES FOR SINGLE FILER
    filing_status_checkboxes = {
        "c1_1[0]": "1",       # Single - CHECKED
        "c1_1[1]": "0",       # Married filing jointly - UNCHECKED
        "c1_1[2]": "0",       # Married filing separately - UNCHECKED
        "c1_1[3]": "0",       # Head of household - UNCHECKED
        "c1_1[4]": "0",       # Qualifying surviving spouse - UNCHECKED
    }

    # OTHER CHECKBOXES - DEFAULT VALUES
    other_checkboxes = {
        "c1_2[0]": "0",       # You as a dependent - UNCHECKED
        "c1_3[0]": "0",       # Spouse as a dependent - UNCHECKED
        "c1_4[0]": "0",       # Spouse itemizes - UNCHECKED
        "c1_5[0]": "0",       # You born before January 2, 1960 - UNCHECKED
        "c1_6[0]": "0",       # You are blind - UNCHECKED
        "c1_7[0]": "0",       # Spouse born before January 2, 1960 - UNCHECKED
        "c1_8[0]": "0",       # Spouse is blind - UNCHECKED
        "c1_9[0]": "0",       # Digital assets - UNCHECKED
        "c1_9[1]": "1",       # Digital assets No - CHECKED
        "c2_1[0]": "0",       # Form 8814 - UNCHECKED
        "c2_1[1]": "0",       # Form 4972 - UNCHECKED
        "c2_1[2]": "0",       # Other tax forms - UNCHECKED
        "c2_2[0]": "1",       # Form 8888 is attached - CHECKED
        "c2_3[0]": "1",       # Checking account type - CHECKED
        "c2_3[1]": "0",       # Savings account type - UNCHECKED
        "c2_4[0]": "1",       # Yes for third party designee - CHECKED
        "c2_4[1]": "0",       # No for third party designee - UNCHECKED
        "c2_5[0]": "0",       # Self-employed checkbox - UNCHECKED
    }

    # DEPENDENT CHECKBOX VALUES
    dependent_checkboxes = {
        "c1_10[0]": "1",      # Child tax credit for dependent 1 - CHECKED
        "c1_10[1]": "0",      # Credit for other dependents for dependent 1 - UNCHECKED
        "c1_11[0]": "1",      # Child tax credit for dependent 2 - CHECKED
        "c1_11[1]": "0",      # Credit for other dependents for dependent 2 - UNCHECKED
        "c1_12[0]": "0",      # Child tax credit for dependent 3 - UNCHECKED (no dependent 3)
        "c1_12[1]": "0",      # Credit for other dependents for dependent 3 - UNCHECKED
        "c1_13[0]": "0",      # Child tax credit for dependent 4 - UNCHECKED (no dependent 4)
        "c1_13[1]": "0",      # Credit for other dependents for dependent 4 - UNCHECKED
    }

    # Combine all checkbox dictionaries
    all_checkbox_data = {**filing_status_checkboxes, **other_checkboxes, **dependent_checkboxes}

    # Load the PDF
    try:
        template = pdfrw.PdfReader(pdf_path)
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return False
    
    # Process each page in the PDF
    for page in template.pages:
        if "/Annots" in page:
            for annot in page["/Annots"]:
                if annot is None:
                    continue
                
                if annot.get("/Subtype") == "/Widget" and annot.get("/T"):
                    raw_field = annot.get("/T")
                    
                    # Get field name
                    if isinstance(raw_field, str) and raw_field.startswith("(") and raw_field.endswith(")"):
                        field = raw_field[1:-1]
                    else:
                        field = raw_field
                    
                    decoded_field = decode_field_name(field)
                    
                    # Handle checkboxes
                    if decoded_field in all_checkbox_data:
                        value = all_checkbox_data[decoded_field]
                        if value == "1":
                            # For checkboxes, set the appropriate value
                            annot.update(pdfrw.PdfDict(AS=pdfrw.PdfName("Yes"), V=pdfrw.PdfName("Yes")))
                        else:
                            annot.update(pdfrw.PdfDict(AS=pdfrw.PdfName("Off"), V=pdfrw.PdfName("Off")))
                    
                    # Handle text fields
                    elif decoded_field in all_field_data:
                        value = all_field_data[decoded_field]
                        annot.update(pdfrw.PdfDict(V=value, AP=None))
                    else:
                        # For unmatched fields, try to determine what they might be based on context
                        # and fill with appropriate data
                        
                        # Check for fields that might be dependent relationships
                        if "Relationship" in decoded_field or "elationship" in decoded_field:
                            if "_1" in decoded_field or decoded_field.endswith("1"):
                                value = "Daughter"
                                annot.update(pdfrw.PdfDict(V=value, AP=None))
                            elif "_2" in decoded_field or decoded_field.endswith("2"):
                                value = "Son"
                                annot.update(pdfrw.PdfDict(V=value, AP=None))
                            else:
                                # For debugging - mark unrecognized relationship fields if debug mode is on
                                if debug_mode:
                                    field_id = decoded_field.replace("[", "_").replace("]", "")
                                    value = f"REL_FIELD: {field_id}"
                                    annot.update(pdfrw.PdfDict(V=value, AP=None))
                        else:
                            # For unmatched fields, create a descriptive identifier to help with debugging
                            if debug_mode:
                                field_id = decoded_field.replace("[", "_").replace("]", "")
                                value = f"FIELD: {field_id}"
                                annot.update(pdfrw.PdfDict(V=value, AP=None))
    
    # Write the filled PDF
    try:
        pdfrw.PdfWriter().write(output_path, template)
        print(f"✓ Filled PDF saved to: {output_path}")
        print(f"✓ All fields and checkboxes filled with realistic sample data for a single filer")
        return True
    except Exception as e:
        print(f"Error writing PDF: {e}")
        return False

# Check if pdfrw is installed
try:
    import pdfrw
except ImportError:
    print("pdfrw module not found. Installing...")
    import pip
    pip.main(['install', 'pdfrw'])
    import pdfrw

# Main execution - runs automatically without menu
if __name__ == "__main__":
    # Set your input and output file paths here - using relative paths in same folder
    input_pdf = "f1040.pdf"  # PDF in the same directory as the script
    output_pdf = "filled_f1040.pdf"  # Output in the same directory as the script

    # Check if PDF exists
    if not os.path.exists(input_pdf):
        print(f"Error: Input PDF file '{input_pdf}' not found")
    else:
        # Fill the PDF with sample data automatically
        print(f"Filling {input_pdf} with sample data...")
        success = fill_form1040_with_sample_data(input_pdf, output_pdf)
        if success:
            print(f"PDF filled successfully with complete sample data for a single filer!")
            print(f"Output saved to: {output_pdf}")
