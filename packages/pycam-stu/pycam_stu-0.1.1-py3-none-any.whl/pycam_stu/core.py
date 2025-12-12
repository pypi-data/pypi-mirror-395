import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import threading
import inspect
import queue
import csv

# 全局变量
_monitor_thread = None
_monitor_running = False
_danger_zone = None
_alert_queue = None
_cap = None
_caller_directory = None  # 存储调用者目录

# 功能状态
_motion_detection_enabled = False
_danger_zone_enabled = False
_pose_detection_enabled = False
_detection_mode = 0  # 0:关闭, 1:区域内报警, 2:区域外报警

# 状态变量
_motion_alert = False
_danger_alert = False

# 计时功能
_jishi_enabled = False
_jishi_start_time = 0
_shouwan_in_zone_time = 0
_shouwan_detect_time = 0
_last_report_time = 0
_camera_type = "USB"  # 默认USB摄像头
_camera_ip = "本地摄像头"  # 默认IP

def all(switch, thread_obj=None, alert_queue=None):
    """
    开启或关闭USB摄像头监控窗口
    
    参数:
        switch: 1 开启监控窗口, 0 关闭监控窗口
        thread_obj: 当关闭监控时，需要传入之前返回的线程对象
        alert_queue: 用于接收报警信息的队列
    
    返回:
        当开启监控时: 返回线程对象
        当关闭监控时: 返回 True/False 表示成功与否
    """
    global _monitor_thread, _monitor_running, _alert_queue, _cap, _caller_directory
    global _jishi_start_time, _shouwan_in_zone_time, _shouwan_detect_time, _last_report_time
    global _camera_type, _camera_ip
    
    if switch == 1:
        # 开启监控窗口
        if _monitor_running:
            print("监控已经在运行中")
            return _monitor_thread
            
        _monitor_running = True
        _alert_queue = alert_queue
        
        # 保存调用者目录
        _caller_directory = _get_caller_directory()
        
        # 重置计时器
        _jishi_start_time = time.time()
        _last_report_time = _jishi_start_time
        _shouwan_in_zone_time = 0
        _shouwan_detect_time = 0
        
        # 设置摄像头类型
        _camera_type = "USB"
        _camera_ip = "本地摄像头"
        
        # 使用USB摄像头
        _cap = cv2.VideoCapture(0)
        if not _cap.isOpened():
            print("无法打开USB摄像头")
            _monitor_running = False
            return None
        
        _monitor_thread = threading.Thread(target=_run_monitoring)
        _monitor_thread.daemon = True
        _monitor_thread.start()
        print("USB摄像头监控已启动")
        print("按键说明:")
        print("  1 - 开启运动检测")
        print("  2 - 开启危险区域检测(区域内报警)")
        print("  3 - 开启危险区域检测(区域外报警)")
        print("  0 - 关闭所有检测")
        print("  P - 退出监控")
        return _monitor_thread
        
    elif switch == 0:
        # 关闭监控
        if not _monitor_running:
            print("监控未在运行")
            return False
            
        _monitor_running = False
        
        # 生成最终计时报告
        if _jishi_enabled:
            _generate_jishi_report(final=True)
            
        if thread_obj and thread_obj.is_alive():
            thread_obj.join(timeout=2.0)
            print("监控已关闭")
            return True
        else:
            print("无法关闭监控线程")
            return False
            
    else:
        print("无效的开关参数，使用 1 开启或 0 关闭")
        return False

