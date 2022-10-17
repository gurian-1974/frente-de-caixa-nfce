from tkinter import *
from datetime import datetime
from datetime import date
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import webbrowser

root = Tk()
root.title('FRENTE DE LOJA')
root.iconbitmap('ico/cal.ico')
root.geometry('1360x680')
root.resizable(width=False, height=False)
root.state('zoomed')
root.configure(bg='midnightblue')
logo_sql = PhotoImage(file='ico/sql.png')
style = ttk.Style()
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), fg="red")

calculadorinha1 = PhotoImage(file="ico/calculator.png")
desligar = PhotoImage(file="ico/desligar.png")
cestinha = PhotoImage(file="ico/cestinha.png")
caixa = PhotoImage(file="ico/caixa.png")
logo_shop = PhotoImage(file="ico/Clothes-.png")
master = PhotoImage(file="ico/Master.png")
login = PhotoImage(file="ico/Login.png")
up = PhotoImage(file="ico/Button-up.png")
visa = PhotoImage(file="ico/Visa.png")
cash = PhotoImage(file="ico/cash.png")
barra = PhotoImage(file="ico/barra.png")
sacola = PhotoImage(file="ico/sacola.png")
carrinho = PhotoImage(file="ico/car01.png")
#############################################relogio

def relogio():
    tempo = datetime.now()
    hora = tempo.strftime("%H:%M:%S")
    # dia_semana = tempo.strftime("%A")
    dia = tempo.day
    mes = tempo.strftime("%b")
    ano = tempo.strftime("%Y")
    l1.after(200, relogio)
    l1.config(text=hora)
    l2.config(text=str(dia) + "/" + str(mes) + "/" + str(ano))

conn = sqlite3.connect('Pdv_loja.db')
item = 1
subtotal = []
lista_compra = []  ################imprtante lista de compra e Subtotal variavel global################


#########################################inicio do dia###########################################

def inicio_dia():
    cursor = conn.cursor()
    veri_inicio = "SELECT total_vezes FROM cupon_venda  WHERE (total_vezes = 'caixa aberto')"
    cursor.execute(veri_inicio)
    login = cursor.fetchone()
    print(login)
    try:
        if 'caixa aberto' in login:
            label_cabe_caixa.config(text="Caixa aberto")
            messagebox.showinfo(title='Iniciar dia', message='caixa esta ja esta aberto!')


    except:
        messagebox.showinfo(title='iniciar dia', message='caixa esta sendo aberto')
        cursor.execute("insert into cupon_venda(total_vezes)values('caixa aberto')")
        conn.commit()
        label_cabe_caixa.config(text="Caixa aberto")


##################################inseri no treevie e banco dados####################################################

def inserir_p():
    if entry_codigo_produto.get() == "":
        messagebox.showinfo("Operacao errada!!!", "Insira o codgo do produto")
    global item
    qtda = entry_quantidade_produto.get()
    if entry_quantidade_produto.get() == "":
        qtda = '1'
    dados = entry_codigo_produto.get()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Produto_loja  WHERE COD_PRODUTO = '" + dados + "'")
    lista = cursor.fetchall()
    cursor.execute(
        "UPDATE produto_loja set QUANT_PRODUTO=(QUANT_PRODUTO)-'" + qtda + "' WHERE COD_PRODUTO = '" + dados + "'")
    conn.commit()
    cursor.execute("INSERT INTO venda_loja(COD_PRODUTO,UND_PRODUTO,DESC_PRODUTO,QUANT_PRODUTO,VALOR_PRODUTO)SELECT COD_PRODUTO,UND_PRODUTO,DESC_PRODUTO,QUANT_PRODUTO,(VALOR_PRODUTO)*2 FROM Produto_loja  WHERE COD_PRODUTO = '" + dados + "'")
    conn.commit()
    #cursor.execute("update venda_loja set ID_PRODUTO = '"+str(item)+"'  WHERE COD_PRODUTO = '" + dados + "'")
    #conn.commit()
    entry_quantidade_produto.delete(0, END)
    entry_codigo_produto.delete(0, END)



    for a, b, c, d, e, f, g, h in lista:
        lista_compra.append(lista)
        vuni = 2 * (f)
        vtotal = (int(qtda) * float(vuni))
        subtotal.append(vtotal)
        tela.insert("", "end", values=(item, b, c, d, qtda, vuni, vtotal))
        label_somatotal.config(text=(sum(subtotal)))
        cursor = conn.cursor()
        cursor.execute("SELECT max(id_cupon) FROM cupon_venda ")
        ultimo_cupon = cursor.fetchone()
        #item += 1
        for a in ultimo_cupon:
            v = a
            print(v)
            cursor.execute(
                "UPDATE venda_loja set ID_PRODUTO = '"+str(item)+"',QUANT_PRODUTO='" + qtda + "', V_TOTAL ='" + str(vtotal) + "',cod_venda='" + str(v) + "' WHERE LOCALIZADOR = '0'")
            conn.commit()
            cursor.execute("UPDATE venda_loja set LOCALIZADOR = 'OK' WHERE LOCALIZADOR ='0'")
            conn.commit()
            item += 1

