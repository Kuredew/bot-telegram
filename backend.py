import json
from datetime import datetime


DATABASE_FILE = 'database.json'
structure_database = {
    "welcome": "Selamat Datang di Imanuts Bot!\n\nChangelog :\n- Penambahan fungsi keuangan (26 Januari 2025)\n\nSilahkan Pakai",
    "user": {}
}

def baca_file():
    try:
        with open(DATABASE_FILE, 'r') as file:
            return json.loads(file.read())
    except:
        return False
    
def tulis_file(query):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(query, file, indent=4)

# Fungsi Logging
def addLog(username, keterangan, nominal, total):
    structure = {
        "date": datetime.today().strftime('%d-%m-%Y'),
        "keterangan": keterangan,
        "nominal": nominal,
        "total": total
    }

    data = baca_file()
    data['user'][username]['log'].append(structure)

    tulis_file(data)


'''INISIALISASI'''
if not baca_file():
    tulis_file(structure_database)

class User:
    def __init__(self, username):
        self.username = username

    def daftar(self):
        query = {
            "pemasukan": 0,
            "pengeluaran": 0,
            "total": 0,
            "log": []
        }

        data = baca_file()
        data['user'][self.username] = query

        tulis_file(data)

    def hapus(self):
        data = baca_file()
        data['user'].pop(self.username)

        tulis_file(data)

    def cekLog(self):
        data = baca_file()
        print('\n\n')

        log_list = data['user'][self.username]['log']
        for log in log_list:
            print(f"{log['date']} ({log['keterangan']})\nNominal : {log['nominal']}\nTotal : {log['total']}\n\n")
        return log_list

    def isInDatabase(self):
        data = baca_file()
        if self.username in data['user']:
            return True
        else:
            return False
        

    # Fungsi total uang
    def totalUang(self):
        data = baca_file()

        total_uang = data['user'][self.username]['total']
        return "Rp. " + '{:,}'.format(total_uang).replace(',', '.') + ',-'
    
    def totalPemasukan(self):
        data = baca_file()

        total_uang = data['user'][self.username]['pemasukan']
        return "Rp. " + '{:,}'.format(total_uang).replace(',', '.') + ',-'
    
    def totalPengeluaran(self):
        data = baca_file()

        total_uang = data['user'][self.username]['pengeluaran']
        return "Rp. " + '{:,}'.format(total_uang).replace(',', '.') + ',-'
    
    def totalDict(self):
        data = baca_file()

        return data['user'][self.username]
    

    # Fungsi pemasukan dan pengeluaran
    def tambahUang(self, uang):
        data = baca_file()
        
        total_sebelumnya = data['user'][self.username]['total']
        total_setelah_ditambah = total_sebelumnya + uang

        pemasukan_sebelumnya = data['user'][self.username]['pemasukan']
        pemasukan_setelah_ditambah = pemasukan_sebelumnya + uang

        data['user'][self.username]['total'] = total_setelah_ditambah
        data['user'][self.username]['pemasukan'] = pemasukan_setelah_ditambah

        tulis_file(data)
        addLog(self.username, 'Masuk', uang, total_setelah_ditambah)

    def keluarUang(self, uang):
        data = baca_file()

        pengeluaran_sebelumnya = data['user'][self.username]['pengeluaran']
        pengeluaran_setelah_ditambah = pengeluaran_sebelumnya + uang

        total_sebelumnya = data['user'][self.username]['total']
        total_setelah_dikurangi = total_sebelumnya - uang

        data['user'][self.username]['total'] = total_setelah_dikurangi
        data['user'][self.username]['pengeluaran'] = pengeluaran_setelah_ditambah

        tulis_file(data)
        addLog(self.username, 'Keluar', uang, total_setelah_dikurangi)
