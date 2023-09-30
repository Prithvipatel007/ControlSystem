import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import numpy as np

# Tank parameters
radius = 5          # Radius of the tank - The tank is round
bottom = 0          # Initial volume of the tank
final_volume = 100  # Final volume of the tank
dVol = 10           # The change of volume on the vertical scale
width_ratio = 1     # Necessary for the horizontal axis
dt = 0.04           # Time interval
t0 = 0              # Initial time of the simulation
t_end = 50          # Final time of the simulation
frame_amount = int(t_end / dt)  # Frame amount of the simulation
t = np.arange(t0, t_end+dt, dt) # Time vector
density_water = 1000    # [Kg/m^3]

Kp1 = 1000          # Proportional constant for the 1st tank
Kp2 = 1000          # Proportional constant for the 2nd tank
Kp3 = 5000          # Proportional constant for hte 3rd tank

vol_o1_i = 30       # Initial volume of the 1st tank
vol_r1_i = 70       # Initial reference volume of the 1st tank
vol_o2_i = 40       # Initial volume of the 2nd tank
vol_r2_i = 10       # Initial reference volume of the 2nd tank
vol_o3_i = 50       # Initial volume of the 3rd tank
vol_r3_i = 20       # Initial reference volume of the 3rd tank

# 1st tank
vol_r1 = np.zeros(len(t))       # zero vector for storing reference volume values
vol_r1[0] = vol_r1_i
volume_tank1 = np.zeros(len(t)) # zero vector for the true volume values
volume_tank1[0] = vol_o1_i      # Insert the initial true volume as the initial element of the vector
error1 = np.zeros(len(t))       # Create a zero vector to store errors in the simulation
m_dot1 = Kp1*error1             # Compute a zero vector to store massflow control inputs

# 2nd tank
vol_r2 = np.zeros(len(t))       # zero vector for storing reference volume values
vol_r2[0] = vol_r2_i
volume_tank2 = np.zeros(len(t)) # zero vector for the true volume values
volume_tank2[0] = vol_o2_i      # Insert the initial true volume as the initial element of the vector
error2 = np.zeros(len(t))       # Cretae a zero vector to store errors in the simulation
m_dot2 = Kp2*error2             # Compute the zero vector to store massflow control inputs

#3rd tank
vol_r3 = vol_o3_i + 1*t*np.sin(2*np.pi*(0.005*t)*t)     # Vector for reference volume values ( Not zero vector this time)
volume_tank3 = np.zeros(len(t)) # zero vector for storing true volume values
error3 = np.zeros(len(t))       # Create a zero vector for storing true volume values
m_dot3 = Kp3*error3             # Compute a zero vector to store massflow control inputs
print(len(t))

# Start the simulation
for i in range(1, len(t)):      # Iterate throughout the simulation (i goes from 1 till the length of the time vector)
    if(i < 300):
        # Determine reference value vector for tank 1 and tank 2 for this region, if i is less than 300
        vol_r1[i] = vol_r1_i
        vol_r2[i] = vol_r2_i + 3*t[i]
    elif(i < 600):
        # Determine reference value vector for tank 1 and tank 2 for this region, if i is greater than 300 and less than 600
        vol_r1[i] = 20
        vol_r2[i] = vol_r2_i + 3*t[i]
        time_temp2 = t[i]
        temp2 = vol_r2[i]
    elif(i < 900):
        # Determine reference value vector for tank 1 and tank 2 for this region, if i is less than 900
        vol_r1[i] = 90
        vol_r2[i] = temp2 - 1*(t[i] - time_temp2)
    else:
        # Determine reference value vector for tank 1 and tank 2 for this region, if i is same as or greater than 900
        vol_r1[i] = 50
        vol_r2[i] = temp2 - 1*(t[i] - time_temp2)

    # Compute the errors between reference values and the true values for tank 1,2 and 3
    error1[i-1] = vol_r1[i-1] - volume_tank1[i-1]   # Reference volume - actual volume in the tank
    error2[i-1] = vol_r2[i-1] - volume_tank2[i-1]   # Reference volume - actual volume in the tank
    error3[i-1] = vol_r3[i-1] - volume_tank3[i-1]   # Reference volume - actual volume in the tank

    # Compute the control inputs for all the tanks
    m_dot1[i] = Kp1*error1[i-1]
    m_dot2[i] = Kp2*error2[i-1]
    m_dot3[i] = Kp3*error3[i-1]

    # Compute the true tank volumes in the next time step through this numberical integration (trapazoidal rule)
    volume_tank1[i] = volume_tank1[i-1] + (m_dot1[i-1]+m_dot1[i])/(2*density_water)*(dt)
    volume_tank2[i] = volume_tank2[i-1] + (m_dot2[i-1]+m_dot2[i])/(2*density_water)*(dt)
    volume_tank3[i] = volume_tank3[i-1] + (m_dot3[i-1]+m_dot3[i])/(2*density_water)*(dt)

