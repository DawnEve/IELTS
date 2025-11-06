# app.py
import os
import re
from collections import defaultdict
from flask import Flask, render_template_string, send_from_directory, abort, make_response

# === 修改为你的本地目录 ===
ROOT_DIR = r"E:\BaiduNetdiskDownload\4.牛津树全套" #结尾不能是\，否则报错，即使前面有r也报错。
AUDIO_DIR = ROOT_DIR+r"\【美音】牛津树1-16级"
PDF_DIR   = ROOT_DIR+r"\【PDF】牛津树1-9级-学校版"
EX_DIR    = ROOT_DIR+r"\【练习册】牛津树1-9级"

KEY_PAT = re.compile(r'(?P<level>\d+)-(?P<idx>\d+)', re.IGNORECASE)

app = Flask(__name__)
resources = defaultdict(dict)  # (level, idx) -> dict


def add_resource(root_dir, filename, kind):
    m = KEY_PAT.search(filename)
    if not m:
        return
    level = int(m.group("level"))
    idx = int(m.group("idx"))
    key = (level, idx)

    full = os.path.join(root_dir, filename)

    # 只取文件名，不含任何上级目录
    base = os.path.basename(filename)                  # e.g. "1-01 At school(无字书).pdf"
    name_wo_ext = os.path.splitext(base)[0]            # 去掉扩展名
    # 去掉前导编号 "1-01 "
    title_guess = re.sub(r'^\d+\s*-\s*\d+\s*', '', name_wo_ext)
    # 去掉一些尾缀（可选）
    #title_guess = title_guess.replace('--美音', '').replace('(无字书)', '').strip(' -_')

    resources[key].setdefault("title_guess", title_guess)
    resources[key][kind] = full



def scan_dir(root_dir, exts, kind):
    if not os.path.isdir(root_dir):
        return
    for r, _, files in os.walk(root_dir):
        for fn in files:
            if os.path.splitext(fn)[1].lower() in exts:
                rel = os.path.relpath(os.path.join(r, fn), root_dir)
                add_resource(root_dir, rel, kind)

def build_index():
    resources.clear()
    scan_dir(AUDIO_DIR, {".mp3"}, "audio")
    scan_dir(PDF_DIR, {".pdf"}, "pdf")
    scan_dir(EX_DIR, {".pdf"}, "ex")

@app.route("/file/audio/<path:relpath>")
def serve_audio(relpath):
    return send_from_directory(AUDIO_DIR, relpath)

@app.route("/file/pdf/<path:relpath>")
def serve_pdf(relpath):
    return send_from_directory(PDF_DIR, relpath)

@app.route("/file/ex/<path:relpath>")
def serve_ex(relpath):
    return send_from_directory(EX_DIR, relpath)

@app.route("/")
def index():
    levels = defaultdict(list)
    for (level, idx), v in resources.items():
        title = v.get("title_guess", "")
        has_audio = "audio" in v
        has_pdf = "pdf" in v
        has_ex = "ex" in v
        levels[level].append((idx, (level, idx), title, has_audio, has_pdf, has_ex))
    for lv in levels:
        levels[lv].sort(key=lambda x: x[0])
    return render_template_string(TPL_INDEX, levels=dict(sorted(levels.items())))

@app.route("/view/<int:level>/<int:idx>")
def view_item(level, idx):
    key = (level, idx)
    if key not in resources:
        abort(404)
    v = resources[key]
    title = v.get("title_guess", f"{level}-{idx:02d}")

    audio_url = None
    if "audio" in v:
        rel = os.path.relpath(v["audio"], AUDIO_DIR).replace("\\", "/")
        audio_url = f"/file/audio/{rel}"

    pdf_url = None
    if "pdf" in v:
        rel = os.path.relpath(v["pdf"], PDF_DIR).replace("\\", "/")
        pdf_url = f"/file/pdf/{rel}"

    ex_url = None
    if "ex" in v:
        rel = os.path.relpath(v["ex"], EX_DIR).replace("\\", "/")
        ex_url = f"/file/ex/{rel}"

    # 找本级别的所有 idx，方便“自动连播”
    level_items = sorted([i for (lv, i) in resources.keys() if lv == level])

    resp= make_response(render_template_string(
        TPL_VIEW,
        level=level, idx=idx, title=title,
        audio_url=audio_url, pdf_url=pdf_url, ex_url=ex_url,
        level_items=level_items
    ))
    resp.set_cookie("last_seen", f"Level {level}-{idx:02d}", max_age=30*24*3600)
    return resp

# ---------------- HTML 模板 ----------------

