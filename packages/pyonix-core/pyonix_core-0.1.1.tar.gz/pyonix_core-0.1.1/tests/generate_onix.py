import os
import argparse
import random
from xml.etree.ElementTree import Element, tostring
from faker import Faker

# CONFIGURATION
OUTPUT_FILENAME = "large_onix_3.0.xml"
CHUNK_SIZE = 1000 

# Initialize Faker
fake = Faker()

def create_header():
    """Creates the ONIX 3.0 Header element."""
    header = Element('Header')
    
    sender = Element('Sender')
    sender_name = Element('SenderName')
    sender_name.text = fake.company()
    sender.append(sender_name)
    
    contact = Element('ContactName')
    contact.text = fake.name()
    sender.append(contact)
    
    email = Element('EmailAddress')
    email.text = fake.company_email()
    sender.append(email)
    
    header.append(sender)
    
    sent_date = Element('SentDateTime')
    sent_date.text = fake.date_time().strftime("%Y%m%dT%H%M%S")
    header.append(sent_date)
    
    return header

def create_product():
    """Creates a single ONIX 3.0 Product element with random data."""
    product = Element('Product')
    
    # --- 1. Record Reference ---
    record_ref = Element('RecordReference')
    record_ref.text = fake.uuid4()
    product.append(record_ref)
    
    # --- 2. Notification Type ---
    notif_type = Element('NotificationType')
    notif_type.text = '03'
    product.append(notif_type)
    
    # --- 3. Product Identifier (ISBN-13) ---
    prod_id = Element('ProductIdentifier')
    id_type = Element('ProductIDType')
    id_type.text = '15'
    prod_id.append(id_type)
    id_val = Element('IDValue')
    id_val.text = fake.isbn13().replace("-", "")
    prod_id.append(id_val)
    product.append(prod_id)
    
    # --- 4. Descriptive Detail ---
    desc_detail = Element('DescriptiveDetail')
    
    prod_comp = Element('ProductComposition')
    prod_comp.text = '00'
    desc_detail.append(prod_comp)
    
    prod_form = Element('ProductForm')
    prod_form.text = random.choice(['BC', 'BB', 'EA']) # Paperback, Hardback, Digital
    desc_detail.append(prod_form)
    
    # -- Dynamic Title Generation --
    title_detail = Element('TitleDetail')
    title_type = Element('TitleType')
    title_type.text = '01'
    title_detail.append(title_type)
    
    title_element = Element('TitleElement')
    title_level = Element('TitleElementLevel')
    title_level.text = '01'
    title_element.append(title_level)
    
    # Random Title Length (1 to 10 words)
    title_text = Element('TitleText')
    title_text.text = fake.sentence(nb_words=random.randint(1, 10)).rstrip('.')
    title_element.append(title_text)
    
    # Randomly add a Subtitle (30% chance)
    if random.random() < 0.3:
        subtitle = Element('Subtitle')
        subtitle.text = fake.sentence(nb_words=random.randint(3, 8)).rstrip('.')
        title_element.append(subtitle)
        
    title_detail.append(title_element)
    desc_detail.append(title_detail)
    
    # -- Contributor --
    contributor = Element('Contributor')
    seq_num = Element('SequenceNumber')
    seq_num.text = '1'
    contributor.append(seq_num)
    
    contrib_role = Element('ContributorRole')
    contrib_role.text = 'A01'
    contributor.append(contrib_role)
    
    person_name = Element('PersonName')
    person_name.text = fake.name()
    contributor.append(person_name)
    
    desc_detail.append(contributor)
    product.append(desc_detail)
    
    # --- 5. Publishing Detail ---
    pub_detail = Element('PublishingDetail')
    publisher = Element('Publisher')
    pub_role = Element('PublishingRole')
    pub_role.text = '01'
    publisher.append(pub_role)
    
    pub_name = Element('PublisherName')
    pub_name.text = fake.company()
    publisher.append(pub_name)
    
    pub_detail.append(publisher)
    
    # Pub Date
    pub_date_comp = Element('PublishingDate')
    pub_date_role = Element('PublishingDateRole')
    pub_date_role.text = '01'
    pub_date_comp.append(pub_date_role)
    
    date_val = Element('Date')
    date_val.text = fake.date_between(start_date='-5y', end_date='+2y').strftime("%Y%m%d")
    pub_date_comp.append(date_val)
    
    pub_detail.append(pub_date_comp)
    product.append(pub_detail)

    # --- 6. Product Supply (Prices) ---
    prod_supply = Element('ProductSupply')
    supply_detail = Element('SupplyDetail')
    
    # Supplier
    supplier = Element('Supplier')
    supplier_role = Element('SupplierRole')
    supplier_role.text = '01'
    supplier.append(supplier_role)
    supplier_name = Element('SupplierName')
    supplier_name.text = fake.company()
    supplier.append(supplier_name)
    supply_detail.append(supplier)
    
    # Product Availability
    avail = Element('ProductAvailability')
    avail.text = '20' # Available
    supply_detail.append(avail)
    
    # Price
    price = Element('Price')
    price_type = Element('PriceType')
    price_type.text = '01' # RRP excluding tax
    price.append(price_type)
    
    # Random Price Generation (0.99 to 199.99)
    price_amount = Element('PriceAmount')
    random_price = round(random.uniform(0.99, 199.99), 2)
    price_amount.text = str(random_price)
    price.append(price_amount)
    
    # Random Currency
    currency = Element('CurrencyCode')
    currency.text = random.choice(['USD', 'GBP', 'EUR', 'CAD'])
    price.append(currency)
    
    supply_detail.append(price)
    prod_supply.append(supply_detail)
    product.append(prod_supply)
    
    return product

