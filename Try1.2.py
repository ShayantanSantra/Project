from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from Login import *
import random
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="root",database="hotel")
cursor = hmdb.cursor(buffered=True)

Builder.load_string('''
<ResTitle>:
    orientation: 'vertical'
    size_hint : 1, .1
    canvas:
        
        Rectangle:
            size : self.size
            pos : self.pos
            source:'Button.jpg'
    Label:
        text : "Resturant"

        color : 0,0,0,1
        bold : True
        italic: True
        font_size : 50
<Orders>:
    canvas:
        Color:
            rgba : 0,1,1,1
        Rectangle:
            size : self.size
            pos : self.pos
<ResMenu>:
    canvas:
        
        Rectangle:
            size : self.size
            pos : self.pos
            source:'Button1.jpg'
                
<Item>:
    canvas:
        Color:
            rgba : 0,1,.5,1
        Rectangle:
            size : self.size
            pos : self.pos
            
            
''')
cartitem = []
nud = False
g_orderid=random.randint(99,1000)
'''class Order(BoxLayout):
    def set(self,item):
        self.rm = False
        self.orientation = 'horizontal'
        self.size_hint = (1,None)
        self.height = 44
        self.name = Label(text = item[0],size_hint = (.4,1))
        self.add_widget(self.name)
        self.quantity = Label(text = str(item[2]),size_hint = (.3,1))
        self.add_widget(self.quantity)
        self.price = Label(text = str(int(item[2]) * int(item[1])),size_hint =(.2,1))
        self.add_widget(self.price)
        self.remove = Button(text = "X",size_hint = (.1,1),on_press = self.removeOrder)
        self.add_widget(self.remove)
        return self

    def removeOrder(self,a):
        self.rm =True'''
class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,x):
        self.title = 'Order status'
        self.content = Label(text = 'Ordered Successfully\n your OrderID is {}'.format(g_orderid))
        self.size_hint = (None,None)
        self.size = (200,200)
