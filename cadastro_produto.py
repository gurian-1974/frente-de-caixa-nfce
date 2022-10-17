from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox




fundo = 'midnightblue'

root = Tk()
root.title("Cadastro de Produtos")
root.configure(bg=fundo,border=4)
root.geometry("990x690+50+20")
style = ttk.Style()
style.configure('Treeview.Heading',font=('arial',10,'bold'))
cor = 'midnightblue'
letra = "white"
risco = "blue"

conn = sqlite3.connect('Pdv_loja.db')

def alterar_produto():
    desc = str(entry_desc_produto.get()).upper()
    quant = str(entry_QUANT.get()).upper()
    valor = str(entry_VAL_PRODUTO.get()).upper()
    marg = str(entry_MAG_LUCRO.get()).upper()
    domanda = messagebox.askquestion("Cadastro de produtos", " Realmente deseja aterar item ?")
    if domanda == 'yes':
        if desc != "" and quant == "" and valor == "" and marg == "":
            itemSelecionado = tela.selection()[0]
            valores = tela.item(itemSelecionado, "values")
            vid = valores[0]
            alterar = "update Produto_loja SET DESC_PRODUTO = '"+desc+"' where ID_PRODUTO = '" + vid + "'"
            cursor = conn.cursor()
            cursor.execute(alterar)
            conn.commit()
            messagebox.showinfo(" Cadastro de produto", "Item alterado com sucesso")

        if desc == "" and quant != "" and valor == "" and marg == "":
            itemSelecionado = tela.selection()[0]
            valores = tela.item(itemSelecionado, "values")
            vid = valores[0]
            alterar = "update Produto_loja SET QUANT_PRODUTO = '" + quant + "' where ID_PRODUTO = '" + vid + "'"
            cursor = conn.cursor()
            cursor.execute(alterar)
            conn.commit()
            messagebox.showinfo(" Cadastro de produto", "Item alterado com sucesso")

        if desc == "" and quant == "" and valor != "" and marg == "":
            itemSelecionado = tela.selection()[0]
            valores = tela.item(itemSelecionado, "values")
            vid = valores[0]
            alterar = "update Produto_loja SET VALOR_PRODUTO = '" + valor + "' where ID_PRODUTO = '" + vid + "'"
            cursor = conn.cursor()
            cursor.execute(alterar)
            conn.commit()
            messagebox.showinfo(" Cadastro de produto", "Item alterado com sucesso")

        if desc == "" and quant == "" and valor == "" and marg != "":
            itemSelecionado = tela.selection()[0]
            valores = tela.item(itemSelecionado, "values")
            vid = valores[0]
            alterar = "update Produto_loja SET MARG_LUCRO = '" + marg + "' where ID_PRODUTO = '" + vid + "'"
            cursor = conn.cursor()
            cursor.execute(alterar)
            conn.commit()
            messagebox.showinfo(" Cadastro de produto", "Item alterado com sucesso")

def deletar_produtos():
    domanda = messagebox.askquestion("Cadastro de produtos"," Realmente deseja deletar item ?")
    if domanda == 'yes' :
        itemSelecionado = tela.selection()[0]
        valores = tela.item(itemSelecionado, "values")
        vid = valores[0]
        print(vid)
        try:
            deletar = "DELETE FROM Produto_loja where ID_PRODUTO = '"+vid+"'"
            cursor = conn.cursor()
            cursor.execute(deletar)
            conn.commit()
        except:
            messagebox.showinfo(title="ERRO", message=" NAO FOI POSSIVEL DELETAR ")
            return
        #tela.delete((itemSelecionado))
        consultar_produtos()
    else:
        consultar_produtos()

def consultar_produtos():
    cod = str(entry_cod_produto.get()).upper()
    desc = str(entry_desc_produto.get()).upper()
    if cod == "" and desc == "":
        tela.delete(*tela.get_children())
        consultar = ('select * from Produto_loja')
        cursor = conn.cursor()
        cursor.execute(consultar)
        lista = cursor.fetchall()

        for a,b,c,d,e,f,g,h in lista:
            tela.insert("", "end", values=(a, b, c, d, e, f, g))
            tela.focus()

    if cod != "" and desc == "":
        tela.delete(*tela.get_children())
        consultar = ('select * from Produto_loja where COD_PRODUTO = "'+cod+'"')
        cursor = conn.cursor()
        cursor.execute(consultar)
        lista = cursor.fetchall()

        for a, b, c, d, e, f, g, h in lista:
            tela.insert("", "end", values=(a, b, c, d, e, f, g))
            tela.focus()

    if cod == "" and desc != "" :
        tela.delete(*tela.get_children())
        consultar = "select * from Produto_loja where DESC_PRODUTO like '%"+desc+"%'"
        cursor = conn.cursor()
        cursor.execute(consultar)
        lista = cursor.fetchall()

        for a, b, c, d, e, f, g, h in lista:
            tela.insert("", "end", values=(a, b, c, d, e, f, g))
            tela.focus()

