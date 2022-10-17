from tkinter import *
from tkinter import ttk
import sqlite3
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox




fundo = 'midnightblue'

root = Tk()
root.title("Cadastro de Produtos")
root.configure(bg=fundo,border=4)
root.geometry("1080x590+50+20")
style = ttk.Style()
style.configure('Treeview.Heading',font=('arial',12,'bold'),fg="red")
cor = 'black'
letra = "white"
risco = "blue"
fundo = 'midnightblue'

conn = sqlite3.connect('Pdv_loja.db')

fr_menu = Frame(root,bg=cor,width=254,height=690)
fr_menu.place(x=0,y=0)


def consultar_venda_cupon():
    tela2.delete(*tela2.get_children())
    cupon = cod_venda.get()
    print(cupon)
    consultar = ('select * from venda_loja where cod_venda = "'+str(cupon)+'" ')
    cursor = conn.cursor()
    cursor.execute(consultar)
    lista = cursor.fetchall()
    for a, b, c, d, e, f, g, h, i in lista:
        tela2.insert("", "end", values=(a,h, b, c, d, e, f, g))
        tela2.focus()
    tela.delete(*tela.get_children())
    consultar = ('select * from cupon_venda where id_cupon = "'+str(cupon)+'" ')
    cursor = conn.cursor()
    cursor.execute(consultar)
    lista = cursor.fetchall()
    for a, b, c, d, e, f, g, h, i, j, l, m in lista:
        tela.insert("", "end", values=(a, b, c, d, e, f, g, h, i, j, l))
        tela.focus()

def consultar_venda_geral():
        tela2.delete(*tela2.get_children())
        consultar = ('select * from venda_loja desc')
        cursor = conn.cursor()
        cursor.execute(consultar)
        lista = cursor.fetchall()
        for a, b, c, d, e, f, g,h,i  in lista:
            tela2.insert("", "end", values=(a,h, b, c, d, e, f, g))
            tela2.focus()


def consultar_geral():
    tela.delete(*tela.get_children())
    consultar = ('select * from cupon_venda order by id_cupon desc')
    cursor = conn.cursor()
    cursor.execute(consultar)
    lista = cursor.fetchall()
    for a, b, c, d, e, f, g, h,i,j,l,m in lista:
            tela.insert("", "end", values=( a,b,c, d,e, f, g,h,i,j,l))
            tela.focus()

def consultar_periodo():
    data_ini = (callenda_inicio.selection_get())
    data_ter = (callenda_termino.selection_get())
    if data_ini != "" and data_ter != "":

        print(data_ini)
        print(data_ter)
        tela.delete(*tela.get_children())
        consultar = ("SELECT max(id_cupon),sum(v_compra) ,sum(v_pago),sum(v_troco),sum(v_dinheiro),sum(v_debito),sum(v_credito),sum(total_vezes),sum(v_pix) ,sum(v_desconto),max(data_compra)FROM cupon_venda where data_compra between '"+ (str(callenda_inicio.selection_get()))+"' and '"+(str(callenda_termino.selection_get()))+"'")
        cursor = conn.cursor()
        cursor.execute(consultar)
        lista = cursor.fetchall()

        for a, b, c, d, e, f, g, h, i, j, l in lista:

            tela.insert("", "end", values=(a, b, c, d, e, f, g, h, i, j, l))
            tela.focus()



#listapagamento = ["v_dinheiro", "v_debito", "v_credito", "v_pix","v_pago"]
#combo_pagamento = ttk.Combobox(fr_menu, width=19, font="arial 16 bold", values=listapagamento)
#combo_pagamento.set("selecione")
#combo_pagamento.place(x=2, y=436)
lb_calendar = Label(fr_menu,text="Data de Inicio",font="arial 12 bold",fg="white",bg="black")
lb_calendar.place(x=30,y=5)
callenda_inicio = Calendar(fr_menu, background='darkblue',foreground='white', borderwidth=2, year=2022,locale='pt_BR',)
callenda_inicio.place(x=1, y=38)
lb_calendar = Label(fr_menu,text="Data de termino",font="arial 12 bold",fg="white",bg="black")
lb_calendar.place(x=30,y=245)
callenda_termino = Calendar(fr_menu, background='darkblue',foreground='white', borderwidth=2, year=2022,locale='pt_BR',)
callenda_termino.place(x=1, y=280)
bt_teste1 = ttk.Button(root,text="Geral",width=10 ,command=consultar_geral)
bt_teste1.place(x=890,y=240)
bt_teste2 = ttk.Button(root, text="Periodo",width=8,command=consultar_periodo)
bt_teste2.place(x=980,y=240)
titulo_01 = Label(root,text="Extratos de recebimentos",font="arial 18 bold",fg="white",bg=fundo)
titulo_01.place(x=500,y=5)