class  Orders(BoxLayout):
    global cartitem
    global itemname
    global nud
    global g_order_id
    def set(self):
        
        self.orientation = 'vertical'
        self.size_hint = (.5,1)
        self.padding = (10,10)
        self.spacing = 10
        self.cart = Label(text='View my order',color=(0,0,0,1),size_hint= (1,.1),height=15)
        self.add_widget(self.cart)
        #self.bl = BoxLayout(orientation='horizontal',size_hint =(1,.1),height=50)
        #self.orderid=self.aw(random.randint(99, 1000))
        #self.blo = BoxLayout(orientation='horizontal',size_hint =(1,.1),height=50)
        #self.orderid = self.aw('OrderId')
        #self.itemname = self.aw('Instruction')
        '''self.qtn1 = self.aw('1st Item Qtn.')
        self.itemname2 = self.aw('2nd Item')
        self.qtn2 = self.aw('2nd Item Qtn.')
        self.itemname3 = self.aw('3rd Item')
        self.qtn3 = self.aw('3nd Item Qtn.')
        self.itemname4 = self.aw('4th Item')
        self.qtn4 = self.aw('4nd Item Qtn.')
        self.itemname5 = self.aw('5th Item')
        self.qtn5 = self.aw('5nd Item Qtn.')'''
        self.t_show=TextInput(readonly=True, font_size=14, size_hint=[1, .75], background_color=[1,1,1,.8])
        self.add_widget(self.t_show)
        self.add_widget(Button(text = 'Show',size_hint = (1,.4),on_press = self.show))

        self.o_total = Label(text='Total :',color=(0,0,0,1),size_hint= (1,.1),height=15)
        self.add_widget(self.o_total)
        self.t_total=TextInput(readonly=True, font_size=14, size_hint=[.4, .75], background_color=[1,1,1,.8])
        self.add_widget(self.t_total)
        
        self.t_delete=TextInput(font_size=14, size_hint=[.5, .75], background_color=[1,1,1,.8])
        self.add_widget(self.t_delete)
        self.add_widget(Button(text = 'Delete',size_hint = (.5,.4),on_press = self.delete))

        self.su = SButton()
        self.su.set()
        self.add_widget(self.su)
        self.add_widget(Button(text = 'Back',size_hint = (1,.4),on_press = self.back))
        #self.add_widget(self.sb1)
        self.shown = []
        self.obj = []
        self.bk = False
        nud = False

    def delete(self,a):

        cursor.execute("delete from orderinfo where item_name = '{}' and order_id = {}".format(self.t_delete.text,g_orderid))
        cursor.execute("select item_name from orderinfo where order_id = {}".format(g_orderid))

        #for i in cursor:
            
        self.d=cursor.fetchall()
        #for i in self.d:
        #    self.df += i
        
        self.t_show.text=str(self.df)
        #cursor.close()
        hmdb.commit()
       
    def show(self,a):
        cursor.execute("SELECT i.item_name, m.price FROM ordermenu as m INNER JOIN orderinfo as i ON m.name=i.item_name where order_id = {}".format(g_orderid))
        #SELECT m.item_name, i.price FROM ordermenu as m INNER JOIN orderinfo as i ON m.item_name=i.item_name;
        self.s=cursor.fetchall()
        self.t_show.text=str(self.s)
        
        cursor.execute("select sum(m.price) FROM ordermenu as m INNER JOIN orderinfo as i ON m.name=i.item_name where order_id = {}".format(g_orderid))
        self.c=cursor.fetchall()
        #cursor.close()
        #hmdb.commit()
        
        self.t_total.text=str(self.c)
    def back(self,a):
        self.bk = True
        
    def aw(self,t):
        w = IL()
        w.set(t)
        self.add_widget(w)
        return w

    def getdata(self):
        self.Itemdetails = []
        self.idetails = [self.itemname]
        for i in self.idetails:
            self.Itemdetails.append(i.ti.text)
        return self.Itemdetails


class SButton(BoxLayout):
    # Sign up button and back button
    def set(self):
        self.backtl = False
        self.signupT = False
        self.orientation = 'horizontal'
        self.spacing = 10
        self.b = Button(text = 'Submit order',on_press = self.SubmitOrderButton,font_size=18,size_hint=(.1,.4))
        self.add_widget(self.b)

    def SubmitOrderButton(self,a):
        self.submitorder = True


        
class IL(BoxLayout):
    # Frame which group the label and input for various attributes
    def set(self,t):
        self.t = t
        self.add_widget(Label(text = t + ' : ', font_size=18,color = (0,0,0,1),size_hint=(.3,.5)))
        self.ti = TextInput(hint_text = t,write_tab = False, size_hint=(.45,.9))
        self.add_widget(self.ti)
        
class Item(BoxLayout):
    global cartitem
    global nud
    global g_orderid
    global g_user
    
    def set(self,row):
        self.orientation = 'vertical'
        self.row = row
        self.size_hint = (.3,.2)
        self.name = Button(text=row[0],size_hint=(1,0.5),color = (1,1,1,1),on_press=self.save)
        self.add_widget(self.name)
        self.bl = BoxLayout(orientation = 'horizontal', size_hint = (1,.5))
        self.price = Label(text='Price :'+str(row[1]),size_hint = (.5,1),color = (0,0,0,1))
        self.bl.add_widget(self.price)
        #self.addtocart = Button(text='Add to Card', size_hint = (.5,1))
        #self.bl.add_widget(self.addtocart)
        self.add_widget(self.bl)
        self.result=TextInput(readonly=True, font_size=24, size_hint=[1, .75], background_color=[1,1,1,.8])
        self.add_widget(self.result)
        return self
    
    def save(self,textval):
        #super(Orders,self).set()
        #x=Orders.set(self)
        self.result.text = textval.text
        cursor.execute("insert into orderinfo (username,order_id,item_name) values('{}',{},'{}')".format(g_un,g_orderid,self.result.text))
        hmdb.commit()

    '''def additem(self,a):
        global nud
        similar = False
        nud = True
        if cartitem==[]:
            cartitem.append(list(self.row))
        else:
            for i in range(len(cartitem)):
                if cartitem[i][0]==self.row[0]:
                    cartitem[i][2] +=1
                    similar = True
                    break
                else:
                    similar = False
            if similar == False:
                cartitem.append(list(self.row))'''


