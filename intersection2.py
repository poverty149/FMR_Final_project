import random
import time
import threading
import pygame
import sys
import math


pygame.init()
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)
G=(0,255,0)
YELLOW=(255,0,255)
speed=2.5
SW=500
SH=720
offset_w=55
offset_h=50
screenSize=(SW,SH)
x_l=0
x_r=100
y_bot=0
y_top=100
track={0:'left',1:'right',2:'up',3:'down'}
track_no=3
signals=['off','left','right']
intersection={'left':[],'right':[],'down':[],'up':[]}
x={0:0,1:SW-10,2:SW/2-20,3:SW/2+10}
y={0:SH/2-offset_h/2,1:SH/2+5,2:SH-30,3:0}
direction = {0:'left', 1:'right', 2:'down', 3:'up'}
vehicles={'left':[],'right':[],'down':[],'up':[]}
stoppingGap=15
movingGap=15
arrivedStop={'left':(None,None),'right':(None,None),'down':(None,None),'up':(None,None)}
defaultStop={'right': SW/2+1*offset_w, 'down': SH/2+1*offset_h, 'left': SW/2-1*offset_w, 'up': SH/2-1*offset_h}
queue=[]
state={'left':{'off':1,'right':2,'left':3},'right':{'off':4,'right':5,'left':6},'down':{'off':7,'right':8,'left':9},'up':{'off':10,'right':11,'left':12},}
def state(dir_no,sig):
    if(sig=='off'):
        num=0
    elif(sig=='left'):
        num=1
    else:
        num=2
    return dir_no*3+num

states_col ={0:{'a':1,'b':1,'c':0,'d':0},1:{'a':0,'b':0,'c':0,'d':0},2:{'a':1,'b':1,'c':1,'d':0},3:{'a':0,'b':0,'c':1,'d':1},
4:{'a':0,'b':0,'c':0,'d':0},5:{'a':1,'b':0,'c':1,'d':1},6:{'a':1,'b':0,'c':0,'d':1},7:{'a':0,'b':0,'c':0,'d':0},
8:{'a':1,'b':1,'c':0,'d':1},9:{'a':0,'b':1,'c':1,'d':0},10:{'a':0,'b':0,'c':0,'d':0},11:{'a':0,'b':1,'c':1,'d':1}}
avoid_col={'a':0,'b':0,'c':0,'d':0}

def avoid():
    avoid_col['a']=0
    avoid_col['b']=0    
    avoid_col['c']=0
    avoid_col['d']=0


    for i in intersection[direction[track_no]]:
        if(states_col[i.state]['a']==1):
            avoid_col['a']=1
        if(states_col[i.state]['b']==1):
            avoid_col['b']=1
        if(states_col[i.state]['c']==1):
            avoid_col['c']=1
        if(states_col[i.state]['d']==1):
            avoid_col['d']=1
def cmp_conf(state,avoid_col):
    if(avoid_col['a']==1 and states_col[state]['a']==1):
        return False
    if(avoid_col['b']==1 and states_col[state]['b']==1):
        return False
    if(avoid_col['c']==1 and states_col[state]['c']==1):
        return False
    if(avoid_col['d']==1 and states_col[state]['d']==1):
        return False
    return True