roletay = Scrollbar(root,orient=VERTICAL)
roletay.place(x=1045,y=40,width=15,height=185)
tela = ttk.Treeview(root,columns=('Cupon','compra', 'v_pago','Troco' ,'v_dinheiro', 'v_debito',
                                  'v_credito','T_vezes', 'v_pix','v_desconto','data'),
                        show='headings',height=8)
tela.column('Cupon', minwidth=0, width=60)
tela.column('compra', minwidth=0, width=70)
tela.column('v_pago', minwidth=0, width=90)
tela.column('Troco', minwidth=0, width=60)
tela.column('v_dinheiro', minwidth=0, width=77)
tela.column('v_debito', minwidth=0, width=70)
tela.column('v_credito', minwidth=0, width=70)
tela.column('T_vezes', minwidth=0, width=70)
tela.column('v_pix', minwidth=0, width=50)
tela.column('v_desconto', minwidth=0, width=85)
tela.column('data', minwidth=0, width=80)
tela.heading('Cupon', text='Cupon')
tela.heading('compra', text='V.Total')
tela.heading('v_pago', text='V.Recebido',anchor=CENTER)
tela.heading('Troco', text='Troco')
tela.heading('v_dinheiro', text='Dinheiro')
tela.heading('v_debito', text='Debito')
tela.heading('v_credito', text='Credito')
tela.heading('T_vezes', text='Vezes')
tela.heading('v_pix', text='Pix')
tela.heading('v_desconto', text='Desconto',anchor=CENTER)
tela.heading('data', text='DATA')
tela.place( x=260, y=40)
tela.configure(yscrollcommand=roletay.set)
tela.configure(selectmode="extended")
roletay.configure(command=tela.yview)

titulo_02 = Label(root,text="Extratos de Vendas",font="arial 18 bold",fg="white",bg=fundo)
titulo_02.place(x=420,y=240)

bt_teste3 = ttk.Button(root,text="Geral",width=10 ,command=consultar_venda_geral)
bt_teste3.place(x=610,y=480)
bt_teste4 = ttk.Button(root, text="Cupon",width=8,command=consultar_venda_cupon)
bt_teste4.place(x=700,y=480)

cod_venda = Entry(fr_menu,width=12,font='arial 14 bold')
cod_venda.place(x=40,y=480)
cod_venda.insert(INSERT, str('Digite o cupon'))
roletay2 = Scrollbar(root,orient=VERTICAL)
roletay2.place(x=803,y=280,width=15,height=185)
tela2 = ttk.Treeview(root,columns=('Item','Cupon','cod_produt', 'unid','produto' ,'quant', 'valor','v_total'),show='headings',height=8)
tela2.column('Item', minwidth=0, width=40)
tela2.column('Cupon', minwidth=0, width=60)
tela2.column('cod_produt', minwidth=0, width=40)
tela2.column('unid', minwidth=0, width=40)
tela2.column('produto', minwidth=0, width=200)
tela2.column('quant', minwidth=0, width=40)
tela2.column('valor', minwidth=0, width=60)
tela2.column('v_total', minwidth=0, width=60)
tela2.heading('Item', text='Item')
tela2.heading('Cupon', text='Cupon')
tela2.heading('cod_produt', text='cod.')
tela2.heading('unid', text='Un.')
tela2.heading('produto', text='Produto')
tela2.heading('quant', text='Qua.')
tela2.heading('valor', text='V.unit')
tela2.heading('v_total', text='V.total')

tela2.place( x=260, y=280)
tela2.configure(yscrollcommand=roletay2.set)
tela2.configure(selectmode="extended")
roletay2.configure(command=tela2.yview)


root.mainloop()