from datetime import datetime, timedelta
import time
import sys

def beijing_to_utc_time_str(beijing_time_str: str):
    # 将字符串转换为 datetime 对象
    beijing_time = datetime.strptime(beijing_time_str, '%Y-%m-%dT%H:%M:%S')

    # 北京时间转为 UTC 时间，减去8小时
    utc_time = beijing_time - timedelta(hours=8)

    # 转换为字符串表示
    utc_time_str = utc_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return utc_time_str

def print_percentage(current, total, start_time):
    """计算进度与时间"""
    elapsed_time = time.time() - start_time

    progress = current / total

    if current > 0:
        estimated_total_time = elapsed_time / progress
        remaining_time = estimated_total_time - elapsed_time
    else:
        estimated_total_time = 0
        remaining_time = 0

    percent = (current / total) * 100
    sys.stdout.write(f"\rProgress: {percent:.2f}% | Elapsed: {
        elapsed_time/60:.1f} min | Remaining: {remaining_time/60:.1f} min")
    # sys.stdout.flush()


def gmst_time(jd_ut1, longitude_deg):
    # 当地平太阳时 计算 当地赤经（right ascension）
    # ALGORITHM 15 (Vallado, D.A. and McClain, W.D. (2013) Fundamentals of Astrodynamics and Applications. Fourth Edition.)
    J2000_jd  = 2_451_545 # January 1, 2000 12:00:00.000
    jd_century = 36_525
    t_ut1 = (jd_ut1 - J2000_jd) / jd_century
    theta_gmst_second = (67_310.548_41 
                + (876_600 * 3600 + 8_640_184.812_866) * t_ut1
                + 0.093_104 * t_ut1**2
                - 6.2e-6 * t_ut1**3)
    
    theta_gmst_second = theta_gmst_second % 86400
    theta_gmst_hour = theta_gmst_second / 3600
    theta_gmst_deg = theta_gmst_hour * 15

    theta_lst_deg = (theta_gmst_deg + longitude_deg) % 360
    
    return theta_gmst_deg, theta_lst_deg



if __name__ == "__main__":
    from astropy.time import Time

    # 如果升交点地方时是22:30:00，则22:30:00对应的升交点赤经可计算如下
    t = Time('2026-01-01T22:30:00', format='isot', scale='ut1')
    theta_gmst_deg, theta_lst_deg = gmst_time(t.jd, 0)
    print(theta_gmst_deg)

    # 利用 astropy 计算当地恒星时
    t = Time('2026-01-01T22:30:00', format='isot', scale='ut1', location=('0d', '0d'))
    longitude_deg = t.sidereal_time('mean').deg
    print(longitude_deg)

    # 比较计算方法偏差
    d_hour = (theta_lst_deg - longitude_deg) / 15
    d_sec = d_hour * 3600
    print(d_sec)

