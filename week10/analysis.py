import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def calculate_physics(e, dt):
    g = 9.81              
    h = 1.0               
    t_total = 1.2        
    t_fall = np.sqrt(2 * h / g)  
    
    v1 = -np.sqrt(2 * g * h)     
    v2 = abs(v1) * e             
    
    time = np.linspace(0, t_total, 3000)
    y_points, a_points = [], []

    for t in time:
        if t < t_fall:
            # 자유 낙하 구간
            y_points.append(h - 0.5 * g * t**2)
            a_points.append(-g)
        elif t < t_fall + dt:
            # 충돌 구간 (가속도 피크 발생)
            y_points.append(0)
            a_points.append((v2 - v1) / dt)
        else:
            # 반등 구간
            t_b = t - (t_fall + dt)
            yt = v2 * t_b - 0.5 * g * t_b**2
            y_points.append(yt if yt > 0 else 0)
            a_points.append(-g if yt > 0 else 0)
            
    return time, np.array(y_points), np.array(a_points), t_fall

t, y_h, a_h, tf = calculate_physics(0.34, 0.005) 
_, y_s, a_s, _ = calculate_physics(0.18, 0.020) 


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

ax1.plot(t, y_h, 'r', lw=2, label='맨바닥 (Hard)')
ax1.plot(t, y_s, 'g', lw=2, label='완충재 (Soft)')
ax1.fill_between(t, y_h, color='red', alpha=0.1)
ax1.fill_between(t, y_s, color='green', alpha=0.1)
ax1.set_title('높이-시간 그래프', fontsize=14)
ax1.set_ylabel('높이 (m)')
ax1.legend()
ax1.grid(True, alpha=0.2)


ax2.plot(t, a_h, 'r', alpha=0.8, label='맨바닥 가속도')
ax2.plot(t, a_s, 'g', alpha=0.8, label='완충재 가속도')

threshold = 600
ax2.axhline(threshold, color='orange', ls='--', lw=2, label=f'손상 임계치 ({threshold} m/s²)')
ax2.fill_between(t, threshold, 1500, color='orange', alpha=0.1) 


axins = inset_axes(ax2, width="35%", height="45%", loc='upper right', borderpad=2)
axins.plot(t, a_h, 'r'); axins.plot(t, a_s, 'g')
axins.set_xlim(tf - 0.01, tf + 0.04)
axins.set_ylim(-50, 1500)
axins.grid(True, alpha=0.2)

ax2.set_title('가속도-시간 그래프', fontsize=14)
ax2.set_xlabel('시간 (s)')
ax2.set_ylabel('가속도 (m/s²)')
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig('analysis_result.png', dpi=300, bbox_inches='tight')
plt.show()