########################################relogio#################################################################

def desligar_do_root_pdv():
    MsgBox = messagebox.askquestion("Frente de Caixa", " Realmente deseja fechar PDV ?")

    if MsgBox == 'yes':

        root.destroy()
    else:
        messagebox.showinfo('Return', 'voce retornara ao PDV')


#######################################################################################################################

def forma_pagamento():

    def verificar_sexta():
        global item
        if item == 1:
            messagebox.showerror("sexto vazio","Deve encher o cesto antes de pagar")
            roote.destroy()

    def desligar_pdv():

        MsgBox = messagebox.askquestion("Frente de Caixa", " Realmente deseja fechar PDV ?")

        if MsgBox == 'yes':
            roote.destroy()
            root.destroy()
        else:
            messagebox.showinfo('Return', 'voce retornara ao PDV')

    def fechar_venda():

        cursor = conn.cursor()
        status_concluido = "SELECT total_vezes FROM cupon_venda  WHERE (total_vezes = 'caixa aberto')"
        cursor.execute(status_concluido)
        login = cursor.fetchone()
        print(login)
        try:
            if 'caixa aberto' in login:
                messagebox.showerror(title='venda nao efetivada', message='Voce deve concluir o pamento!')
                roote.destroy()
                forma_pagamento()

        except:

            cursor.execute("insert into cupon_venda(total_vezes)values('caixa aberto')")
            conn.commit()
            print("inserido")
            subtotal.clear()
            print(len(subtotal))
            print(subtotal)
            roote.destroy()

    def concluir_pamento():
        global item
        cursor = conn.cursor()
        des_porcento = ENTRY_DESCONTO.get()
        v_emdebito = ENTRY_DEBITO.get()
        if v_emdebito == "":
            v_emdebito = 0
        v_emdinheiro = entry_dinheiro.get()
        if v_emdinheiro == "":
            v_emdinheiro = 0
        v_emcredito = ENTRY_CREDITO.get()
        if v_emcredito == "":
            v_emcredito = 0
        v_empix = ENTRY_PIX.get()
        if v_empix == "":
            v_empix = 0
        v_compra = (round(float(sum(subtotal)), 2))
        total_dec = (float(des_porcento) * float(v_compra)) / 100
        v_compra_cdesconto = v_compra - total_dec
        valor_recebido = float(v_emdinheiro) + float(v_emdebito) + float(v_emcredito) + float(v_empix)
        V_faltante = float(valor_recebido) - float(v_compra_cdesconto)
        if V_faltante < 0:
            messagebox.showinfo(f"Valor da compra! R${float(v_compra_cdesconto)}", f" valor a receber! R${V_faltante} ")
            roote.destroy()
            forma_pagamento()
        else:
            des_porcento = ENTRY_DESCONTO.get()
            v_compra = float(sum(subtotal))
            print(des_porcento)
            print(v_compra)
            total_dec = (float(des_porcento) * v_compra) / 100
            troco_apagar = valor_recebido - (v_compra - total_dec)
            v_compra_cdesconto = v_compra - total_dec
            print(v_compra_cdesconto)
            for_pagamento = combo_pagamento.get()
            datahoje = date.today()
            tempo_compra = datetime.now()
            hora_compra = tempo_compra.strftime("%H:%M:%S")
            label_troco.config(text=(round(float(troco_apagar), 2)))  # (text=(round(float(sum(subtotal)),1)))
            label_valor_REBIDO.config(text=valor_recebido)
            label_somatotal.config(text=("0,00"))
            label_valor_desc.config(text=v_compra_cdesconto)
            tela.delete(*tela.get_children())
            cursor.execute("SELECT max(id_cupon) FROM cupon_venda ")
            ultimo_cupon = cursor.fetchone()
            global v
            for a in ultimo_cupon:
                v = a
                print(v)
            cursor.execute("update cupon_venda set  v_compra = '" + (str(v_compra_cdesconto)) + "', v_pago = '" + (str(valor_recebido)) + "', v_troco = '" + (str(round(troco_apagar, 2))) + "' ,v_dinheiro = '" + str(float(v_emdinheiro) - (troco_apagar)) + "',v_debito = '" + str(float(v_emdebito)) + "',v_credito = '" + str(float(v_emcredito)) + "',total_vezes = '" + for_pagamento + "',v_pix = '" + str(float(v_empix)) + "' ,v_desconto = '" + str(total_dec) + "',data_compra = '" + (str(datahoje)) + "',hora_compra = '" + str(hora_compra) + "' where id_cupon = '" + (str(v)) + "'")
            conn.commit()
            entry_dinheiro.delete(0, END)
            ENTRY_PIX.delete(0,END)
            ENTRY_DEBITO.delete(0, END)
            ENTRY_CREDITO.delete(0,END)
            entry_codigo_produto.delete(0, END)
            entry_quantidade_produto.delete(0, END)
            item=1


    def imprimir_cupon():
        data = datetime.now()
        cursor = conn.cursor()
        list_produto = "SELECT * FROM venda_loja where cod_venda = '" + str(v) + "'"
        cursor.execute(list_produto)
        list_01 = cursor.fetchall()

        list_form_pag = "SELECT * FROM cupon_venda where id_cupon = '" + str(v) + "'"
        cursor.execute(list_form_pag)
        list_02 = cursor.fetchall()


        with open(f'{(str(v))}.txt', 'a') as pro:
            pro.write("a|Lojas de roupas Luciano guria da silva me\n"
                              "B|rua: amazonas 55 centro Marilia - sp\n")
            pro.write("\n")
            pro.write("h|item|cod|un|Produto|Qut|v.un|v.Tot\n")
            pro.write("\n")
            print(list_01)
            for a in list_01:
                pro.write(f'{a[0]} {a[1]} {a[2]:<1}{a[3]: <15} {a[4]} {a[5]: <3} {a[6]: <3}\n')

            pro.write("\n")
            for a in list_02:
                pro.write(f'total a pagar  R$ {a[1]}\n')
                pro.write("Formas de pagamento:\n")
                pro.write("\n")
                pro.write(f"total desconto  R$ {a[9]}\n")
                pro.write(f"Dinheiro: R$ {a[4]}\n")
                pro.write(f"Debito: R$ {a[5]}\n")
                pro.write(f"credito: R$ {a[6]} / total parcela {a[7]}\n")
                pro.write(f"Pix: R$ {a[8]}\n")
                pro.write(f"Troco: R$ {a[3]}\n")
                pro.write("\n")


            webbrowser.open(f"{str(v)}.txt")

    verificar_sexta()
    roote = Toplevel()
    roote.title("Pagamento")
    roote.geometry("680x650+5+10")
    roote.configure(bg='slategray')
    bg = 'slategray'

    label_entrada_valor = Label(roote, text="TOTAL A PAGAR", bg=bg, fg='white', font="arial 22 bold")
    label_entrada_valor.place(x=50, y=20)

    label_dinheiro = Label(roote, text="1.DINHEIRO", fg='white', bg=bg, font="arial 12 bold")
    label_dinheiro.place(x=50, y=360)

    entry_dinheiro = Entry(roote, width=10, font="arial 12 bold")
    entry_dinheiro.place(x=50, y=380)
    # entry_dinheiro.insert(INSERT, str(0))

    label_DEBITO = Label(roote, text="2.DEBITO", fg='white', bg=bg, font="arial 12 bold")
    label_DEBITO.place(x=160, y=360)

    ENTRY_DEBITO = Entry(roote, width=10, font="arial 12 bold")
    ENTRY_DEBITO.place(x=160, y=380)
    # ENTRY_DEBITO.insert(INSERT, str(0))

    label_CREDITO = Label(roote, text="3.CREDITO", fg='white', bg=bg, font="arial 12 bold")
    label_CREDITO.place(x=270, y=360)

    ENTRY_CREDITO = Entry(roote, width=10, font="arial 12 bold")
    ENTRY_CREDITO.place(x=270, y=380)
    # ENTRY_CREDITO.insert(INSERT, str(0))

    label_desconto = Label(roote, text=" % DESCONTO", fg='white', bg=bg, font="arial 12 bold")
    label_desconto.place(x=50, y=430)

    ENTRY_DESCONTO = Entry(roote, width=10, font="arial 12 bold")
    ENTRY_DESCONTO.place(x=50, y=480)
    ENTRY_DESCONTO.insert(INSERT, str(0))

    label_pix = Label(roote, text="4.PIX", fg='white', bg=bg, font="arial 12 bold")
    label_pix.place(x=480, y=360)

    ENTRY_PIX = Entry(roote, width=10, font="arial 12 bold")
    ENTRY_PIX.place(x=480, y=380)
    # ENTRY_PIX.insert(INSERT, str(0))

    valor_areceber = Frame(roote, width=220, height=45, bg="white", relief="raised", bd=1)
    valor_areceber.place(x=40, y=60)

    valor_con_desconto = Label(roote, text="VALOR C/ DESCONTO", fg='white', bg=bg, font="arial 22 bold")
    valor_con_desconto.place(x=360, y=20)

    valor_recebiudo = Label(roote, text="VALOR RECEBIDO", fg='white', bg=bg, font="arial 22 bold")
    valor_recebiudo.place(x=50, y=160)

    valor_pago_condec = Frame(roote, width=220, height=45, bg="white", relief="raised", bd=1)
    valor_pago_condec.place(x=380, y=60)

    label_valor_desc = Label(valor_pago_condec, text="00.00", bg='white', fg='black', font="arial 22 bold")
    label_valor_desc.place(x=60, y=0)

    valor_pago = Frame(roote, width=220, height=45, bg="white", relief="raised", bd=1)
    valor_pago.place(x=50, y=220)

    label_valor_REBIDO = Label(valor_pago, text="00.00", bg='white', fg='black', font="arial 22 bold")
    label_valor_REBIDO.place(x=60, y=0)
    # label_valor.config(text=entry_dinheiro.get())


    label_valor_arceber = Label(valor_areceber, text="00.00", bg='white', fg='black', font="arial 22 bold")
    label_valor_arceber.place(x=80, y=0)
    label_valor_arceber.config(text=(round(float(sum(subtotal)), 2)))

    listapagamento = [" A VISTA", "2 x Cartão", "3 X Cartão", "4 X Cartão", "5 X Cartão", "6 X Cartão"]

    combo_pagamento = ttk.Combobox(roote, width=6, font="arial 12 bold", values=listapagamento)
    combo_pagamento.set("A vista")
    combo_pagamento.place(x=385, y=380)

    label_combobox = Label(roote, text=" Nº x", bg=bg, fg='WHITE', font="arial 12 bold")
    label_combobox.place(x=390, y=350)

    valor_troco = Label(roote, text=" TROCO", bg=bg, fg='white', font="arial 22 bold")
    valor_troco.place(x=400, y=160)

    troco = Frame(roote, width=200, height=45, bg="white", relief="raised", bd=1)
    troco.place(x=380, y=220)

    frame_buton = Frame(roote, width=645, height=80, relief="raised", bd=4, bg="black")
    frame_buton.place(x=10, y=550)
    #######################################################boton tela pamento#########################

    fechar_pagamento = Button(roote, text="Receber ", width=10, height=2, fg="white", bg="green",
                              font="arial 12 bold", command=concluir_pamento)
    fechar_pagamento.place(x=50,y=560)

    fechar_pagamento = Button(roote, text="Concluir", width=12, height=2, fg="white", bg="blue",
                              font="arial 12 bold", command=fechar_venda)
    fechar_pagamento.place(x=240,y=560)

    DESLIGAR_PDV = Button(roote, text="ENCERRAR PDV", width=14, height=2, fg="white", bg="red", font="arial 12 bold",
                          command=desligar_pdv)
    DESLIGAR_PDV.place(x=480, y=5060)

    imprimir_cupom = Button(roote, text="Imprimir cupom", width=14, height=2, fg="white", bg="red", font="arial 12 bold",
                            command=imprimir_cupon)
    imprimir_cupom.place(x=480, y=560)

    label_troco = Label(troco, text="00.00", bg='white', fg='black', font="arial 22 bold")
    label_troco.place(x=60, y=0)


