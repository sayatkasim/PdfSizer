import tkinter
from fileinput import filename
from tkinter import filedialog
from PIL import Image
from reportlab.lib.testutils import outputfile
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
from ai import extend_image_to_fit_page

# Global değişkenler
selected_input_path = None
selected_output_path = None

windows = tkinter.Tk()
windows.title("PDF Sizer")
windows.geometry("854x450")

fileLabel = tkinter.Label(windows, text="Düzenlenecek Görseli Seçin")
fileLabel.pack()

def browseFiles():
    global selected_input_path
    selected_input_path = filedialog.askopenfilename(initialdir="/",
                                          title="Görsel Seçin",
                                          filetypes=(("JPG Files","*.jpg"),
                                                     ("PNG Files","*.png"),
                                                     ("All files","*.*")))
    # Change label contents
    if selected_input_path:
        fileLabel.configure(text="File Opened: " + selected_input_path.split("/")[-1])
    return selected_input_path

filesSelected = tkinter.Button(text="Dosyayı Seçin",command=browseFiles)
filesSelected.pack()

outLabel = tkinter.Label(windows, text="Kayıt Yapılacak Dosyayı Seçin")
outLabel.pack()

def selectFile():
    global selected_output_path
    selected_output_path = filedialog.askdirectory()
    if selected_output_path:
        outLabel.configure(text="File Roaded: " + selected_output_path)
    return selected_output_path

outputFile = tkinter.Button(text="Kayıt Yeri Seçin",command=selectFile)
outputFile.pack()

def pdfSizer():
    global selected_input_path, selected_output_path
    
    if not selected_input_path or not selected_output_path:
        tkinter.messagebox.showerror("Hata", "Lütfen önce dosya ve klasör seçiniz!")
        return
        
    sizes = [
        ("8x10", 8 * inch, 10 * inch),
        ("11x14", 11 * inch, 14 * inch),
        ("16x20", 16 * inch, 20 * inch),
        ("18x24", 18 * inch, 24 * inch),
        ("24x36", 24 * inch, 36 * inch)
    ]

    input_folder = os.path.dirname(selected_input_path)  # Seçilen dosyanın klasörünü al
    output_folder = selected_output_path
    os.makedirs(output_folder, exist_ok=True)

    # Sadece seçilen dosyayı işle
    selected_file = os.path.basename(selected_input_path)
    if selected_file.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = selected_input_path
        img = Image.open(img_path)

        for name, width, height in sizes:
            img = extend_image_to_fit_page(img, width, height)
            output_filename = f"{os.path.splitext(selected_file)[0]}_{name}.pdf"
            c = canvas.Canvas(os.path.join(output_folder, output_filename), pagesize=(width, height))
            img_width, img_height = img.size
            img_ratio = img_width / img_height
            page_ratio = width / height

            if img_ratio > page_ratio:
                new_width = width
                new_height = width / img_ratio
            else:
                new_height = height
                new_width = height * img_ratio

            x = (width - new_width) / 2
            y = (height - new_height) / 2
            c.drawImage(img_path, x, y, new_width, new_height)
            c.showPage()
            c.save()
            
    tkinter.messagebox.showinfo("Başarılı", "PDF dönüşümü tamamlandı!")

pdfSizeStarter = tkinter.Button(text="PDF Sizer", command=pdfSizer)
pdfSizeStarter.pack()

windows.mainloop()