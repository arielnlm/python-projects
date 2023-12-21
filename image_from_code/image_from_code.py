from tkinter import *
from tkinter import filedialog
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from PIL import Image
from io import BytesIO

def generisi_sliku_koda():
    izvorni_kod = text.get("1.0", "end-1c")
    jezik = jezik_var.get()

    try:
        lexer = get_lexer_by_name(jezik, stripall=True)
    except Exception:
        rezultat.config(text="Language not supported.")
        return

    kod = highlight(izvorni_kod, lexer, ImageFormatter(font_size=16, line_numbers=True))
    
    # Dodajte dijalog za izbor direktorijuma i naziva slike
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    
    if file_path:
        slika = Image.open(BytesIO(kod))
        slika.save(file_path)
        rezultat.config(text="Photo saved!")

def odaberi_fajl():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            izvorni_kod = file.read()
        text.delete("1.0", "end")
        text.insert("1.0", izvorni_kod)

# Kreiranje glavnog prozora
prozor = Tk()
prozor.title("Generate photo from code")

# Kreiranje tekstualnog polja za unos koda
text = Text(prozor, width=40, height=10)
text.pack()

# Kreiranje padajućeg menija za izbor jezika
jezik_var = StringVar()
jezik_var.set("python")  # Postavite željeni podrazumevani jezik
jezik_label = Label(prozor, text="Choose language:")
jezik_label.pack()
jezik_menu = OptionMenu(prozor, jezik_var, "python", "c", "java", "javascript")
jezik_menu.pack()

# Dugme za generisanje slike
generisi_dugme = Button(prozor, text="Generate photo", command=generisi_sliku_koda)
generisi_dugme.pack()

# Dugme za odabir fajla
odaberi_dugme = Button(prozor, text="Choose file with code", command=odaberi_fajl)
odaberi_dugme.pack()

# Rezultat generisanja slike
rezultat = Label(prozor, text="", fg="green")
rezultat.pack()

prozor.mainloop()