######################################### fim top level concluir pagamento      #############################################


#                      conjunto label e entry 01

lb_codigo_produto = Label(root, text="CODIGO PRODUTO", font="arial 22 bold", bg="midnightblue", fg="white")
lb_codigo_produto.place(x=40, y=50)

entry_codigo_produto = Entry(root, width=20, font="arial 22 bold")
entry_codigo_produto.place(x=40, y=100)
root.bind("<Return>",inserir_p)
entry_codigo_produto.focus()

Frame(root, width=322, height=5, bg="blue").place(x=41, y=132)

#                                 conjunto entry e label 2

lb_quantidade_produto = Label(root, text="QUANTIDADE", font="arial 22 bold", bg="midnightblue", fg="white")
lb_quantidade_produto.place(x=40, y=150)

entry_quantidade_produto = Entry(root, width=20, font="arial 22 bold")
entry_quantidade_produto.place(x=40, y=200)

Frame(root, width=322, height=5, bg="blue").place(x=41, y=232)

#                frames
rodape = Frame(root, width=1358, height=60, background="blue")
rodape.place(y=680)

label_cabe = Label(rodape, text="SYSTEM PYTHOM PDV rev.002", font="arial 16 bold", fg="white", bg="blue")
label_cabe.place(x=20, y=20)