class Items(TabbedPanelItem):
    def set(self,text):
        cursor.execute('select * from {}'.format(text))
        row = cursor.fetchone()
        self.sl = StackLayout(orientation = 'lr-tb',padding=(10,10),spacing = 10)
        self.l = []
        i = 0
        while row is not None:
            self.l.append(Item())
            self.l[i] = self.l[i].set(row)
            self.sl.add_widget(self.l[i])
            i += 1
            row = cursor.fetchone()
        self.add_widget(self.sl)
        


class ResMenu(TabbedPanel,BoxLayout):
    def set(self):
        self.orientaion = 'horizontal'
        self.do_default_tab = False
        self.starter = Items(text='Starter')
        self.starter.set('starter')
        self.add_widget(self.starter)
        self.default_tab = self.starter
        self.maincourse = Items(text= 'Main Course')
        self.maincourse.set('maincourse')
        self.add_widget(self.maincourse)
        self.breads = Items(text='Breads')
        self.breads.set('breads')
        self.add_widget(self.breads)
        self.extras = Items(text="Extras")
        self.extras.set('extras')
        self.add_widget(self.extras)


class ResBg(BoxLayout,FloatLayout):
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint = (1,.9)
        self.m = ResMenu()
        self.m.set()
        self.o = Orders()
        self.o.set()
        self.add_widget(self.o)
        self.add_widget(self.m)
        self.o.su.b.on_press = self.getdata
        #self.o.su.back.on_press=self.backtask
        #self.add_widget(self.o,index = 1)

    def getdata(self):
        global g_orderid
        self.o.getdata()
        self.item = self.o.Itemdetails
        #self.X.SL.getdata()
        #self.sl = self.X.SL.SecondListItem
        self.total = self.item 
        self.o.su.back = True
        #self.query = 'INSERT INTO orderinfo VALUES ('
        #for i in range(len(self.total)):
        #    self.query += "'"+self.total[i]+"'"
        #    if i == len(self.total)-1:
        #        self.query = self.query
        #    else:
        #        self.query += ','
        #self.query += ')'
        #cursor.execute(self.query)
        
        self.x=random.randint(99,1000)
        self.g_orderid = self.x
        #self.q = "insert into orderdata1 values ('{}')".format(self.x)
        #cursor.execute(self.q)
        #hmdb.commit()
        self.p = PopUp()
        self.p.set(self.x)
        self.p.open()
        
class ResTitle(BoxLayout):
        # Main title of the Application
    def set(self):
        self.size_hint = (1, .1)
        self.pos_hint = {'top': 1, 'center_x': 0.5}

class ResScreen(Screen,BoxLayout):
    def set(self):
        self.name = "CustResScreen"
        self.orientation = 'vertical'
        self.Ti = ResTitle()
        self.Ti.set()
        self.add_widget(self.Ti)
        self.rb = ResBg()
        self.rb.set()
        self.add_widget(self.rb)
        

class ResScreenM(ScreenManager):
    def set(self):
        self.R = ResScreen()
        self.R.set()
        self.add_widget(self.R)

class ResScreenApp(App):
    def build(self):
        self.s = ResScreenM()
        self.s.set()
        #Clock.schedule_interval(self.s.R.rb.o.up, 1.0 / 60.0)
        inspector.create_inspector(Window, self.s)
        return self.s


if __name__ == '__main__':
    ResScreenApp().run()

