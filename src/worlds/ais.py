import glm

pi = glm.pi()

class AI:
    def calculate_forward_vector(self):
        rotation_matrix = glm.mat4(1.0)  # Identity matrix

        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.y, glm.vec3(0, -1, 0))
        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.x, glm.vec3(1, 0, 0))
        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.z, glm.vec3(0, 0, 1))
        
        # Initial forward vector is (0, -1, 0) pointing downwards
        initial_forward = glm.vec4(0, -1, 0, 0)
        
        # Rotate the forward vector
        rotated_forward = rotation_matrix * initial_forward
        
        # Return the rotated forward vector as glm.vec3
        return glm.vec3(rotated_forward)


class StarDestroyerAI(AI):
    def __init__(self):
        self.position = glm.vec3(0, 1500, 0)
        self.scale = glm.vec3(5,5,5)
        self.rotation = glm.vec3(0, 0, 0)
        self.forward = glm.vec3(0, -1, 0)
        self.flag = False
    
    def update(self, app):
        t = app.time - 6
        dt = 1/app.framerate # app.delta_time
        self.forward = self.calculate_forward_vector()
        if 0 < (t%110) < 0.2:
            self.position += self.forward * (11400 * dt)
        elif (t%110) < 5:
            self.position += self.forward * (70 * dt)
        elif (t%110) < 8:
            if not self.flag:       # make sure the start position is coherent
                self.position = glm.vec3(0, 200, 0)
                self.flag = True
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(0, 1, 0) * dt
        elif (t%110) < 21:
            self.flag = False
            self.position += self.forward * (20 * dt)
            self.rotation += glm.vec3(-0.6, 0, 0) * dt
        elif (t%110) < 24:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0, 1, 0) * dt
        elif (t%110) < 27:
            self.position += self.forward * (30 * dt)
        elif (t%110) < 32:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0.4, 0, 0) * dt
        elif (t%110) < 36:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0, 0.5, -0.2) * dt
        elif (t%110) < 43:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(0.5, 0.0, 0.0) * dt
        elif (t%110) < 47:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(1, 0, 0) * dt
        elif (t%110) < 50:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(1, 0, 1) * dt
        elif (t%110) < 52:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(0, -0.5, 0) * dt
        elif (t%110) < 55:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(-0.5, 0, 0) * dt
        elif (t%110) < 60:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(0, 0.5, 0) * dt
        elif (t%110) < 68:
            self.position += self.forward * (40 * dt)
            self.rotation += glm.vec3(-0.5, 0, -0.3) * dt
        elif (t%110) < 72:
            self.position += self.forward * (20 * dt)
            self.rotation += glm.vec3(-0.2, 0.5, 0.0) * dt
        elif (t%110) < 75:
            self.position += self.forward * (20 * dt)
            self.rotation += glm.vec3(0, -0.5, 0.0) * dt
        elif (t%110) < 80:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0.1, 0.1, 0.1) * dt
        elif (t%110) < 83:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0, 0, 0.4) * dt
        elif (t%110) < 90:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0, 0.7, 0.5) * dt
        elif (t%110) < 95:
            self.position += self.forward * (30 * dt)
            self.rotation += glm.vec3(0.2, -0.5, 0) * dt
        elif (t%110) < 105:
            self.position += self.forward * (40 * dt)
        elif (t%110) < 107:
            self.position += self.forward * (10000 * dt)
        else:
            self.position = glm.vec3(0, 1500, 0)
            self.rotation = glm.vec3(0, 0, 0)


