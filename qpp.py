import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & DATA PERSISTENCE
# ==========================================
st.set_page_config(
    page_title="สาบาย Stock  — Corporate Edition", 
    page_icon="cat.png.jpg", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_FILE = "inventory_db.json"
HISTORY_FILE = "inventory_history.json"
APP_PASSWORD = os.getenv("INVENTORY_APP_PASSWORD")

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"id": "SKU-001", "name": "เสื้อยืด Oversize ลายกราฟิก", "category": "เสื้อ", "price": 390, "qty": 2, "style": "#Streetwear", "date": "2023-10-01"},
        {"id": "SKU-002", "name": "กางเกง Cargo ขากระบอก", "category": "กางเกง", "price": 590, "qty": 10, "style": "#Y2K", "date": "2023-11-15"},
        {"id": "SKU-003", "name": "กระโปรงเทนนิสสีพาสเทล", "category": "กระโปรง", "price": 290, "qty": 5, "style": "#Minimal", "date": "2023-12-01"},
        {"id": "SKU-004", "name": "เสื้อเชิ้ตลายสก็อตวินเทจ", "category": "เสื้อ", "price": 420, "qty": 4, "style": "#Vintage", "date": "2024-01-10"}
    ]

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def record_history(action, item_id, details):
    history = load_history()
    history.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "item_id": item_id,
        "details": details,
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[:500], f, ensure_ascii=False, indent=4)

