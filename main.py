from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager #!
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty, NumericProperty
from kivy.animation import Animation
from random import randint
from kivy.uix.behaviors import DragBehavior



class menu_scr(Screen):
    anim=Animation(x=randint(0, 100), y=randint(0, 100))
    anim.repeat=True
    start_btn=ObjectProperty()
    setup_btn=ObjectProperty()
    def __init__(self, gamescr, **kwargs):
        super(menu_scr, self).__init__(**kwargs)
        self.game=gamescr
    def float_btn(self, dt):
        self.anim=Animation(x=randint(0, self.width), y=randint(0, self.height), duration=2)
        self.anim.start(self.start_btn)
        self.anim=Animation(x=randint(0, self.width), y=randint(0, self.height), duration=2)
        self.anim.start(self.setup_btn)
    def start_game(self):
        self.manager.current='game'
        #self.manager.get_screen('game').gstart=1
        self.game.gstart=1
        
class setup_scr(Screen):
    pass
    
class enemy(Widget):
    def fall(self):
        Animation(y=100).start(self)
    
class candy(Widget):
    pass
    
class game_scr(Screen):
    score=NumericProperty(0)
    player=ObjectProperty()
    enemy=ObjectProperty()
    grass=ObjectProperty()
    pogo_stck=ObjectProperty()
    pogo_pos_x=str(randint(10, 580))+'dp'
    enemyfall=0
    gstart=0
    
    def right(self):
        pass
    def move_r(self):
        Animation(x=self.player.parent.width-self.player.width-70).start(self.player)
    def move_l(self):
        Animation(x=10).start(self.player)
    def stop(self):
        #Animation.stop(self.player)
        Animation.cancel_all(self.player)
    def update(self, dt):
        if self.enemyfall==0:
            self.enemy.fall()
            self.enemyfall=1
        if self.player.collide_widget(self.pogo_stck) and self.gstart==1:
            self.score+=1
            self.pogo_stck.width/=2
            self.pogo_stck.center_x+=self.pogo_stck.width/2
        if self.score%10==0:
            #self.add_widget(enemy())
            #self.ids.enemy.fall()
            self.score+=1
        if self.player.collide_widget(self.enemy) and self.gstart==1:
            self.manager.current='game over'
            self.score=0
            Animation.cancel_all(self.enemy)
            self.remove_widget(self.enemy)
            self.enemy.pos=(randint(10, self.player.parent.width-self.player.width-70), '800dp')
            self.add_widget(self.enemy)
            self.enemyfall=0
            self.gstart=0
        if self.grass.collide_widget(self.enemy):
            Animation.cancel_all(self.enemy)
            self.remove_widget(self.enemy)
            self.enemy.pos=(randint(10, self.player.parent.width-self.player.width-70), '800dp')
            self.enemy.width=str(randint(10, 100))+'dp'
            self.add_widget(self.enemy)
            self.enemyfall=0
        if abs(self.pogo_stck.width-1)<0.01:
            self.pogo_stck.pos=(randint(10, self.player.parent.width-self.player.width-70), '225dp')
            self.pogo_stck.width=200
            
class gameover_scr(Screen):
    pass
        
        
class DragLabel(DragBehavior, Label):
    pass


class RebelApp(App):
    
    def build(self):
        sm=ScreenManager()
        #menu=menu_scr(name='menu')
        settings=setup_scr(name='settings')
        game=game_scr(name='game')
        game_over=gameover_scr(name='game over')
        menu=menu_scr(gamescr=game, name='menu')
        sm.add_widget(menu)
        sm.add_widget(settings)
        sm.add_widget(game)
        sm.add_widget(game_over)
        Clock.schedule_interval(menu.float_btn, 2)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return sm
        
    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    RebelApp().run()
