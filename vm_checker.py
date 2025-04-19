import os
import platform
import subprocess

def is_vm_by_system_info():
    try:
        system = platform.system()
        
        if system == "Windows":
            model = subprocess.check_output("wmic computersystem get model", shell=True).decode()
            manufacturer = subprocess.check_output("wmic computersystem get manufacturer", shell=True).decode()
            bios = subprocess.check_output("wmic bios get serialnumber", shell=True).decode()
            combined_info = (model + manufacturer + bios).lower()
            vm_keywords = ["virtual", "vmware", "virtualbox", "qemu", "kvm", "xen", "hyper-v"]
            for keyword in vm_keywords:
                if keyword in combined_info:
                    return True, f"System info contains keyword: '{keyword}'"
        
        elif system == "Linux":
            try:
                output = subprocess.check_output("systemd-detect-virt", shell=True).decode().strip()
                if output != "none":
                    return True, f"systemd-detect-virt returned: '{output}'"
            except:
                pass

            if os.path.exists("/sys/class/dmi/id/product_name"):
                with open("/sys/class/dmi/id/product_name") as f:
                    product = f.read().lower()
                    for kw in ["virtual", "vmware", "kvm", "qemu", "xen", "hyper-v"]:
                        if kw in product:
                            return True, f"Product name contains keyword: '{kw}'"
            if os.path.exists("/sys/class/dmi/id/sys_vendor"):
                with open("/sys/class/dmi/id/sys_vendor") as f:
                    vendor = f.read().lower()
                    for kw in ["virtual", "vmware", "kvm", "qemu", "xen", "hyper-v"]:
                        if kw in vendor:
                            return True, f"System vendor contains keyword: '{kw}'"
    except:
        pass
    return False, ""

def is_vm_by_mac_address():
    try:
        output = subprocess.check_output("getmac" if platform.system() == "Windows" else "ip link", shell=True).decode().lower()
        vm_macs = {
            "00:05:69": "VMware",
            "00:0c:29": "VMware",
            "00:1c:14": "VMware",
            "00:50:56": "VMware",
            "08:00:27": "VirtualBox",
            "52:54:00": "QEMU/KVM"
        }
        for mac_prefix, vendor in vm_macs.items():
            if mac_prefix in output:
                return True, f"MAC address prefix '{mac_prefix}' indicates {vendor}"
    except:
        pass
    return False, ""

def is_virtual_machine():
    vm_sys, reason_sys = is_vm_by_system_info()
    if vm_sys:
        return True, reason_sys
    vm_mac, reason_mac = is_vm_by_mac_address()
    if vm_mac:
        return True, reason_mac
    return False, ""

if __name__ == "__main__":
    print("Checking if the program is running inside a virtual machine...\n")
    is_vm, reason = is_virtual_machine()
    if is_vm:
        print("Detected: This system is running inside a virtual machine.")
        print("Reason:", reason)
    else:
        print("No virtual machine detected.")
    
    input("\nPress Enter to exit...")