# Start the animation
vol_r1_2 = vol_r1
vol_r2_2 = vol_r2
vol_r3_2 = vol_r3

def update_plot(num):
    if(num >= len(volume_tank1)):
        num = len(volume_tank1)-1

    tank_12.set_data([0,0],[-63,volume_tank1[num]-63])
    tnk_1.set_data(t[0:num],volume_tank1[0:num])
    vol_r1.set_data([-radius*width_ratio,radius*width_ratio],[vol_r1_2[num],vol_r1_2[num]])
    vol_r1_line.set_data([t0,t_end],[vol_r1_2[num],vol_r1_2[num]])

    tank_22.set_data([0,0],[-63,volume_tank2[num]-63])
    tnk_2.set_data(t[0:num],volume_tank2[0:num])
    vol_r2.set_data([-radius*width_ratio,radius*width_ratio],[vol_r2_2[num],vol_r2_2[num]])
    vol_r2_line.set_data([t0,t_end],[vol_r2_2[num],vol_r2_2[num]])

    tank_32.set_data([0,0],[-63,volume_tank3[num]-63])
    tnk_3.set_data(t[0:num],volume_tank3[0:num])
    vol_r3.set_data([-radius*width_ratio,radius*width_ratio],[vol_r3_2[num],vol_r3_2[num]])
    vol_r3_line.set_data([t0,t_end],[vol_r3_2[num],vol_r3_2[num]])


    return  vol_r1,tank_12,vol_r1_line,tnk_1,\
            vol_r2,tank_22,vol_r2_line,tnk_2,\
            vol_r3,tank_32,vol_r3_line,tnk_3,\
            
#Set up your figure properties
fig = plt.figure(figsize=(16,9), dpi=120, facecolor=(0.8,0.8,0.8))
gs=gridspec.GridSpec(2,3)

# Create object for Tank 1
ax0 = fig.add_subplot(gs[0,0], facecolor=(0.9,0.9,0.9))
vol_r1,=ax0.plot([],[],'r',linewidth=2)
tank_12,=ax0.plot([],[],'royalblue',linewidth=260, zorder=0)
plt.xlim(-radius*width_ratio, radius*width_ratio)
plt.ylim(bottom, final_volume)
plt.xticks(np.arange(-radius, radius+1, radius))
plt.yticks(np.arange(bottom,final_volume+dVol, dVol))
plt.ylabel('tank volume [m^3]')
plt.title('Tank 1')

# Create object for Tank 2
ax1 = fig.add_subplot(gs[0,1], facecolor=(0.9,0.9,0.9))
vol_r2,=ax1.plot([],[],'r',linewidth=2)
tank_22,=ax1.plot([],[], 'royalblue', linewidth=260, zorder=0)
plt.xlim(-radius*width_ratio, radius*width_ratio)
plt.ylim(bottom, final_volume)
plt.xticks(np.arange(-radius, radius+1, radius))
plt.yticks(np.arange(bottom,final_volume+dVol, dVol))
plt.title('Tank 2')

# create object for Tank 3
ax2 = fig.add_subplot(gs[0,2], facecolor=(0.9,0.9,0.9))
vol_r3,=ax2.plot([],[],'r',linewidth=2)
tank_32,=ax2.plot([],[], 'royalblue', linewidth=260, zorder=0)
plt.xlim(-radius*width_ratio, radius*width_ratio)
plt.ylim(bottom, final_volume)
plt.xticks(np.arange(-radius, radius+1, radius))
plt.yticks(np.arange(bottom,final_volume+dVol, dVol))
plt.title('Tank 3')

# Create volume function
ax3=fig.add_subplot(gs[1,:], facecolor=(0.9,0.9,0.9))
vol_r1_line,=ax3.plot([],[],'r', linewidth=2)
vol_r2_line,=ax3.plot([],[],'r', linewidth=2)
vol_r3_line,=ax3.plot([],[],'r', linewidth=2)
tnk_1,=ax3.plot([],[],'blue', linewidth=4,label='Tank 1')
tnk_2,=ax3.plot([],[],'green', linewidth=4,label='Tank 2')
tnk_3,=ax3.plot([],[],'red', linewidth=4,label='Tank 3')
plt.xlim(0,t_end)
plt.ylim(0,final_volume)
plt.ylabel('Tank volume [m^3]')
plt.grid(True)
plt.legend(loc='upper right', fontsize='small')

plane_ani = animation.FuncAnimation(fig, update_plot, frames=frame_amount, interval=20, repeat=True, blit=True)
plt.show()