def ip(switch, ip_addr, username, password, channel=1, thread_obj=None, alert_queue=None):
    """
    开启或关闭海康威视网络摄像头监控
    
    参数:
        switch: 1 开启监控窗口, 0 关闭监控窗口
        ip_addr: 摄像头IP地址
        username: 用户名
        password: 密码
        channel: 通道号，默认为1
        thread_obj: 当关闭监控时，需要传入之前返回的线程对象
        alert_queue: 用于接收报警信息的队列
    
    返回:
        当开启监控时: 返回线程对象
        当关闭监控时: 返回 True/False 表示成功与否
    """
    global _monitor_thread, _monitor_running, _alert_queue, _cap, _caller_directory
    global _jishi_start_time, _shouwan_in_zone_time, _shouwan_detect_time, _last_report_time
    global _camera_type, _camera_ip
    
    if switch == 1:
        # 开启监控窗口
        if _monitor_running:
            print("监控已经在运行中")
            return _monitor_thread
            
        _monitor_running = True
        _alert_queue = alert_queue
        
        # 保存调用者目录
        _caller_directory = _get_caller_directory()
        
        # 重置计时器
        _jishi_start_time = time.time()
        _last_report_time = _jishi_start_time
        _shouwan_in_zone_time = 0
        _shouwan_detect_time = 0
        
        # 设置摄像头类型和IP
        _camera_type = "海康威视"
        _camera_ip = ip_addr
        
        # 使用海康威视网络摄像头
        rtsp_url = f"rtsp://{username}:{password}@{ip_addr}//Streaming/Channels/{channel}"
        _cap = cv2.VideoCapture(rtsp_url)
        if not _cap.isOpened():
            print(f"无法连接到海康威视摄像头: {ip_addr}")
            _monitor_running = False
            return None
        
        _monitor_thread = threading.Thread(target=_run_monitoring)
        _monitor_thread.daemon = True
        _monitor_thread.start()
        print(f"海康威视摄像头监控已启动: {ip_addr}")
        print("按键说明:")
        print("  1 - 开启运动检测")
        print("  2 - 开启危险区域检测(区域内报警)")
        print("  3 - 开启危险区域检测(区域外报警)")
        print("  0 - 关闭所有检测")
        print("  P - 退出监控")
        return _monitor_thread
        
    elif switch == 0:
        # 关闭监控
        if not _monitor_running:
            print("监控未在运行")
            return False
            
        _monitor_running = False
        
        # 生成最终计时报告
        if _jishi_enabled:
            _generate_jishi_report(final=True)
            
        if thread_obj and thread_obj.is_alive():
            thread_obj.join(timeout=2.0)
            print("监控已关闭")
            return True
        else:
            print("无法关闭监控线程")
            return False
            
    else:
        print("无效的开关参数，使用 1 开启或 0 关闭")
        return False

def js(switch):
    """
    开启或关闭计时功能
    
    参数:
        switch: 1 开启计时, 0 关闭计时
    """
    global _jishi_enabled, _jishi_start_time, _shouwan_in_zone_time, _shouwan_detect_time, _last_report_time
    
    if switch == 1:
        _jishi_enabled = True
        _jishi_start_time = time.time()
        _last_report_time = _jishi_start_time
        _shouwan_in_zone_time = 0
        _shouwan_detect_time = 0
        print("计时功能已开启")
    elif switch == 0:
        _jishi_enabled = False
        print("计时功能已关闭")
    else:
        print("无效的开关参数，使用 1 开启或 0 关闭")

def _generate_jishi_report(final=False):
    """生成计时报告CSV文件"""
    if not _jishi_enabled or not _caller_directory:
        return
        
    # 计算总时长
    current_time = time.time()
    total_time = current_time - _jishi_start_time
    
    # 计算手腕在区域内时长占比
    if _shouwan_detect_time > 0:
        in_zone_ratio = _shouwan_in_zone_time / _shouwan_detect_time
    else:
        in_zone_ratio = 0
    
    # 创建CSV文件 - 使用调用者目录
    csv_file = os.path.join(_caller_directory, "jishi_report.csv")
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 写入基本信息
        writer.writerow(["监控报告"])
        writer.writerow(["启动时间", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_jishi_start_time))])
        writer.writerow(["报告时间", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))])
        writer.writerow(["摄像头类型", _camera_type])
        writer.writerow(["摄像头IP", _camera_ip])
        writer.writerow([])  # 空行
        
        # 写入数据表头
        writer.writerow(["项目", "数值", "单位"])
        # 写入数据
        writer.writerow(["总监控时长", round(total_time, 2), "秒"])
        writer.writerow(["手腕在区域内时长", round(_shouwan_in_zone_time, 2), "秒"])
        writer.writerow(["手腕检测总时长", round(_shouwan_detect_time, 2), "秒"])
        writer.writerow(["手腕在区域内时长占比", f"{round(in_zone_ratio * 100, 2)}%", ""])
    
    if final:
        print(f"最终计时报告已保存: {csv_file}")
    else:
        print(f"计时报告已更新: {csv_file}")

def _check_and_generate_report():
    """检查是否需要生成报告（每10秒一次）"""
    global _last_report_time
    
    current_time = time.time()
    if current_time - _last_report_time >= 10.0:  # 每10秒更新一次
        _generate_jishi_report()
        _last_report_time = current_time

