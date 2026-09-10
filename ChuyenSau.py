def calculate_driver_payout(transactions):
    result = {}
    
    # Bước 1: Đếm số đơn theo trạng thái cho từng tài xế
    for tx in transactions:
        driver = tx["driver_id"]
        status = tx["status"]
        
        if driver not in result:
            result[driver] = {"ok": 0, "disputed": 0}
            
        if status == "DELIVERED":
            result[driver]["ok"] += 1
        elif status == "DISPUTED":
            result[driver]["disputed"] += 1

    # Bước 2: Tính tiền theo quy tắc
    for driver, data in result.items():
        ok = data["ok"]
        base = ok * 20000
        held = data["disputed"] * 20000
        bonus = int(base * 0.1) if ok > 50 else 0  # Chỉ thưởng khi > 50 đơn
        
        result[driver] = {
            "so_don_giao": ok,
            "tien_tam_giu": held,
            "tien_thuong": bonus,
            "thuc_nhan": base + bonus
        }
        
    return result


# --- Chạy thử kiểm tra ---
du_lieu_mau = (
    [{"driver_id": "D01", "status": "DELIVERED"}] * 52 + [{"driver_id": "D01", "status": "DISPUTED"}] * 2 +  # > 50 đơn
    [{"driver_id": "D02", "status": "DELIVERED"}] * 50                                                        # đúng 50 đơn
)

for driver, tien in calculate_driver_payout(du_lieu_mau).items():
    print(f"Tài xế {driver}:", tien)