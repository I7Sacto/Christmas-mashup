#!/usr/bin/env python3
import os
import time
from datetime import datetime
import subprocess
import pwd
import glob

PROGRESS_FILE = '/var/tmp/progress.txt'
LOGFILE = '/var/log/progress-check.log'
def get_sudo_output(command):
    rules = open_sudo_proc(command)
    output = rules.stdout.read().decode()
    return output
def open_sudo_proc(command):
    passwd = subprocess.Popen(['echo', 'sysadmin'], stdout=subprocess.PIPE)
    return subprocess.Popen(['sudo', '-S'] +  command.split(), stdin=passwd.stdout, stdout=subprocess.PIPE)


def write_progress(pct: int):
    fd = os.open(PROGRESS_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    os.write(fd, str(pct).encode())
    os.close(fd)

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if os.path.exists(LOGFILE):
        with open(LOGFILE, 'a') as f:
            f.write(f"[{ts}] {msg}\n")

# --- Перевірки ---
def check_fstab():
    try:
        with open("/etc/fstab") as f:
            content = f.read()
        return all(x in content for x in [
            "/dev/mapper/ol-root     /                       xfs     defaults        0 0",
            "UUID=b83390ed-0aac-41f1-b0d4-bc4b7a64f98d /boot                   xfs     defaults        0 0",
            "/dev/mapper/ol-swap     none                    swap    defaults        0 0"
        ])
    except: return False

def check_petclinic_olena():
    return subprocess.getoutput("systemctl is-active petclinic-olena.service").strip() == "active"

def check_mysqld():
    return (subprocess.getoutput("systemctl is-active mysqld").strip() == "active" and
            subprocess.getoutput("systemctl is-enabled mysqld").strip() == "enabled")

def check_prerouting_rule():
    try:
        output = get_sudo_output("iptables -t nat -S PREROUTING")
        # True тільки якщо немає цього правила
        return "-A PREROUTING -p tcp -m tcp --dport 8080 -j REDIRECT --to-ports 80" not in output
    except Exception as e:
        return False


def check_petclinic_julia():
    try:
        with open("/etc/systemd/system/petclinic-julia.service") as f:
            return "--spring.profiles.active=mysql" in f.read()
    except: return False

def check_bashrc_yulia():
    try:
        content = get_sudo_output("cat /home/yulia/.bashrc")
        mshell = True
        secho = True
        for line in content.splitlines():
            line_clean = line.strip()
            # ігноруємо порожні рядки і коментарі
            if not line_clean or line_clean.startswith("#"):
                continue
            if "meme-shell" in line_clean:
                mshell = False
            if "stty -echo" in line_clean:
                secho = False
        return mshell and secho
    except:
        return False

def check_qwiklabs_archive():
    try:
        files = get_sudo_output("ls /home/ludmila").splitlines()
        for f in files:
            if "qwiklabs.net.ical.zip" in f.lower():
                return True
        return False
    except:
        return False

def check_alina_shell():
    try:
        pw = pwd.getpwnam("alina")
        return pw.pw_shell == "/usr/bin/bash"
    except: return False

def check_yum_repos():
    try:
        for repo in glob.glob("/etc/yum.repos.d/*.repo"):
            with open(repo) as f:
                for line in f:
                    if line.strip().startswith("enabled=") and line.strip() != "enabled=1":
                        return False
        return True
    except: return False


def check_sshd_config():
    try:
        content = get_sudo_output("cat /etc/ssh/sshd_config")
        for line in content.splitlines():
            line_clean = line.strip()
            # ігноруємо порожні рядки і коментарі
            if not line_clean or line_clean.startswith("#"):
                continue
            # якщо знайдено активний рядок DenyUsers anna → False
            if line_clean == "DenyUsers anna":
                return False
        return True
    except:
        return False


# --- Словник завдань з відсотками ---
TASKS = {
   1: (check_fstab, 15),
   2: (check_petclinic_olena, 11),
   3: (check_prerouting_rule, 7), 
   4: (check_mysqld, 7),
   5: (check_petclinic_julia, 10),
   6: (check_bashrc_yulia, 13),
   7: (check_qwiklabs_archive, 7),
   8: (check_alina_shell, 10),
   9: (check_yum_repos, 8),
   10: (check_sshd_config, 12)
}
SOCK_PATH = "/tmp/myservice.sock"

import socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    os.remove(SOCK_PATH)
except OSError:
    pass

sock.bind(SOCK_PATH)
sock.listen(1)

conn, _ = sock.accept()

def update_progress(task_status):
    percent = sum(pct for num,(func,pct) in TASKS.items() if task_status.get(num))
    write_progress(percent)
    print(f"\rProgress1: {percent} % user@localhost ~$", end='')
    if percent >= 100:
        log("Progress reached 100%, launching tree.py")
        proc = subprocess.Popen(["python3","-u" ,"/usr/bin/tree.py"], stdout=subprocess.PIPE, stderr=None)
        while True:
            chunk = proc.stdout.read(1024)  # Read in 1KB chunks
            conn.sendall(chunk)  # Send to the client
        # open_sudo_proc("python3 -u /usr/bin/tree.py")
        # subprocess.check_output(('grep', 'process_name'), stdin=proc.stdout)
        # time.sleep(180)
        # proc.terminate()

def monitor_tasks():
    task_status = {num: False for num in TASKS}
    while True:
        updated = False
        for num,(func,pct) in TASKS.items():
            current = func()
            if current and not task_status[num]:
                task_status[num] = True
                updated = True
                log(f"Task {num}=OK (+{pct}%)")
        if updated:
            update_progress(task_status)
        time.sleep(2)

if __name__ == "__main__":
    write_progress(0)
    update_progress({})
    monitor_tasks()