class MalevolenceAIFilix(AI):
   def __init__(self):
       self.position = glm.vec3(0, 500, 0)
       self.scale = glm.vec3(5,5,5)
       self.rotation = glm.vec3(0, 0, 0)
       self.forward = glm.vec3(0, -1, 0)
  
   def update(self, app):
       # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
       t = app.time
       sd = [0,5,2,8,10,5,5]
       loop_length = sum(sd) - sd[0]
       self.forward = self.calculate_forward_vector()
       if 0 < t < sd[0]:
           self.position = glm.vec3(0, 300, 0) + (glm.vec3(0, 0, 25) - glm.vec3(0, 300, 0)) * t / sd[0]
      
       elif 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
           st = (t-sum(sd[:1]))%loop_length/sd[1]
           self.position = glm.vec3(0, 300, 0) + glm.vec3(0,-200,15)*st
           self.rotation = glm.vec3(0,0,0)
       elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
           st = (t-sum(sd[:2]))%loop_length/sd[2]
           self.position = glm.vec3(0, 100, 15) + glm.vec3(50,-100,0)*st
           self.rotation = glm.vec3(0,0,pi/4*st)
       elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
           st = (t-sum(sd[:3]))%loop_length/sd[3]
           self.position = glm.vec3(30, 15, 0) + glm.vec3(-60,0,0)*st
           self.rotation = glm.vec3(0,0,-pi/2)
       elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
           st = (t-sum(sd[:4]))%loop_length/sd[4]
           self.position = glm.vec3(-40, 15, 0) + glm.vec3(30,250,-30)*st
           self.rotation = glm.vec3(0,-0.06656,-pi+0.06656)
       elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
           st = (t-sum(sd[:5]))%loop_length/sd[5]
           self.position = glm.vec3(-10, 265, -30) + glm.vec3(10,35,30*4/5)*st
           self.rotation = glm.vec3(pi*st*(4/5),-0.06656 + 0.06656*st,-pi+0.06656 -0.06656*st)
       elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
           st = (t-sum(sd[:6]))%loop_length/sd[6]
           self.position = glm.vec3(0, 300, -30*1/5) + glm.vec3(0,0,30*1/5)*st
           self.rotation = glm.vec3(pi*(4/5)+pi*(1/5)*st,pi*st,-pi)


