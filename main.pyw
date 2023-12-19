import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

import platform
from pypdf import PdfMerger
from pathlib import Path
import os
import threading

def make_window():
    root = tkinter.Tk()
    def quit():
        if flag_processing:
            op = tkinter.messagebox.askyesno(title='Still in progress', message='If you quit now, the operation will be aborted.\nDo you want to quit?', icon=tkinter.messagebox.WARNING)
            if not op:
                return
        root.quit()
        exit(0)

    root.title('Processing')
    root.resizable(0, 0)
    root.geometry('250x100')
    root.resizable(0, 0)
    root.protocol('WM_DELETE_WINDOW', quit)
    
    text_var = tkinter.StringVar()
    
    text = tkinter.Label(root, textvariable=text_var)
    text.pack(expand=True)

    style = tkinter.ttk.Style()
    if not platform.system() == 'Darwin':
        style.theme_use('vista')

    button = tkinter.ttk.Button(root, text="Quit", command=quit)
    button.place(relx=1.0, rely=1.0, x=-8, y=-8, anchor="se")

    return text_var, root


if __name__ == '__main__':
    global flag_processing
    flag_processing = False
    pdfs = tkinter.filedialog.askopenfilenames(filetypes=[('PDF Files', ('.pdf'))])
    
    if len(pdfs) == 0:
        pass

    elif len(pdfs) < 2:
        tkinter.messagebox.Message(title='Operation not possible', message='Please select more than one file.').show()
    
    else:
        text_var, root = make_window()
        dots_counter = 0
        def update_idle_indicator():
            global timer, dots_counter
            if not platform.system() == 'Darwin':
                text_var.set(f'Saving{"." * dots_counter}')
            dots_counter = (dots_counter + 1) % 4
            timer = threading.Timer(2, update_idle_indicator)
            timer.start()

        def proceed():
            global flag_processing
            flag_processing = True

            merger = PdfMerger()
            parent_folder = os.path.join(*Path(pdfs[0]).parts[:-1])
            for idx, pdf in enumerate(pdfs):
                name = Path(pdf).parts[-1]

                if not platform.system() == 'Darwin':
                    text_var.set(f'Processing\n{name}')
                merger.append(pdf)

            update_idle_indicator()
            merger.write(os.path.join(parent_folder, f'Merged {len(pdfs)} PDFs.pdf'))
            merger.close()
            timer.cancel()
            if not platform.system() == 'Darwin':
                text_var.set(f'Done. You can close the window.\nSaved in "{parent_folder}"')
            flag_processing = False

        pdf_thread = threading.Thread(target=lambda: proceed())
        pdf_thread.daemon = True
        pdf_thread.start()
        root.mainloop()

