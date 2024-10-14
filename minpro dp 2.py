import os
from prettytable import PrettyTable
import ast  

Akun_Login = {
    'gfarlz': {'password': 'sigmarizz', 'role': 'admin'},
    'bangmaupesan': {'password': 'hargatemen', 'role': 'pelanggan'},
    'maxverstappen': {'password': 'tututurut', 'role': 'pelanggan'}
}

def Login():
    username = input("ID: ")
    password = input("Password: ")

    if username in Akun_Login and Akun_Login[username]['password'] == password:
        role = Akun_Login[username]['role']
        print(f"berhasil masuk sebagai {role}!")
        return username, role
    else:
        print("Login gagal!")
        return None, None

def tampilkan_menu_pelanggan():
    print("\n==== Menu Custom Hot Wheels (Pelanggan) ====")
    print("1. Order Custom")
    print("2. Liat pesanan")
    print("3. Keluar")
    return input("Pilih Opsi: ")

def tampilkan_menu_admin():
    print("\n==== Menu Custom Hot Wheels (Admin) ====")
    print("1. Tambah pesanan")
    print("2. Liat pesanan")
    print("3. Update pesanan")
    print("4. Hapus pesanan")
    print("5. Keluar")
    return input("Pilih Opsi: ")

def tampilkan_pilihan_Custom():
    print("\n==== Pilihan Customikasi ====")
    print("1. Warna, Ban, Bodykit")
    print("2. Warna, Bodykit")
    print("3. Warna, Ban")
    print("4. Bodykit, Ban")
    print("5. Warna")
    print("6. Ban")
    print("7. Bodykit")
    return input("Pilih Opsi: ")

def isi_detail_Custom(pilihan):
    detail = {}
    if pilihan in ['1', '2', '3', '5']:
        detail['warna'] = input("Isi Warna: ")
    if pilihan in ['1', '3', '4', '6']:
        detail['ban'] = input("Isi Jenis Ban: ")
    if pilihan in ['1', '2', '4', '7']:
        detail['bodykit'] = input("Isi Bodykit: ")
    return detail

def tambah_pesanan(username):
    jenis_hotwheels = input("Jenis Hot Wheels: ")
    pilihan_Custom = tampilkan_pilihan_Custom()
    detail_Custom = isi_detail_Custom(pilihan_Custom)
    catatan_tambahan = input("catatan tambahan: ")

    detail_pesanan = f"{username}|{jenis_hotwheels}|{pilihan_Custom}|{str(detail_Custom)}|{catatan_tambahan}"

    with open('pesanan.txt', 'a') as file:
        file.write(detail_pesanan + "\n")
    print("Order Berhasil!")

def liat_pesanan(username):
    tabel = PrettyTable()
    tabel.field_names = ["Username", "Model Mobil", "Pilihan Custom", "Detail Custom", "Catatan Tambahan"]
    
    if not os.path.exists('pesanan.txt'):
        print("Pesanan Tidak Ada")
        return

    with open('pesanan.txt', 'r') as file:
        for baris in file:
            try:
                data_pesanan = baris.strip().split('|')
                if len(data_pesanan) < 5:
                    data_pesanan.extend([''] * (5 - len(data_pesanan)))
                
                if Akun_Login[username]['role'] == 'admin' or data_pesanan[0] == username:
                    try:
                        detail_Custom = ast.literal_eval(data_pesanan[3])
                        if isinstance(detail_Custom, dict):
                            detail_format = ', '.join([f"{k}: {v}" for k, v in detail_Custom.items()])
                        else:
                            detail_format = "Format salah"
                    except (ValueError, SyntaxError) as e:
                        detail_format = "Error baca detail Custom"
                    
                    tabel.add_row([
                        data_pesanan[0],
                        data_pesanan[1],
                        data_pesanan[2],
                        detail_format,
                        data_pesanan[4]
                    ])
            except Exception as e:
                print(f"Duh, error nih baca data pesanan: {e}")
    
    if tabel.rowcount == 0:
        print("Pesanan tidak ada.")
    else:
        print(tabel)

def update_pesanan():
    jenis_hotwheels = input("Masukan jenis hotwheels yang mau diupdate: ")
    with open('pesanan.txt', 'r') as file:
        semua_baris = file.readlines()

    ketemu = False
    baris_baru = []
    for baris in semua_baris:
        data_pesanan = baris.strip().split('|')
        if len(data_pesanan) < 5:
            data_pesanan.extend([''] * (5 - len(data_pesanan)))
        if data_pesanan[1] == jenis_hotwheels:
            print("data pesanan:")
            print(f"Model: {data_pesanan[1]}")
            print(f"Pilihan Custom: {data_pesanan[2]}")
            print(f"Detail Custom: {data_pesanan[3]}")
            print(f"Catatan Tambahan: {data_pesanan[4]}")
            
            pilihan_Custom = tampilkan_pilihan_Custom()
            detail_Custom = isi_detail_Custom(pilihan_Custom)
            catatan_tambahan = input("Catatan tambahan: ")
            
            detail_pesanan_baru = f"{data_pesanan[0]}|{jenis_hotwheels}|{pilihan_Custom}|{str(detail_Custom)}|{catatan_tambahan}"
            baris_baru.append(detail_pesanan_baru + "\n")
            ketemu = True
            print("Update pesanan berhasil")
        else:
            baris_baru.append(baris)

    if ketemu:
        with open('pesanan.txt', 'w') as file:
            file.writelines(baris_baru)
    else:
        print("Pesanan tidak ada")

def hapus_pesanan():
    jenis_hotwheels = input("Isi pesanan yang mau dihapus: ")
    with open('pesanan.txt', 'r') as file:
        semua_baris = file.readlines()

    ketemu = False
    baris_baru = []
    for baris in semua_baris:
        data_pesanan = baris.strip().split('|')
        if data_pesanan[1] != jenis_hotwheels:
            baris_baru.append(baris)
        else:
            ketemu = True

    if ketemu:
        with open('pesanan.txt', 'w') as file:
            file.writelines(baris_baru)
        print(f"Pesanan custom {jenis_hotwheels} berhasil dihapus!")
    else:
        print("Pesanan tidak ada")

def main():
    if not os.path.exists('pesanan.txt'):
        with open('pesanan.txt', 'w') as file:
            pass  
        
    while True:
        print("\n==== Menu Utama ====")
        print("1. LogIn")
        print("2. Exit")
        pilihan = input("Pilih Opsi: ")

        if pilihan == '1':
            username, role = Login()
            if username:
                if role == 'admin':
                    while True:
                        pilihan_admin = tampilkan_menu_admin()
                        if pilihan_admin == '1':
                            tambah_pesanan(username)
                        elif pilihan_admin == '2':
                            liat_pesanan(username)
                        elif pilihan_admin == '3':
                            update_pesanan()
                        elif pilihan_admin == '4':
                            hapus_pesanan()
                        elif pilihan_admin == '5':
                            print("Berhasil keluar!")
                            break
                        else:
                            print("Opsi tidak ada")
                elif role == 'pelanggan':
                    while True:
                        pilihan_pelanggan = tampilkan_menu_pelanggan()
                        if pilihan_pelanggan == '1':
                            tambah_pesanan(username)
                        elif pilihan_pelanggan == '2':
                            liat_pesanan(username)
                        elif pilihan_pelanggan == '3':
                            print("Berhasil keluar!")
                            break
                        else:
                            print("Opsi tidak ada")
        elif pilihan == '2':
            print("Sampai jumpa!")
            break
        else:
            print("Opsi tidak ada")

if __name__ == "__main__":
    main()