l1 = Label(rodape, text="horas", fg="white", bg="blue", font="arial 12 bold")
l1.place(x=1260, y=10)

l2 = Label(rodape, text="data", fg="white", bg="blue", font="arial 12 bold")
l2.place(x=1260, y=30)
relogio()

label_cabe_caixa = Label(rodape, text="Caixa Fechado", font="arial 12 bold", fg="white", bg="blue")
label_cabe_caixa.place(x=1000, y=14)

dysplay = Frame(root, width=658, height=580)
dysplay.pack(anchor=N, side=RIGHT, padx=5, pady=5)

total_frame = Frame(root, width=656, height=80, background="midnightblue")
total_frame.place(x=698, y=590)

label_total = Label(total_frame, text="Total Compra  =   R$", font="arial 22 bold", width=20, fg="white",
                    bg="midnightblue", height=2, relief="flat")
label_total.place(x=40, y=2)

label_somatotal = Label(total_frame, text="0,00", font="arial 22 bold", fg="white", width=0, bg="midnightblue",
                        height=2, relief="flat")
label_somatotal.place(x=370, y=2)

dysplay_logo = Frame(root, width=250, height=320, background="blue")
dysplay_logo.place(x=420, y=50)

lb_logo = Label(dysplay_logo, image=logo_shop, background="blue")
lb_logo.place(x=5, y=30)