def generate_large_onix(target_size_gb):
    target_bytes = target_size_gb * 1024 * 1024 * 1024
    current_bytes = 0
    
    print(f"Starting generation of {target_size_gb} GB ONIX 3.0 file...")
    print(f"Output path: {os.path.abspath(OUTPUT_FILENAME)}")
    
    with open(OUTPUT_FILENAME, 'wb') as f:
        # Write XML Declaration and Root Start Tag
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(b'<ONIXMessage release="3.0" xmlns="http://ns.editeur.org/onix/3.0/reference">\n')
        
        # Generate and write Header
        header_node = create_header()
        f.write(tostring(header_node, encoding='utf-8'))
        f.write(b'\n')
        
        products_generated = 0
        
        while current_bytes < target_bytes:
            chunk_buffer = []
            for _ in range(CHUNK_SIZE):
                product_node = create_product()
                chunk_buffer.append(tostring(product_node, encoding='utf-8'))
            
            # Write chunk
            data_to_write = b'\n'.join(chunk_buffer) + b'\n'
            f.write(data_to_write)
            
            # Update progress
            current_bytes = f.tell()
            products_generated += CHUNK_SIZE
            
            # Print status every 10 chunks
            if products_generated % (CHUNK_SIZE * 10) == 0:
                print(f"Generated {products_generated} records... ({current_bytes / 1024 / 1024:.2f} MB)")
        
        # Write Root End Tag
        f.write(b'</ONIXMessage>')
        
    print(f"\nSuccess! Final Size: {os.path.getsize(OUTPUT_FILENAME) / 1024 / 1024 / 1024:.2f} GB")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a large random ONIX 3.0 XML file.")
    
    # Argument for size
    parser.add_argument(
        "size", 
        type=float, 
        help="Target file size in Gigabytes (e.g., 5)"
    )
    
    args = parser.parse_args()
    
    try:
        generate_large_onix(args.size)
    except KeyboardInterrupt:
        print("\nProcess interrupted. Cleaning up XML tags...")
        with open(OUTPUT_FILENAME, 'ab') as f:
            f.write(b'</ONIXMessage>')
        print("File closed.")