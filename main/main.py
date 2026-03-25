import random
import time

# Dictionary of passwords organized by difficulty (word length)
PASSWORD_DB = {
    4: ["BYTE", "DATA", "CODE", "NODE", "FILE", "HACK", "WORM", "CORE", "PORT", "USER", "LOCK", "BOOT"],
    5: ["VIRUS", "PROXY", "MACRO", "LOGON", "CACHE", "ADMIN", "SHELL", "CYBER", "GHOST", "DRIVE", "BOARD"],
    6: ["ROUTER", "SERVER", "SYSTEM", "KERNEL", "BREACH", "BOTNET", "UPLOAD", "ACCESS", "CIPHER", "UPLINK"]
}

class Hacker:
    """Represents the player's character, wallet, and heat (wanted level)."""
    def __init__(self, alias):
        self.alias = alias
        self.credits = 0
        self.heat = 0           # If heat reaches 100, you are traced and arrested
        self.max_heat = 100
        self.rig_level = 1      # Determines how many guesses you get per hack
        
class TargetSystem:
    """A corporate server to be hacked."""
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty # 4, 5, or 6 (corresponds to word length)
        self.reward = difficulty * 50
        self.heat_risk = difficulty * 10

def get_likeness(guess, actual):
    """Calculates how many letters match exactly in the same position."""
    # Using the zip() function to compare characters side-by-side
    return sum(1 for g_char, a_char in zip(guess, actual) if g_char == a_char)

def run_hack_minigame(player, target):
    """The core hacking puzzle logic."""
    print(f"\n[INITIATING UPLINK TO: {target.name}]")
    print(f"[SECURITY LEVEL: {target.difficulty}]")
    time.sleep(1)
    
    # Generate a list of decoy passwords + 1 real password
    word_length = target.difficulty
    available_words = random.sample(PASSWORD_DB[word_length], 8)
    password = random.choice(available_words)
    
    attempts_allowed = 3 + player.rig_level
    
    print("\n--- TERMINAL INTERFACE ---")
    print("Bypass required. Select correct password from memory dump.")
    for word in available_words:
        # Adding some fake hex addresses for cyberpunk flavor
        hex_addr = f"0x{random.randint(1000, 9999)}"
        print(f"{hex_addr}  {word}")
        
    while attempts_allowed > 0:
        print(f"\n[ATTEMPTS REMAINING: {attempts_allowed}]")
        guess = input("Enter password guess: ").strip().upper()
        
        if len(guess) != word_length:
            print(f"[ERR] Password must be {word_length} characters long.")
            continue
            
        if guess == password:
            print("\n>>> ACCESS GRANTED <<<")
            print(f"Transferring {target.reward} Crypto-Credits to your ghost account.")
            player.credits += target.reward
            return True
            
        else:
            likeness = get_likeness(guess, password)
            print(f"[ACCESS DENIED] Likeness: {likeness}/{word_length}")
            attempts_allowed -= 1
            
    # If the loop finishes, the player ran out of attempts
    print("\n>>> ALARM TRIGGERED: TRACE INITIATED <<<")
    print(f"Your connection was forcibly terminated. Heat increased by {target.heat_risk}%.")
    player.heat += target.heat_risk
    return False

def black_market(player):
    """Shop to upgrade hacking equipment."""
    print("\n--- THE BLACK MARKET ---")
    print(f"Your Balance: {player.credits} Credits")
    
    upgrade_cost = player.rig_level * 150
    
    print(f"1. Upgrade Deck CPU (Grants +1 Hack Attempt) - {upgrade_cost}C")
    print("2. Buy Fake ID (Clears 20% Heat) - 50C")
    print("3. Jack Out")
    
    choice = input("Select an option: ")
    
    if choice == '1':
        if player.credits >= upgrade_cost:
            player.credits -= upgrade_cost
            player.rig_level += 1
            print(f"\n[SUCCESS] Deck upgraded to Level {player.rig_level}!")
        else:
            print("\n[ERR] Insufficient Credits.")
    elif choice == '2':
        if player.credits >= 50:
            player.credits -= 50
            player.heat = max(0, player.heat - 20)
            print(f"\n[SUCCESS] Digital footprints scrubbed. Heat is now {player.heat}%.")
        else:
            print("\n[ERR] Insufficient Credits.")
    elif choice == '3':
        print("\nLeaving the underground node...")
    else:
        print("\n[ERR] Invalid input.")

def generate_targets():
    """Creates a fresh list of targets on the network."""
    corps = ["OmniCorp", "Militech", "Arasaka", "Tyrell Corp", "Cyberdyne"]
    diffs = [4, 5, 6]
    return [TargetSystem(random.choice(corps) + " Subnet", random.choice(diffs)) for _ in range(3)]

def main():
    print("=========================================")
    print("           NEON GRID HACKER              ")
    print("=========================================")
    
    alias = input("Enter your hacker alias: ")
    if not alias.strip():
        alias = "ZeroCool"
        
    player = Hacker(alias)
    current_targets = generate_targets()
    
    while player.heat < player.max_heat:
        print(f"\n=========================================")
        print(f" ALIAS: {player.alias} | RIG LEVEL: {player.rig_level}")
        print(f" CREDITS: {player.credits}C | HEAT: [ {'#' * (player.heat // 10)}{'-' * (10 - (player.heat // 10))} ] {player.heat}%")
        print(f"=========================================")
        print("1. Scan Network for Targets")
        print("2. Visit Black Market")
        print("3. Refresh Target List (Costs 10C)")
        print("4. Disconnect (Quit Game)")
        
        choice = input("Enter command: ")
        
        if choice == '1':
            print("\n--- AVAILABLE TARGETS ---")
            for i, target in enumerate(current_targets, 1):
                print(f"{i}. {target.name} (Sec-Level {target.difficulty} | Reward: {target.reward}C)")
            print("4. Back to Main Menu")
            
            target_choice = input("Select target to breach: ")
            if target_choice in ['1', '2', '3']:
                idx = int(target_choice) - 1
                run_hack_minigame(player, current_targets[idx])
                # Remove the target after a hack attempt (success or fail)
                current_targets[idx] = TargetSystem("Scorched Server (UNAVAILABLE)", 0)
        
        elif choice == '2':
            black_market(player)
            
        elif choice == '3':
            if player.credits >= 10:
                player.credits -= 10
                current_targets = generate_targets()
                print("\n[SUCCESS] Pinged network for new vulnerabilities.")
            else:
                print("\n[ERR] Need 10C to run a deep scan.")
                
        elif choice == '4':
            print(f"\nDisconnecting... You retired with {player.credits}C. Stay off the grid.")
            break
        else:
            print("\n[ERR] Unknown command.")
            
    if player.heat >= player.max_heat:
        print("\n🚨🚨🚨 CRITICAL ALERT 🚨🚨🚨")
        print(f"Your location has been compromised. Cyber-Division agents are at your door.")
        print(f"GAME OVER, {player.alias}.")

if __name__ == "__main__":
    main()