TPL_INDEX = """
<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<title>牛津树 本地播放器</title>
<style>
body { font-family: sans-serif; margin:20px; }
.tabs { display: flex; border-bottom: 2px solid #ccc; }
.tab { padding:10px 20px; cursor:pointer; border:1px solid #ccc; border-bottom:none; margin-right:5px; background:#eee; border-top-left-radius:6px; border-top-right-radius:6px; }
.tab.active { background:#fff; font-weight:bold; }
.tab-content { display:none; padding:10px; border:1px solid #ccc; }
.tab-content.active { display:block; }
.grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(200px,1fr)); gap:8px; }
.item { border:1px solid #ddd; border-radius:6px; padding:6px; }
.tag { font-size:12px; background:#eee; padding:2px 6px; border-radius:10px; margin-right:4px; }


a.open-btn {
  display:inline-block;
  padding:4px 10px;
  background:#007bff;
  color:white;
  text-decoration:none;
  border-radius:6px;
  transition:0.2s;
}
a.open-btn:hover { background:#0056b3; }

</style>
</head>
<body>
<h1>牛津树 L1-L9</h1>



{% if request.cookies.get('last_seen') %}
  <p style="color:#555;font-style:italic;">上次看到：{{request.cookies.get('last_seen')}}</p>
{% endif %}

<div class="tabs">
  {% for lv in levels.keys() %}
    <div class="tab" onclick="showTab({{lv}})">级别 {{lv}}</div>
  {% endfor %}
</div>
{% for lv, items in levels.items() %}
  <div id="tab-{{lv}}" class="tab-content">
    <div class="grid">
    {% for idx, key, title, has_audio, has_pdf, has_ex in items %}
      <div class="item">
        <div><strong>{{lv}}-{{"%02d"|format(idx)}}</strong></div>
        <div>{{title}}</div>
        <div>
          {% if has_audio %}<span class="tag">音频</span>{% endif %}
          {% if has_pdf %}<span class="tag">PDF</span>{% endif %}
          {% if has_ex %}<span class="tag">练习册</span>{% endif %}
        </div>
        <a href="/view/{{lv}}/{{idx}}" class="open-btn">打开</a>
      </div>
    {% endfor %}
    </div>
  </div>
{% endfor %}
<script>
function showTab(lv){
  document.querySelectorAll('.tab').forEach(el=>el.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(el=>el.classList.remove('active'));
  document.querySelector('.tab[onclick="showTab('+lv+')"]').classList.add('active');
  document.getElementById('tab-'+lv).classList.add('active');
}
// 默认显示第一个tab
showTab({{levels.keys()|list|first}});
</script>
</body>
</html>
"""



TPL_VIEW = """
<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8"/>
<title>{{level}}-{{idx}} | 牛津树</title>
<style>
body { font-family: sans-serif; margin:20px; }
audio { width:100%; margin:10px 0; }
.controls button { margin-right:6px; }
iframe { width:100%; height:75vh; border:1px solid #ddd; }

#toast2 {
  position:fixed; bottom:20px; right:20px;
  background:rgba(0,0,0,0.7); color:white;
  padding:8px 14px; border-radius:6px; display:none;
}

#toast {
  position: fixed;
  top: 20px;                  /* 顶部距离 */
  left: 50%;                  /* 水平居中基准 */
  transform: translateX(-50%);/* 左右居中 */
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 14px;
  border-radius: 6px;
  display: none;
  z-index: 9999;              /* 确保在最上层 */
}

</style>
</head>
<body>

<div id="toast"></div>
<script>
function toast(msg){
  let t=document.getElementById('toast');
  t.innerText=msg; t.style.display='block';
  setTimeout(()=>{t.style.display='none';},1500);
}
</script>

<a href="/">← 返回列表</a>
<h2>{{level}}-{{"%02d"|format(idx)}} {{title}}</h2>

{% if audio_url %}
  <audio id="player" controls>
    <source src="{{audio_url}}" type="audio/mpeg">
  </audio>
  <div class="controls">
    <button onclick="setA()">Set A</button>
    <button onclick="setB()">Set B</button>
    <button onclick="toggleLoop()">Loop A-B</button>
    <button onclick="changeSpeed(0.5)">0.5x</button>
    <button onclick="changeSpeed(1)">1x</button>
    <button onclick="changeSpeed(1.5)">1.5x</button>
    <button onclick="changeSpeed(2)">2x</button>
    <button onclick="toggleAutoNext()">自动连播: <span id="autonext">关</span></button>
  </div>
{% endif %}

{% if pdf_url %}
  <p><a href="{{pdf_url}}" target="_blank">在新窗口打开 PDF</a></p>
  <iframe src="{{pdf_url}}"></iframe>
{% endif %}
{% if ex_url %}
  <p><a href="{{ex_url}}" target="_blank">下载练习册</a></p>
{% endif %}

<script>
let player = document.getElementById('player');
let pointA=null, pointB=null, looping=false, autoNext=false;
function setA(){ pointA=player.currentTime; toast("A点设置为 "+pointA.toFixed(1)+"s"); }
function setB(){ pointB=player.currentTime; toast("B点设置为 "+pointB.toFixed(1)+"s"); }
function toggleLoop(){ looping=!looping; toast("A-B循环: "+(looping?"开":"关")); }
function changeSpeed(s){ player.playbackRate=s; }
function toggleAutoNext(){ autoNext=!autoNext; document.getElementById('autonext').innerText = autoNext?"开":"关"; }
player.addEventListener('timeupdate',()=>{
  if(looping && pointA!==null && pointB!==null && player.currentTime>=pointB){
    player.currentTime=pointA;
  }
});
player.addEventListener('ended',()=>{
  if(autoNext){
    let items={{level_items|tojson}};
    let idx={{idx}};
    let pos=items.indexOf(idx);
    if(pos>=0 && pos<items.length-1){
      let next=items[pos+1];
      window.location.href="/view/{{level}}/"+next;
    }
  }
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build_index()
    app.run(host="127.0.0.1", port=5000, debug=True)

