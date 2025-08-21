import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
from fpdf import FPDF
import customtkinter as ctk

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

def resimden_pdf_yap(resimler, pdf_adi):
    if not resimler:
        messagebox.showinfo("Bilgi", "Dönüştürülecek resim bulunamadı.")
        return

    pdf = FPDF('P', 'mm', 'A4')
    
    for resim_yolu in resimler:
        try:
            img = Image.open(resim_yolu)
            genislik, yukseklik = img.size
            
            oran = genislik / yukseklik
            a4_genislik_mm = 210
            a4_yukseklik_mm = 297

            if oran > (a4_genislik_mm / a4_yukseklik_mm):
                yeni_genislik = a4_genislik_mm
                yeni_yukseklik = yeni_genislik / oran
            else:
                yeni_yukseklik = a4_yukseklik_mm
                yeni_genislik = yeni_yukseklik * oran

            pdf.add_page()
            x_pozisyonu = (a4_genislik_mm - yeni_genislik) / 2
            y_pozisyonu = (a4_yukseklik_mm - yeni_yukseklik) / 2
            pdf.image(resim_yolu, x=x_pozisyonu, y=y_pozisyonu, w=yeni_genislik, h=yeni_yukseklik)
            
            print(f"'{os.path.basename(resim_yolu)}' resmi PDF'e eklendi.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"'{os.path.basename(resim_yolu)}' işlenirken bir hata oluştu: {e}")
            continue

    try:
        pdf.output(pdf_adi, "F")
        messagebox.showinfo("Başarılı", f"PDF dosyası başarıyla oluşturuldu:\n'{pdf_adi}'")
    except Exception as e:
        messagebox.showerror("Hata", f"PDF kaydedilirken bir hata oluştu: {e}")


class PdfDonusturucuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Resimden PDF'e Dönüştürücü")
        self.geometry("500x350")
        self.resizable(False, False) 

        self.konum = StringVar()
        self.secilen_dosyalar = []
        self.konum.set("Resimlerinizi sürükleyip buraya bırakın veya 'Dosya Yükle' butonunu kullanın.")

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(main_frame, text="PDF Olusturucu Adam", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(10, 20))

        self.drop_area = ctk.CTkFrame(main_frame, fg_color=("gray90", "gray20"))
        self.drop_area.pack(pady=(0, 20), padx=10, fill="both", expand=True)

        self.drop_label = ctk.CTkLabel(self.drop_area, textvariable=self.konum, wraplength=400, justify="center", text_color=("black", "white"), font=ctk.CTkFont(size=14))
        self.drop_label.pack(expand=True)
        
        #self.drop_area.drop_target_register(DND_FILES)
        #self.drop_area.dnd_bind('<<Drop>>', self.surukle_birak)

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        self.dosya_sec_butonu = ctk.CTkButton(button_frame, text="Dosya Yükle", command=self.dosya_sec, font=ctk.CTkFont(size=14, weight="bold"))
        self.dosya_sec_butonu.pack(side="left", padx=10)

        self.donustur_butonu = ctk.CTkButton(button_frame, text="PDF'e Dönüştür", command=self.donustur, font=ctk.CTkFont(size=14, weight="bold"), state="disabled")
        self.donustur_butonu.pack(side="left", padx=10)

        self.temizle_butonu = ctk.CTkButton(button_frame, text="Temizle", command=self.temizle, fg_color="gray", hover_color="gray50", font=ctk.CTkFont(size=14, weight="bold"))
        self.temizle_butonu.pack(side="left", padx=10)

    def dosya_sec(self):
        self.secilen_dosyalar = filedialog.askopenfilenames(
            title="Resim Seçin",
            filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        self.guncelle_arayuz()

    def surukle_birak(self, event):
        dosya_yollari = event.data.replace("{", "").replace("}", "").split()
        self.secilen_dosyalar = [os.path.normpath(yol) for yol in dosya_yollari]
        self.guncelle_arayuz()
    
    def guncelle_arayuz(self):
        if self.secilen_dosyalar:
            self.konum.set(f"{len(self.secilen_dosyalar)} adet dosya seçildi. PDF'e dönüştürmek için butona basın.")
            self.donustur_butonu.configure(state="normal")
        else:
            self.konum.set("Resimlerinizi sürükleyip buraya bırakın veya 'Dosya Yükle' butonunu kullanın.")
            self.donustur_butonu.configure(state="disabled")

    def donustur(self):
        if not self.secilen_dosyalar:
            messagebox.showerror("Hata", "Lütfen önce dönüştürmek istediğiniz resimleri seçin veya sürükleyip bırakın.")
            return

        kaydet_yolu = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Dosyası", "*.pdf")],
            initialfile="yeni_belge.pdf"
        )
        
        if kaydet_yolu:
            resimden_pdf_yap(list(self.secilen_dosyalar), kaydet_yolu)
            self.temizle()

    def temizle(self):
        self.secilen_dosyalar = []
        self.guncelle_arayuz()

if __name__ == "__main__":
    app = PdfDonusturucuApp()
    app.mainloop()
