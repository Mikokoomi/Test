# -*- coding: utf-8 -*-
"""
Created on Sun May 11 09:15:00 2025

@author: Administrator
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime
from tkinter import font
from tkinter import ttk


FILE_NAME = "orders.json"
STAFF_FILE = "staff_users.json"
TRASH_FILE = "trash.json"
HISTORY_FILE = "history.log"
USER_FILE = "users.json"  # File để lưu thông tin người dùng


# ==================== Utils =====================
def load_orders():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_orders(orders):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)

def generate_order_id(orders):
    """Tạo mã đơn hàng duy nhất, dựa vào số lượng đơn hàng hiện tại"""
    if orders:
        max_id = max([int(order["ma_don_hang"][2:]) for order in orders])  # Lấy mã đơn hàng lớn nhất
        return f"DH{max_id + 1:04d}"
    else:
        return "DH0001"
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


# ==================== Đăng nhập =====================
def login_ui():
    def toggle_password():
        if entry_password.cget('show') == '*':
            entry_password.config(show='')
        else:
            entry_password.config(show='*')

    def login():
        user = username.get().strip()
        pw = password.get().strip()

        users = load_users()
        staff_users = {}
        if os.path.exists(STAFF_FILE):
            with open(STAFF_FILE, "r", encoding="utf-8") as f:
                staff_users = json.load(f)
        
        if user == "admin" and pw == "123":
            login_window.destroy()
            main_ui("admin", user)
        elif user in users and users[user]["password"] == pw:
            login_window.destroy()
            main_ui("user", user) if user.isdigit() else main_ui("staff", user)
        elif user in staff_users and staff_users[user]["password"] == pw:
            login_window.destroy()
            main_ui("staff", user)
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")


    login_window = tk.Tk()
    login_window.title("Đăng nhập hệ thống")
    login_window.geometry("700x500")
    login_window.resizable(False, False)
    login_window.configure(bg="#f0f4f7")

    # Canh giữa màn hình
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 350) // 2
    login_window.geometry(f"+{x}+{y}")

    # Font đẹp hơn
    title_font = font.Font(family="Helvetica", size=20, weight="bold")
    label_font = font.Font(family="Arial", size=12)
    entry_font = font.Font(family="Arial", size=12)

    # Tiêu đề
    title_label = tk.Label(login_window, text="Đăng nhập", bg="#f0f4f7", fg="#333333", font=title_font)
    title_label.pack(pady=(30, 20))

    frame_form = tk.Frame(login_window, bg="#f0f4f7")
    frame_form.pack(padx=40, fill="x")

    # Tên đăng nhập
    tk.Label(frame_form, text="Tên người dùng", bg="#f0f4f7", fg="#555555", font=label_font).pack(anchor="w", pady=(0, 5))
    username = tk.StringVar()
    entry_user = tk.Entry(frame_form, textvariable=username, font=entry_font, relief="solid", bd=1)
    entry_user.pack(fill="x", pady=(0, 15))

    # Mật khẩu
    tk.Label(frame_form, text="Mật khẩu", bg="#f0f4f7", fg="#555555", font=label_font).pack(anchor="w", pady=(0, 5))
    password = tk.StringVar()
    entry_password = tk.Entry(frame_form, textvariable=password, font=entry_font, show="*", relief="solid", bd=1)
    entry_password.pack(fill="x", pady=(0, 10))

    # Hiển thị mật khẩu
    chk_show_pw = tk.Checkbutton(frame_form, text="Hiển thị mật khẩu", bg="#f0f4f7", command=toggle_password, font=("Arial", 10), fg="#333")
    chk_show_pw.pack(anchor="w", pady=(0, 20))

    # Nút đăng nhập
    btn_login = tk.Button(login_window, text="Đăng nhập", font=("Arial", 14), bg="#007ACC", fg="white", relief="flat", padx=10, pady=5, command=login)
    btn_login.pack(pady=(0, 30), ipadx=10)
    # Nút đăng ký
    btn_register = tk.Button(login_window, text="Đăng ký", font=("Arial", 14), bg="#007ACC", fg="white", relief="flat", padx=10, pady=5, command=register_ui)
    btn_register.pack(pady=(0, 10))

    # Đặt focus vào ô username để tiện nhập
    entry_user.focus()

    login_window.mainloop()

# ==================== Đăng kí =====================
def register_ui():
    def register():
        phone = entry_phone.get().strip()
        pw = entry_password.get().strip()
        name = entry_name.get().strip()

        if not (phone.isdigit() and len(phone) == 10 and phone.startswith("0")):
            messagebox.showerror("Lỗi", "Số điện thoại không hợp lệ.")
            return
        if not pw or not name:
            messagebox.showerror("Lỗi", "Vui lòng nhập mật khẩu và tên thật.")
            return

        users = load_users()
        staff_users = {}
        if os.path.exists(STAFF_FILE):
            with open(STAFF_FILE, "r", encoding="utf-8") as f:
                staff_users = json.load(f)
        if phone in users:
            messagebox.showerror("Lỗi", "Số điện thoại đã được đăng ký.")
            return

        users[phone] = {
            "password": pw,
            "ten": name
        }
        save_users(users)
        messagebox.showinfo("Thành công", f"Đăng ký thành công cho {name}!")

    register_window = tk.Toplevel()
    register_window.title("Đăng ký tài khoản")
    register_window.geometry("300x250")

    tk.Label(register_window, text="Số điện thoại").pack()
    entry_phone = tk.Entry(register_window)
    entry_phone.pack()

    tk.Label(register_window, text="Mật khẩu").pack()
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack()

    tk.Label(register_window, text="Tên thật").pack()
    entry_name = tk.Entry(register_window)
    entry_name.pack()

    tk.Button(register_window, text="Đăng ký", command=register).pack(pady=10)

# ==================== lịch sử giao dịch và thùng rác =====================
def load_trash():
    if not os.path.exists(TRASH_FILE):
        return []
    with open(TRASH_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_trash(trash):
    with open(TRASH_FILE, "w", encoding="utf-8") as f:
        json.dump(trash, f, indent=4, ensure_ascii=False)
        
def log_history(action, order):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        time_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        line = f"{time_str} - {action}: {order.get('ma_don_hang', '')} - {order.get('ten_khach_hang', '')}\n"
        f.write(line)


# ==================== Giao diện chính =====================
def main_ui(role, username):
    orders = load_orders()
    sort_key = "ma_don_hang"
    reverse_sort = False
    
    def refresh_tree():
        nonlocal sort_key, reverse_sort
        for item in tree.get_children():
            tree.delete(item)
        visible_orders = orders
        if role == "user":
            visible_orders = [o for o in orders if o.get("so_dien_thoai") == username]
        sorted_orders = sorted(visible_orders, key=lambda o: o.get(sort_key, ""), reverse=reverse_sort)
        for i, order in enumerate(sorted_orders):
            tree.insert("", "end", iid=i, values=(
                order["ma_don_hang"],
                order["ten_khach_hang"],
                order["san_pham"],
                order["so_dien_thoai"],
                order["trang_thai"]
            ))
    def show_order_detail(event):
        selected = tree.focus()
        if not selected:
            return
        order = orders[int(selected)]
        detail = "\n".join([f"{k}: {v}" for k, v in order.items()])
        messagebox.showinfo("Chi tiết đơn hàng", detail)

    def add_order():
        def submit_order():
            order = {}
            order["ma_don_hang"] = generate_order_id(orders)  # Sinh mã đơn hàng duy nhất
            order["ten_khach_hang"] = entry_ten.get()
            order["dia_chi"] = entry_dia_chi.get()
            order["san_pham"] = entry_sp.get()
            try:
                order["so_luong"] = int(entry_sl.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")
                return
            order["thoi_gian"] = datetime.now().strftime("%d-%m-%Y %H:%M")
            order["so_dien_thoai"] = entry_sdt.get()
            order["hinh_thuc_thanh_toan"] = combo_tt.get()
            order["trang_thai"] = "xử lý"

            if not (order["so_dien_thoai"].isdigit() and len(order["so_dien_thoai"]) == 10 and order["so_dien_thoai"].startswith("0")):
                messagebox.showerror("Lỗi", "Số điện thoại phải bắt đầu bằng số 0 và gồm đúng 10 chữ số.")
                return

            orders.append(order)
            save_orders(orders)
            refresh_tree()
            add_window.destroy()
            messagebox.showinfo("Thành công", "Đã thêm đơn hàng.")
            log_history("Thêm đơn hàng", order)


        add_window = tk.Toplevel(main_window)
        add_window.title("Thêm đơn hàng")
        add_window.geometry("400x400")

        tk.Label(add_window, text="Tên khách hàng").pack()
        entry_ten = tk.Entry(add_window)
        entry_ten.pack()

        tk.Label(add_window, text="Địa chỉ").pack()
        entry_dia_chi = tk.Entry(add_window)
        entry_dia_chi.pack()

        
        tk.Label(add_window, text="Sản phẩm").pack()
        entry_sp = ttk.Combobox(add_window, values=[
            "Ram", "CPU", "Màn hình", "Chuột", "Bàn Phím", "Laptop", "USB", "Tai nghe"
        ], state="readonly")
        entry_sp.current(0)
        entry_sp.pack()


        tk.Label(add_window, text="Số lượng").pack()
        entry_sl = tk.Entry(add_window)
        entry_sl.pack()

        tk.Label(add_window, text="Số điện thoại").pack()
        entry_sdt = tk.Entry(add_window)
        entry_sdt.pack()

        tk.Label(add_window, text="Hình thức thanh toán").pack()
        combo_tt = ttk.Combobox(add_window, values=["Thanh toán khi nhận hàng", "Thanh toán online"], state="readonly")
        combo_tt.current(0)
        combo_tt.pack()

        tk.Button(add_window, text="Lưu đơn hàng", command=submit_order).pack(pady=10)
        
        
        
        
    
    def set_sort_key(key):
        nonlocal sort_key, reverse_sort
        if sort_key == key:
            reverse_sort = not reverse_sort
        else:
            sort_key = key
            reverse_sort = False
        refresh_tree()



    def delete_order():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một đơn hàng để xóa.")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa?"):
            idx = int(selected)
            order = orders.pop(idx)
            trash.append(order)
            save_orders(orders)
            save_trash(trash)
            refresh_tree()
            log_history("Xóa đơn hàng vào thùng rác", order)
            messagebox.showinfo("Thành công", "Đã chuyển đơn hàng vào thùng rác.")


    def edit_order():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một đơn hàng để chỉnh sửa.")
            return
       
        idx = int(selected)
        order = orders[idx]
       
        def submit_edit():
            try:
                so_luong = int(entry_sl.get())
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")
                return
       
            order["ten_khach_hang"] = entry_ten.get().strip()
            order["dia_chi"] = entry_dia_chi.get().strip()
            order["san_pham"] = entry_sp.get().strip()
            order["so_luong"] = so_luong
            order["so_dien_thoai"] = entry_sdt.get().strip()
            order["hinh_thuc_thanh_toan"] = combo_tt.get()
       
            if not (order["so_dien_thoai"].isdigit() and len(order["so_dien_thoai"]) == 10 and order["so_dien_thoai"].startswith("0")):
                messagebox.showerror("Lỗi", "Số điện thoại phải bắt đầu bằng số 0 và gồm đúng 10 chữ số.")
                return

            save_orders(orders)
            log_history("Chỉnh sửa đơn hàng", order)
            refresh_tree()
            edit_win.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật đơn hàng.")
    
        
        
            
        
        # Giao diện chỉnh sửa
        edit_win = tk.Toplevel(main_window)
        edit_win.title("Chỉnh sửa đơn hàng")
        edit_win.geometry("400x500")
       
        tk.Label(edit_win, text="Tên khách hàng").pack(pady=3)
        entry_ten = tk.Entry(edit_win)
        entry_ten.insert(0, order["ten_khach_hang"])
        entry_ten.pack()
       
        tk.Label(edit_win, text="Địa chỉ").pack(pady=3)
        entry_dia_chi = tk.Entry(edit_win)
        entry_dia_chi.insert(0, order["dia_chi"])
        entry_dia_chi.pack()
       
        
        tk.Label(edit_win, text="Sản phẩm").pack(pady=3)
        entry_sp = ttk.Combobox(edit_win, values=[
            "Ram", "CPU", "Màn hình", "Chuột", "Bàn Phím", "Laptop", "USB", "tai nghe"
        ], state="readonly")
        entry_sp.set(order["san_pham"])
        entry_sp.pack()

       
        tk.Label(edit_win, text="Số lượng").pack(pady=3)
        entry_sl = tk.Entry(edit_win)
        entry_sl.insert(0, order["so_luong"])
        entry_sl.pack()
       
        tk.Label(edit_win, text="Số điện thoại").pack(pady=3)
        entry_sdt = tk.Entry(edit_win)
        entry_sdt.insert(0, order["so_dien_thoai"])
        entry_sdt.pack()
       
        tk.Label(edit_win, text="Thời gian đặt hàng").pack(pady=3)
        tk.Label(edit_win, text=order["thoi_gian"]).pack()
       
        tk.Label(edit_win, text="Hình thức thanh toán").pack(pady=3)
        combo_tt = ttk.Combobox(edit_win, values=["Thanh toán khi nhận hàng", "Thanh toán online"], state="readonly")
        combo_tt.set(order.get("hinh_thuc_thanh_toan", "Thanh toán khi nhận hàng"))
        combo_tt.pack()
       
        tk.Button(edit_win, text="Lưu thay đổi", command=submit_edit).pack(pady=15)
        
    def open_trash():
            trash_win = tk.Toplevel(main_window)
            trash_win.title("Thùng rác")
            trash_win.geometry("700x400")

            trash_tree = ttk.Treeview(trash_win, columns=columns, show="headings")
            for col in columns:
                trash_tree.heading(col, text=col)
                trash_tree.column(col, width=120)
            trash_tree.pack(fill=tk.BOTH, expand=True)

            for i, order in enumerate(trash):
                trash_tree.insert("", "end", iid=i, values=(
                    order["ma_don_hang"],
                    order["ten_khach_hang"],
                    order["san_pham"],
                    order["so_dien_thoai"],
                    order["trang_thai"]
                    ))

            btn_frame = tk.Frame(trash_win)
            btn_frame.pack(pady=10)

            def restore_selected():
                selected = trash_tree.focus()
                if not selected:
                    return
                idx = int(selected)
                order = trash.pop(idx)
                orders.append(order)
                save_orders(orders)
                save_trash(trash)
                trash_win.destroy()
                refresh_tree()
                log_history("Khôi phục đơn hàng", order)
                messagebox.showinfo("Thành công", "Đã khôi phục đơn hàng.")

            def delete_selected_forever():
                selected = trash_tree.focus()
                if not selected:
                    return
                idx = int(selected)
                order = trash.pop(idx)
                save_trash(trash)
                trash_win.destroy()
                log_history("Xóa vĩnh viễn đơn hàng", order)
                messagebox.showinfo("Thành công", "Đã xóa đơn hàng vĩnh viễn.")

            tk.Button(btn_frame, text="Khôi phục", bg="#4CAF50", fg="white", command=restore_selected).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Xóa vĩnh viễn", bg="#F44336", fg="white", command=delete_selected_forever).pack(side=tk.LEFT, padx=5)

      
    
    def logout():
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            main_window.destroy()
        login_ui()


    def update_status():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn một đơn hàng để cập nhật trạng thái.")
            return
   
        idx = int(selected)
        order = orders[idx]
   
        def save_new_status():
            new_status = combo_status.get()
            if new_status:
                order["trang_thai"] = new_status
                log_history("Cập nhật trạng thái", order)
                save_orders(orders)
                refresh_tree()
                status_win.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật trạng thái đơn hàng.")
   
        status_win = tk.Toplevel(main_window)
        status_win.title("Cập nhật trạng thái")
        status_win.geometry("300x150")
   
        tk.Label(status_win, text="Chọn trạng thái mới:").pack(pady=10)
        combo_status = ttk.Combobox(status_win, values=[
            "xử lý",
            "chờ lấy hàng",
            "đang giao hàng",
            "chuẩn bị nhận hàng",
            "đã giao hàng"
        ], state="readonly")
        combo_status.set(order["trang_thai"])
        combo_status.pack(pady=5)
   
        tk.Button(status_win, text="Cập nhật", command=save_new_status).pack(pady=10)
    def manage_staff():
        win = tk.Toplevel()
        win.title("Danh sách nhân viên")
        win.geometry("500x400")

        if not os.path.exists(STAFF_FILE):
            staff_data = {}
        else:
            with open(STAFF_FILE, "r", encoding="utf-8") as f:
                staff_data = json.load(f)

        columns = ("Tên đăng nhập", "Mật khẩu","Tên nhân vien")
        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            for username, info in staff_data.items():
                password = info["password"] if isinstance(info, dict) else info
                ten = info["name"] if isinstance(info, dict) and "name" in info else ""
                tree.insert("", "end", values=(username, password, ten))

        def add_staff():
            new_user = simpledialog.askstring("Thêm nhân viên", "Nhập tên đăng nhập:")
            if not new_user:
                return
            if new_user in staff_data:
                messagebox.showerror("Lỗi", "Tên đã tồn tại.")
                return
            new_pass = simpledialog.askstring("Thêm nhân viên", "Nhập mật khẩu:")
            new_name = simpledialog.askstring("Thêm nhân viên", "Nhập tên nhân viên:")
            if new_pass and new_name:
                staff_data[new_user] = {
                    "password": new_pass,
                    "name": new_name
            }
                with open(STAFF_FILE, "w", encoding="utf-8") as f:
                    json.dump(staff_data, f, indent=4, ensure_ascii=False)
            refresh_tree()


        def delete_staff():
            selected = tree.focus()
            if not selected:
                return
            username = tree.item(selected)["values"][0]
            if messagebox.askyesno("Xác nhận", f"Xóa nhân viên {username}?"):
                del staff_data[username]
                with open(STAFF_FILE, "w", encoding="utf-8") as f:
                    json.dump(staff_data, f, indent=4, ensure_ascii=False)
                refresh_tree()

        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Thêm", bg="#4CAF50", fg="white", command=add_staff).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Xóa", bg="#F44336", fg="white", command=delete_staff).pack(side=tk.LEFT, padx=10)

        refresh_tree()
    
    def show_customers():
        customers = load_users()
        customer_window = tk.Toplevel()
        customer_window.title("Danh sách khách hàng")
        customer_window.geometry("500x400")
    
        tree = ttk.Treeview(customer_window, columns=("SĐT", "Tên"), show="headings")
        tree.heading("SĐT", text="Số điện thoại")
        tree.heading("Tên", text="Tên")
        tree.pack(fill="both", expand=True)

        for phone, info in customers.items():
            ten = info["ten"] if isinstance(info, dict) and "ten" in info else "Không rõ"
            tree.insert("", "end", values=(phone, ten))

    # Khung tìm kiếm
        frame_search = tk.Frame(customer_window)
        frame_search.pack(pady=5)
        tk.Label(frame_search, text="Tìm:").pack(side="left")
        search_entry = tk.Entry(frame_search)
        search_entry.pack(side="left", padx=5)

        def do_search():
            keyword = search_entry.get().lower()
            for item in tree.get_children():
                tree.delete(item)
            for phone, info in customers.items():
                ten = info["ten"] if isinstance(info, dict) and "ten" in info else "Không rõ"
                if keyword in phone.lower() or keyword in ten.lower():
                    tree.insert("", "end", values=(phone, ten))

        tk.Button(frame_search, text="Tìm", command=do_search).pack(side="left")

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Chọn dòng", "Vui lòng chọn khách hàng để xóa.")
                return
            for item in selected:
                values = tree.item(item, "values")
                phone = values[0]
                if phone in customers:
                    del customers[phone]
            save_users(customers)
            messagebox.showinfo("Đã xóa", "Xóa khách hàng thành công.")
            customer_window.destroy()
            show_customers()

        tk.Button(customer_window, text="Xóa khách hàng", command=delete_selected).pack(pady=5)
   
    def search_order():
        result = []

        search_win = tk.Toplevel(main_window)
        search_win.title("Tìm kiếm nâng cao")
        search_win.geometry("400x400")

        tk.Label(search_win, text="Tên khách hàng").pack()
        entry_name = tk.Entry(search_win)
        entry_name.pack()

        tk.Label(search_win, text="Số điện thoại").pack()
        entry_phone = tk.Entry(search_win)
        entry_phone.pack()

        tk.Label(search_win, text="Sản phẩm").pack()

        entry_product = ttk.Combobox(search_win, values=[
            "Ram", "CPU", "Màn hình", "Chuột", "Bàn Phím", "Laptop", "USB", "Tai nghe"
        ], state="readonly")  # readonly giúp người dùng không gõ được sai
        entry_product.set("")  # Giá trị mặc định rỗng để dễ lọc tất cả
        entry_product.pack()


        tk.Label(search_win, text="Trạng thái").pack()
        combo_status = ttk.Combobox(search_win, values=[
            "", "xử lý", "chờ lấy hàng", "đang giao hàng", "chuẩn bị nhận hàng", "đã giao hàng"
        ], state="readonly")
        combo_status.current(0)
        combo_status.pack()

        def perform_search():
            nonlocal result
            name = entry_name.get().strip().lower()
            phone = entry_phone.get().strip()
            product = entry_product.get().strip().lower()
            status = combo_status.get().strip().lower()

            result = []
            for order in orders:
                match_name = name in order["ten_khach_hang"].lower() if name else True
                match_phone = phone in order["so_dien_thoai"] if phone else True
                match_product = product in order["san_pham"].lower() if product else True
                match_status = status == order["trang_thai"].lower() if status else True

                if match_name and match_phone and match_product and match_status:
                    result.append(order)

            if not result:
                messagebox.showinfo("Kết quả", "Không tìm thấy đơn hàng phù hợp.")
                return

            res_win = tk.Toplevel(search_win)
            res_win.title("Kết quả tìm kiếm")
            res_tree = ttk.Treeview(res_win, columns=("Tên", "Sản phẩm", "SĐT", "Trạng thái"), show="headings")
            for col in res_tree["columns"]:
                res_tree.heading(col, text=col)
            res_tree.pack(fill=tk.BOTH, expand=True)

            for order in result:
                res_tree.insert("", "end", values=(
                    order["ten_khach_hang"],
                    order["san_pham"],
                    order["so_dien_thoai"],
                    order["trang_thai"]
                ))

            def export_search_results():
                if not result:
                    messagebox.showwarning("Cảnh báo", "Không có kết quả để xuất.")
                    return
                time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ket_qua_tim_kiem_{time_str}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Thành công", f"Đã lưu kết quả vào file: {filename}")

            tk.Button(res_win, text="Xuất kết quả ra file JSON", command=export_search_results).pack(pady=10)

        tk.Button(search_win, text="Tìm kiếm", command=perform_search).pack(pady=10)

 # Thêm nút xuất file
    
    def export_search_results():
        if not result:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để xuất.")
            return

        time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ket_qua_tim_kiem_{time_str}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Thành công", f"Đã lưu kết quả vào file: {filename}")


    def view_history():
        if not os.path.exists(HISTORY_FILE):
            messagebox.showinfo("Lịch sử giao dịch", "Không có lịch sử nào.")
            return
        
        history_win = tk.Toplevel(main_window)
        history_win.title("Lịch sử giao dịch")
        history_win.geometry("700x500")

        text_box = tk.Text(history_win, wrap="word", font=("Arial", 11), bg="#f8f8f8")
        text_box.pack(fill=tk.BOTH, expand=True)

        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
            text_box.insert(tk.END, log_content)

        text_box.config(state=tk.DISABLED)
    
    def view_saved_searches():
        import glob
        files = glob.glob("ket_qua_tim_kiem_*.json")
        if not files:
            messagebox.showinfo("Thông báo", "Chưa có kết quả tìm kiếm nào được lưu.")
            return
        
        select_win = tk.Toplevel(main_window)
        select_win.title("Chọn file kết quả")
        select_win.geometry("400x200")

        tk.Label(select_win, text="Chọn file để xem kết quả:").pack(pady=10)
        file_listbox = tk.Listbox(select_win)
        file_listbox.pack(fill=tk.BOTH, expand=True, padx=10)

        for f in files:
            file_listbox.insert(tk.END, f)

        def open_selected():
            selected = file_listbox.curselection()
            if not selected:
                return
            filename = file_listbox.get(selected[0])
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            view_win = tk.Toplevel(select_win)
            view_win.title(f"Kết quả: {filename}")
            tree = ttk.Treeview(view_win, columns=("Tên", "Sản phẩm", "SĐT", "Trạng thái"), show="headings")
            for col in tree["columns"]:
                tree.heading(col, text=col)
            tree.pack(fill=tk.BOTH, expand=True)

            for order in data:
                tree.insert("", "end", values=(
                    order["ten_khach_hang"],
                    order["san_pham"],
                    order["so_dien_thoai"],
                    order["trang_thai"]
            ))

        tk.Button(select_win, text="Xem kết quả", command=open_selected).pack(pady=10)

   
    orders = load_orders()
    main_window = tk.Tk()
    main_window.title("Quản lý đơn hàng")
    
    columns = ("Mã ĐH", "Tên KH", "Sản phẩm", "SĐT", "Trạng thái")
    
    tree = ttk.Treeview(main_window, columns=columns, show="headings")
    
    trash = load_trash()
    

    
    # Thiết lập các tiêu đề cột
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Style cho Treeview: nền xanh nhạt
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#d0e7f9",  # xanh nhạt
                    foreground="black",
                    fieldbackground="#d0e7f9",
                    rowheight=25)
    
    # Tạo các tag màu chữ "xanh đậm" cho các hàng theo cột ví dụ (giả lập, thực chất tag áp dụng cả hàng)
    tree.tag_configure("ma_dh", foreground="#0B3C5D")
    tree.tag_configure("ten_kh", foreground="#1D4E89")
    tree.tag_configure("san_pham", foreground="#2E5984")
    tree.tag_configure("sdt", foreground="#3E7CB1")
    tree.tag_configure("trang_thai", foreground="#36648B")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<Double-1>", show_order_detail)

        # Frame chứa phần sắp xếp (nằm phía trên)
    sort_frame = tk.LabelFrame(main_window, text="Sắp xếp theo", padx=10, pady=5)
    sort_frame.pack(pady=10, fill=tk.X)

    tk.Button(sort_frame, text="Mã ĐH", width=12, bg="#32CD32", fg="white", command=lambda: set_sort_key("ma_don_hang")).pack(side=tk.LEFT, padx=5)
    tk.Button(sort_frame, text="Tên KH", width=12, bg="#32CD32", fg="white", command=lambda: set_sort_key("ten_khach_hang")).pack(side=tk.LEFT, padx=5)
    tk.Button(sort_frame, text="Sản phẩm", width=12, bg="#32CD32", fg="white", command=lambda: set_sort_key("san_pham")).pack(side=tk.LEFT, padx=5)
    tk.Button(sort_frame, text="Trạng thái", width=12, bg="#32CD32", fg="white", command=lambda: set_sort_key("trang_thai")).pack(side=tk.LEFT, padx=5)

    # Frame chứa các nút chức năng chính
    button_frame = tk.LabelFrame(main_window, text="Chức năng", padx=10, pady=5)
    button_frame.pack(pady=10, fill=tk.X)

    if role == "admin":
        tk.Button(button_frame, text="Thêm đơn hàng", width=15, bg="#00A5CF", fg="white", command=add_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", width=12, bg="#00A5CF", fg="white", command=delete_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Chỉnh sửa", width=12, bg="#00A5CF", fg="white", command=edit_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cập nhật trạng thái", width=18, bg="#00A5CF", fg="white", command=update_status).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Thùng rác", width=12, bg="#00A5CF", fg="white", command=open_trash).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Lịch sử", width=12, bg="#00A5CF", fg="white", command=view_history).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xem kết quả tìm", width=15, bg="#00A5CF", fg="white", command=view_saved_searches).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Tìm kiếm", width=12, bg="#00A5CF", fg="white", command=search_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Danh sách nhân viên", width=18, bg="#795548", fg="white", command=manage_staff).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Danh sách khách hàng",width=18, bg="#795548", fg="white", command=show_customers).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Đăng xuất", width=12, bg="#9E9E9E", fg="white", command=logout).pack(side=tk.LEFT, padx=5)
        

    elif role == "user":
        tk.Button(button_frame, text="Tìm kiếm", width=12, bg="#00A5CF", fg="white", command=search_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Đăng xuất", width=12, bg="#9E9E9E", fg="white", command=logout).pack(side=tk.LEFT, padx=5)

    elif role == "staff":
        tk.Button(button_frame, text="Cập nhật trạng thái", width=18, bg="#00A5CF", fg="white", command=update_status).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Tìm kiếm", width=12, bg="#00A5CF", fg="white", command=search_order).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Lịch sử", width=12, bg="#00A5CF", fg="white", command=view_history).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xem kết quả tìm", width=15, bg="#00A5CF", fg="white", command=view_saved_searches).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Danh sách nhân viên", width=18, bg="#795548", fg="white", command=manage_staff).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Danh sách khách hàng",width=18, bg="#795548", fg="white", command=show_customers).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Đăng xuất", width=12, bg="#9E9E9E", fg="white", command=logout).pack(side=tk.LEFT, padx=5)
        
    refresh_tree()
    main_window.mainloop()



# ==================== Chạy =====================
login_ui()