class MillenniumFalconAIFilix(AI):
    def __init__(self):
        self.position = glm.vec3(-15, 90, -15)
        self.scale = glm.vec3(5,5,5)
        self.rotation = glm.vec3(0, 0, 0)
        self.forward = glm.vec3(0, -1, 0)
   
    def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        sd = [0,5,1,1,0.25,2,3,2,3,3,2,3,1.25,1.25,1.25,1.25,5,1,0.5]
        loop_length = sum(sd) - sd[0]
        self.forward = self.calculate_forward_vector()
        if 0 < t < sd[0]:
            self.position = glm.vec3(0, 30, 0)
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636)/60)
       
        elif 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(-15, 90, -15) + glm.vec3(110,200,60)*st
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636)/60)
        elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
            st = (t-sum(sd[:2]))%loop_length/sd[2]
            self.position = glm.vec3(95, 290, 45) + glm.vec3(1000,2000,600)*st
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636)/60)
        elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
            st = (t-sum(sd[:3]))%loop_length/sd[3]
            self.position = glm.vec3(-30, -40, -30) + glm.vec3(40,80,20)*st
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636)/60)
        elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
            st = (t-sum(sd[:4]))%loop_length/sd[4]
            self.position = glm.vec3(10, 40, -10)
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636)/60)
        elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
            st = (t-sum(sd[:5]))%loop_length/sd[5]
            self.position = glm.vec3(10, 40, -10)
            self.rotation = glm.vec3(0.2914*1/60,0,(pi-0.4636+0.4636*st)/60)
        elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
            st = (t-sum(sd[:6]))%loop_length/sd[6]
            self.position = glm.vec3(10, 40, -10) + glm.vec3(0,120,30)*st*3/5
            self.rotation = glm.vec3(0.2914*1/60,0,pi/60)
        elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
            st = (t-sum(sd[:7]))%loop_length/sd[7]
            self.position = glm.vec3(10, 40+72, -10+18) + glm.vec3(0,120,30)*st*2/5
            self.rotation = glm.vec3((0.2914+(pi/2-0.2914)*st)*1/60,pi/4/60*st,pi/60)
        elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
            st = (t-sum(sd[:8]))%loop_length/sd[8]
            self.position = glm.vec3(10, 160, 20) + glm.vec3(-5,10,5)*st
            self.rotation = glm.vec3((pi/2)*1/60,pi/4/60+pi/2/60*st,pi/60)
        elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
            st = (t-sum(sd[:9]))%loop_length/sd[9]
            self.position = glm.vec3(5, 170, 25) + glm.vec3(-5,-30,-5)*st
            self.rotation = glm.vec3((pi/2*(1+0.75*st))*1/60,3*pi/4/60+pi/4/60*st,pi/60)
        elif 0 < (t-sum(sd[:10]))%loop_length/sd[10] < 1 :
            st = (t-sum(sd[:10]))%loop_length/sd[10]
            self.position = glm.vec3(0, 140, 20) + glm.vec3(-5,-80,-16)*st*1/2
            self.rotation = glm.vec3((7*pi/8)*1/60,pi/60,pi/60)
        elif 0 < (t-sum(sd[:11]))%loop_length/sd[11] < 1 :
            st = (t-sum(sd[:11]))%loop_length/sd[11]
            self.position = glm.vec3(-2.5, 100, 12) + glm.vec3(-5,-80,-16)*st*1/2
            self.rotation = glm.vec3(((7+st)*pi/8)*1/60,pi/60+pi/2/60*st,pi/60)
        elif 0 < (t-sum(sd[:12]))%loop_length/sd[12] < 1 :
            st = (t-sum(sd[:12]))%loop_length/sd[12]
            self.position = glm.vec3(-5, 60, 4) + glm.vec3(-5,-20,-9)*st*1/4
            self.rotation = glm.vec3(pi/60+pi/60*st*1/4,1.5*pi/60,pi/60)
        elif 0 < (t-sum(sd[:13]))%loop_length/sd[13] < 1 :
            st = (t-sum(sd[:13]))%loop_length/sd[13]
            self.position = glm.vec3(-6.25, 55, 4-9/4) + glm.vec3(-10,-15,-9)*st*1/4
            self.rotation = glm.vec3(pi/60+pi/60*1/4+pi/60*st*1/4,1.5*pi/60,pi/60)
        elif 0 < (t-sum(sd[:14]))%loop_length/sd[14] < 1 :
            st = (t-sum(sd[:14]))%loop_length/sd[14]
            self.position = glm.vec3(-8.75, 51.25, 4-9/2) + glm.vec3(-15,-10,-9)*st*1/4
            self.rotation = glm.vec3(pi/60+pi/60*2/4+pi/60*st*1/4,1.5*pi/60,pi/60)
        elif 0 < (t-sum(sd[:15]))%loop_length/sd[15] < 1 :
            st = (t-sum(sd[:15]))%loop_length/sd[15]
            self.position = glm.vec3(-12.5, 48.75, 4-3*9/4) + glm.vec3(-10,5,-9)*st*1/4
            self.rotation = glm.vec3(pi/60+pi/60*(3+st)/4,1.5*pi/60,pi/60)
        elif 0 < (t-sum(sd[:16]))%loop_length/sd[16] < 1 :
            st = (t-sum(sd[:16]))%loop_length/sd[16]
            self.position = glm.vec3(-15, 50, -5) + glm.vec3(0,0,-10)*st
            self.rotation = glm.vec3(pi/30+0.2914/60*st,1.5*pi/60+pi/2/60*st,pi/60-0.4636/60*st)
        elif 0 < (t-sum(sd[:17]))%loop_length/sd[17] < 1 :
            st = (t-sum(sd[:17]))%loop_length/sd[17]
            self.position = glm.vec3(-15, 50, -15) + glm.vec3(0,20,0)*st
            self.rotation = glm.vec3(pi/30+0.2914/60+0.14/60*st,pi/30+0.14/60*st,pi/60-0.4636/60)
        elif 0 < (t-sum(sd[:18]))%loop_length/sd[18] < 1 :
            st = (t-sum(sd[:18]))%loop_length/sd[18]
            self.position = glm.vec3(-15, 70, -15) + glm.vec3(0,20,0)*st
            self.rotation = glm.vec3(pi/30+0.2914/60+0.14/60+0.14/60*st,pi/30+0.14/60+0.14/60*st,pi/60-0.4636/60)


