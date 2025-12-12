import signal
import sys
import os
import time
import traceback

# حفظ النسخ الأصلية
_ORIG = {
    "sys_exit": sys.exit,
    "os_exit": os._exit,
    "builtins_exit": getattr(builtins, "exit", None),
    "builtins_quit": getattr(builtins, "quit", None),
}

# قفل ضد التغيير
_LOCK = True

# دالة منع exit
def _fake_exit(*args, **kwargs):
    print("\n[!] محاولة إنهاء البرنامج تم اعتراضها 🔒")
    if args:
        print("[i] السبب:", args)

# =======================
#     حماية موسعة ضد الإنهاء
# =======================

def _alert(msg):
    print(f"⚠️ {msg} — تم المنع ✔")

# منع exit/quit/sys.exit
def _block_exit(*a, **k):
    _alert("exit/quit/sys.exit")
builtins.exit = _block_exit
builtins.quit = _block_exit
sys.exit      = _block_exit

# منع os._exit
def _block_os_exit(code=0):
    _alert("os._exit")
os._exit = _block_os_exit

# منع SystemExit
_real_ex = sys.excepthook
def _hook(t, e, tb):
    if t is SystemExit:
        _alert("SystemExit raised")
        return
    return _real_ex(t, e, tb)
sys.excepthook = _hook

# منع signals
def _stop_signal(signum, frame):
    _alert(f"إشارة إيقاف ({signum})")

# ========================
#  حماية ضد الإشارات
# ========================
if os.name != 'nt':  # إذا كان النظام ليس Windows
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGHUP]:
        try:
            signal.signal(sig, _stop_signal)
        except AttributeError:
            pass  # في حال كانت الإشارة غير موجودة على النظام الحالي
else:  # إذا كان النظام هو Windows
    for sig in [signal.SIGINT, signal.SIGTERM]:
        try:
            signal.signal(sig, _stop_signal)
        except AttributeError:
            pass  # في حال كانت الإشارة غير موجودة على النظام الحالي

# منع threading._stop
try:
    _orig_stop = threading.Thread._stop
    def _patched_stop(self):
        _alert("Thread stop attempt")
    threading.Thread._stop = _patched_stop
except:
    pass

# asyncio loop.stop
try:
    def _loop_stop_patch(self):
        _alert("Async loop stop attempt")
    asyncio.BaseEventLoop.stop = _loop_stop_patch
except:
    pass

# ctypes exit
try:
    libc = ctypes.CDLL(None)
    for fn in ["exit", "_exit", "abort"]:
        if hasattr(libc, fn):
            setattr(libc, fn, lambda *a, **k: _alert(f"ctypes.{fn}"))
except:
    pass

# تعطيل crash من recursion
def _safe_rec(n):
    _alert("recursion crash attempt")
sys.setrecursionlimit = _safe_rec

# تعطيل faulthandler
try:
    faulthandler.disable()
except:
    pass

# منع os.kill
if hasattr(os, "kill"):
    _real_kill = os.kill
    def _patched_kill(pid, sig):
        _alert(f"os.kill({pid}, {sig})")
    os.kill = _patched_kill

# =======================
#       أصل أداة Guardian
# =======================
class _Protector:
    def __setattr__(self, name, value):
        if _LOCK:
            raise RuntimeError("🚫 ممنوع تعديل Guardian أثناء التشغيل")
        super().__setattr__(name, value)

protector = _Protector()

def enable():
    global _LOCK
    _LOCK = True
    print("[+] Guardian Ultimate: الحماية مفعلة ✅")

def disable():
    global _LOCK
    _LOCK = False
    sys.exit = _ORIG["sys_exit"]
    os._exit = _ORIG["os_exit"]
    if _ORIG["builtins_exit"]:
        builtins.exit = _ORIG["builtins_exit"]
    if _ORIG["builtins_quit"]:
        builtins.quit = _ORIG["builtins_quit"]
    print("[-] Guardian: تم تعطيل الحماية")

def integrity_check():
    if sys.exit != _block_exit:
        raise RuntimeError("🚨 تم اكتشاف تلاعب بـ sys.exit")
    if os._exit != _block_os_exit:
        raise RuntimeError("🚨 تم اكتشاف تلاعب بـ os._exit")

def spinner(text="جاري الإنهاء", duration=3):
    spinner_cycle = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{text}... {next(spinner_cycle)} ")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r" + " " * 40 + "\r", end="")

def stop_tool(msg="⛔ تم توقف الأداة"):
    spinner("جاري إيقاف الأداة", duration=3)
    print(f"🐌 {msg}")
    _fake_exit(msg)

def run_file_protected(path):
    print(f"[~] تشغيل الأداة تحت الحماية: {path}")
    while True:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            exec(code, globals(), globals())
            print("\n[!] الأداة وصلت لنهاية التنفيذ الطبيعي")
        except SystemExit as e:
            print("\n🚫 تم اعتراض SystemExit:", e)
        except KeyboardInterrupt:
            print("\n🚫 تم اعتراض Ctrl+C")
        except Exception as e:
            print("\n⚠️ استثناء داخل الأداة:")
            traceback.print_exc()

        choice = input("\n↩️ تعيد تشغيل الأداة؟ (y/n): ").lower()
        if choice != "y":
            print("✅ تم الخروج من Guardian بدون إنهاء بايثون")
            break

def run_code(code):
    try:
        exec(code, globals(), globals())
    except Exception as e:
        print("⚠️ خطأ أثناء التنفيذ:", e)
