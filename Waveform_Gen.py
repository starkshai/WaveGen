import csv
from math import ceil
import matplotlib.pyplot as plt

def generate_square_wave(delay, clk_period, period, high_level, low_level, risetime, falltime, pulse_width, phase_step, num_cycles):
    data = []
    phase = 0
    data.append([0, 0])
    for i in range(num_cycles):
        time = i * period + delay#脉冲周期的开始
        value = low_level
        data.append([time, value])
        time = i * period + clk_period + phase + delay#当前脉冲周期内上升沿
        value = low_level
        data.append([time, value])
        time = i * period + clk_period + phase +  risetime + delay#当前脉冲周期内上升沿
        value = high_level
        data.append([time, value])
        time = i * period + clk_period + phase + pulse_width + delay#当前脉冲周期内下降沿
        value = high_level
        data.append([time, value])
        time = i * period + clk_period + phase +pulse_width + falltime + delay#当前脉冲周期内下降沿
        value = low_level
        data.append([time, value])

        phase = (phase + phase_step)

    return data

# 参数设置
clk_period = 5.0e-9  # 时钟周期（秒）
delay = 2 * clk_period  # 开始的延迟时间（秒）
pulse_period_number = 15 #多少个时钟周期内会产生一次脉冲
pulse_period = clk_period*pulse_period_number  # 脉冲周期（秒）
high_level = 1.8  # 高电平值
low_level = 0.0  # 低电平值
risetime = 100e-12  # 上升时间（秒）
falltime = 100e-12  # 下降时间（秒）
pulse_width = 3 *clk_period  # 脉冲宽度（秒）
bit_number = 6 # 转化器位数
lsb_number = 2  #每级台阶分成2^lsb_number份
phase_step = clk_period / (2 ** (bit_number + lsb_number))  # 相邻周期变化的相位（秒）
pulse_number = ceil(clk_period / phase_step) #脉冲相位变化刚好遍历一个clk

# 生成波形数据
waveform_data = generate_square_wave(delay, clk_period, pulse_period, high_level, low_level, risetime, falltime, pulse_width, phase_step, pulse_number)

# 将数据保存到CSV文件
filename = "square_wave.csv"
with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Value"])  # 写入CSV文件的标题行
    writer.writerows(waveform_data)  # 写入波形数据

print(f"CSV文件 '{filename}' 已生成。")
# check the waveforms
def detect_rising_edges(waveform_data, clk_period):
    rising_edges = []
    for i in range(1, len(waveform_data)):
        if waveform_data[i][1] > waveform_data[i-1][1]:
            time_diff = ceil(waveform_data[i][0] / clk_period) * clk_period - waveform_data[i][0]
            rising_edges.append(time_diff)
    return rising_edges

rising_edge_diffs = detect_rising_edges(waveform_data, clk_period)
print("Rising edge time differences:",rising_edge_diffs[0],rising_edge_diffs[250],rising_edge_diffs[251],rising_edge_diffs[255])
print("Rising edge number:", len(rising_edge_diffs))
plt.plot(range(len(rising_edge_diffs)), rising_edge_diffs)
# 设置横轴标签为整数
xtickswidth=2**4
plt.xticks(range(0, len(rising_edge_diffs)+xtickswidth, xtickswidth), range(0, len(rising_edge_diffs)+xtickswidth, xtickswidth))
# 设置纵轴标签
plt.ylabel('Time Difference')
# 设置图形标题
plt.title('Rising Edge Time Differences')
plt.savefig('rising_edge_diffs.png')
