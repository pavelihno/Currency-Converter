from tkinter import * 
import tkinter.ttk as ttk
import tkinter
import xml.dom.minidom
import urllib.request
import datetime
import dateutil.relativedelta
import decimal
from decimal import Decimal
import locale
locale.setlocale(locale.LC_ALL, "ru")
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")

class application:
    def __init__(self, window):
        window.title("Конвертер валют")
        window.geometry("1240x720")          #размер окна
        icon = PhotoImage(file = r"C:\Users\crazy\Desktop\STUDYING\Ознакомительная практика\Тема E\icon.png")   #иконка программы
        window.iconphoto(False, icon)
        self.tab_control = ttk.Notebook(window)
        self.tab1 = ttk.Frame(self.tab_control)   #вкладка Калькулятор валют
        self.tab2 = ttk.Frame(self.tab_control)   #вкладка Динамика курса
        self.tab_control.add(self.tab1, text="Калькулятор валют")
        self.tab_control.add(self.tab2, text="Динамика курса")
        self.tab_control.pack(expand = True, fill=BOTH)

        #вкладка Калькулятор валют
        self.currency_from_name = tkinter.StringVar()   #строчка с названием имеющейся валюты
        self.currency_from = ttk.Combobox(self.tab1, values = self.parse_currency_names(), state = "readonly", 
        width = 42, textvariable = self.currency_from_name)   #комбобокс имеющейся валюты
        self.currency_from.current(11)
        self.currency_from.grid(row = 0, column = 0, pady = 12, padx = 12)

        self.currency_to_name = tkinter.StringVar()   #строчка с названием нужной валюты
        self.currency_to = ttk.Combobox(self.tab1, values = self.parse_currency_names(), state = "readonly", 
        width = 42, textvariable = self.currency_to_name)     #комбобокс нужной валюты
        self.currency_to.current(0)
        self.currency_to.grid(row = 1, column = 0, pady = 12, padx = 12)

        self.currency_from_amount_text = tkinter.StringVar()    #default состояние поля ввода
        self.currency_from_amount_text.set(1.00)
        self.currency_from_amount = ttk.Entry(self.tab1, textvariable = self.currency_from_amount_text)    #поле ввода кол-ва единиц имеющейся валюты
        self.currency_from_amount.grid(row = 0, column = 1, pady = 12, padx = 12)

        self.currency_to_amount_text = tkinter.StringVar()
        self.currency_to_amount = ttk.Label(self.tab1, textvariable = self.currency_to_amount_text)  #поле вывода кол-ва единиц нужной валюты
        self.currency_to_amount.grid(row = 1, column = 1, pady = 12, padx = 12)

        self.convert_button = ttk.Button(self.tab1, text = "Конвертировать", command = self.convert_button_click, width = 30)   #кнопка "Конвертировать"
        self.convert_button.grid(row = 0, column = 2, pady = 12, padx = 12)

        #вкладка Динамика курса

        self.label_valute = ttk.Label(self.tab2, text = "Валюта")   #текстовые надписи
        self.label_valute.grid(row = 0, column = 0, pady = (5, 0),padx = 12)
        self.label_period = ttk.Label(self.tab2, text = "Период")
        self.label_period.grid(row = 0, column = 1, pady = (5, 0), padx = 12)
        self.label_choose_period = ttk.Label(self.tab2, text = "Выбор периода")
        self.label_choose_period.grid(row = 0, column = 2, pady = (5, 0), padx = 12)

        self.currency_trend_name = tkinter.StringVar()  #строчка с названием валюты, для который необходимо построить график
        self.currency_trend = ttk.Combobox(self.tab2, values = self.parse_currency_names()[1:], state = "readonly", 
        width = 20, textvariable = self.currency_trend_name)    #комбобокс валюты, для который необходимо построить график
        self.currency_trend.current(11)
        self.currency_trend.grid(row = 1, column = 0, pady = 5, padx = 12)

        self.build_graph_button = ttk.Button(self.tab2, text = "Построить график", command = self.build_graph_button_click, 
        width = 20) #кнопка "Построить график"
        self.build_graph_button.grid(row = 4, column = 0, pady = 5, padx = 12)
        
        self.period_name = tkinter.StringVar()
        self.period_combobox = ttk.Combobox(self.tab2, width = 20, state = "readonly", postcommand = self.period_combobox_values, 
        textvariable = self.period_name)   #комбобокс выбора периода
        self.period_combobox.grid(row = 1, column = 2, pady = 5, padx = 12)

        self.r_var = tkinter.IntVar()  #объединение радио баттонов для выбора периода
        self.r_var.set(0)
        self.week_radio = ttk.Radiobutton(self.tab2, text = "Неделя", variable = self.r_var, value = 0, command = self.period_combobox_values())
        self.week_radio.grid(row = 1, column = 1, pady = 5, padx = 12, sticky = W)
        self.month_radio = ttk.Radiobutton(self.tab2, text = "Месяц", variable = self.r_var, value = 1, command = self.period_combobox_values())
        self.month_radio.grid(row = 2, column = 1, pady = 5, padx = 12, sticky = W)
        self.quarter_radio =  ttk.Radiobutton(self.tab2, text = "Квартал", variable = self.r_var, value = 2, command = self.period_combobox_values())
        self.quarter_radio.grid(row = 3, column = 1, pady = 5, padx = 12, sticky = W)
        self.year_radio = ttk.Radiobutton(self.tab2, text = "Год", variable = self.r_var, value = 3, command = self.period_combobox_values())
        self.year_radio.grid(row = 4, column = 1, pady = 5, padx = 12, sticky = W)

        self.fig = plt.figure(figsize = (8, 5)) #график
        self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(self.fig, master = self.tab2)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row = 5, column = 3)
        plt.grid()
       
    def convert(self, currency_from_name, currency_to_name):  #перевод из одной валюты в другую
        url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(datetime.datetime.now().strftime("%d/%m/%Y"))
        response = urllib.request.urlopen(url)
        dom = xml.dom.minidom.parse(response)
        dom.normalize()
        valutes = dom.getElementsByTagName("Valute")
        currency_from_value, currency_from_nominal = 0, 0   #стоимость(value) в рублях за кол-во(nominal) имеющейся валюты
        currency_to_value, currency_to_nominal = 0, 0       #стоимость(value) в рублях за кол-во(nominal) нужной валюты
        flag_found_from = True #флаг для поиска currency_from
        flag_found_to = True   #флаг для поиска currency_to
        if (currency_from_name == "Российский рубль"):
            currency_from_value = Decimal(1.0000)
            currency_from_nominal = Decimal(1.0000)
        else:
            for valute in valutes:  #поиск currency_from
                valuteTags = valute.childNodes
                for tag in valuteTags:  #поиск тега Name
                    if (tag.nodeName == "Name"):
                        if (tag.childNodes[0].nodeValue == currency_from_name):
                            flag_found_from = False
                if (flag_found_from): 
                    continue
                for tag in valuteTags:  #поиск тега Value
                    if (tag.nodeName == "Value"):
                        currency_from_value = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
    
                for tag in valuteTags:  #поиск тега Nominal
                    if (tag.nodeName == "Nominal"):
                        currency_from_nominal = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
                break

        if (currency_to_name == "Российский рубль"):
            currency_to_value = Decimal(1.0000)
            currency_to_nominal = Decimal(1.0000)
        else:
            for valute in valutes:  #поиск currency_to
                valuteTags = valute.childNodes
                for tag in valuteTags:  #поиск тега Name
                    if (tag.nodeName == "Name"):
                        if (tag.childNodes[0].nodeValue == currency_to_name):
                            flag_found_to = False
                if (flag_found_to): 
                    continue
                for tag in valuteTags:  #поиск тега Value
                    if (tag.nodeName == "Value"):
                        currency_to_value = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
                for tag in valuteTags:  #поиск тега Nominal
                    if (tag.nodeName == "Nominal"):
                        currency_to_nominal = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
                break
        try:
            return (Decimal(self.currency_from_amount_text.get())*(currency_from_value/currency_from_nominal)/
            (currency_to_value/currency_to_nominal)).quantize(Decimal("1.0000"))
        except decimal.InvalidOperation:
            print("Введены некорректные символы")
            return Decimal("0.0000")

    def parse_currency_names(self):     #возврат названий всех валют
        url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(datetime.datetime.now().strftime("%d/%m/%Y"))
        response = urllib.request.urlopen(url)
        dom = xml.dom.minidom.parse(response)
        dom.normalize()
        valutes = dom.getElementsByTagName("Valute")
        valute_names = ["Российский рубль"]
        for valute in valutes:
            valuteTags = valute.childNodes
            for tag in valuteTags:
                if (tag.nodeName == "Name"):
                    valute_names.append(tag.childNodes[0].nodeValue)
        return valute_names

    def convert_button_click(self):     #кнопка "конвертировать"
        self.currency_to_amount_text.set(self.convert(self.currency_from_name.get(), self.currency_to_name.get()))
    
    def build_graph_button_click(self): #кнопка "построить график"
        self.build_graph()
    
    def build_graph(self):              #построить график
        i = self.r_var.get()
        period_name = self.period_name.get()
        currency_name = self.currency_trend_name.get()  #имя валюты
        x = []
        y = []
        if (i == 0):    #неделя
            day = int(period_name[0:2])             #день выбранного периода
            month = int(period_name[3:5])           #месяц выбранного периода
            year = int(period_name[6:10])           #год выбранного периода
            date = datetime.date(year, month, day)  #дата первого дня выбранного периода
            for i in range(7):
                x.append(str(date.strftime("%d.%m")))
                y.append(self.valute_price(currency_name, date))
                date = date + dateutil.relativedelta.relativedelta(days = 1)

        elif (i == 1):  #месяц
            MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
            month = MONTHS.index(period_name.split(" ")[0]) + 1
            year = int(period_name.split(" ")[1])
            date = datetime.date(year, month, 1)
            month_len = ((date + dateutil.relativedelta.relativedelta(months = 1)) - date).days
            for i in range(14):
                date = datetime.date(year, month, 1 + i * (month_len // 14))
                x.append(str(date.strftime("%d")))
                y.append(self.valute_price(currency_name, date))
            
        elif (i == 2):  #квартал
            QUARTERS = ['I', 'II', 'III', 'IV']
            month = (QUARTERS.index(period_name.split(" ")[0]) + 1) * 3 - 2
            year = int(period_name.split(" ")[2])
            date_start = datetime.date(year, month, 1)
            date_end = date_start + dateutil.relativedelta.relativedelta(months = 3)
            while ((date_end - date_start).days > 0):
                x.append(str(date_start.strftime("%d.%m")))
                y.append(self.valute_price(currency_name, date_start))
                date_start = date_start + dateutil.relativedelta.relativedelta(days = 8)

        elif (i == 3):  #год
            x = ['янв', '', 'фев', ' ', 'март', '  ', 'апр', '   ', 'май', '    ', 'июнь',
                 '     ', 'июль', '      ', 'авг', '       ', 'сен', '        ', 'окт',
                 '         ', 'ноя', '          ', 'дек', '           ']
            year = int(period_name)
            for i in range(1, 13):
                date = datetime.date(year, i, 1)
                y.append(self.valute_price(currency_name, date))    #курс 1 числа месяца
                date = date + dateutil.relativedelta.relativedelta(days = 14)
                y.append(self.valute_price(currency_name, date))    #курс 15 числа месяца
    
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, len(x) - 1)
        plt.plot(x, y)
        plt.grid()
        plt.draw()
    
    def period_combobox_values(self):   #установление значений комбобокса для выбора периода
        i = self.r_var.get()
        values = []
        current_day = datetime.datetime.today()
        if (i == 0):    #неделя
            for i in range(1, 260):
                d = datetime.date(current_day.year, 1, 4) - dateutil.relativedelta.relativedelta(weeks = i)
                week_num = current_day.isocalendar()[1]
                monday = d + datetime.timedelta(weeks=(week_num-1), days=-d.weekday())
                sunday = monday + dateutil.relativedelta.relativedelta(days = 6)
                values.append(str(monday.strftime("%d.%m.%Y")) + " - " + str(sunday.strftime("%d.%m.%Y")))
        elif (i == 1):  #месяц
            for i in range(1, 120):
                d = current_day - dateutil.relativedelta.relativedelta(months = i)
                values.append(str(d.strftime("%B %Y")))
        elif (i == 2):  #квартал
            for i in range(30):
                d = current_day - dateutil.relativedelta.relativedelta(months = 3*i)
                prev_quarter_map = ((4, -1), (1, 0), (2, 0), (3, 0))
                quarter, yd = prev_quarter_map[(d.month - 1) // 3]
                values.append(str(quarter).replace("1", "I").replace("2", "II").replace("3", "III").replace("4", "IV") + " квартал " + str(d.year + yd)) 
        elif (i == 3):  #год
            for i in range(1, 22):
                d = current_day - dateutil.relativedelta.relativedelta(years = i)
                values.append(str(d.strftime("%Y")))
        self.period_combobox['values'] = values
        self.period_combobox.current(0)

    def valute_price(self, currency_name, date):   #стоимость валюты в рублях в введенную дату
        url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + str(date.strftime("%d/%m/%Y"))
        response = urllib.request.urlopen(url)
        dom = xml.dom.minidom.parse(response)
        dom.normalize()
        valutes = dom.getElementsByTagName("Valute")
        currency_value, currency_nominal = 0, 0   #стоимость(value) в рублях за кол-во(nominal) валюты
        flag_found = True   #флаг для поиска currency
        for valute in valutes:  #поиск currency
            valuteTags = valute.childNodes
            for tag in valuteTags:  #поиск тега Name
                if (tag.nodeName == "Name"):
                    if (tag.childNodes[0].nodeValue == currency_name):
                        flag_found = False
            if (flag_found): 
                continue
            for tag in valuteTags:  #поиск тега Value
                if (tag.nodeName == "Value"):
                    currency_value = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
            for tag in valuteTags:  #поиск тега Nominal
                if (tag.nodeName == "Nominal"):
                    currency_nominal = Decimal(tag.childNodes[0].nodeValue.replace(",", "."))
            break
        
        try:
            return (Decimal(currency_value/currency_nominal).quantize(Decimal("1.0000")))
        except decimal.InvalidOperation:
            print("Введены некорректные символы")
            return Decimal("0.00")

window = Tk()
app = application(window)
window.mainloop()
