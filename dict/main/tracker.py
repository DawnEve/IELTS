# tracker module
#
from __init__ import *
from urllib.parse import unquote

def  add_tracker_routes(app):
    from datetime import datetime

    def get_monthly_filename():
        """生成按月分组的文件名"""
        return f"dustbin_video_logs_{datetime.now().strftime('%Y%m')}.txt"

    def ensure_log_directory():
        """确保日志目录存在"""
        if not os.path.exists('dustbin'):
            os.makedirs('dustbin')


    import time
    def timeStamp2human(timeStamp=0, time_format="%Y/%m/%d %H:%M:%S"):
        if timeStamp == None:
            timeStamp = 0
        timeArray = time.localtime(timeStamp)
        return time.strftime(time_format, timeArray)
    #test
    #timeStamp2human(time.time())
    # '2024.01.09 08:44:35'


# curl -I  http://192.168.1.3:20180/api/tracker/video-tracker
# curl -v -X post  http://192.168.1.3:20180/api/tracker/video-tracker -d '{ipAddress:"0.0.10.1"}'
# curl -v -X POST http://192.168.1.3:20180/api/tracker/video-tracker      -H "Content-Type: application/json"      -d '{"videoName":"test01234-好的.mp4", "userAgent":"chrome1000"}'

    # 记录视频的播放情况
    # 在 preflight 上耗时较多
    @app.route('/api/tracker/video-tracker', methods=['GET', 'POST', 'OPTIONS'])
    def video_tracker():
        # test for API
        if request.method == 'GET':
            return cors('tracker GET: invalid request')
        
        if request.method == 'OPTIONS':
            # 处理预检请求
            return cors({}, 1, request), 200

        try:
            data = request.json
            ip=data.get('ipAddress', 'unknown')
            if ip=="unknown":
                ip=request.remote_addr;

            videoName=unquote( data.get('videoName', 'unnamed') )

            log_entry = (
                f"server:{timeStamp2human(time.time())}|"
                f"bowser:{data.get('timestamp', 'NA')}|"
                f"ip:{ip}|"
                f"videoName:{videoName}|"
                f"actionName:{data.get('actionName', 'unnamed')}|"
                f"userAgent:{data.get('userAgent', 'unknown')}\n"
            )

            ensure_log_directory()
            with open(f"dustbin/{get_monthly_filename()}", 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return cors({"status": "success"}, 1, request), 200

        except Exception as e:
            return cors({"error": str(e)}, 1, request), 500
#
