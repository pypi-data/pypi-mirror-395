import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
from pathlib import Path

# Constants
SCHEMA_URL = "https://www.editeur.org/files/ONIX%203/ONIX_BookProduct_3.0_strict_XSDs+codes_Issue_71.zip"
PROJECT_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = PROJECT_ROOT / "schemas"
MODELS_DIR = PROJECT_ROOT / "pyonix_core" / "models"
XSDATA_CONFIG = PROJECT_ROOT / ".xsdata.xml"

def download_and_extract():
    print(f"Downloading schemas from {SCHEMA_URL}...")
    SCHEMAS_DIR.mkdir(exist_ok=True)
    zip_path = SCHEMAS_DIR / "onix_schemas.zip"
    
    try:
        subprocess.run(
            ["curl", "-L", "-A", "Mozilla/5.0", "-o", str(zip_path), SCHEMA_URL], 
            check=True
        )
    except Exception as e:
        print(f"Failed to download schemas: {e}")
        sys.exit(1)

    print("Extracting schemas...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(SCHEMAS_DIR)
    
    # Cleanup zip file
    os.remove(zip_path)
    print("Download and extraction complete.")

def create_xsdata_config(package_name):
    print(f"Creating xsdata configuration for {package_name}...")
    config_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Config xmlns="http://pypi.org/project/xsdata" version="24.5">
  <Output>
    <Package>{package_name}</Package>
    <Format>dataclasses</Format>
    <Structure>clusters</Structure>
    <DocstringStyle>Google</DocstringStyle>
    <RelativeImports>true</RelativeImports>
    <CompoundFields>false</CompoundFields>
  </Output>
  <Conventions>
    <ClassName case="pascalCase" safePrefix="Type"/>
    <FieldName case="snakeCase" safePrefix="value"/>
    <ConstantName case="screamingSnakeCase" safePrefix="VALUE"/>
    <ModuleName case="snakeCase" safePrefix="mod"/>
    <PackageName case="snakeCase" safePrefix="pkg"/>
  </Conventions>
  <Substitutions>
    <Substitution type="package" search="http://www.editeur.org/onix/2.1/reference" replace="onix_2_1"/>
    <Substitution type="package" search="http://www.editeur.org/onix/book/coding" replace="codelists"/>
  </Substitutions>
</Config>
"""
    with open(XSDATA_CONFIG, "w") as f:
        f.write(config_content)

def generate_models():
    print("Generating models with xsdata...")
    
    # Generate Short Models
    short_xsd = list(SCHEMAS_DIR.rglob("*short_strict.xsd"))[0]
    print(f"Using Short XSD: {short_xsd}")
    create_xsdata_config("pyonix_core.models.short")
    
    cmd_short = [
        sys.executable, "-m", "xsdata",
        "generate",
        str(short_xsd),
        "--config", str(XSDATA_CONFIG),
    ]
    subprocess.run(cmd_short, cwd=PROJECT_ROOT, check=True)
    
    # Generate Reference Models
    ref_xsd = list(SCHEMAS_DIR.rglob("*reference_strict.xsd"))[0]
    print(f"Using Reference XSD: {ref_xsd}")
    create_xsdata_config("pyonix_core.models.reference")
    
    cmd_ref = [
        sys.executable, "-m", "xsdata",
        "generate",
        str(ref_xsd),
        "--config", str(XSDATA_CONFIG),
    ]
    subprocess.run(cmd_ref, cwd=PROJECT_ROOT, check=True)
    
    print("Model generation complete.")

if __name__ == "__main__":
    # download_and_extract()
    # create_xsdata_config() # This is now called inside generate_models
    generate_models()
