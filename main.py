import kivy 
kivy.require("1.9.0")
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button 
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.checkbox import CheckBox

Builder.load_file("drop.kv")



class Labelish(ButtonBehavior,Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BoxTarefa(BoxLayout):
    
    def __init__(self, tarefa):
        super().__init__()
        self.descricoes = BoxLayout(orientation="vertical")
        self.botoes = BoxLayout(orientation="vertical")
        self.botoes.size_hint = (0.2, 1)
        

        self.add_widget(self.descricoes)
        self.add_widget(self.botoes)

        self.tarefa = tarefa 

        self.descricoes.add_widget(Label(text=f"Descrição da {tarefa.text}:"))

        self.descricao = Label(text="Edite para acrescentar detalhes...")
        self.descricoes.add_widget(self.descricao)

        self.excluir = Button(text="Excluir")
        self.excluir.bind(on_release= lambda btn: [self.parent.excluindo(self.tarefa)])
        self.botoes.add_widget(self.excluir)
        

        self.editar = Button(text="Editar")
        self.editar.bind(on_press=self.editar_descricao)
        self.botoes.add_widget(self.editar)

        
        # Flag
        self.editando=False


    def editar_descricao(self, instance):
        self.descricoes.remove_widget(self.descricao)

        if not self.editando:
            self.descricao = TextInput()
            self.descricoes.add_widget(self.descricao)
            self.editar.text="Salvar"
            self.editando=True 
        else:
            self.descricao = Label(text="Edite para acrescentar detalhes...")
            self.descricoes.add_widget(self.descricao)
            self.editar.text="Editar"
            self.editando=False




class Lista(BoxLayout):
    aberto = False
    num=0
    new_ids = {}

    def dropping(self, tarefa):

        if Lista.aberto == False:
            self.box_tarefa = BoxTarefa(tarefa)
            index = list(reversed(Lista.new_ids.values())).index(tarefa)
            self.add_widget(self.box_tarefa, index=index)
            Lista.aberto = True 
        else:
            self.remove_widget(self.box_tarefa)
            Lista.aberto = False

    def cadastrar(self, texto):
        texto = texto.strip().title()


        nova_tarefa = Labelish()
        nova_tarefa.text=texto 


        num_id = f"tarefa_{Lista.num}"
        nova_tarefa.id=num_id
        Lista.new_ids[num_id]=nova_tarefa


        self.add_widget(nova_tarefa)
        nova_tarefa.bind(on_release=self.dropping)


        Lista.num+=1


    def excluindo(self, tarefa):
        for key, value in Lista.new_ids.items():
            if tarefa == value:
                key_to_remove = key
        del Lista.new_ids[key_to_remove]
        self.dropping(tarefa)
        self.remove_widget(tarefa)
        print(Lista.new_ids)

    def excluir_tarefas(self):
        for _, value in Lista.new_ids.items():
            self.remove_widget(value)
        Lista.new_ids.clear()







class MainApp(App):
    def build(self):
        return Lista()

MainApp().run()