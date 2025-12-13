import requests
import json
import time
import csv
import os
from pathlib import Path

# --- Configuration ---
BIN_LOOKUP_API = "https://bins.antipublic.cc/bins/"
OWNER_CREDIT = "@unik_xd"

# Path to the vbvbin.txt file within the package
VBV_DATA_PATH = Path(__file__).parent / "vbvbin.txt"

# Dictionary to store VBV data: {bin: vbv_status}
vbv_data = {}

def load_vbv_data():
    """Loads VBV status data from the local file."""
    global vbv_data
    vbv_data = {}
    try:
        with open(VBV_DATA_PATH, mode='r') as file:
            # The user's file is pipe-separated, not CSV with commas, and has no header.
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('|')
                if len(parts) >= 2:
                    bin_code = parts[0].strip()
                    # The VBV status is the second part, e.g., "3D TRUE ❌"
                    vbv_status = parts[1].strip()
                    vbv_data[bin_code] = vbv_status
        return True
    except FileNotFoundError:
        print(f"ERROR: VBV data file not found at {VBV_DATA_PATH}. VBV checks will fail.")
        return False
    except Exception as e:
        print(f"ERROR loading VBV data: {e}")
        return False

# Load data on module import
load_vbv_data()

def get_vbv_status(bin_code):
    """Looks up VBV status for a given BIN."""
    return vbv_data.get(bin_code, "NOT FOUND IN LOCAL DB")

def get_bin_lookup(bin_code):
    """Performs an external BIN lookup."""
    try:
        response = requests.get(f"{BIN_LOOKUP_API}{bin_code}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "External BIN lookup failed", "details": str(e)}

def check(cc_data):
    """
    Main function to check VBV and BIN status.
    cc_data format: cc|mm|yy|cvv
    """
    start_time = time.time()

    # 1. Parse CC data
    try:
        parts = cc_data.split('|')
        if len(parts) != 4:
            raise ValueError("Invalid CC data format. Expected: cc|mm|yy|cvv")
        
        cc_number = parts[0].strip()
        if not cc_number.isdigit() or len(cc_number) < 6:
            raise ValueError("Invalid CC number or too short.")
        
        bin_code = cc_number[:6]
    
    except ValueError as e:
        return {
            "status": "ERROR",
            "message": str(e),
            "owner": OWNER_CREDIT,
            "time_taken": f"{time.time() - start_time:.2f}s"
        }

    # 2. Perform VBV Status Check (Local)
    vbv_status = get_vbv_status(bin_code)

    # 3. Perform BIN Lookup (External)
    bin_lookup_result = get_bin_lookup(bin_code)

    # 4. Construct Final Response
    end_time = time.time()
    time_taken = f"{end_time - start_time:.2f}s"

    # Clean up the BIN lookup result for the final response
    if "error" in bin_lookup_result:
        bin_info = bin_lookup_result
    else:
        # Extract key information from the external API response
        bin_info = {
            "bin": bin_lookup_result.get("bin"),
            "brand": bin_lookup_result.get("brand"),
            "type": bin_lookup_result.get("type"),
            "level": bin_lookup_result.get("level"),
            "country": bin_lookup_result.get("country"),
            "country_code": bin_lookup_result.get("country_code"),
            "bank": bin_lookup_result.get("bank"),
            "url": bin_lookup_result.get("url"),
            "phone": bin_lookup_result.get("phone"),
        }

    final_response = {
        "status": "SUCCESS",
        "cc_bin": bin_code,
        "vbv_status": vbv_status,
        "bin_lookup": bin_info,
        "owner": OWNER_CREDIT,
        "time_taken": time_taken
    }

    return final_response

def main():
    """Command-line entry point."""
    import sys
    if len(sys.argv) != 2:
        print("Usage: vbvstatus <cc|mm|yy|cvv>")
        sys.exit(1)
    
    cc_data = sys.argv[1]
    result = check(cc_data)
    
    # Pretty print the result
    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
