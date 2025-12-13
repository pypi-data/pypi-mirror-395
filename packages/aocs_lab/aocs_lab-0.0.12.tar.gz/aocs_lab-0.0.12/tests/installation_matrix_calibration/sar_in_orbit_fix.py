from scipy.spatial.transform import Rotation as R

# 校正俯仰轴 (俯仰角增加为正，俯仰角减小为负)
r1 = R.from_euler('xyz', [0, -0.390555583, 0], degrees=True)

# 原始 SAR 天线安装矩阵
r2 = R.from_quat([0.9999999677867,
                  0.0001570796351,
                  -0.0000785398185,
                  -0.0001832595732], scalar_first=True)

r3 = r1*r2

q3 = r3.as_quat(scalar_first=True)

for q in q3:
    print(f'{q:.16f}')
