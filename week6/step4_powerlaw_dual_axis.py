"""
Step 4: Power Law Model - Interactive Dual Axis Analysis 
전단 속도에 따른 전단 응력(τ)과 겉보기 점도(η)의 변화를 이중 Y축으로 시각화하며,
슬라이더를 통해 비선형 파라미터 조작에 따른 실시간 거동 변화를 분석합니다.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

# 1. 한글 및 마이너스 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2. 초기 데이터 및 변수 설정
initial_K = 4.0160  # 농도 계수 (Pa·s^n)
initial_n = 0.6650  # 유동 지수 (n < 1: 전단 박화)
shear_rate = np.linspace(0.1, 100, 500)  # 전단 속도 (1/s)

def calc_power_law(K, n, gamma):
    stress = K * (gamma ** n)
    viscosity = K * (gamma ** (n - 1))
    return stress, viscosity

stress_init, viscosity_init = calc_power_law(initial_K, initial_n, shear_rate)

# 3. 그래프 및 UI 레이아웃 설정
fig, ax1 = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25, top=0.9)  # 슬라이더 공간(하단) 확보

# 3-1. 첫 번째 Y축: 전단 응력 (Shear Stress)
color1 = 'tab:red'
ax1.set_xlabel('Shear Rate ($\dot{\gamma}$, $s^{-1}$)', fontsize=12)
ax1.set_ylabel('Shear Stress ($\\tau$, Pa)', color=color1, fontsize=12)
line1, = ax1.plot(shear_rate, stress_init, color=color1, lw=3, label='Shear Stress ($\\tau$)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 200)
ax1.grid(True, linestyle='--', alpha=0.5)

# 3-2. 두 번째 Y축: 겉보기 점도 (Apparent Viscosity)
ax2 = ax1.twinx()
color2 = 'tab:blue'
ax2.set_ylabel('Apparent Viscosity ($\eta$, Pa·s)', color=color2, fontsize=12)
line2, = ax2.plot(shear_rate, viscosity_init, color=color2, lw=3, linestyle='--', label='Apparent Viscosity ($\eta$)')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(0, 50)

# 범례 통합 (하단 배치)
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=11)

# 4. 슬라이더 인터페이스 배치
ax_K = plt.axes([0.15, 0.1, 0.7, 0.03], facecolor='whitesmoke')
ax_n = plt.axes([0.15, 0.04, 0.7, 0.03], facecolor='whitesmoke')

slider_K = Slider(ax_K, 'Consistency (K) ', 1.0, 20.0, valinit=initial_K, valstep=0.1)
slider_n = Slider(ax_n, 'Flow Index (n) ', 0.1, 1.8, valinit=initial_n, valstep=0.05)

# 5. 실시간 업데이트 함수
def update(val):
    c_K = slider_K.val
    c_n = slider_n.val
    
    # 데이터 재계산
    new_stress, new_viscosity = calc_power_law(c_K, c_n, shear_rate)
    
    # 그래프 데이터 갱신
    line1.set_ydata(new_stress)
    line2.set_ydata(new_viscosity)
    
    # 유체 유형 판별 및 제목 업데이트
    f_type = "Pseudoplastic (n<1)" if c_n < 0.95 else ("Dilatant (n>1)" if c_n > 1.05 else "Newtonian (n=1)")
    ax1.set_title(f"Dynamic Power Law Analysis: {f_type}\n(K = {c_K:.2f}, n = {c_n:.2f})", 
                 fontsize=14, fontweight='bold', pad=20)
    
    fig.canvas.draw_idle()

# 슬라이더 이벤트 연결
slider_K.on_changed(update)
slider_n.on_changed(update)

# 초기 호출 (제목 설정용)
update(None)

# 6. 결과 저장 및 출력
save_path = '../../assets/week6/power_law_model_chart.png'
os.makedirs(os.path.dirname(save_path), exist_ok=True)
plt.savefig(save_path, dpi=300, bbox_inches='tight')

print(f"인터랙티브 시뮬레이터가 실행됩니다. (저장 경로: {os.path.abspath(save_path)})")
plt.show()
