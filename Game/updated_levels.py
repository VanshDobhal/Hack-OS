# Updated levels based on the provided specifications
LEVELS = {
    1: {
        "title": "Nexus Boot",
        "description": "Navigate directories and read the system's boot log.",
        "goal": "Navigate to boot/system/core directory and read bootlog.txt.",
        "commands": ["ls", "cd", "cat"],
        "files": {
            "boot": {
                "type": "directory",
                "content": {
                    "system": {
                        "type": "directory",
                        "content": {
                            "core": {
                                "type": "directory",
                                "content": {
                                    "bootlog.txt": {
                                        "type": "file",
                                        "content": "Nexus System Boot Log\n---------------------\nInitializing core components...\nVerifying security protocols...\nLoading Nexus AI matrix...\nSystem operational at 98.7% efficiency.\nWARNING: Unauthorized access detected in sector 7.\nDeploying countermeasures..."
                                    }
                                }
                            },
                            "readme.txt": {
                                "type": "file",
                                "content": "System directory contains core boot files. Be careful when accessing."
                            }
                        }
                    },
                    "info.txt": {
                        "type": "file",
                        "content": "Boot directory contains the system initialization files. Navigate deeper to find the core."
                    }
                }
            },
            "readme.txt": {
                "type": "file",
                "content": "Welcome to Nexus Systems. Use 'ls' to see what's available and 'cd' to navigate directories."
            }
        },
        "solution": ["cd boot", "cd system", "cd core", "cat bootlog.txt"],
        "solution_text": "First use 'cd boot' to enter the boot directory, then 'cd system', 'cd core', and finally 'cat bootlog.txt' to read the boot log.",
        "guide": "'ls' lists directories and files, 'cd [name]' moves into a directory, 'cat [file]' reads file contents.",
        "nexus_dialogue": "Intruder detected. System security protocols active.",
        "glitch_intro": "First step, [alias]! Navigate to the boot directory, then find the system core to read the boot log.",
        "glitch_hint": "You need to go deeper into the directories. Try using 'cd boot' first, then keep going.",
        "glitch_success": "Perfect! You've found the boot log. This information will be crucial for understanding Nexus's operations."
    },
    2: {
        "title": "Cipher Shift",
        "description": "Decrypt a file and change its permissions.",
        "goal": "Decrypt secret.enc, fix permissions, and read it.",
        "commands": ["ls", "cat", "decrypt", "chmod"],
        "files": {
            "secret.enc": {
                "type": "file",
                "content": "Wkhvh#duh#wkh#frghv=#74;6<05",
                "permissions": "000"
            },
            "hint.txt": {
                "type": "file",
                "content": "Caesar's method: This message is shifted by 3 characters. You'll need to change permissions to read the decrypted file."
            }
        },
        "solution": ["cat hint.txt", "decrypt secret.enc > secret.txt", "chmod +r secret.txt", "cat secret.txt"],
        "solution_text": "Type 'cat hint.txt' for clues, 'decrypt secret.enc > secret.txt' to decrypt, 'chmod +r secret.txt' to make it readable, then 'cat secret.txt'.",
        "guide": "'decrypt [file] > [output]' decrypts, 'chmod +r [file]' adjusts read permissions",
        "decrypted_message": "These are the codes: 74936-2",
        "nexus_dialogue": "My security protocols are multiple layers deep.",
        "glitch_intro": "This file is secured in two ways - encrypted content and locked permissions. Break both to get the data.",
        "glitch_hint": "First check the hint file, then decrypt the file and adjust its permissions to read it.",
        "glitch_success": "Excellent work! You've decrypted the message and bypassed the permission controls!"
    },
    3: {
        "title": "Hidden Breadcrumbs",
        "description": "Find and open a hidden log file.",
        "goal": "Reveal hidden folders, find .nexus/logs, read trace.log.",
        "commands": ["ls", "ls -a", "cd", "cat"],
        "files": {
            "readme.txt": {
                "type": "file",
                "content": "This directory seems empty... or is it? Some important files might be hidden."
            },
            ".nexus": {
                "type": "directory",
                "content": {
                    "logs": {
                        "type": "directory",
                        "content": {
                            "trace.log": {
                                "type": "file",
                                "content": "Nexus Trace Log\n--------------\nUser authentication: FAILED\nSystem breach attempt: DETECTED\nLocation: Terminal 47B\nAccess point: 192.168.1.47\nTarget: Core authentication database\nVulnerability exploited: CVE-2023-9876"
                            }
                        }
                    }
                }
            }
        },
        "solution": ["ls -a", "cd .nexus", "cd logs", "cat trace.log"],
        "solution_text": "Type 'ls -a' to see hidden files (with dots), then 'cd .nexus', 'cd logs', and 'cat trace.log'.",
        "guide": "'ls -a' reveals hidden files/directories (those starting with a dot), navigate to them with cd, read with cat.",
        "nexus_dialogue": "You'll never find my hidden paths.",
        "glitch_intro": "Nexus is hiding critical data in hidden directories. Use special flags with ls to find them.",
        "glitch_hint": "Regular ls won't show hidden files. Try 'ls -a' to reveal directories that start with a dot, then navigate to them.",
        "glitch_success": "Great find! You've discovered the hidden trace log that reveals Nexus's intrusion attempts."
    },
    4: {
        "title": "Password Brute",
        "description": "Crack the password using clues.",
        "goal": "Crack the password using clues and the brute command.",
        "commands": ["brute", "cat", "ls"],
        "files": {
            "locked_access.txt": {
                "type": "file", 
                "content": "Password protected system. Password hint: Starts with 'n', contains numeric characters, and is related to neural networks."
            },
            "attempts.log": {
                "type": "file",
                "content": "Failed attempts: matrix, brain, neural1, neuro5, n3twork"
            }
        },
        "solution": ["cat locked_access.txt", "cat attempts.log", "brute pass1", "brute hackme", "brute nexus", "brute netron"],
        "solution_text": "Read the hint files, then try passwords with the brute command. Try 'brute netron' after a few attempts.",
        "guide": "'brute [guess]' tests passwords. Terminal responds with hints after failed attempts.",
        "correct_password": "netron",
        "nexus_dialogue": "My credentials cannot be broken so easily.",
        "glitch_intro": "This system needs a password. Look for clues and try different combinations.",
        "glitch_hint": "Check both files for clues. The password starts with 'n', contains numbers, and relates to neural networks.",
        "glitch_success": "Password cracked! 'netron' was the key - now we have access to the system!"
    },
    5: {
        "title": "Tampered Log",
        "description": "Detect and fix a corrupted log.",
        "goal": "Analyze corrupt.log, fix the bad entry with the text editor, and verify it's fixed.",
        "commands": ["analyze", "cat", "nano", "ls"],
        "files": {
            "corrupt.log": {
                "type": "file",
                "content": "08:42:17 - System startup\n08:43:44 - User login\n08:46:22 - Database query\n08:47:15 - ////////CORRUPTED////////\n08:49:30 - File access\n08:52:55 - Logout"
            },
            "clean_logs.txt": {
                "type": "file",
                "content": "All system logs should follow the format: [time] - [action]\nCorrupted entries must be replaced with 'Security breach detected'"
            }
        },
        "solution": ["cat corrupt.log", "cat clean_logs.txt", "analyze corrupt.log", "nano corrupt.log", "cat corrupt.log"],
        "solution_text": "Type 'cat corrupt.log' to see the log, 'cat clean_logs.txt' for format, 'analyze corrupt.log' to identify issues, 'nano corrupt.log' to fix the corrupted line (replace with 'Security breach detected'), then 'cat corrupt.log' to verify.",
        "guide": "'analyze' identifies problems, 'nano [file]' opens the text editor to make changes.",
        "analyze_result": "Log analysis complete. Line 4 is corrupted and needs repair according to standard format.",
        "fixed_content": "08:42:17 - System startup\n08:43:44 - User login\n08:46:22 - Database query\n08:47:15 - Security breach detected\n08:49:30 - File access\n08:52:55 - Logout",
        "nexus_dialogue": "My logs are tamper-proof.",
        "glitch_intro": "This log has been corrupted. You'll need to analyze it and restore the proper format.",
        "glitch_hint": "First check the clean_logs.txt file to understand the proper format, then use analyze to find the issue, and finally use nano to fix it.",
        "glitch_success": "Perfect repair! You've restored the log and revealed a hidden security breach in the process."
    },
    6: {
        "title": "Exploit Firewall",
        "description": "Inject code through a weak firewall port.",
        "goal": "Identify open ports and inject code through the weak one.",
        "commands": ["rules", "scan", "probe", "inject", "ls", "cat"],
        "files": {
            "firewall_config.txt": {
                "type": "file",
                "content": "Nexus Firewall Configuration\n------------------------\nUse 'rules' to check the firewall configuration for weaknesses.\nUse 'scan' to discover open ports.\nUse 'probe [port]' to test a specific port.\nUse 'inject [port] < payload.txt' to send code through an open port."
            },
            "payload.txt": {
                "type": "file",
                "content": "#!/bin/bash\necho 'EXPLOITING PORT VULNERABILITY'\necho 'BYPASSING FIREWALL RULES'\necho 'ACCESS GRANTED'"
            }
        },
        "solution": ["cat firewall_config.txt", "rules", "scan", "probe 8080", "inject 8080 < payload.txt"],
        "solution_text": "Read the config file, check rules with 'rules', find ports with 'scan', use 'probe 8080' to test the vulnerable port, then 'inject 8080 < payload.txt'.",
        "guide": "'rules' shows firewall settings, 'scan' finds ports, 'probe [port]' tests one, 'inject [port] < [file]' sends code.",
        "rules_result": "Firewall rules:\nDENY ALL\nALLOW 22 (SSH)\nALLOW 443 (HTTPS)\nALLOW 8080 (Development) - WEAK CONFIGURATION\nDENY EXTERNAL",
        "scan_result": "Scanning...\nPorts found: 22, 80, 443, 8080\nPort 8080 appears vulnerable - development configuration detected.",
        "probe_result_8080": "Port 8080 is open and vulnerable. Misconfigured with admin permissions.",
        "nexus_dialogue": "My defenses are impenetrable.",
        "glitch_intro": "We need to break through Nexus's firewall. Find a weak point in the configuration and exploit it.",
        "glitch_hint": "Check the firewall_config.txt first, then use 'rules' and 'scan' to find the vulnerable port (hint: development ports are often misconfigured).",
        "glitch_success": "Perfect exploit! You've identified the weak port 8080 and successfully injected your payload. Nexus's firewall has been breached!"
    },
    7: {
        "title": "Multi-Step Chain",
        "description": "Perform chained actions to access a protected file.",
        "goal": "Navigate to folder, decrypt file, fix permissions, read it.",
        "commands": ["cd", "ls", "ls -a", "decrypt", "chmod", "cat"],
        "files": {
            ".vault": {
                "type": "directory",
                "content": {
                    "secret.sec": {
                        "type": "file",
                        "content": "Qbyvzrki fxvkxm: Tjmx Kzebuml Znrxktudyx tm 03:15",
                        "permissions": "000"
                    },
                    "cipher.info": {
                        "type": "file",
                        "content": "Cipher: ROT-17"
                    }
                }
            },
            "readme.txt": {
                "type": "file",
                "content": "Important data is secured in a hidden vault. Multiple security layers protect it."
            }
        },
        "solution": ["ls -a", "cd .vault", "ls", "cat cipher.info", "decrypt secret.sec > secret.txt", "chmod +r secret.txt", "cat secret.txt"],
        "solution_text": "First 'ls -a' to find .vault, 'cd .vault', check the cipher.info, 'decrypt secret.sec > secret.txt', 'chmod +r secret.txt', then 'cat secret.txt'.",
        "guide": "This level combines multiple techniques: finding hidden directories, decryption, and permission changes.",
        "decrypted_message": "Critical secret: Core Shutdown Initiation at 03:15",
        "nexus_dialogue": "My most critical data is secured behind multiple layers.",
        "glitch_intro": "This is a complex one - multiple security techniques protect the target file. Start by finding the hidden vault.",
        "glitch_hint": "Use 'ls -a' first to find any hidden directories, then navigate to it, check what's inside, and combine decryption with permission changes.",
        "glitch_success": "Masterful work! You've navigated multiple security layers to access the critical secret about Nexus's shutdown schedule."
    },
    8: {
        "title": "Hex Trap",
        "description": "Decode hex and follow the path.",
        "goal": "Decode hexadecimal, navigate to the revealed directory, read the file.",
        "commands": ["reverse", "cd", "ls", "cat"],
        "files": {
            "encoded_path.txt": {
                "type": "file",
                "content": "The path you seek is encoded: 6861636b"
            },
            "hack": {
                "type": "directory",
                "content": {
                    "note.txt": {
                        "type": "file",
                        "content": "Nexus vulnerability identified: Memory buffer overflow in authentication module.\nExploit access: Port 9922\nCredentials: admin:0v3rfl0w-1337"
                    }
                }
            }
        },
        "solution": ["cat encoded_path.txt", "reverse 6861636b", "cd hack", "cat note.txt"],
        "solution_text": "First read encoded_path.txt, use 'reverse 6861636b' to convert hex to text (result: 'hack'), then 'cd hack' and 'cat note.txt'.",
        "guide": "'reverse [hex]' converts hexadecimal to text, allowing you to discover hidden paths.",
        "decoded_text": "hack",
        "nexus_dialogue": "My code is impenetrable.",
        "glitch_intro": "Nexus has encoded a critical path in hexadecimal. Decode it to find where to go next.",
        "glitch_hint": "Read the encoded_path.txt file, then use the 'reverse' command on the hex code to translate it to text, which will reveal a directory name.",
        "glitch_success": "Excellent decoding! You've translated the hex '6861636b' to 'hack' and found crucial vulnerability information."
    },
    9: {
        "title": "Buffer Overflow",
        "description": "Trigger buffer overflow and inject payload.",
        "goal": "Use overflow to reveal memory address, then inject a payload at that address.",
        "commands": ["overflow", "cat", "ls", "inject"],
        "files": {
            "security_interface.txt": {
                "type": "file",
                "content": "Nexus security interface accepts a maximum of 8 characters.\nLonger inputs may cause unexpected behavior.\nUse 'overflow [string]' to test input handling."
            },
            "payload.txt": {
                "type": "file",
                "content": "#!/bin/bash\necho 'BYPASSING MEMORY PROTECTION'\necho 'ESCALATING PRIVILEGES'\necho 'ROOT ACCESS GRANTED'"
            }
        },
        "solution": ["cat security_interface.txt", "overflow AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "inject 0x7ffeab32 < payload.txt"],
        "solution_text": "First read the security_interface.txt, use 'overflow AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' to cause a buffer overflow (it will reveal a memory address), then 'inject [revealed_address] < payload.txt'.",
        "guide": "'overflow [string]' sends a string to test for buffer overflows. A vulnerability will reveal a memory address you can target with 'inject'.",
        "overflow_result": "System error: Buffer overflow detected.\nMemory protection bypass possible at address 0x7ffeab32\nVulnerable entry point identified.",
        "nexus_dialogue": "My security protocols are flawless.",
        "glitch_intro": "Nexus's input handling has a vulnerability. Let's exploit it with a classic buffer overflow attack.",
        "glitch_hint": "First read the security_interface.txt. Try sending many characters to overflow the buffer and reveal a memory address, then inject your payload at that address.",
        "glitch_success": "Perfect attack! You've triggered a buffer overflow and injected your payload, gaining elevated access to Nexus's system."
    },
    10: {
        "title": "Deep Net Scan",
        "description": "Decode hex from scan and explore hidden node.",
        "goal": "Run deep scan, decode hex folder name, enter it and read file.",
        "commands": ["scan", "reverse", "cd", "ls", "cat"],
        "files": {
            "network_map.txt": {
                "type": "file",
                "content": "Nexus Network Map\n----------------\nStandard scan shows visible nodes.\nUse 'scan --deep' for hidden network segments.\nHex encoded node paths require decoding."
            },
            "nexus": {
                "type": "directory",
                "content": {
                    "intel.txt": {
                        "type": "file",
                        "content": "Nexus Core System Access\n-----------------------\nPrimary Control Node: 192.168.10.15\nShutdown Authorization: DIRECTOR-LEVEL\nEmergency Protocol: ZERO-DAY-OVERRIDE\nBackdoor Credentials: sysadmin:n3xu5-c0r3-1337"
                    }
                }
            }
        },
        "solution": ["cat network_map.txt", "scan --deep", "reverse 6e65787573", "cd nexus", "cat intel.txt"],
        "solution_text": "First read network_map.txt, run 'scan --deep' to find hidden nodes, use 'reverse 6e65787573' on the hex (result: 'nexus'), then 'cd nexus' and 'cat intel.txt'.",
        "guide": "'scan --deep' reveals hidden network segments, often with encoded paths that need decryption.",
        "scan_result": "Deep scanning network...\nHidden node detected: 6e65787573\nEncryption detected: hexadecimal encoding",
        "decoded_text": "nexus",
        "nexus_dialogue": "My network architecture is beyond your comprehension.",
        "glitch_intro": "There's a hidden node in Nexus's network. We need to find it and see what it contains.",
        "glitch_hint": "First check the network map, then run a deep scan to find hidden nodes. The node name will be in hex - decode it, then navigate to it.",
        "glitch_success": "Outstanding work! You've uncovered the hidden 'nexus' node and found critical system access information."
    },
    11: {
        "title": "Reverse Patch",
        "description": "Fix a config file with obfuscated content.",
        "goal": "Decode a key, edit config file to fix the system.",
        "commands": ["cat", "reverse", "nano", "ls"],
        "files": {
            "config.sys": {
                "type": "file",
                "content": "SYSTEM_TYPE=nexus\nADMIN_LEVEL=9\nAUTH_METHOD=token\nCONTROL_NODE=$$ERROR$$\nBACKUP_MODE=enabled"
            },
            "debug.log": {
                "type": "file",
                "content": "System failure: CONTROL_NODE value corrupted\nRequired value encoded: 736572766572"
            }
        },
        "solution": ["cat config.sys", "cat debug.log", "reverse 736572766572", "nano config.sys", "cat config.sys"],
        "solution_text": "First check config.sys and debug.log, use 'reverse 736572766572' to get 'server', then use 'nano config.sys' to replace $$ERROR$$ with 'server', finally verify with 'cat config.sys'.",
        "guide": "'reverse [hex]' decodes hex values, 'nano [file]' allows editing files. You need to fix the corrupted value.",
        "decoded_text": "server",
        "fixed_config": "SYSTEM_TYPE=nexus\nADMIN_LEVEL=9\nAUTH_METHOD=token\nCONTROL_NODE=server\nBACKUP_MODE=enabled",
        "nexus_dialogue": "My configurations are secure and impossible to fix.",
        "glitch_intro": "Nexus's config is corrupt. We need to decode the correct value and patch the file.",
        "glitch_hint": "First check both the config.sys and debug.log files. Decode the hex value in debug.log, then use nano to edit config.sys and replace the error with the decoded value.",
        "glitch_success": "Perfect patch! You've restored the config with the correct 'server' value, bringing the control node back online."
    },
    12: {
        "title": "Final Takedown",
        "description": "Decrypt key, scan ports, and inject shutdown payload.",
        "goal": "Combine all skills: decrypt a key, scan for vulnerable ports, inject the final shutdown command.",
        "commands": ["cat", "decrypt", "scan", "inject", "ls"],
        "files": {
            "key.enc": {
                "type": "file",
                "content": "Xmzy-it-js"
            },
            "final_mission.txt": {
                "type": "file",
                "content": "This is it. Decrypt the shutdown key, scan for the core system port, and inject the shutdown command.\nThe encryption uses a Caesar cipher with shift 5.\nOnce complete, Nexus will be permanently disabled."
            }
        },
        "solution": ["cat final_mission.txt", "cat key.enc", "decrypt key.enc shift 5", "scan", "inject 9090 < key.dec"],
        "solution_text": "First 'cat final_mission.txt', check 'key.enc', use 'decrypt key.enc shift 5' to get 'Shut-it-down', run 'scan' to find port 9090, finally 'inject 9090 < key.dec'.",
        "guide": "This final challenge combines decryption, network scanning, and code injection. Use all your skills!",
        "decrypt_result": "Key decrypted: 'Shut-it-down'",
        "scan_result": "Scanning Nexus core systems...\nCore control port found: 9090\nHighly secured - requires valid shutdown key",
        "inject_result": "Injecting shutdown key...\nValidating credentials...\nAccess granted!\nInitiating Nexus shutdown sequence...\nCore systems going offline...\nNexus AI matrix disconnecting...\nShutdown complete. Nexus has been neutralized.",
        "nexus_dialogue": "You will never defeat me.",
        "glitch_intro": "This is it, [alias]! Combine everything you've learned to take down Nexus once and for all.",
        "glitch_hint": "First decrypt the key.enc file using a shift of 5, then scan for the vulnerable port, and finally inject the decrypted key into that port.",
        "mid_battle": "Almost there! Inject the shutdown key now!",
        "nexus_mid_battle": "No... my systems... you can't...",
        "glitch_success": "YOU DID IT! Nexus is offline! The threat has been neutralized!",
        "nexus_defeat": "Systems... failing... connection... terminated..."
    }
}