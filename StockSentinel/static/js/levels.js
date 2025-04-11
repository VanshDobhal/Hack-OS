/**
 * Level-specific functionality and data
 */

// Level-specific command mappings and handlers
const levelHandlers = {
    // Level 1: Terminal Navigation
    1: {
        commands: {
            'ls': handleLs,
            'cd': handleCd,
            'cat': handleCat
        },
        state: {
            currentDirectory: '/'
        }
    },
    
    // Level 2: Decryption
    2: {
        commands: {
            'ls': handleLs,
            'cat': handleCat,
            'decrypt': handleDecrypt
        },
        state: {}
    },
    
    // Level 3: File Permissions
    3: {
        commands: {
            'ls': handleLs,
            'cat': handleCat,
            'chmod': handleChmod
        },
        state: {
            permissions: {
                'locked_data.txt': '000'
            }
        }
    },
    
    // Level 4: Hidden Files
    4: {
        commands: {
            'ls': handleLs,
            'cat': handleCat
        },
        state: {
            showHidden: false
        }
    },
    
    // Level 5: Firewall Intro
    5: {
        commands: {
            'scan': handleScan,
            'probe': handleProbe
        },
        state: {
            scanned: false
        }
    },
    
    // Level 6: Port Scanning
    6: {
        commands: {
            'scan': handleScan,
            'deep-scan': handleDeepScan,
            'analyze': handleAnalyze
        },
        state: {
            scanned: false,
            deepScanned: false
        }
    },
    
    // Level 7: Password Cracking
    7: {
        commands: {
            'bruteforce': handleBruteforce,
            'access': handleAccess
        },
        state: {
            bruteforced: false
        }
    },
    
    // Level 8: Log Analysis
    8: {
        commands: {
            'ls': handleLs,
            'cat': handleCat,
            'grep': handleGrep,
            'analyze-logs': handleAnalyzeLogs
        },
        state: {}
    },
    
    // Level 9: Firewall Bypass
    9: {
        commands: {
            'scan-firewall': handleScanFirewall,
            'analyze': handleAnalyze,
            'exploit': handleExploit
        },
        state: {
            scanned: false,
            analyzed: false
        }
    },
    
    // Level 10: Reverse Engineering
    10: {
        commands: {
            'cat': handleCat,
            'hex2text': handleHexToText
        },
        state: {}
    },
    
    // Level 11: Buffer Overflow
    11: {
        commands: {
            'access-system': handleAccessSystem,
            'inject': handleInject
        },
        state: {
            accessed: false
        }
    },
    
    // Level 12: Final Battle
    12: {
        commands: {
            'decrypt': handleDecrypt,
            'scan': handleScan,
            'exploit': handleExploit,
            'execute': handleExecute
        },
        state: {
            decrypted: false,
            scanned: false,
            exploited: false
        }
    }
};

/**
 * Command handler for 'ls'
 * Lists files in current directory
 */
function handleLs(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'cd'
 * Changes current directory
 */
function handleCd(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'cat'
 * Displays file contents
 */
function handleCat(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'decrypt'
 * Decrypts encrypted files
 */
function handleDecrypt(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'chmod'
 * Changes file permissions
 */
function handleChmod(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'scan'
 * Scans for open ports
 */
function handleScan(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'probe'
 * Probes a specific port
 */
function handleProbe(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'deep-scan'
 * Performs a detailed scan
 */
function handleDeepScan(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'analyze'
 * Analyzes vulnerabilities
 */
function handleAnalyze(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'bruteforce'
 * Attempts to brute force a password
 */
function handleBruteforce(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'access'
 * Attempts to access a system with credentials
 */
function handleAccess(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'grep'
 * Searches for patterns in files
 */
function handleGrep(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'analyze-logs'
 * Analyzes log files for patterns
 */
function handleAnalyzeLogs(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'scan-firewall'
 * Scans a firewall for vulnerabilities
 */
function handleScanFirewall(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'exploit'
 * Exploits a vulnerability
 */
function handleExploit(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'hex2text'
 * Converts hex to text
 */
function handleHexToText(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'access-system'
 * Accesses a system
 */
function handleAccessSystem(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'inject'
 * Injects code or data
 */
function handleInject(args) {
    // Implementation will be handled server-side
    return null;
}

/**
 * Command handler for 'execute'
 * Executes a command or program
 */
function handleExecute(args) {
    // Implementation will be handled server-side
    return null;
}
