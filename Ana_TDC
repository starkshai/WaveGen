import csv
import matplotlib.pyplot as plt
import numpy as np

# 定义两个空数组用于存储两列数据
time = []
vout = []

# 打开 CSV 文件
with open('TDCSOUT1.csv', 'r') as file:
    # 创建 CSV 读取器
    reader = csv.reader(file)
    
    # 跳过标题行（如果有）
    next(reader)
    
    # 读取每一行并将数据存入数组
    for row in reader:
        time.append(float(row[0]))
        vout.append(float(row[1]))

n=1 # debug index
#print("time:",time[n],"vout:",vout[n])
en_plot=0 # 1 for plot sout

if en_plot==1:

# 设置图形大小，例如宽度为10，高度为6
    plt.figure(figsize=(15, 6))
    plt.plot(time, vout,marker='o')

# 添加标题和轴标签
    plt.title('Vout vs Time')
    plt.xlabel('Time')
    plt.ylabel('Vout')
    plt.savefig('Sout.png')
    print("Sout.png saved")

#convert analog waveform to digital data with sampling at falling edge of clk
clk_frequency = 200e6
clk_period = 1/clk_frequency
clk_delay = 0 #assume the first point is the rising edge of clk
clk_time = clk_delay + clk_period/2
doutraw = []
dout = []
bout = []

for i in range(len(time)):
    if time[i] > clk_time:
        if vout[i] > 0.9:
            doutraw.append(1)
        else:
            doutraw.append(0)
        clk_time = clk_time + clk_period

en_save_doutraw=0 # 1 for save doutraw

if en_save_doutraw==1:
    filename = "Doutraw.csv"
# 打开文件并写入数据
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
    
    # 每一行写入8个数据
        for i in range(0, len(doutraw), 8):
            if i + 8 > len(doutraw):
                writer.writerow(doutraw[i:])
            else:
                writer.writerow(doutraw[i:i+8])

    print(f"数据已写入到文件 {filename} 中。")

# pick up the 8-bit data
i=0
while i<len(doutraw)-7:
    if doutraw[i]==1 and doutraw[i+7]==1:
        tmp=0
        for j in range(6):
            dout.append(doutraw[i+1+j])
            tmp=tmp+doutraw[i+1+j]*2**(5-j)
        bout.append(tmp)
        #print("bout",tmp)
        i=i+8
    else:
        i=i+1

en_save_dout=0 # 1 for save dout
if en_save_dout==1:
    filename = "Dout.csv"

# 打开文件并写入数据
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
    
    # 每一行写入6个数据
        for i in range(0, len(dout), 6):
            if i + 6 > len(dout):
                writer.writerow(dout[i:])
            else:
                writer.writerow(dout[i:i+6])

    print(f"数据已写入到文件 {filename} 中。")

en_save_bout=1 # 1 for save bout

if en_save_bout==1:
    filename = "Bout.csv"

# 打开文件并写入数据
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
    
    # 每一行写入1个数据
        for i in range(len(bout)):
                writer.writerow([str(bout[i])])

    print(f"数据已写入到文件 {filename} 中。")

index=0
for i in range(len(bout)):
    if bout[i] < 10 and bout[i+1] > 40:
        index=i+1
#rearrange bout
bout=bout[index:]+bout[0:index]
bout = bout[::-1]

delaytime= np.linspace(0, 5000, len(bout))
plt.figure(figsize=(15, 6))
plt.plot(delaytime, bout,marker='o')

# 添加标题和轴标签
plt.title('TDC transfer function (pre-simulation)')
plt.xlabel('Delay time (ps)')
plt.ylabel('TDC code')
plt.savefig('Bout.png')
print("Bout.png saved")
