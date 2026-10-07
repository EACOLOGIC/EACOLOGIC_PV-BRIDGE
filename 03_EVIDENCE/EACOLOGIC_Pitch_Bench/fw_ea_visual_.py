import time

class BridgeVisualizer:
    def __init__(self, initial_budget_usd=100.00):
        self.state_active = True  # True = Mit pv_bridge, False = Ohne Bridge (Standard)
        self.compression_factor = 6.4
        self.standard_budget = initial_budget_usd
        self.standard_values = 16384
        
    def toggle_state(self):
        self.state_active = not self.state_active
        self.render_screen()
        
    def render_screen(self):
        print("\n" + "="*40)
        print("    E4COLOGIC pv_bridge ESP32 MONITOR    ")
        print("="*40)
        
        if self.state_active:
            reduced_budget = self.standard_budget / self.compression_factor
            saved_budget = self.standard_budget - reduced_budget
            reduced_values = int(self.standard_values / self.compression_factor)
            
            print("[MODUS: MIT pv_bridge ACTIVE (6.4x)]")
            print(f"Datenvolumen : {reduced_values} Werte (statt {self.standard_values})")
            print(f"Speicherlast : 15.63% (Optimiert)")
            print(f"Rechenkosten : ${reduced_budget:.2f} USD")
            print(f"Ersparnis    : ${saved_budget:.2f} USD (84.38%)")
        else:
            print("[MODUS: OHNE BRIDGE (Standard / Vollfeld)]")
            print(f"Datenvolumen : {self.standard_values} Werte (Vollfeld)")
            print(f"Speicherlast : 100% (Voller Overhead)")
            print(f"Rechenkosten : ${self.standard_budget:.2f} USD")
            print(f"Ersparnis    : $0.00 USD")
            
        print("="*40 + "\n")

# Initialisierung mit deinen 100.00 USD Startwert
ui = BridgeVisualizer(initial_budget_usd=100.00)
ui.render_screen()

print("Visualisierung läuft. Simuliere Touch-Wechsel alle 5 Sekunden...\n")

# Hauptschleife (Simuliert den Wechsel per Touch-Button)
while True:
    time.sleep(5)
    ui.toggle_state()  # Schaltet automatisch zwischen Mit/Ohne Bridge um