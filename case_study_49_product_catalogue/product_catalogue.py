"""
Case Study 49: Tuple-Based Product Catalogue Audit
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Maintains product catalogue records stored in immutable tuples.
Validates records against integrity rules, calculates granular inventory valuations,
identifies inventory requiring replenishment, and computes reorder capital requirements.
Concepts Used: Tuples, Tuple Immutability & Packing/Unpacking, Lists of Tuples,
               Conditionals, Nested Loops, Error Segregation, and Formatted Ledgers.
"""

def print_banner(title):
    border = "=" * 88
    print(border)
    print(title.center(88))
    print(border)

def validate_catalogue_record(record):
    """
    Validates tuple structure:
    (product_id, product_name, category, unit_price, stock_quantity, reorder_threshold)
    Returns: (is_valid, error_reason)
    """
    if len(record) != 6:
        return False, f"Malformed tuple length ({len(record)} elements, expected 6)"
        
    pid, name, cat, price, stock, reorder = record
    
    if not isinstance(pid, str) or len(pid.strip()) == 0:
        return False, "Invalid or missing Product ID"
        
    if not isinstance(name, str) or len(name.strip()) == 0:
        return False, "Invalid or missing Product Name"
        
    if not isinstance(price, (int, float)) or price <= 0:
        return False, f"Invalid unit price ({price}): Must be positive numeric"
        
    if not isinstance(stock, int) or stock < 0:
        return False, f"Invalid stock quantity ({stock}): Must be non-negative integer"
        
    if not isinstance(reorder, int) or reorder < 0:
        return False, f"Invalid reorder threshold ({reorder}): Must be non-negative integer"
        
    return True, "Valid"