lb_TEL = Label(dysplay_logo, text="tel: (14) 2232-8769", background="blue", font="arial 16 bold", fg="white")
lb_TEL.place(x=20, y=290)

#             botoes

bt01 = Button(root, width=155, image=barra, height=80, bg="blue")
bt01.place(x=11, y=586)

bt02 = Button(root, width=155, image=visa, height=80, bg="blue")
bt02.place(x=182, y=586)

bt03 = Button(root, width=155, image=master, height=80, bg="blue")
bt03.place(x=353, y=586)

bt04 = Button(root, width=155, image=up, height=80, bg="blue", command=inicio_dia)
bt04.place(x=525, y=586)

bt05 = Button(root, width=155, image=calculadorinha1, height=80, bg="blue")
bt05.place(x=11, y=486)

bt06 = Button(root, width=155, image=sacola, height=80, bg="blue")
bt06.place(x=182, y=486)

bt07 = Button(root, width=155, image=carrinho, height=80, bg="blue")
bt07.place(x=353, y=486)

bt08 = Button(root, width=155, image=desligar, height=80, bg="blue", command=desligar_do_root_pdv)
bt08.place(x=525, y=486)

bt09 = Button(root, width=155, image=cestinha, height=80, bg="blue", command=inserir_p)
bt09.place(x=40, y=286)

bt10 = Button(root, width=155, image=cash, height=80, bg="blue", command=forma_pagamento)
bt10.place(x=216, y=286)

tela = ttk.Treeview(dysplay,
                    columns=('id', 'Cod.Produto', 'Unid.', 'Descr. Produto', 'Quant.', 'V.Unit.', 'Tot. Compra'),
                    show='headings', height=26)
tela.column('id', minwidth=0, width=40)
tela.column('Cod.Produto', minwidth=0, width=80)
tela.column('Unid.', minwidth=0, width=40)
tela.column('Descr. Produto', minwidth=0, width=260)
tela.column('Quant.', minwidth=0, width=50)
tela.column('V.Unit.', minwidth=0, width=80)
tela.column('Tot. Compra', minwidth=0, width=80)
tela.heading('id', text='Id')
tela.heading('Cod.Produto', text='Cod.')
tela.heading('Unid.', text='UNID')
tela.heading('Descr. Produto', text='Desc.Produto')
tela.heading('Quant.', text='Quant.')
tela.heading('V.Unit.', text='VALOR')
tela.heading('Tot. Compra', text='TOTAL')
tela.pack(padx=10, pady=10)

root.mainloop()