class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        super(Vehicle,self).__init__()
        width = 20
        height = 20
        self.image =  pygame.Surface([width,height])

        #Create a car
        self.image.fill(RED)
        # self.image.set_colorkey(RED)
        # pygame.draw.rect(self.image, G, [0, 40, width, height])
        self.rect = self.image.get_rect()
        
        self.length=4
        
        

        self.signal=random.choice(signals)
        self.lane=random.randint(0,4)
        self.speed=speed
        self.direction_number=random.randint(0,3)
        self.x=x[self.direction_number]
        self.y=y[self.direction_number]
        self.direction=direction[self.direction_number]
        self.state=state(self.direction_number,self.signal)
        # print(self.state)

        
        vehicles[self.direction].append(self)
        # self.start=
        # self.goal=
        self.intersection=False
        self.stop=False
        self.crossed=0
        self.steering=0
        self.junction_index=None
        self.index=len(vehicles[self.direction])-1
        if(len(vehicles[self.direction])>1 and vehicles[self.direction][self.index-1].crossed==0):
            if(self.direction=='right'):
                self.stop=vehicles[self.direction][self.index-1].stop+vehicles[self.direction][self.index-1].image.get_rect().width+stoppingGap
            elif(self.direction=='left'):
                self.stop=vehicles[self.direction][self.index-1].stop-vehicles[self.direction][self.index-1].image.get_rect().width-stoppingGap
            elif(self.direction=='up'):
                self.stop=vehicles[self.direction][self.index-1].stop+vehicles[self.direction][self.index-1].image.get_rect().height+stoppingGap
            elif(self.direction=='down'):
                self.stop=vehicles[self.direction][self.index-1].stop-vehicles[self.direction][self.index-1].image.get_rect().height-stoppingGap
        else:
            self.stop = defaultStop[self.direction]
            self.junction_index=self.index-1
            queue.append([self,clock])




        sprites_list.add(self)
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    

    def update(self):
        if(self.direction=='right'):
            if(self.x<defaultStop['left'] or self.y<defaultStop['up'] or self.y>defaultStop['down']):
                 self.crossed=1
                 self.intersection=False
                 intersection['right'].remove(self)
            # if(track[track_no]=='right'):
            if(self.x<defaultStop['right']):
                self.intersection=True
                intersection['right'].append(self)
            if(defaultStop['right']+5>self.x>defaultStop['right']):
                arrivedStop['right']=(pygame.time.get_ticks(),self.index)
                if(track[track_no]=='right'):
                    avoid()
                if(track[track_no]!='right' and cmp_conf(self.state,avoid_col)):
                    self.x-=self.speed
                # print(arrivedStop['right'])
            if(self.x>=defaultStop['right'] and (self.x>vehicles[self.direction][self.index-1].x+vehicles[self.direction][self.index-1].image.get_rect().width+stoppingGap or self.index==0)):
                self.x-=self.speed
            elif(track[track_no]=='right' and self.x+self.image.get_rect().width>=defaultStop['right']):
                self.x-=self.speed
            elif(defaultStop['right']>self.x+self.image.get_rect().width>=defaultStop['right']-5):
                
                if(track[track_no]=='right'):
                    self.x-=self.speed
            elif(defaultStop['right']-5>self.x+self.image.get_rect().width>=defaultStop['right']-55):
                if(self.signal=='left'):
                    self.y+=self.speed
                else:
                    self.x-=self.speed
            elif(defaultStop['right']-55>self.x+self.image.get_rect().width>=defaultStop['left']):
                if(self.signal=='right'):
                    self.y-=self.speed
                else:
                    self.x-=self.speed
            elif(self.x+self.image.get_rect().width<=defaultStop['left']):
                self.x-=self.speed
        elif(self.direction=='left'):
            if(self.x>defaultStop['right'] or self.y<defaultStop['up'] or self.y>defaultStop['down']):
                 self.crossed=1
                 self.intersection=False
                 intersection['left'].remove(self)
            if(self.x>defaultStop['left']):
                self.intersection=True
                intersection['left'].append(self)
            if(defaultStop['left']-5<self.x+self.image.get_rect().width<defaultStop['left']):
                arrivedStop['left']=(pygame.time.get_ticks(),self.index)
                if(track[track_no]=='left'):
                    avoid()
                if(track[track_no]!='left' and cmp_conf(self.state,avoid_col)):
                    self.x+=self.speed
            # if(track[track_no]=='right'):
            if(self.x+self.image.get_rect().width<=defaultStop['left'] and (self.x+self.image.get_rect().width<vehicles[self.direction][self.index-1].x-stoppingGap or self.index==0)):
                self.x+=self.speed
            elif(track[track_no]=='left' and self.x<=defaultStop['left']):
                self.x+=self.speed
            elif(defaultStop['left']<self.x<=defaultStop['left']+5):
                if(track[track_no]=='left'):
                    self.x+=self.speed
            elif(defaultStop['left']+5<self.x<=defaultStop['left']+55):
                if(self.signal=='left'):
                    self.y-=self.speed
                else:
                    self.x+=self.speed
            elif(defaultStop['left']+55<self.x<=defaultStop['right']):
                if(self.signal=='right'):
                    self.y+=self.speed
                else:
                    self.x+=self.speed
            elif(self.x>defaultStop['right']):
                self.x+=self.speed
        elif(self.direction=='up'):
            if(self.x>defaultStop['right'] or self.x<defaultStop['left'] or self.y>defaultStop['down']):
                 self.crossed=1
                 self.intersection=False
                 intersection['up'].remove(self)
            if(self.y>defaultStop['up']):
                self.intersection=True
                intersection['up'].append(self)
            if(defaultStop['up']-5<self.y+self.image.get_rect().height<defaultStop['up']):
                arrivedStop['up']=(pygame.time.get_ticks(),self.index)
                if(track[track_no]=='up'):
                    avoid()
                if(track[track_no]!='up' and cmp_conf(self.state,avoid_col)):
                    self.y+=self.speed
            # if(track[track_no]=='right'):
            if(self.y+self.image.get_rect().height<=defaultStop['up'] and (self.y+self.image.get_rect().height<vehicles[self.direction][self.index-1].y-stoppingGap or self.index==0)):
                self.y+=self.speed
            elif(track[track_no]=='up' and self.y<=defaultStop['up']):
                self.y+=self.speed
            elif(defaultStop['up']<self.y<=defaultStop['up']+5):
                if(track[track_no]=='up'):
                    self.y+=self.speed
            elif(defaultStop['up']+5<self.y<=defaultStop['up']+55):
                if(self.signal=='left'):
                    self.x+=self.speed
                else:
                    self.y+=self.speed
            elif(defaultStop['up']+55<self.y<=defaultStop['down']):
                if(self.signal=='right'):
                    self.x-=self.speed
                else:
                    self.y+=self.speed
            elif(self.y>defaultStop['down']):
                self.y+=self.speed
        elif(self.direction=='down'):
            if(self.x>defaultStop['right'] or self.x<defaultStop['left'] or self.y<defaultStop['up']):
                 self.crossed=1
                 self.intersection=False
                 intersection['down'].remove(self)
            if(self.y<defaultStop['down']):
                self.intersection=True
                intersection['down'].append(self)
            if(defaultStop['down']<self.y<defaultStop['down']+5):
                arrivedStop['down']=(pygame.time.get_ticks(),self.index)
                if(track[track_no]=='down'):
                    avoid()
                if(track[track_no]!='down' and cmp_conf(self.state,avoid_col)):
                    self.y-=self.speed
            # if(track[track_no]=='right'):
            if(self.y>=defaultStop['down'] and (self.y>vehicles[self.direction][self.index-1].y+vehicles[self.direction][self.index-1].image.get_rect().height+stoppingGap or self.index==0)):
                self.y-=self.speed
            elif(track[track_no]=='down' and self.y+self.image.get_rect().height>defaultStop['down']):
                self.y-=self.speed
            elif(defaultStop['down']>=self.y+self.image.get_rect().height>=defaultStop['down']-2):
                if(track[track_no]=='down'):
                    self.y-=self.speed
            elif(defaultStop['down']-2>self.y+self.image.get_rect().height>=defaultStop['down']-52):
                if(self.signal=='left'):
                    self.x-=self.speed
                else:
                    self.y-=self.speed
            elif(defaultStop['down']-52>self.y+self.image.get_rect().height>=defaultStop['up']):
                if(self.signal=='right'):
                    self.x+=self.speed
                else:
                    self.y-=self.speed
            elif(self.y+self.image.get_rect().height<defaultStop['up']):
                self.y-=self.speed

            


            # if(self.x>=defaultStop['right']):
            #     if(self.x>=vehicles[self.direction][self.index-1].x+vehicles[self.direction][self.index-1].image.get_rect().width+stoppingGap):
            #         self.x-=self.speed
            #     if(track[track_no]=='right'):
            #         self.x-=self.speed
            # if(self.x)



            # if(self.crossed==0 and self.x>=vehicles[self.direction][self.index-1].x+vehicles[self.direction][self.index-1].image.get_rect().width+stoppingGap or 
            # (self.crossed==1 and self.signal=='off')or
            # track[track_no]=='right'): #and self.x>=defaultStop['right']):
            #     self.x-=self.speed
            #     # print(vehicles[self.direction][self.index-1].image.get_rect().width)
            # elif (self.x+self.image.get_rect().width>=self.stop or (track[track_no]=='right' and self.signal=='off') or (track[track_no]=='right' and self.x+self.image.get_rect().width>defaultStop['right']) ):
            #     self.x-=self.speed
            # elif(self.crossed==0 and self.signal=='left'):
            #     if( self.x+self.image.get_rect().width<=defaultStop['right']-40):
            #     # self.x-=2.4
            #         self.y+=self.speed
            #     elif( self.x+self.image.get_rect().width<=defaultStop['right']):
            #         self.x-=self.speed
            # elif(self.crossed==0 and self.signal=='right'):
            #     if( self.x+self.image.get_rect().width<=defaultStop['right']-80):
            #     # self.x-=2.4
            #         self.y-=self.speed
            #     elif( self.x+self.image.get_rect().width<=defaultStop['right']):
            #         self.x-=self.speed
            # elif(self.crossed==1 and self.signal=='left'):
            #     self.y+=self.speed
            # elif(self.crossed==1 and self.signal=='right'):
            #     self.y-=self.speed

            # self.rect.move_ip(5,0)
        # elif(self.direction=='left'):
        #     if(self.x>defaultStop['right'] or self.y>defaultStop['up'] or self.y<defaultStop['down']):
        #          self.crossed=1
        #     if (self.x+self.image.get_rect().width<=self.stop or (track[track_no]=='left' and self.signal=='off') or (track[track_no]=='left' and self.x+self.image.get_rect().width<defaultStop['left']) or (self.crossed==1 and self.signal=='off')):
        #         self.x+=self.speed
        #     # if(self.x<SW/2+offset_w):
        #     #     self.crossed=1
        #     elif(self.crossed==0 and self.signal=='left'):
        #          if( self.x+self.image.get_rect().width>=defaultStop['left']+50):

        #             # self.x-=2.4
        #             self.y-=self.speed
        #          elif(self.x+self.image.get_rect().width>=defaultStop['left']):
        #             self.x+=self.speed
        #     elif(self.crossed==0 and self.signal=='right'):
        #         if( self.x+self.image.get_rect().width>=defaultStop['left']+100):
        #         # self.x-=2.4
        #             self.y+=self.speed
        #         elif( self.x+self.image.get_rect().width>=defaultStop['left']):
        #             self.x+=self.speed
        #     elif(self.crossed==1 and self.signal=='left'):
        #         self.y-=self.speed
        #     elif(self.crossed==1 and self.signal=='right'):
        #         self.y+=self.speed

            # if (self.x-self.image.get_rect().width<=self.stop or track[track_no]=='left' or self.crossed==1):
            #     self.x+=self.speed
            # self.rect.move_ip(-5,0)
        # elif(self.direction=='up'):
        #     if(self.x<defaultStop['left'] or self.x>defaultStop['right'] or self.y<defaultStop['down']):
        #          self.crossed=1
        #     # if(self.y<SH/2+offset_h):
        #     #     self.crossed=1
        #     if (self.y>=self.stop or (track[track_no]=='up' and self.signal=='off') or(track[track_no]=='up' and self.y+self.image.get_rect().height>defaultStop['up']) or (self.crossed==1 and self.signal=='off')):
        #         self.y-=self.speed
        #     elif(self.crossed==0 and self.signal=='left'):
        #          if( self.y+self.image.get_rect().height<=defaultStop['up']-30 ):

        #             # self.x-=2.4
        #             self.x-=self.speed
        #          elif(self.y+self.image.get_rect().height<=defaultStop['up']):
        #             self.y-=self.speed
        #     elif(self.crossed==0 and self.signal=='right'):
        #         if( self.y+self.image.get_rect().height<=defaultStop['up']-80):
        #         # self.x-=2.4
        #             self.x+=self.speed
        #         elif( self.y+self.image.get_rect().height<=defaultStop['up']):
        #             self.y-=self.speed
        #     elif(self.crossed==1 and self.signal=='right'):
        #         self.x+=self.speed
        #     elif(self.crossed==1 and self.signal=='left'):
        #         self.x-=self.speed
        #     # self.rect.move_ip(0,5)
        # elif(self.direction=='down'):
        #     if(self.x<defaultStop['left'] or self.x>defaultStop['right'] or self.y>defaultStop['up']):
        #          self.crossed=1
        #     # if(self.y>SH/2-offset_h):
        #     #     self.crossed=1
        #     # if (self.y<=self.stop or track[track_no]=='down' or self.crossed==1):
        #     #     self.y+=self.speed
        #     if (self.y<=self.stop or (track[track_no]=='down' and self.signal=='off') or(track[track_no]=='down' and self.y+self.image.get_rect().height<defaultStop['down']) or (self.crossed==1 and self.signal=='off')):
        #         self.y+=self.speed
        #     elif(self.crossed==0 and self.signal=='left'):
        #          if( self.y+self.image.get_rect().height>=defaultStop['down']+50):

        #             # self.x-=2.4
        #             self.x+=self.speed
        #          elif(self.y+self.image.get_rect().height>=defaultStop['down']):
        #             self.y+=self.speed
        #     elif(self.crossed==0 and self.signal=='right'):
        #         if(self.y+self.image.get_rect().height>=defaultStop['down']+100):
        #         # self.x-=2.4
        #             self.x-=self.speed
        #         elif( self.y+self.image.get_rect().height>=defaultStop['down']):
        #             self.y+=self.speed
        #     elif(self.crossed==1 and self.signal=='left'):
        #         self.x+=self.speed
        #     elif(self.crossed==1 and self.signal=='right'):
        #         self.x-=self.speed
        #     # self.rect.move_ip(0,-5)
        

        # if(self.x,self.y):
        #     #fill later
        #     return self.x+speed,self.y+speed 

        if self.steering:
            turning_radius = self.length / math.sin(math.radians(self.steering))
            angular_velocity = self.speed / turning_radius
        else:
            angular_velocity = 0
        
    def is_intersection(self,x,y):
        if(x_l<=x<=x_r and y_bot<=y<=y_top):
            self.intersection=True
        else:
            self.intersection=False
