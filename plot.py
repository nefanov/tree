import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


x = np.array([1*1024,2*1024,3*1024,4*1024,5*1024,6*1024,7*1024,8*1024])

#Simple load

y1_sus = np.array([1299,2174,3012,4119,5043,6053,7113,8011])
y2_sus = np.array([1243,2128,2931,3975,4953,5987,6801,8079])
y1_rec = np.array([639,1140,1633,2057,2608,3027,3579,4012])
y2_rec = np.array([245,693,1454,2243,3500,4878,6284,8070])

y1_ker = np.array([639,1140,1633,2057,2608,3027,3579,4012])
y2_ker = np.array([324,456,615,631,920,1041,1201,1323])

y1= y1_sus + y1_rec
y2 = y2_sus + y2_rec


plt.subplot(1, 1, 1)
plt.plot(x, y1, '.-')

plt.ylabel('Overhead, ms')
blue_patch = mpatches.Patch(color='lightblue', label='AGTTM-Simple Test')

plt.subplot(1, 1, 1)
plt.plot(x, y2, '.-',color='green')
plt.xlabel('Number of processes')
plt.ylabel('Overhead, ms')
red_patch = mpatches.Patch(color='green', label='BPSF-Simple Test')
plt.legend(handles=[red_patch,blue_patch])

y3_sus = np.array([1201,2055,3203,4242,4962,5649,6988,7702])
y4_sus = np.array([1609,2195,3217,4059,5025,6129,7092,7804])

y3_rec = np.array(sorted([554,3993,7957,3130,2222,2080,2459,3207]))
y4_rec = np.array([316,718,1479,2529,3843,5481,7481,9723])

y3 = y3_sus + y3_rec
y4 = y4_sus + y4_rec

y5_sus = y3_sus
y5_rec = np.array([0.001907/2*((1024*1)**2),0.001907/2*((1024*2)**2),0.001907/2*((1024*3)**2), 0.001907/2*((1024*4)**2)]) #,0.001907*((1024*2)**2),0.001907*((1024*2)**2),0.001907*((1024*2)**2)])

y5 = y5_sus[:4]+y5_rec[:4]
print(y1, y2)

print(y3, y4)
plt.subplot(1, 1, 1)
plt.plot(x, y3, '.-')
plt.title('Results of Tests')

b_patch = mpatches.Patch(color='orange', label='AGTTM-Context Test')

plt.subplot(1, 1, 1)

plt.plot(x, y4, '.-',color='red')
plt.xlabel('Number of processes')

r_patch = mpatches.Patch(color='red', label='BPSF-Context Test')

plt.subplot(1, 1, 1)
plt.plot(x[:4], y5, '--',color='black')
plt.title('Results of Tests')

t_patch = mpatches.Patch(color='black', label='The theoretical worst case')


plt.legend(handles=[red_patch,t_patch, blue_patch,r_patch,b_patch])
plt.rc('grid', linestyle='dotted', color='black')
plt.grid(True)
plt.show()