def _get_caller_directory():
    """获取调用者文件的目录"""
    # 获取调用栈
    frame = inspect.currentframe()
    try:
        # 向上回溯两层：当前函数 -> all/ip函数 -> 调用者
        caller_frame = frame.f_back.f_back
        caller_file = caller_frame.f_globals.get('__file__', '')
        if caller_file:
            return os.path.dirname(os.path.abspath(caller_file))
    finally:
        del frame  # 避免循环引用
    
    # 如果无法获取调用者路径，使用当前工作目录
    return os.getcwd()

def _send_alert(alert_type, message=""):
    """发送报警信息到队列"""
    global _alert_queue
    if _alert_queue:
        try:
            _alert_queue.put_nowait({
                "type": alert_type,
                "message": message,
                "timestamp": time.time()
            })
        except queue.Full:
            pass  # 如果队列已满，忽略新的报警

def _draw_status_panel(frame):
    """在图像上绘制状态面板"""
    global _motion_detection_enabled, _danger_zone_enabled, _pose_detection_enabled
    global _motion_alert, _danger_alert, _detection_mode
    global _jishi_enabled, _camera_type, _camera_ip
    
    # 面板背景
    panel_height = 220
    panel = np.zeros((panel_height, frame.shape[1], 3), dtype=np.uint8)
    
    # 标题
    cv2.putText(panel, "pycam_stu Monitoring", (10, 25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # 摄像头信息
    cv2.putText(panel, f"Camera: {_camera_type} ({_camera_ip})", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 监控状态
    status_color = (0, 255, 0) if _monitor_running else (0, 0, 255)
    status_text = "ACTIVE" if _monitor_running else "INACTIVE"
    cv2.putText(panel, f"Monitoring: {status_text}", (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
    
    # 计时状态
    jishi_color = (0, 255, 0) if _jishi_enabled else (0, 0, 255)
    jishi_text = "ON" if _jishi_enabled else "OFF"
    cv2.putText(panel, f"Timing: {jishi_text}", (10, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, jishi_color, 1)
    
    # 功能状态
    motion_color = (0, 255, 0) if _motion_detection_enabled else (0, 0, 255)
    motion_text = "ON" if _motion_detection_enabled else "OFF"
    cv2.putText(panel, f"Motion Detection: {motion_text}", (10, 110), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, motion_color, 1)
    
    pose_color = (0, 255, 0) if _pose_detection_enabled else (0, 0, 255)
    pose_text = "ON" if _pose_detection_enabled else "OFF"
    cv2.putText(panel, f"Pose Estimation: {pose_text}", (10, 130), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, pose_color, 1)
    
    danger_color = (0, 255, 0) if _danger_zone_enabled else (0, 0, 255)
    
    # 显示检测模式
    if _danger_zone_enabled:
        if _detection_mode == 1:
            danger_text = "ON (Inside Alert)"
        elif _detection_mode == 2:
            danger_text = "ON (Outside Alert)"
        else:
            danger_text = "ON"
    else:
        danger_text = "OFF"
        
    cv2.putText(panel, f"Danger Zone: {danger_text}", (10, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, danger_color, 1)
    
    # 警报状态
    motion_alert_color = (0, 0, 255) if _motion_alert else (0, 255, 0)
    motion_alert_text = "Yes" if _motion_alert else "No"
    cv2.putText(panel, f"Motion Alert: {motion_alert_text}", (10, 170), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, motion_alert_color, 1)
    
    danger_alert_color = (0, 0, 255) if _danger_alert else (0, 255, 0)
    danger_alert_text = "Yes" if _danger_alert else "No"
    cv2.putText(panel, f"Danger Alert: {danger_alert_text}", (200, 170), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, danger_alert_color, 1)
    
    # 操作提示
    cv2.putText(panel, "Press 1: Motion, 2: Inside Alert, 3: Outside Alert, 0: Off, P: Exit", 
                (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    # 将面板添加到帧的顶部
    result = np.vstack([panel, frame])
    return result

def _run_monitoring():
    """监控主循环，运行在单独的线程中"""
    global _monitor_running, _danger_zone, _cap, _caller_directory
    global _motion_detection_enabled, _danger_zone_enabled, _pose_detection_enabled
    global _motion_alert, _danger_alert, _detection_mode
    global _jishi_enabled, _shouwan_in_zone_time, _shouwan_detect_time, _last_report_time
    
    # 检查模型文件是否存在 - 使用调用者目录
    model_paths = [
        os.path.join(_caller_directory, 'yolov8n-pose.pt'),
        os.path.join(_caller_directory, 'yolov8n.pt'),
        'yolov8n-pose.pt',  # 回退到当前工作目录
        'yolov8n.pt'        # 回退到当前工作目录
    ]
    
    model_path = None
    for path in model_paths:
        if os.path.exists(path):
            model_path = path
            break
    
    if not model_path:
        print("错误: 未找到YOLO模型文件")
        print("请将以下任一模型文件放在调用脚本的同一目录下:")
        print("- yolov8n-pose.pt (推荐)")
        print("- yolov8n.pt")
        print("下载链接: https://github.com/ultralytics/assets/releases/download/v8.3.0/")
        return
    
    try:
        # 初始化YOLO模型
        model = YOLO(model_path)
        print(f"成功加载模型: {model_path}")
    except Exception as e:
        print(f"模型加载失败: {e}")
        print("请确保模型文件存在且格式正确")
        return
    
    # 检查摄像头是否打开
    if not _cap.isOpened():
        print("摄像头未打开")
        return
    
    # 选择危险区域
    _danger_zone = _select_danger_zone(_cap)
    if not _danger_zone:
        print("未选择危险区域，监控结束")
        _cap.release()
        return
    
    print(f"危险区域已设置: {_danger_zone}")
    
    # 监控循环变量
    fps_counter = 0
    pre_frame = None
    last_time = time.time()
    
    # 主监控循环
    while _monitor_running:
        success, frame = _cap.read()
        if not success:
            print("无法读取摄像头帧，尝试重新连接...")
            time.sleep(1)
            continue

        # 检查是否需要生成报告
        if _jishi_enabled:
            _check_and_generate_report()
        
        # 重置警报状态
        _motion_alert = False
        _danger_alert = False
        
        # 计算时间间隔
        current_time = time.time()
        time_interval = current_time - last_time
        last_time = current_time

        # 运动检测
        if _motion_detection_enabled:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (480, 480))
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            if pre_frame is None:
                pre_frame = gray
            else:
                frame_diff = cv2.absdiff(pre_frame, gray)
                thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > 1000:
                        _motion_alert = True
                        if fps_counter > 30:
                            # 发送运动报警
                            _send_alert("Dong", "检测到人员活动!")
                            # 保存到调用者目录
                            alert_path = os.path.join(_caller_directory, "alert_" + str(int(time.time())) + ".jpg")
                            cv2.imwrite(alert_path, frame)
                            fps_counter = 0
                        else:
                            fps_counter += 1
                        break
                
                pre_frame = gray

        # YOLO检测和危险区域检测
        wrist_in_zone = False
        wrist_detected = False  # 新增：标记是否检测到手腕
        if _pose_detection_enabled and _danger_zone_enabled:
            try:
                results = model(frame, verbose=False)
                
                # 绘制危险区域
                if _danger_zone:
                    cv2.rectangle(frame, (_danger_zone[0], _danger_zone[1]), 
                                 (_danger_zone[2], _danger_zone[3]), (0, 255, 0), 2)
                
                # 检测关键点是否进入危险区域
                for result in results:
                    if hasattr(result, 'keypoints') and result.keypoints is not None:
                        keypoints = result.keypoints.data
                        if len(keypoints) > 0:
                            # 使用第一个检测到的人
                            person_keypoints = keypoints[0]
                            
                            # 重置检测状态
                            wrist_detected = False
                            wrist_in_zone = False
                            
                            # 根据不同模型调整关键点索引
                            if 'pose' in model_path:
                                # 姿态估计模型的关键点
                                left_wrist_idx, right_wrist_idx = 9, 10
                            else:
                                # 标准检测模型，使用边界框中心点作为检测点
                                left_wrist_idx, right_wrist_idx = 0, 0
                            
                            # 检查左手腕
                            if len(person_keypoints) > left_wrist_idx:
                                left_wrist = person_keypoints[left_wrist_idx]
                                if left_wrist[2] > 0.5:  # 置信度阈值
                                    wrist_detected = True
                                    x, y = int(left_wrist[0]), int(left_wrist[1])
                                    if _danger_zone and (_danger_zone[0] < x < _danger_zone[2] and 
                                                      _danger_zone[1] < y < _danger_zone[3]):
                                        wrist_in_zone = True
                                        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                                    else:
                                        cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
                            
                            # 检查右手腕
                            if len(person_keypoints) > right_wrist_idx:
                                right_wrist = person_keypoints[right_wrist_idx]
                                if right_wrist[2] > 0.5:  # 置信度阈值
                                    wrist_detected = True
                                    x, y = int(right_wrist[0]), int(right_wrist[1])
                                    if _danger_zone and (_danger_zone[0] < x < _danger_zone[2] and 
                                                      _danger_zone[1] < y < _danger_zone[3]):
                                        wrist_in_zone = True
                                        cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                                    else:
                                        cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)
                            
                            # 计时：只在检测到手腕时累加时间
                            if _jishi_enabled and wrist_detected:
                                _shouwan_detect_time += time_interval
                                
                                # 如果至少有一只手腕在区域内，累加区域内时间
                                if wrist_in_zone:
                                    _shouwan_in_zone_time += time_interval
                            
                            # 根据检测模式判断是否报警
                            if _detection_mode == 1 and wrist_in_zone:
                                _danger_alert = True
                                _send_alert("IN", "检测到手腕进入危险区域")
                            elif _detection_mode == 2 and not wrist_in_zone:
                                _danger_alert = True
                                _send_alert("OUT", "检测到手腕离开安全区域")
                    
            except Exception as e:
                print(f"YOLO检测错误: {e}")

        # 添加状态面板并显示结果
        frame_with_status = _draw_status_panel(frame)
        cv2.imshow('pycam_stu Safety Monitoring', frame_with_status)
        
        # 检查按键
        key = cv2.waitKey(1) & 0xFF
        if key == ord('1'):
            # 开启运动检测
            _motion_detection_enabled = True
            _danger_zone_enabled = False
            _pose_detection_enabled = False
            _detection_mode = 0
            print("已开启运动检测")
        elif key == ord('2'):
            # 开启危险区域检测(区域内报警)
            _motion_detection_enabled = False
            _danger_zone_enabled = True
            _pose_detection_enabled = True
            _detection_mode = 1
            print("已开启危险区域检测(区域内报警)")
        elif key == ord('3'):
            # 开启危险区域检测(区域外报警)
            _motion_detection_enabled = False
            _danger_zone_enabled = True
            _pose_detection_enabled = True
            _detection_mode = 2
            print("已开启危险区域检测(区域外报警)")
        elif key == ord('0'):
            # 关闭所有检测
            _motion_detection_enabled = False
            _danger_zone_enabled = False
            _pose_detection_enabled = False
            _detection_mode = 0
            print("已关闭所有检测")
        elif key == ord('p') or key == ord('P') or key == 27:  # P键或ESC键
            break

    # 清理资源
    _cap.release()
    cv2.destroyAllWindows()
    _monitor_running = False
    print("监控线程已退出")

def _select_danger_zone(cap):
    """选择危险区域"""
    danger_zone = None
    drawing = False
    ix, iy = -1, -1
    current_x, current_y = -1, -1
    
    def draw_danger_zone(event, x, y, flags, param):
        nonlocal ix, iy, drawing, danger_zone, current_x, current_y
        current_x, current_y = x, y
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            danger_zone = (min(ix, x), min(iy, y), max(ix, x), max(iy, y))
    
    print("请用鼠标选择危险区域：点击并拖动绘制矩形，按'm'键继续")
    cv2.namedWindow('Select Danger Zone')
    cv2.setMouseCallback('Select Danger Zone', draw_danger_zone)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取摄像头帧")
            break
            
        temp_frame = frame.copy()
        if drawing:
            cv2.rectangle(temp_frame, (ix, iy), (current_x, current_y), (0, 255, 0), 2)
        elif danger_zone:
            cv2.rectangle(temp_frame, (danger_zone[0], danger_zone[1]), 
                         (danger_zone[2], danger_zone[3]), (0, 255, 0), 2)
        
        cv2.imshow('Select Danger Zone', temp_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('m') and danger_zone:
            break
        elif key == 27:  # ESC键
            danger_zone = None
            break
    
    cv2.destroyWindow('Select Danger Zone')
    return danger_zone