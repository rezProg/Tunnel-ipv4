#!/usr/bin/env python3
import sys
import subprocess

def check_password(username, password):
    valid_passwords = {
        "reza": "reza"
    }

    if username in valid_passwords and password == valid_passwords[username]:
        return True
    else:
        return False

def main():
    # دریافت نام کاربری و رمز عبور از کاربر
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_password(username, password):
        print("Password correct")
        continue_execution = input("Get started (yes/no): ")
        if continue_execution.lower() == "yes":
            print("Please wait...")
            # دانلود فایل bbr.sh
            print("Downloading bbr.sh...")
            subprocess.run(["wget", "-N", "--no-check-certificate", "https://github.com/teddysun/across/raw/master/bbr.sh"])
            
            # تغییر سطح دسترسی فایل bbr.sh
            print("Changing permissions for bbr.sh...")
            subprocess.run(["chmod", "+x", "bbr.sh"])

            # اجرای فایل bbr.sh
            print("Executing bbr.sh...")
            subprocess.run(["bash", "bbr.sh"])
            print("bbr.sh executed successfully.")

            # بررسی وجود دسترسی root
            if not subprocess.run(["id", "-u"], capture_output=True, text=True).stdout.strip() == '0':
                print("This script must be run as root.")
                sys.exit(1)
            
            # آپدیت لیست پکیج‌ها
            print("Updating package list...")
            subprocess.run(["apt", "update"])

            # آپدیت پکیج‌ها
            print("Upgrading packages...")
            subprocess.run(["apt", "upgrade", "-y"])

            # آپگرید سیستم به آخرین نسخه
            print("Upgrading system...")
            subprocess.run(["apt", "dist-upgrade", "-y"])

            # پاکسازی فایل‌های اضافی
            print("Removing unused packages...")
            subprocess.run(["apt", "autoremove", "-y"])

            # پاکسازی فایل‌های کش
            print("Cleaning package cache...")
            subprocess.run(["apt", "clean"])

            print("Server update successful.")

            # نصب بسته iptables
            print("Installing iptables package...")
            subprocess.run(["sudo", "apt-get", "install", "iptables", "-y"])

            # دریافت مقادیر iranip و kharegip از فرد اجرا کننده
            iranip = input("Enter iranIP: ")
            kharegip = input("Enter kharejIP: ")

            # تنظیمات iptables
            print("Configuring iptables...")
            subprocess.run(["sysctl", "net.ipv4.ip_forward=1"])
            subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp", "--dport", "22", "-j", "DNAT", "--to-destination", iranip])
            subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-j", "DNAT", "--to-destination", kharegip])
            subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-j", "MASQUERADE"])

            # اضافه کردن دستورات به فایل rc.local
            print("Adding commands to rc.local...")
            rc_local_commands = [
                "#! /bin/bash",
                "sysctl net.ipv4.ip_forward=1",
                f"iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination {iranip}",
                f"iptables -t nat -A PREROUTING -j DNAT --to-destination {kharegip}",
                "iptables -t nat -A POSTROUTING -j MASQUERADE",
                "exit 0"
            ]
            rc_local_path = "/etc/rc.local"
            with open(rc_local_path, "a") as rc_local_file:
                rc_local_file.write("\n".join(rc_local_commands))

            # تغییر سطح دسترسی فایل rc.local
            print("Changing permissions for rc.local...")
            subprocess.run(["sudo", "chmod", "+x", rc_local_path])

            print("Script execution completed successfully.")
            print("Enjoy.")
            sys.exit()
        else:
            print("Execution aborted.")
            sys.exit()
    else:
        print("Invalid username or password.")
        sys.exit()

if __name__ == "__main__":
    main()
