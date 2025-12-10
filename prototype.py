import sqlite3
import csv
import os
import time
import random

# --- CONFIGURATION ---
OFFICIAL_DB = "db_comelec.sqlite"
WATCHDOG_DB = "db_namfrel.sqlite"
INPUT_FILE = "mock_votes.csv"

# Colors for the terminal to make it look cool/urgent
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def setup_databases():
    """Creates two empty databases: One for Govt, One for Civil Society"""
    print(f"{YELLOW}--- SYSTEM RESET: Clearing old servers... ---{RESET}")
    for db_name in [OFFICIAL_DB, WATCHDOG_DB]:
        if os.path.exists(db_name):
            os.remove(db_name)
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE votes (
                voter_id TEXT PRIMARY KEY,
                candidate TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()
    print(f"{GREEN}✔ Servers Online: {OFFICIAL_DB} and {WATCHDOG_DB} ready.{RESET}\n")

def process_votes():
    """Simulates the Dual Transmission Policy"""
    print(f"{YELLOW}--- STARTING ELECTION: DUAL TRANSMISSION MODE ---{RESET}")
    
    conn_official = sqlite3.connect(OFFICIAL_DB)
    conn_watchdog = sqlite3.connect(WATCHDOG_DB)
    
    with open(INPUT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            v_id = row['voter_id']
            cand = row['candidate']
            time_stamp = row['timestamp']
            
            # 1. Send to Official Server
            conn_official.execute("INSERT INTO votes VALUES (?, ?, ?)", (v_id, cand, time_stamp))
            
            # 2. Send to Watchdog Server (THE POLICY INNOVATION)
            conn_watchdog.execute("INSERT INTO votes VALUES (?, ?, ?)", (v_id, cand, time_stamp))
            
            print(f"Vote from {v_id}: {GREEN}Transmitted to BOTH servers.{RESET}")
            time.sleep(0.3) # Pause to look like real-time processing
            
    conn_official.commit()
    conn_watchdog.commit()
    conn_official.close()
    conn_watchdog.close()
    print(f"\n{GREEN}✔ All votes cast successfully.{RESET}\n")

def simulate_hack():
    """Simulates a 'Man-in-the-Middle' attack on the Official Server only"""
    print(f"{RED}!!! SECURITY ALERT: UNAUTHORIZED ACCESS DETECTED !!!{RESET}")
    print(f"{RED}!!! TAMPERING WITH OFFICIAL COMELEC SERVER... !!!{RESET}")
    time.sleep(2)
    
    conn = sqlite3.connect(OFFICIAL_DB)
    cursor = conn.cursor()
    
    # The Hack: Change 3 votes for 'Candidate A' to 'Candidate B'
    cursor.execute("UPDATE votes SET candidate = 'Candidate B' WHERE candidate = 'Candidate A' AND voter_id IN ('V8821', 'V7712', 'V3321')")
    
    conn.commit()
    conn.close()
    
    print(f"{RED}>>> MALICIOUS CODE EXECUTED. VOTES FLIPPED.{RESET}\n")

def perform_audit():
    """Compares the two databases to find the differences"""
    print(f"{YELLOW}--- INITIATING AUDIT: CROSS-REFERENCING SERVERS ---{RESET}")
    time.sleep(1)
    
    conn_official = sqlite3.connect(OFFICIAL_DB)
    conn_watchdog = sqlite3.connect(WATCHDOG_DB)
    
    # Get all votes from both
    official_data = conn_official.execute("SELECT * FROM votes ORDER BY voter_id").fetchall()
    watchdog_data = conn_watchdog.execute("SELECT * FROM votes ORDER BY voter_id").fetchall()
    
    discrepancies = 0
    
    print(f"{'VOTER ID':<10} | {'OFFICIAL SERVER':<15} | {'WATCHDOG SERVER':<15} | {'STATUS'}")
    print("-" * 60)
    
    for i in range(len(official_data)):
        v_id = official_data[i][0]
        off_cand = official_data[i][1]
        watch_cand = watchdog_data[i][1]
        
        if off_cand == watch_cand:
            status = f"{GREEN}MATCH{RESET}"
        else:
            status = f"{RED}MISMATCH DETECTED{RESET}"
            discrepancies += 1
            
        print(f"{v_id:<10} | {off_cand:<15} | {watch_cand:<15} | {status}")
        time.sleep(0.1)

    print("-" * 60)
    if discrepancies > 0:
        print(f"{RED}CRITICAL FAILURE: {discrepancies} votes have been tempered with!{RESET}")
        print(f"{RED}EVIDENCE: The Watchdog Server proves the Official Count is wrong.{RESET}")
    else:
        print(f"{GREEN}SUCCESS: Integrity Verified. No tampering found.{RESET}")
    
    conn_official.close()
    conn_watchdog.close()
    print("\n")

# --- MAIN MENU ---
def main():
    while True:
        print("=== DIGITAL YOUTH VOTING PILOT (PROTOTYPE) ===")
        print("1. Setup/Reset Databases")
        print("2. Run Election (Dual Transmission)")
        print("3. SIMULATE HACK (Modify Official DB)")
        print("4. Perform Audit (Verify Integrity)")
        print("5. Exit")
        choice = input("Select Option: ")
        
        if choice == '1':
            setup_databases()
        elif choice == '2':
            process_votes()
        elif choice == '3':
            simulate_hack()
        elif choice == '4':
            perform_audit()
        elif choice == '5':
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()