class CorvetteAI(AI):
   def __init__(self):
       self.position = glm.vec3(50, 50, 0)
       self.scale = glm.vec3(5,5,5)
       self.rotation = glm.vec3(0, 0, 0)
  
   def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        sd = [0,6,9,2,2,3,3,2,6,6,1]
        loop_length = sum(sd) - sd[0]
        if 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(50, 50, 0) + glm.vec3(-100,0,0)*st
            self.rotation = glm.vec3(0, 0, 0)
        elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
            st = (t-sum(sd[:2]))%loop_length/sd[2]
            self.position = glm.vec3(-50, 50, -50) + glm.vec3(100,100,100)*st
            self.rotation = glm.vec3(pi/4, 0, 5*pi/4)
        elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
            st = (t-sum(sd[:3]))%loop_length/sd[3]
            self.position = glm.vec3(50, 150, 50) + glm.vec3(50,150,50)*st
            self.rotation = glm.vec3(pi/4, 0, 5*pi/4) + glm.vec3(-pi/4, 0, pi/4)*st
        elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
            st = (t-sum(sd[:4]))%loop_length/sd[4]
            self.position = glm.vec3(100, 300, 100) + glm.vec3(0,100,0)*st
        elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
            st = (t-sum(sd[:5]))%loop_length/sd[5]
            self.position = glm.vec3(100, 400, 100) + glm.vec3(-50,50,0)*st
            self.rotation = glm.vec3(0, 0, 6*pi/4) + glm.vec3(0, 0, pi/2)*st
        elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
            st = (t-sum(sd[:6]))%loop_length/sd[6]
            self.position = glm.vec3(50, 450, 100) + glm.vec3(-50,-50,0)*st
            self.rotation = glm.vec3(0, 0, 0) + glm.vec3(0, 0, pi/2)*st
        elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
            st = (t-sum(sd[:7]))%loop_length/sd[7]
            self.position = glm.vec3(0, 400, 100) + glm.vec3(0,-100,-30)*st
            self.rotation = glm.vec3(0, 0, pi/2) + glm.vec3(pi/8, 0, 0)*st
        elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
            st = (t-sum(sd[:8]))%loop_length/sd[8]
            self.position = glm.vec3(0, 300, 70) + glm.vec3(0,-350,-100)*st
        elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
            st = (t-sum(sd[:9]))%loop_length/sd[9]
            self.position = glm.vec3(0, 80, -50) + glm.vec3(0, 0, 100)*st
            self.rotation = glm.vec3(0, 3*pi/2, 0) + glm.vec3(2*pi, 0, 0)*st