def insert_produtos():
    cod = str(entry_cod_produto.get()).upper()
    und = str(entry_UNID.get()).upper()
    desc = str(entry_desc_produto.get()).upper()
    quant = str(entry_QUANT.get()).upper()
    valor = str(entry_VAL_PRODUTO.get()).upper()
    marg = str(entry_MAG_LUCRO.get()).upper()
    if cod == "" and desc == "":
        messagebox.showerror(" Os campos nulos!!!","Favor inserir dados")
        return consultar_produtos()
    insert = f'insert into Produto_loja(COD_PRODUTO,UND_PRODUTO,DESC_PRODUTO,QUANT_PRODUTO,VALOR_PRODUTO,MARG_LUCRO) values("{cod}","{und}","{desc}","{quant}","{valor}","{marg}")'
    cursor = conn.cursor()
    cursor.execute(insert)
    conn.commit()
    messagebox.showinfo(" Cadastro de produtod", "Item inserido com sucesso")
    tela.delete(*tela.get_children())
    comand = ('select * from Produto_loja  order by ID_PRODUTO desc')
    cursor = conn.cursor()
    cursor.execute(comand)
    lista = cursor.fetchall()
    entry_cod_produto.delete(0, END)
    entry_UNID.delete(0, END)
    entry_desc_produto.delete(0, END)
    entry_QUANT.delete(0, END)
    entry_VAL_PRODUTO.delete(0, END)
    entry_MAG_LUCRO.delete(0, END)

    for a, b, c, d, e, f, g, h in lista:
        tela.insert("", "end", values=(a, b, c, d, e, f, g))
        tela.focus()

painel01 = Frame(root,width="990",height="230",bg=cor).pack(anchor=N,side=RIGHT)

Label(painel01,text="CADASTRO DE PRODUTOS",font="arial 20 bold",fg=letra,bg=cor).place(x=20,y=20)
Label(painel01,text="COD_PRODUTO:",font="arial 18 bold",fg=letra,bg=cor).place(x=20,y=90)
Label(painel01,text="DES_PRODUTO:",font="arial 18 bold",fg=letra,bg=cor).place(x=418,y=90)
Label(painel01,text="UNID:",font="arial 18 bold",fg=letra,bg=cor).place(x=20,y=150)
Label(painel01,text="QUANT:",font="arial 18 bold",fg=letra,bg=cor).place(x=175,y=150)
Label(painel01,text="VAL_PRODUTO:",font="arial 18 bold",fg=letra,bg=cor).place(x=350,y=150)
Label(painel01,text="MAG_LUCRO:",font="arial 18 bold",fg=letra,bg=cor).place(x=690,y=150)
entry_cod_produto = Entry(painel01,font="arial 18 bold",width=14)
entry_cod_produto.place(x=220,y=90)
Frame(root,width="186",height=4,bg=risco).place(x=221,y=118)
entry_desc_produto = Entry(painel01,font="arial 18 bold",width=26)
entry_desc_produto.place(x=610,y=90)
Frame(root,width="339",height=4,bg=risco).place(x=611,y=118)
entry_UNID = Entry(painel01,font="arial 18 bold",width=4)
entry_UNID.place(x=100,y=150)
Frame(root,width="52",height=4,bg=risco).place(x=102,y=178)
entry_QUANT = Entry(painel01,font="arial 18 bold",width=4)
entry_QUANT.place(x=280,y=150)
Frame(root,width="52",height=4,bg=risco).place(x=282,y=178)
entry_VAL_PRODUTO = Entry(painel01,font="arial 18 bold",width=10)
entry_VAL_PRODUTO.place(x=550,y=150)
Frame(root,width="130",height=4,bg=risco).place(x=552,y=178)
entry_MAG_LUCRO = Entry(painel01,font="arial 18 bold",width=6)
entry_MAG_LUCRO.place(x=870,y=150)
Frame(root,width="76",height=4,bg=risco).place(x=872,y=178)

Frame(root,width="990",height=2,bg="black").place(x=0,y=220)

inserir = PhotoImage(file="ico/iserte.png")
consultar = PhotoImage(file="ico/consultar.png")
alterar = PhotoImage(file="ico/udade.png")
deletar = PhotoImage(file="ico/Delete-icon.png")

bt01 = Button(root,width=155,image=inserir,height=80,bg="blue",command=insert_produtos,activebackground="lightblue", cursor="hand2",relief="raised")
bt01.place(x=740,y=250)

bt02 = Button(root,width=155,image=alterar,height=80,bg="blue",command=alterar_produto,activebackground="lightblue", cursor="hand2",relief="raised")
bt02.place(x=740,y=340)

bt03 = Button(root,width=155,image=consultar,height=80,bg="blue",command=consultar_produtos,activebackground="lightblue", cursor="hand2",relief="raised")
bt03.place(x=740,y=430)

bt04 = Button(root,width=155,image=deletar,height=80,bg="blue",command=deletar_produtos,activebackground="lightblue", cursor="hand2",relief="raised")
bt04.place(x=740,y=520)

roletay = Scrollbar(root,orient=VERTICAL)
roletay.place(x=683,y=251,width=19,height=364)
tela = ttk.Treeview(root,columns=('id', 'Cod.Produto', 'Unid.', 'Descr. Produto', 'Quant.', 'V.Unit.', 'Mag_lucro'),
                        show='headings',height=17)
tela.column('id', minwidth=0, width=40)
tela.column('Cod.Produto', minwidth=0, width=80)
tela.column('Unid.', minwidth=0, width=40)
tela.column('Descr. Produto', minwidth=0, width=260)
tela.column('Quant.', minwidth=0, width=50)
tela.column('V.Unit.', minwidth=0, width=80)
tela.column('Mag_lucro', minwidth=0, width=80)
tela.heading('id', text='Id')
tela.heading('Cod.Produto', text='Cod.')
tela.heading('Unid.', text='UNID')
tela.heading('Descr. Produto', text='Desc.Produto')
tela.heading('Quant.', text='Quant.')
tela.heading('V.Unit.', text='VALOR')
tela.heading('Mag_lucro', text='Lucro')
tela.place( x=50, y=250)
tela.configure(yscrollcommand=roletay.set)
tela.configure(selectmode="extended")
roletay.configure(command=tela.yview)




root.mainloop()
