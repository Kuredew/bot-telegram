from telethon import TelegramClient, events
from telethon.tl.custom import Button
import asyncio
import backend
import os

SESSION = os.environ['SESSION']
API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']



client = TelegramClient(SESSION, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


'''MAIN BOT'''
@client.on(events.NewMessage(pattern='/start'))
async def home_handler(event, edit=False):
    username = event.chat.username

    userData = backend.User(username)
    if not userData.isInDatabase():
        userData.daftar()
    
    if edit == True:
        await event.edit(backend.baca_file()['welcome'], parse_mode='HTML', buttons=[
            Button.inline('Atur Keuangan', 'keuangan')
        ])
    if edit == False:
        await client.send_message(username, backend.baca_file()['welcome'], parse_mode='HTML', buttons=[
            Button.inline('Atur Keuangan', 'keuangan')
        ])


@client.on(events.CallbackQuery)
async def callback_handler(event):
    username = event.chat.username
    await event.answer()

    userData = backend.User(username)
    if event.data == b'keuangan':
        await event.edit(f'<b>Keuangan Digital V1.0-ALPHA</b>\nby @zeanetstd\n\n<code>Pemasukan   : {userData.totalPemasukan()}\nPengeluaran : {userData.totalPengeluaran()}\nTotal Uang  : {userData.totalUang()}</code>\n\nPilih Fungsi Dibawah Ini.', parse_mode='HTML', buttons=[
            [Button.inline('Tambah Uang', 'tambah'),
            Button.inline('Ambil Uang', 'ambil')],
            [Button.inline('Hapus Akun', 'hapusakun'),
             Button.inline('Riwayat', 'log')],
            [Button.inline('Kembali', 'home')]
        ])

    # Handle Tombol Kembali (home)
    if event.data == b'home':
        await home_handler(event, True)
    
    
    # handle Button pada pesan Keuangan
    if event.data == b'tambah':
        await event.edit('Tambah Uang\n\nMasukkan Nominal yang kamu inginkan.', buttons=[
            [Button.inline('Rp. 5.000', 'tambah5'),
            Button.inline('Rp. 10.000', 'tambah10')],
            [Button.inline('Rp. 20.000', 'tambah20'),
            Button.inline('Custom', 'tambahcustom')]
        ])
    if event.data == b'ambil':
        await event.edit('Ambil Uang\n\nMasukkan Nominal yang kamu inginkan.', buttons=[
            [Button.inline('Rp. 5.000', 'ambil5'),
            Button.inline('Rp. 10.000', 'ambil10')],
            [Button.inline('Rp. 20.000', 'ambil20'),
            Button.inline('Custom', 'ambilcustom')]
        ])


    # Handle pesan tambah
    if event.data == b'tambah5':
        user = backend.User(username)
        user.tambahUang(5000)
        await event.edit('Uang Sebesar Rp. 5.000,- Berhasil ditambah ke data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'tambah10':
        user = backend.User(username)
        user.tambahUang(10000)
        await event.edit('Uang Sebesar Rp. 10.000,- Berhasil ditambah ke data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'tambah20':
        user = backend.User(username)
        user.tambahUang(20000)
        await event.edit('Uang Sebesar Rp. 20.000,- Berhasil ditambah ke data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'tambahcustom':
        user = backend.User(username)
        async with client.conversation(username) as conversation:
            await conversation.send_message('Masukkan Nominal Uang Yang Kamu Ingin Tambah.')

            pesan = await conversation.get_response()
            nominal = int(pesan.text)
            user.tambahUang(nominal)

            formatted = '{:,}'.format(nominal).replace(',', '.')
            uang = str(formatted) + ',-'

            await conversation.send_message(f'Uang Sebesar Rp. {uang} Berhasil ditambah ke data Keuangan.')
            await asyncio.sleep(2)
            await home_handler(event, edit=False)


    # Handle pesan ambil
    if event.data == b'ambil5':
        user = backend.User(username)
        user.keluarUang(5000)
        await event.edit('Uang Sebesar Rp. 5.000,- Berhasil diambil dari data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'ambil10':
        user = backend.User(username)
        user.keluarUang(10000)
        await event.edit('Uang Sebesar Rp. 10.000,- Berhasil diambil dari data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'ambil20':
        user = backend.User(username)
        user.keluarUang(20000)
        await event.edit('Uang Sebesar Rp. 20.000,- Berhasil diambil dari data Keuangan.')
        await asyncio.sleep(2)
        await home_handler(event, True)
    if event.data == b'ambilcustom':
        user = backend.User(username)
        async with client.conversation(username) as conversation:
            await conversation.send_message('Masukkan Nominal Uang Yang Kamu Keluarkan.')

            pesan = await conversation.get_response()
            nominal = int(pesan.text)
            user.keluarUang(nominal)

            formatted = '{:,}'.format(nominal).replace(',', '.')
            uang = str(formatted) + ',-'

            await conversation.send_message(f'Uang Sebesar Rp. {uang} Berhasil diambil dari data Keuangan.')
            await asyncio.sleep(2)
            await home_handler(event, edit=False)


    # Fungsi Hapus Akun
    if event.data == b'hapusakun':
        await event.edit('Apakah Kamu Yakin Ingin Menghapus Akun?', buttons=[
            [Button.inline('Hapus', 'hapusakun-yakin')],
            [Button.inline('Batal', 'home')]
        ])
    if event.data == b'hapusakun-yakin':
        user = backend.User(username)
        user.hapusAkun()

        await event.edit('Akun Berhasil Dihapus. Riwayat dikosongkan!')
        await asyncio.sleep(2)
        await home_handler(event, True)

    # Fungsi Logging
    if event.data == b'log':
        user = backend.User(username)
        log_list = user.cekLog()

        log_str_complete = ''
        for log in log_list:
            nominal = 'Rp. ' + '{:,}'.format(log['nominal']).replace(',', '.') + ',-'
            total = 'Rp. ' + '{:,}'.format(log['total']).replace(',', '.') + ',-'

            log_str = f'{log['date']} ({log['keterangan']})\nNominal : {nominal}\nTotal   : {total}\n\n'

            log_str_complete += log_str

        await event.edit(f'<b>Log Data Keuangan</b>\n\n<code>{log_str_complete}</code>Klik Tombol dibawah ini untuk Kembali.', buttons=[
            Button.inline('Kembali', 'home')
        ], parse_mode='HTML')

        

'''END'''
print('Bot Dijalankan.')
client.run_until_disconnected()