class AWingAI(AI):
   def __init__(self):
       self.position = glm.vec3(-50, 50, -20)
       self.scale = glm.vec3(5,5,5)
       self.rotation = glm.vec3(0, 0, 0)
  
   def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        s = 4e-1
        sd = [0,8,6,1,1,1,1,3,5,2,2,5]
        loop_length = sum(sd) - sd[0]
        if 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(-50, 50, -10) + glm.vec3(70,0,0)*st
            self.rotation = glm.vec3(0, 4*pi, 0)*st
        elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
            st = (t-sum(sd[:2]))%loop_length/sd[2]
            self.position = glm.vec3(20, 50, -10) + glm.vec3(0,50,0)*st
            self.rotation = glm.vec3(0, 2*pi, 0)*st
        elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
            st = (t-sum(sd[:3]))%loop_length/sd[3]
            self.position = glm.vec3(20, 100, -10) + glm.vec3(0,-10,5)*st
            self.rotation = glm.vec3(-pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
            st = (t-sum(sd[:4]))%loop_length/sd[4]
            self.position = glm.vec3(20, 90, -5) + glm.vec3(0,-5,10)*st
            self.rotation = glm.vec3(-pi/4, 0, 0) + glm.vec3(-pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
            st = (t-sum(sd[:5]))%loop_length/sd[5]
            self.position = glm.vec3(20, 85, 5) + glm.vec3(0,5,10)*st
            self.rotation = glm.vec3(-pi/2, 0, 0) + glm.vec3(-pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
            st = (t-sum(sd[:6]))%loop_length/sd[6]
            self.position = glm.vec3(20, 90, 15) + glm.vec3(0,10,5)*st
            self.rotation = glm.vec3(-3*pi/4, 0, 0) + glm.vec3(-pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
            st = (t-sum(sd[:7]))%loop_length/sd[7]
            self.position = glm.vec3(20, 100, 20) + glm.vec3(0,40,0)*st
            self.rotation = glm.vec3(pi, 0, 0) + glm.vec3(0, pi, 0)*st
        elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
            st = (t-sum(sd[:8]))%loop_length/sd[8]
            self.position = glm.vec3(20, 140, 20) + glm.vec3(0,90,0)*st
            self.rotation = glm.vec3(pi, pi, 0)
        elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
            st = (t-sum(sd[:9]))%loop_length/sd[9]
            self.position = glm.vec3(20, 230, 20) + glm.vec3(-20,20,0)*st
            self.rotation = glm.vec3(pi, pi, 0) + glm.vec3(0, 0, pi/2)*st
        elif 0 < (t-sum(sd[:10]))%loop_length/sd[10] < 1 :
            st = (t-sum(sd[:10]))%loop_length/sd[10]
            self.position = glm.vec3(0, 250, 20) + glm.vec3(-20,-20,0)*st
            self.rotation = glm.vec3(pi, pi, pi/2) + glm.vec3(0, 0, pi/2)*st
        elif 0 < (t-sum(sd[:11]))%loop_length/sd[11] < 1 :
            st = (t-sum(sd[:11]))%loop_length/sd[11]
            self.position = glm.vec3(-20, 230, 20) + glm.vec3(0,-240,-30)*st
            self.rotation = glm.vec3(0, 0, 0)


class RoyalStarshipAI(AI):
   def __init__(self):
       self.position = glm.vec3(-200, 400, -20)
       self.scale = glm.vec3(10,10,10)
       self.rotation = glm.vec3(0, 0, 5*pi/8)
  
   def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        s = 1e-1
        sd = [0,8,5,5,4,2,2,2,4,3,7,5,1,1,0.4]
        loop_length = sum(sd) - sd[0]
        if 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(-200, 400, -20) + glm.vec3(100,-200,0)*st
        elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
            st = (t-sum(sd[:2]))%loop_length/sd[2]
            self.position = glm.vec3(-100, 200, -20) + glm.vec3(50,-50,30)*st
            self.rotation = glm.vec3(0, 0, 5*pi/8) + glm.vec3(-pi/4, pi/4, 3*pi/8)*st
        elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
            st = (t-sum(sd[:3]))%loop_length/sd[3]
            self.position = glm.vec3(-50, 150, 10) + glm.vec3(50,50,30)*st
            self.rotation = glm.vec3(-pi/4, pi/4, pi) + glm.vec3(0, pi/4, pi/2)*st
        elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
            st = (t-sum(sd[:4]))%loop_length/sd[4]
            self.position = glm.vec3(0, 200, 40) + glm.vec3(50,50,0)*st
            self.rotation = glm.vec3(-pi/4, pi/2, 3*pi/2) + glm.vec3(pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
            st = (t-sum(sd[:5]))%loop_length/sd[5]
            self.position = glm.vec3(50, 250, 40) + glm.vec3(0,10,-15)*st
            self.rotation = glm.vec3(0, pi/2, 3*pi/2) + glm.vec3(0, -pi/2, 0)*st
        elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
            st = (t-sum(sd[:6]))%loop_length/sd[6]
            self.position = glm.vec3(50, 260, 25) + glm.vec3(0,10,-15)*st
            self.rotation = glm.vec3(0, 0, 3*pi/2) + glm.vec3(0, 0, pi)*st
        elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
            st = (t-sum(sd[:7]))%loop_length/sd[7]
            self.position = glm.vec3(50, 270, 10) + glm.vec3(0,-20,-20)*st
        elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
            st = (t-sum(sd[:8]))%loop_length/sd[8]
            self.position = glm.vec3(50, 250, -10) + glm.vec3(0,-100,-20)*st
            self.rotation = glm.vec3(0, 0, 5*pi/2) + glm.vec3(0, 3*pi/2, 0)*st
        elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
            st = (t-sum(sd[:9]))%loop_length/sd[9]
            self.position = glm.vec3(50, 150, -30) + glm.vec3(40,-70,0)*st
            self.rotation = glm.vec3(0, 3*pi/2, 5*pi/2) + glm.vec3(-pi/4, 0, 0)*st
        elif 0 < (t-sum(sd[:10]))%loop_length/sd[10] < 1 :
            st = (t-sum(sd[:10]))%loop_length/sd[10]
            self.position = glm.vec3(75, 75, -20) + glm.vec3(-150,0,0)*st
            self.rotation = glm.vec3(pi/2, 0, 0) + glm.vec3(pi, 0, 0)*st
        elif 0 < (t-sum(sd[:11]))%loop_length/sd[11] < 1 :
            st = (t-sum(sd[:11]))%loop_length/sd[11]
            self.position = glm.vec3(-75, 75, -20) + glm.vec3(0,200,0)*st
            self.rotation = glm.vec3(0, 0, -pi/2)
        elif 0 < (t-sum(sd[:12]))%loop_length/sd[12] < 1 :
            st = (t-sum(sd[:12]))%loop_length/sd[12]
            self.position = glm.vec3(-75, 275, -20) + glm.vec3(0,6000,0)*st
        elif 0 < (t-sum(sd[:13]))%loop_length/sd[13] < 1 :
            st = (t-sum(sd[:13]))%loop_length/sd[13]
            self.position = glm.vec3(-300, 450, -20) + glm.vec3(100,-50,0)*st
            self.rotation = glm.vec3(0, -pi/6, 5*pi/8)
        elif 0 < (t-sum(sd[:14]))%loop_length/sd[14] < 1 :
            st = (t-sum(sd[:14]))%loop_length/sd[14]
            self.rotation = glm.vec3(0, -pi/6, 5*pi/8) + glm.vec3(0, pi/6, 0)*st


class TieFighterAIFilix(AI):
    def __init__(self):
        self.position = glm.vec3(-30, 75, 20)
        self.scale = glm.vec3(3,3,3)
        self.rotation = glm.vec3(0, 0, 0)
        self.forward = glm.vec3(0, -1, 0)

    def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        sd = [0,2,1]
        loop_length = sum(sd) - sd[0]
        self.forward = self.calculate_forward_vector()
        if 0 < t < sd[0]:
           self.position = glm.vec3(0, 500, 0) + (glm.vec3(0, 0, 25) - glm.vec3(0, 500, 3)) * t / sd[0]

        elif 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(-30, 75, 20) + glm.vec3(30,-70,-50+15*st)*st
            self.rotation = glm.vec3(0.708626272128-0.5*st,0,-0.4049)


class StarDestroyerAIFilix(AI):
   def __init__(self):
       self.position = glm.vec3(0, -15, 5)
       self.scale = glm.vec3(5,5,5)
       self.rotation = glm.vec3(0, 0, pi)
       self.forward = glm.vec3(0, -1, 0)

   def update(self, app):
       # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
       t = app.time
       sd = [0,4,1,6,4/3,2,1,1,1,1,4]
       loop_length = sum(sd) - sd[0]
       self.forward = self.calculate_forward_vector()
       if 0 < t < sd[0]:
          self.position = glm.vec3(0, 500, 0) + (glm.vec3(0, 0, 25) - glm.vec3(0, 500, 3)) * t / sd[0]

       elif 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
           st = (t-sum(sd[:1]))%loop_length/sd[1]
           self.position = glm.vec3(0, -15, 5) + glm.vec3(0,65,3)*st
           self.rotation = glm.vec3(0,0,pi)
       elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
           st = (t-sum(sd[:2]))%loop_length/sd[2]
           self.position = glm.vec3(0, 50, 8) + glm.vec3(0,10,-3)*st
           self.rotation = glm.vec3(-0.291456794478*st,0,pi)
       elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
           st = (t-sum(sd[:3]))%loop_length/sd[3]
           self.position = glm.vec3(0, 60, 5) + glm.vec3(0,175,-52.5)*st
           self.rotation = glm.vec3(-0.291456794478,0,pi)
       elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
           st = (t-sum(sd[:4]))%loop_length/sd[4]
           self.position = glm.vec3(0, 235, -47.5) + glm.vec3(0,65,-12.5)*st
           self.rotation = glm.vec3(-0.291456794478+0.291456794478*st+pi/12*st,-pi/2*st,pi)
       elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
           st = (t-sum(sd[:5]))%loop_length/sd[5]
           self.position = glm.vec3(0, 300, -60) + glm.vec3(60,0,0)*st*3/4
           self.rotation = glm.vec3(1/12*pi+11/12*3/4*pi*st,-pi/2,pi)
       elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
           st = (t-sum(sd[:6]))%loop_length/sd[6]
           self.position = glm.vec3(45, 300, -60) + glm.vec3(40,0,0)*st/4
           self.rotation = glm.vec3(1/12*pi+11/16*pi+11/12/4*pi*st,-pi/2-pi/2*st,pi)
       elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
           st = (t-sum(sd[:7]))%loop_length/sd[7]
           self.position = glm.vec3(55, 300, -60) + glm.vec3(0,-40,0)*st
           self.rotation = glm.vec3(pi,-pi,pi)
       elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
           st = (t-sum(sd[:8]))%loop_length/sd[8]
           self.position = glm.vec3(55, 260, -60) + glm.vec3(0,-60,35)*st/2
           if st < 1/3 :
               self.rotation = glm.vec3(pi+pi/12*3*st,-pi,pi)
           else :
               self.rotation = glm.vec3(pi+pi/12,-pi,pi)
       elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
           st = (t-sum(sd[:9]))%loop_length/sd[9]
           self.position = glm.vec3(55, 230, -60+35/2) + glm.vec3(0,-60,35)*st/2
           self.rotation = glm.vec3(pi+pi/12,-pi,pi)
       elif 0 < (t-sum(sd[:10]))%loop_length/sd[10] < 1 :
           st = (t-sum(sd[:10]))%loop_length/sd[10]
           self.position = glm.vec3(55, 200, -25) + glm.vec3(-80,-210,30)*st
           if st<1/3:
               self.rotation = glm.vec3(pi+pi/12,-pi,pi-pi/6*st*3)
           else:
               self.rotation = glm.vec3(pi+pi/12,-pi,pi-pi/6)


class ImperialShuttleAI(AI):
   def __init__(self):
       self.position = glm.vec3(0, -100, 0)
       self.scale = glm.vec3(10,10,10)
       self.rotation = glm.vec3(0, 0, 0)
  
   def update(self, app):
        # st describes the time within a given step and sd[n] is the time it takes to do step n with n=0 being the setup
        t = app.time
        s = 1e-1
        sd = [0,1,1,3,4,4,4,4,3,3,2,2,2,3]
        loop_length = sum(sd) - sd[0]
        if 0 < (t-sum(sd[:1]))%loop_length/sd[1] < 1 :
            st = (t-sum(sd[:1]))%loop_length/sd[1]
            self.position = glm.vec3(0, 6000, -20) + glm.vec3(0,-5350,0)*st
            self.rotation = glm.vec3(0, 0, 0)
        elif 0 < (t-sum(sd[:2]))%loop_length/sd[2] < 1 :
            st = (t-sum(sd[:2]))%loop_length/sd[2]
            self.position = glm.vec3(0, 650, -20) + glm.vec3(0,-50,0)*st
        elif 0 < (t-sum(sd[:3]))%loop_length/sd[3] < 1 :
            st = (t-sum(sd[:3]))%loop_length/sd[3]
            self.position = glm.vec3(0, 600, -20) + glm.vec3(80, -50, 40)*st
            self.rotation = glm.vec3(0, 0, 0) + glm.vec3(0, pi/4, 0)*st
        elif 0 < (t-sum(sd[:4]))%loop_length/sd[4] < 1 :
            st = (t-sum(sd[:4]))%loop_length/sd[4]
            self.position = glm.vec3(80, 550, 20) + glm.vec3(-130, -50, -30)*st
            self.rotation = glm.vec3(0, pi/4, 0) + glm.vec3(0, -pi/2, 0)*st
        elif 0 < (t-sum(sd[:5]))%loop_length/sd[5] < 1 :
            st = (t-sum(sd[:5]))%loop_length/sd[5]
            self.position = glm.vec3(-50, 500, -10) + glm.vec3(30, -50, 50)*st
            self.rotation = glm.vec3(0, -pi/4, 0) + glm.vec3(0, 10*pi/4, 0)*st
        elif 0 < (t-sum(sd[:6]))%loop_length/sd[6] < 1 :
            st = (t-sum(sd[:6]))%loop_length/sd[6]
            self.position = glm.vec3(-20, 450, 40) + glm.vec3(30, -50, -60)*st
            self.rotation = glm.vec3(0, pi/4, 0) + glm.vec3(0, -pi/4, 0)*st
        elif 0 < (t-sum(sd[:7]))%loop_length/sd[7] < 1 :
            st = (t-sum(sd[:7]))%loop_length/sd[7]
            self.position = glm.vec3(10, 400, -20) + glm.vec3(-100, -50, 80)*st
            self.rotation = glm.vec3(0, 0, 0) + glm.vec3(0, -17*pi/4, 0)*st
        elif 0 < (t-sum(sd[:8]))%loop_length/sd[8] < 1 :
            st = (t-sum(sd[:8]))%loop_length/sd[8]
            self.position = glm.vec3(-90, 350, 60) + glm.vec3(170, -50, 10)*st
            self.rotation = glm.vec3(0, -pi/4, 0) + glm.vec3(0, pi/2, 0)*st
        elif 0 < (t-sum(sd[:9]))%loop_length/sd[9] < 1 :
            st = (t-sum(sd[:9]))%loop_length/sd[9]
            self.position = glm.vec3(80, 300, 70) + glm.vec3(-150, -50, -150)*st
            self.rotation = glm.vec3(0, pi/4, 0) + glm.vec3(0, -18*pi/4, 0)*st
        elif 0 < (t-sum(sd[:10]))%loop_length/sd[10] < 1 :
            st = (t-sum(sd[:10]))%loop_length/sd[10]
            self.position = glm.vec3(-70, 250, -80) + glm.vec3(10, -50, 40)*st
            self.rotation = glm.vec3(0, -pi/4, 0) + glm.vec3(0, pi/4, 0)*st
        elif 0 < (t-sum(sd[:11]))%loop_length/sd[11] < 1 :
            st = (t-sum(sd[:11]))%loop_length/sd[11]
            self.position = glm.vec3(-60, 200, -40) + glm.vec3(80, -50, 10)*st
            self.rotation = glm.vec3(0, 0, 0) + glm.vec3(0, 9*pi/4, 0)*st
        elif 0 < (t-sum(sd[:12]))%loop_length/sd[12] < 1 :
            st = (t-sum(sd[:12]))%loop_length/sd[12]
            self.position = glm.vec3(20, 150, -30) + glm.vec3(-20, -50, 40)*st
            self.rotation = glm.vec3(0, pi/4, 0) + glm.vec3(0, -pi/4, 0)*st
        elif 0 < (t-sum(sd[:13]))%loop_length/sd[13] < 1 :
            st = (t-sum(sd[:13]))%loop_length/sd[13]
            self.position = glm.vec3(0, 100, 10) + glm.vec3(0, -150, 0)*st
            self.rotation = glm.vec3(0, 0, 0)