proceed = True
def GenerateVehicles():
    while (True):
        Vehicle()
        time.sleep(0.5)
def updateTrack(track_no):
    return (track_no+1)% 4

#Capturing events till exit
sprites_list=pygame.sprite.Group()
clock=pygame.time.Clock()
dt=pygame.USEREVENT+1
pygame.time.set_timer(dt,1000)
# print(dt)
screen = pygame.display.set_mode(screenSize)
# vehicle1=Vehicle()
thread = threading.Thread(name="generateVehicles",target=GenerateVehicles, args=())    # Generating vehicles
thread.daemon = True
thread.start()

while proceed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proceed = False
        elif event.type ==dt:
            min_time=None
            sel_track=None
            for i in range(0,3):
                min_time=arrivedStop[track[i]][0]
                
                if(min_time!=None):
                    sel_track=i
                    break
            if(sel_track==None):
                track_no=random.randint(0,3)
            else:
                for i in range(0,4):
                    if(sel_track!=i and arrivedStop[track[i]][0]!=None and arrivedStop[track[i]][0]<min_time):
                        min_time=arrivedStop[track[i]][0]
                        sel_track=i
                        

                track_no=sel_track


    

    # vehicle1.update()
    # sprites_list.update()
    screen.fill(G)
    pygame.draw.rect(screen,BLACK,pygame.Rect(SW/2-50,0,100,SH))
    pygame.draw.rect(screen,BLACK,pygame.Rect(0,SH/2-50,SW,100))
    pygame.draw.line(screen,YELLOW,[SW/2,0],[SW/2,SH/2-offset_h],4)
    pygame.draw.line(screen,YELLOW,[SW/2,SH/2+offset_h],[SW/2,SH],4)
    pygame.draw.line(screen,YELLOW,[0,SH/2],[SW/2-offset_w,SH/2],4)
    pygame.draw.line(screen,YELLOW,[SW/2+offset_w,SH/2],[SW,SH/2],4)
    pygame.draw.line(screen,WHITE,[SW/2-50,SH/2-55],[SW/2+50,SH/2-55],4)
    pygame.draw.line(screen,WHITE,[SW/2-50,SH/2+55],[SW/2+50,SH/2+55],4)
    pygame.draw.line(screen,WHITE,[SW/2-50,SH/2-50],[SW/2-50,SH/2+50],4)
    pygame.draw.line(screen,WHITE,[SW/2+50,SH/2-50],[SW/2+50,SH/2+50],4)
    pygame.draw.line(screen,RED,[0,defaultStop['down']],[500,defaultStop['down']])
    # image =  pygame.Surface([40,5])
    # image.fill(BLACK)
    # screen.blit(image,(0,0))








    #screen.pygame.Surface.fill(color, rect=None, special_flags=0)
    # pygame.draw.line(screen, BLACK, [0, 0],  [700, 300], 5)
    # screen.blit(vehicle1.image,vehicle1.rect)

    # self.screen.blit(rotated, [20,30])
    # sprites_list.draw(screen)
    # vehicle1.update()
    for vehicle in sprites_list:
        # print(vehicle.x)
        screen.blit(vehicle.image,(vehicle.x,vehicle.y))
    sprites_list.update()
    # surf=pygame.surface([7,8])
    # surf.fill(BLACK)
    # screen.blit(surf,(5,10))

    pygame.draw.circle(screen,(0,255,0),(480,4),6)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()


