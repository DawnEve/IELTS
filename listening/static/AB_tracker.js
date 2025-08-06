// 获取用户IP地址
function getUserIP() {
	try {
		//const response = await fetch('https://api.ipify.org?format=json');
		const response = fetch('https://api64.ipify.org/?format=json');
		const data = response.json();
		return data.ip;
	} catch (error) {
		//console.error('Get IP address error:', error);
		return 'unknown';
	}
}
const userIP = getUserIP();

// 获取浏览器时间戳
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  
  return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}

// 使用示例
//console.log(formatDate( new Date() )); // 输出格式如：2025/08/06 16:14:25



// 视频名称监控上报脚本
function reportVideoToMonitor(videoName, actionName="") {
    const endpoint = 'http://192.168.1.3:20180/api/tracker/video-tracker';

    const payload = {
        videoName: videoName,
        timestamp: formatDate(new Date()),
        userAgent: navigator.userAgent,
		ipAddress: userIP,
		actionName: actionName
    };

    // 使用navigator.sendBeacon确保可靠发送，即使页面关闭
    if (navigator.sendBeacon) {
        const blob = new Blob([JSON.stringify(payload)], {type: 'application/json'});
        navigator.sendBeacon(endpoint, blob);
    } else {
        // 回退到fetch API
        fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: {
                //'Content-Type': 'application/json'
                'Content-Type': 'application/json;charset=UTF-8'
            },
            keepalive: true  // 确保请求在页面卸载时也能完成
        }).catch(() => {});  // 忽略所有错误
    }
}

// How to use?
// reportVideoToMonitor("test2-HP3000-中文-功夫熊猫-动画剧.mp4", "load");