def require_login():
    if not APP_PASSWORD:
        return True
    if st.session_state.get("authenticated"):
        return True
    st.markdown("<h2 style='color:#333333 !important; text-align:center;'>เข้าสู่ระบบคลังสินค้า</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        password = st.text_input("รหัสผ่าน", type="password")
        if st.form_submit_button("เข้าสู่ระบบ", width="stretch"):
            if password == APP_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            st.error("รหัสผ่านไม่ถูกต้อง")
    return False

if 'inventory' not in st.session_state:
    st.session_state.inventory = load_data()

for inventory_item in st.session_state.inventory:
    inventory_item.setdefault('cost', 0)

if not require_login():
    st.stop()

# ==========================================
# 2. ULTRA CSS (Black Top Bar & Light Blue Main)
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Sarabun', sans-serif; }
        .stApp, .main, [data-testid="stAppViewContainer"] { background-color: transparent !important; }
        [data-testid="stSidebar"] { display: none !important; }
        .block-container {
            position: relative !important;
            padding-top: 3.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 1500px !important;
        }
        .admin-inline {
            color: #aaaaaa !important;
            font-size: 0.8rem;
            text-align: right;
            padding: 8px 6px;
        }
        .top-bar {
            background-color: #000000 !important; padding: 8px 12px; 
            position: relative;
            min-height: 44px;
            display: flex; flex-direction: column; justify-content: center; align-items: flex-start;
            border-radius: 0px 0px 15px 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            color: #ffffff !important;
            gap: 0;
            flex-wrap: wrap;
        }
        .brand-title {
            position: absolute;
            top: 6px;
            left: 12px;
            z-index: 2;
        }
        .header-row {
            align-items: center !important;
            gap: 0.5rem !important;
        }
        .header-row .stRadio > div {
            margin-bottom: 0 !important;
            border-radius: 0 0 12px 12px;
        }
        div[data-testid="stHorizontalBlock"]:has(.top-bar) {
            background-color: #000000 !important;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            padding: 8px 12px !important;
            align-items: center !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.top-bar) .top-bar {
            background-color: transparent !important;
            box-shadow: none !important;
            padding: 8px 6px !important;
        }
        div[data-testid="stWidgetLabel"] p { color: #ffffff !important; font-weight: 600 !important; font-size: 1rem !important; margin-bottom: 0px !important; }
        .stRadio div[role="radiogroup"] label { color: #ffffff !important; font-weight: 500 !important; font-size: 1.05rem !important; }
        .stRadio > div {
            display: flex; justify-content: center; gap: 100px; padding: 6px 8px;
            background-color: #000000 !important; border-radius: 0px 0px 15px 15px;
            margin-bottom: 0; border: none !important;
            flex-wrap: wrap;
        }
        .info-card {
            background-color: #ffffff !important; padding: 20px 16px; border-radius: 15px; 
            border: 1px solid #dee2e6 !important; box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important; 
            margin-bottom: 18px; color: #333333 !important;
        }
        .card-title {
            color: #333333 !important; font-weight: 600 !important; font-size: 1.05rem !important; 
            margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f0f0f0 !important; 
            display: flex; align-items: center;
        }
        .data-row { display: flex; padding: 8px 0; border-bottom: 1px solid #fafafa !important; font-size: 0.9rem; color: #333333 !important; }
        .data-label { color: #777777 !important; width: 35%; }
        .data-value { color: #000000 !important; width: 65%; font-weight: 500; }
        .kpi-card {
            background: #ffffff !important; padding: 18px 10px; border-radius: 15px; 
            border-left: 5px solid #0056b3 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.05) !important; 
            text-align: center; color: #333333 !important; box-sizing: border-box;
            min-height: 132px; height: 132px; display: flex; flex-direction: column;
            justify-content: center; align-items: center;
        }
        .kpi-val { font-size: 1.7rem; font-weight: 700; color: #0056b3 !important; }
        .kpi-lab { font-size: 0.8rem; color: #888888 !important; }
        .badge-success { background-color:#d1e7dd !important; color:#0f5132 !important; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:bold; }
        .badge-warning { background-color:#fff3cd !important; color:#856404 !important; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:bold; }
        .badge-danger { background-color:#f8d7da !important; color:#842029 !important; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:bold; }
        .stButton>button { border-radius: 8px; border: 1px solid #dee2e6; background-color: white !important; color: #333333 !important; }
        div[data-testid="stForm"] .stButton>button { background-color: #0056b3 !important; color: white !important; }
        textarea, input, select, .stSelectbox, .stNumberInput, .stTextInput {
            font-size: 16px !important;
        }
        @media (max-width: 768px) {
            .stApp, [data-testid="stAppViewContainer"] {
                overflow-x: hidden !important;
            }
            .block-container {
                padding-top: 3.5rem !important;
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
                width: 100% !important;
                max-width: 100% !important;
                box-sizing: border-box !important;
            }
            .admin-inline {
                font-size: 0.72rem;
                text-align: left;
            }
            .top-bar {
                padding: 12px 14px;
                border-radius: 0 0 12px 12px;
            }
            .top-bar > div {
                width: 100%;
            }
            .top-bar > div > div:first-child {
                font-size: 0.85rem !important;
            }
            .top-bar > div > div:last-child {
                font-size: 0.72rem !important;
            }
            .header-row .stRadio > div {
                margin-top: 0.25rem !important;
            }
            .stRadio > div {
                justify-content: flex-start;
                gap: 5px;
            }
            .stRadio div[role="radiogroup"] label {
                font-size: 0.9rem !important;
                padding: 8px 10px !important;
            }
            div[data-testid="stHorizontalBlock"] > div {
                width: 100% !important;
                min-width: 0 !important;
                flex: 1 1 100% !important;
            }
            div[data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
                width: 100% !important;
                min-width: 0 !important;
            }
            h2 {
                font-size: 1.35rem !important;
                line-height: 1.25 !important;
            }
            .kpi-card {
                min-height: 110px !important;
                height: 110px !important;
                padding: 14px 8px !important;
            }
            .kpi-val { font-size: 1.35rem !important; }
            .kpi-lab { font-size: 0.72rem !important; }
            .data-row {
                flex-direction: column;
                gap: 4px;
            }
            .data-label, .data-value {
                width: 100%;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def render_data_row(label, value):
    return f"""<div class="data-row"><div class="data-label">{label}</div><div class="data-value">{value}</div></div>"""

def get_status_badge(qty):
    if qty <= 0: return '<span class="badge-danger">❌ สินค้าหมด</span>'
    if qty <= 3: return '<span class="badge-warning">⚠️ ใกล้หมด</span>'
    return '<span class="badge-success">✅ พร้อมจำหน่าย</span>'

# ==========================================
# 4. TOP BAR & HORIZONTAL MENU
# ==========================================
header_col, menu_col, admin_col = st.columns([1.8, 7.0, 1.2])
with header_col:
    st.markdown(f"""
        <div class="top-bar">
            <div class="brand-title" style="background-color:#0f0f0f; color:#ffffff !important; padding:6px 12px; border:2px solid #000000; border-radius:6px; font-weight:bold; letter-spacing:1px;">สาบาย Stock</div>
        </div>
    """, unsafe_allow_html=True)
with menu_col:
    menu = st.radio(
        "",
        ["📈 Dashboard", "📄 รายละเอียดสินค้า", "📦 จัดการคลังสินค้า", "📊 วิเคราะห์ข้อมูล"],
        horizontal=True,
        label_visibility="collapsed"
    )
with admin_col:
    st.markdown(f"""
        <div class="admin-inline">Admin User | {datetime.now().strftime('%d %B %Y')}</div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. PAGES
# ==========================================
df_stock = pd.DataFrame(st.session_state.inventory)

if menu == "📈 Dashboard":
    st.markdown("<h2 style='color:#333333 !important; text-align:center;'>Executive Summary</h2>", unsafe_allow_html=True)
    
    
    if 'qty' not in df_stock.columns: df_stock['qty'] = 0
    if 'price' not in df_stock.columns: df_stock['price'] = 0
    
    total_items = len(df_stock)
    total_qty = df_stock['qty'].sum()
    total_cost = (df_stock['cost'] * df_stock['qty']).sum()
    total_sales_value = (df_stock['price'] * df_stock['qty']).sum()
    total_profit = total_sales_value - total_cost
    low_stock_count = len(df_stock[df_stock['qty'] <= 3])
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.markdown(f'<div class="kpi-card"><div class="kpi-lab">รายการสินค้าทั้งหมด</div><div class="kpi-val">{total_items}</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="kpi-card"><div class="kpi-lab">จำนวนชิ้นรวมในคลัง</div><div class="kpi-val">{total_qty:,}</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="kpi-card"><div class="kpi-lab">ต้นทุนรวมในคลัง</div><div class="kpi-val">฿{total_cost:,.0f}</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="kpi-card" style="border-left-color:#198754 !important;"><div class="kpi-lab">กำไรคาดการณ์</div><div class="kpi-val" style="color:#198754 !important;">฿{total_profit:,.0f}</div></div>', unsafe_allow_html=True)
    with col5: st.markdown(f'<div class="kpi-card" style="border-left-color:#dc3545 !important;"><div class="kpi-lab">สินค้าที่ต้องสั่งเพิ่ม</div><div class="kpi-val" style="color:#dc3545 !important;">{low_stock_count}</div></div>', unsafe_allow_html=True)
    st.write("")
    if low_stock_count > 0:
        st.markdown("<div class='info-card'><div class='card-title' style='color:#dc3545 !important;'>⚠️ รายการสินค้าที่ต้องเติมสต็อกด่วน</div>", unsafe_allow_html=True)
        low_df = df_stock[df_stock['qty'] <= 3]
        cols_to_show = [c for c in ['id', 'name', 'qty'] if c in low_df.columns]
        st.table(low_df[cols_to_show])
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📄 รายละเอียดสินค้า":
    st.markdown("<h2 style='color:#333333 !important;'>Product Data Sheet</h2>", unsafe_allow_html=True)
    if not st.session_state.inventory:
        st.warning("ไม่มีข้อมูลสินค้าในระบบ")
    else:
        selected_item_name = st.selectbox("🔍 ค้นหาและเลือกสินค้าเพื่อดูรายละเอียด", [item['name'] for item in st.session_state.inventory])
        item = next((i for i in st.session_state.inventory if i['name'] == selected_item_name), None)
        if item:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"""
                    <div class="info-card">
                        <div class="card-title">📋 ข้อมูลทางเทคนิคของสินค้า</div>
                        {render_data_row("ชื่อสินค้า", item['name'])}
                        {render_data_row("รหัสสินค้า (SKU)", item['id'])}
                        {render_data_row("หมวดหมู่", item['category'])}
                        {render_data_row("สไตล์", item['style'])}
                        {render_data_row("ราคาต่อหน่วย", f"฿{item['price']:,}")}
                        {render_data_row("ต้นทุนต่อหน่วย", f"฿{item.get('cost', 0):,}")}
                        {render_data_row("กำไรต่อหน่วย", f"฿{item['price'] - item.get('cost', 0):,}")}
                        {render_data_row("จำนวนคงเหลือ", f"{item['qty']} ชิ้น")}
                        {render_data_row("วันที่บันทึกล่าสุด", item['date'])}
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="info-card">
                        <div class="card-title">🏷️ สถานะการคลัง</div>
                        {render_data_row("สถานะปัจจุบัน", get_status_badge(item['qty']))}
                        {render_data_row("การหมุนเวียน", "Fast Moving" if item['qty'] < 5 else "Normal")}
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="info-card">
                        <div class="card-title">⚙️ การตรวจสอบ</div>
                        <p style="font-size:0.8rem; color:#999999 !important;">Verified by System<br>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    </div>
                """, unsafe_allow_html=True)

elif menu == "📦 จัดการคลังสินค้า":
    st.markdown("<h2 style='color:#333333 !important;'>Inventory Control Panel</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📋 รายการทั้งหมด", "➕ เพิ่มสินค้า", "📝 แก้ไข/ลบ", "🕘 ประวัติ"])
    with tab1:
        st.markdown("<div class='info-card'><div class='card-title'>📋 รายการสินค้าทั้งหมด</div>", unsafe_allow_html=True)
        search_query = st.text_input("ค้นหาสินค้า", placeholder="ค้นหาด้วย SKU ชื่อสินค้า หรือหมวดหมู่")
        filtered_df = df_stock
        if search_query.strip():
            query = search_query.strip().lower()
            searchable = df_stock.fillna("").astype(str).apply(lambda column: column.str.lower())
            filtered_df = df_stock[searchable.apply(lambda row: row.str.contains(query, regex=False).any(), axis=1)]
        st.dataframe(filtered_df, width="stretch", hide_index=True, use_container_width=True)
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Download CSV Report", data=csv, file_name="stock_report.csv", mime="text/csv", width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab2:
        st.markdown("<div class='info-card'><div class='card-title'>เพิ่มสินค้าใหม่เข้าระบบ</div>", unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                new_id = st.text_input("รหัสสินค้า (SKU)", placeholder="เช่น SKU-005")
                new_name = st.text_input("ชื่อสินค้า")
                new_cat = st.selectbox("หมวดหมู่", ["เสื้อ", "กางเกง", "กระโปรง", "เครื่องประดับ"])
            with c2:
                new_price = st.number_input("ราคา (บาท)", min_value=0)
                new_cost = st.number_input("ต้นทุนต่อหน่วย (บาท)", min_value=0)
                new_qty = st.number_input("จำนวนเริ่มต้น", min_value=0)
                new_style = st.selectbox("สไตล์", ["#Minimal", "#CafeOutfit", "#Streetwear", "#Y2K", "#Vintage"])
            if st.form_submit_button("บันทึกข้อมูลลงระบบ", width="stretch"):
                normalized_id = new_id.strip().upper()
                normalized_name = new_name.strip()
                existing_ids = {item['id'].strip().upper() for item in st.session_state.inventory}
                if not normalized_id or not normalized_name:
                    st.warning("กรุณากรอกรหัสสินค้าและชื่อสินค้า")
                elif normalized_id in existing_ids:
                    st.error("รหัสสินค้านี้มีอยู่ในระบบแล้ว")
                else:
                    st.session_state.inventory.append({"id": normalized_id, "name": normalized_name, "category": new_cat, "price": new_price, "cost": new_cost, "qty": new_qty, "style": new_style, "date": datetime.now().strftime('%Y-%m-%d')})
                    save_data(st.session_state.inventory)
                    record_history("เพิ่มสินค้า", normalized_id, f"เพิ่ม {normalized_name} จำนวน {new_qty} ชิ้น")
                    st.success("เพิ่มสินค้าเรียบร้อย!")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with tab3:
        st.markdown("<div class='info-card'><div class='card-title'>แก้ไขข้อมูลหรือปรับสต็อก</div>", unsafe_allow_html=True)
        if not st.session_state.inventory:
            st.warning("ไม่มีข้อมูลสินค้าให้แก้ไข")
        else:
            edit_item_id = st.selectbox("เลือกรหัสสินค้าที่ต้องการแก้ไข", [i['id'] for i in st.session_state.inventory])
            item_to_edit = next((i for i in st.session_state.inventory if i['id'] == edit_item_id), None)
            if item_to_edit:
                with st.form("edit_form"):
                    col_e1, col_e2 = st.columns(2)
                    with col_e1:
                        up_name = st.text_input("แก้ไขชื่อ", value=item_to_edit['name'])
                        up_price = st.number_input("แก้ไขราคา", value=item_to_edit['price'])
                        up_cost = st.number_input("แก้ไขต้นทุนต่อหน่วย", min_value=0, value=item_to_edit.get('cost', 0))
                    with col_e2:
                        up_qty = st.number_input("แก้ไขจำนวน", value=item_to_edit['qty'])
                        style_options = ["#Minimal", "#CafeOutfit", "#Streetwear", "#Y2K", "#Vintage"]
                        current_style = item_to_edit.get('style', style_options[0])
                        up_style = st.selectbox("แก้ไขสไตล์", style_options, index=style_options.index(current_style) if current_style in style_options else 0)
                    c_btn1, c_btn2, c_btn3 = st.columns(3)
                    if c_btn1.form_submit_button("✅ อัปเดตข้อมูล", width="stretch"):
                        for i in st.session_state.inventory:
                            if i['id'] == edit_item_id: i['name'], i['price'], i['cost'], i['qty'], i['style'] = up_name.strip(), up_price, up_cost, up_qty, up_style
                        save_data(st.session_state.inventory)
                        record_history("แก้ไขสินค้า", edit_item_id, f"แก้ไขชื่อ ราคา จำนวน และสไตล์")
                        st.toast("อัปเดตข้อมูลแล้ว")
                        st.rerun()
                    if c_btn2.form_submit_button("➕ เพิ่มสต็อก (+1)", width="stretch"):
                        for i in st.session_state.inventory:
                            if i['id'] == edit_item_id: i['qty'] += 1
                        save_data(st.session_state.inventory)
                        record_history("เพิ่มสต็อก", edit_item_id, "เพิ่มจำนวน 1 ชิ้น")
                        st.rerun()
                    if c_btn3.form_submit_button("➖ ลดสต็อก (-1)", width="stretch"):
                        for i in st.session_state.inventory:
                            if i['id'] == edit_item_id and i['qty'] > 0: i['qty'] -= 1
                        save_data(st.session_state.inventory)
                        record_history("ลดสต็อก", edit_item_id, "ลดจำนวน 1 ชิ้น")
                        st.rerun()
                st.write("---")
                if st.button("🗑️ ลบสินค้านี้ออกจากระบบ", type="secondary"):
                    st.session_state.inventory = [i for i in st.session_state.inventory if i['id'] != edit_item_id]
                    save_data(st.session_state.inventory)
                    record_history("ลบสินค้า", edit_item_id, "ลบสินค้าออกจากระบบ")
                    st.warning("ลบข้อมูลเรียบร้อย")
                    st.rerun()
            else:
                st.error("ไม่พบข้อมูลสินค้า กรุณาเลือกใหม่อีกครั้ง")
        st.markdown("</div>", unsafe_allow_html=True)
    with tab4:
        st.markdown("<div class='info-card'><div class='card-title'>ประวัติการเปลี่ยนแปลงล่าสุด</div>", unsafe_allow_html=True)
        history_df = pd.DataFrame(load_history())
        if history_df.empty:
            st.info("ยังไม่มีประวัติการเปลี่ยนแปลง")
        else:
            st.dataframe(history_df, width="stretch", hide_index=True, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📊 วิเคราะห์ข้อมูล":
    st.markdown("<h2 style='color:#333333 !important;'>Business Intelligence Analytics</h2>", unsafe_allow_html=True)
    if df_stock.empty:
        st.info("ยังไม่มีข้อมูลเพียงพอสำหรับแสดงผลการวิเคราะห์")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("<div class='info-card'><div class='card-title'>สัดส่วนสินค้าแยกตามหมวดหมู่</div>", unsafe_allow_html=True)
            fig1 = px.pie(df_stock, names='category', values='qty', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
            fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_b:
            st.markdown("<div class='info-card'><div class='card-title'>มูลค่าสินค้าตามสไตล์</div>", unsafe_allow_html=True)
            df_stock['total_val'] = df_stock['price'] * df_stock['qty']
            fig2 = px.bar(df_stock, x='style', y='total_val', color='category', text_auto='.2s', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), xaxis_title=None, yaxis_title="มูลค่ารวม (บาท)")
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