def audit_product_catalogue(raw_catalogue):
    print_banner("ENTERPRISE PRODUCT CATALOGUE INTEGRITY & INVENTORY AUDIT")
    print(f"Total Catalogue Records Ingested: {len(raw_catalogue)}\n")
    
    valid_products = []
    invalid_records = []
    
    # 1. Validation phase
    for item in raw_catalogue:
        is_valid, err_msg = validate_catalogue_record(item)
        if is_valid:
            valid_products.append(item)
        else:
            invalid_records.append((item, err_msg))
            
    # Print Invalid Records Audit if any
    print("SECTION 1: CATALOGUE SANITY & INTEGRITY VALIDATION")
    if len(invalid_records) > 0:
        print(f"[!] Detected {len(invalid_records)} corrupt/invalid records. Quarantined for review:")
        for inv_tuple, reason in invalid_records:
            print(f"    - Quarantined: {inv_tuple} --> REASON: {reason}")
    else:
        print("[OK] All ingested catalogue tuples passed structural schema validation.")
    print("-" * 88)
    
    # 2. Inventory Valuation (Row-wise unpacking)
    print("\nSECTION 2: CERTIFIED PRODUCT INVENTORY VALUATION LEDGER")
    v_fmt = "{:<8} {:<24} {:<15} {:>10} {:>8} {:>14} {:<12}"
    headers = ("ID", "Product Name", "Category", "Price (INR)", "Stock", "Value (INR)", "Stock Status")
    print(v_fmt.format(*headers))
    print("-" * 98)
    
    grand_inventory_value = 0.0
    total_stock_units = 0
    replenishment_orders = []
    
    # Category summary using list of lists: [[cat_name, total_val, total_units], ...]
    category_summary = []
    
    for prod in valid_products:
        # Tuple unpacking
        pid, name, cat, price, stock, reorder = prod
        item_val = price * stock
        grand_inventory_value += item_val
        total_stock_units += stock
        
        # Category aggregation
        cat_found = False
        for c_entry in category_summary:
            if c_entry[0] == cat:
                c_entry[1] += item_val
                c_entry[2] += stock
                cat_found = True
                break
        if not cat_found:
            category_summary.append([cat, item_val, stock])
            
        # Replenishment check
        if stock <= reorder:
            if stock == 0:
                status = "OUT OF STOCK"
                priority = "CRITICAL"
            else:
                status = "REORDER"
                priority = "HIGH"
                
            # Order to achieve 2x reorder threshold buffer
            target_stock = max(2 * reorder, reorder + 10)
            order_qty = target_stock - stock
            estimated_cost = order_qty * price
            replenishment_orders.append((pid, name, stock, reorder, order_qty, estimated_cost, priority))
        else:
            status = "HEALTHY"
            
        print(v_fmt.format(pid, name, cat, f"{price:,.2f}", stock, f"{item_val:,.2f}", status))
        
    print("-" * 98)
    print(f"Grand Total Warehouse Stock Units : {total_stock_units} Units")
    print(f"Grand Total Inventory Asset Value : INR {grand_inventory_value:,.2f}")
    
    # 3. Category-Wise Distribution
    print("\nSECTION 3: CATEGORY-WISE ASSET VALUATION")
    c_fmt = "{:<20} {:>12} {:>18} {:>15}"
    print(c_fmt.format("Category", "Total Units", "Valuation (INR)", "Asset Share %"))
    print("-" * 68)
    for c_entry in category_summary:
        c_name, c_val, c_units = c_entry
        share = (c_val / grand_inventory_value) * 100.0 if grand_inventory_value > 0 else 0.0
        print(c_fmt.format(c_name, c_units, f"{c_val:,.2f}", f"{share:.1f}%"))
    print("-" * 68)
    
    # 4. Replenishment Action Orders
    print("\nSECTION 4: REPLENISHMENT PURCHASE REQUISITION")
    if len(replenishment_orders) == 0:
        print("[OK] All product items are above minimum safety reorder thresholds.")
    else:
        r_fmt = "{:<8} {:<24} {:>8} {:>10} {:>11} {:>16} {:<10}"
        print(r_fmt.format("ID", "Product Name", "Current", "Min Level", "Order Qty", "Est. Cost (INR)", "Priority"))
        print("-" * 94)
        total_reorder_capital = 0.0
        for ro in replenishment_orders:
            pid, name, cur, min_lvl, o_qty, cost, pri = ro
            total_reorder_capital += cost
            print(r_fmt.format(pid, name, cur, min_lvl, o_qty, f"{cost:,.2f}", pri))
        print("-" * 94)
        print(f"Total Items Requiring Purchase   : {len(replenishment_orders)}")
        print(f"Total Reorder Capital Required   : INR {total_reorder_capital:,.2f}")

if __name__ == "__main__":
    # Test dataset containing valid tuples and deliberate edge-case corrupt tuples
    catalogue_dataset = [
        ("PRD101", "Wireless Ergonomic Mouse", "Electronics", 1250.0, 45, 15),
        ("PRD102", "Mechanical Gaming Keyboard", "Electronics", 3499.0, 8, 10),   # Reorder triggered
        ("PRD103", "Noise Cancelling Headset", "Electronics", 5999.0, 3, 5),     # Reorder triggered
        ("PRD104", "USB-C Fast Charging Hub", "Accessories", 1850.0, 60, 20),
        ("PRD105", "27-inch 4K IPS Monitor", "Hardware", 28500.0, 0, 4),        # Out of stock critical!
        ("PRD106", "Aluminum Laptop Riser", "Accessories", 1450.0, 22, 10),
        ("PRD107", "CAT-6 Ethernet Cable 5m", "Networking", 350.0, 110, 30),
        ("PRD108", "Thunderbolt 4 Dock", "Hardware", 14999.0, 5, 5),            # Borderline reorder
        # Malformed & Invalid test records:
        ("PRD109", "Defective Pricing Item", "Hardware", -450.0, 10, 5),          # Negative price
        ("PRD110", "", "Accessories", 800.0, 15, 5),                              # Empty name
        ("PRD111", "Negative Stock Barcode", "Hardware", 2500.0, -4, 2)           # Negative stock
    ]
    
    audit_product_catalogue(catalogue_dataset)

