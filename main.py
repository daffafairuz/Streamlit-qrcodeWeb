import qrcode
import streamlit as st
from io import BytesIO
import re

st.title("QR Code Generator")
st.subheader("by Dafruz")

# Input URL dan nama file
url = st.text_input("Masukkan URL:", "")
filename = st.text_input("Masukkan nama file:", "")

# Fungsi cek URL valid
def is_valid_url(url: str) -> bool:
    regex = re.compile(
        r'^(https?:\/\/)?'              # http:// atau https:// (opsional)
        r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain
        r'(\/\S*)?$'                    # path opsional
    )
    return re.match(regex, url) is not None

# Tombol generate
if st.button("Generate QR Code"):
    if not is_valid_url(url):
        st.warning("⚠️ Masukkan URL yang valid, contoh: https://www.google.com")
    else:
        # Buat QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Simpan ke buffer (tanpa tulis file dulu)
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Tampilkan gambar dengan ukuran lebih kecil
        st.image(byte_im, caption="QR Code", width=200)

        # Default nama file kalau kosong
        download_name = filename.strip() if filename.strip() else "qrcode"

        # Tombol download
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name=f"{download_name}.png",
            mime="image/png"
        )
