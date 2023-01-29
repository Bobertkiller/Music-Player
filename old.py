# # Versão 0.2

# from tkinter import *
# from tkinter import filedialog, ttk

# import playsound as ps


# def abra_arquivo():
#     filepath = filedialog.askopenfilename()
#     print(filepath)
#     ps.playsound(filepath)


# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Escolha o audio!").grid(column=0, row=0)
# ttk.Button(frm, text="Open", command=abra_arquivo).grid(
#     column=1, row=0
# )
# ttk.Button(frm, text="Close", command=root.destroy).grid(
#     column=1, row=1
# )
# root.mainloop()


# # Versão 0.1

# from tkinter import *
# from tkinter import filedialog

# import playsound as ps


# def abra_arquivo():
#     filepath = filedialog.askopenfilename()
#     print(filepath)
#     ps.playsound(filepath)


# janela = Tk()
# botao = Button(text="Open", command=abra_arquivo)
# botao.pack()
# janela.mainloop()
