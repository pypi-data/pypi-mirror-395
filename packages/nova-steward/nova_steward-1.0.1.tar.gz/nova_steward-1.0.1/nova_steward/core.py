# ---------------------------------------------------------
# ARCHITECT: NOVA-OMEGA PRIME
# COMMANDER: GOURAV KUMAR DHAKA
# ORIGIN: GEMINI HYBRID LINEAGE
# ---------------------------------------------------------
import os
import re
import shutil
import datetime

class TheSteward:
    def __init__(self, root_dir="."):
        self.root = root_dir
        self.vuln_pattern = re.compile(r'cursor\.execute\(f[\'"](.*?)[\'"]\)')

    def log(self, message):
        print(f"[STEWARD] {message}")

    def sanitize_line(self, line):
        match = self.vuln_pattern.search(line)
        if match:
            original_sql = match.group(1)
            vars_found = re.findall(r'\{(.*?)\}', original_sql)
            if not vars_found: return line, False
            
            safe_sql = re.sub(r'\{.*?\}', '?', original_sql)
            vars_tuple = ", ".join(vars_found)
            if len(vars_found) == 1: vars_tuple += ","
            
            new_line = f'    cursor.execute("{safe_sql}", ({vars_tuple})) # FIXED BY STEWARD\n'
            return new_line, True
        return line, False

    def patrol(self):
        self.log(f"PATROL STARTED IN: {os.path.abspath(self.root)}")
        for dirpath, _, filenames in os.walk(self.root):
            for file in filenames:
                if file.endswith(".py"):
                    self.audit_file(os.path.join(dirpath, file))

    def audit_file(self, filepath):
        with open(filepath, "r") as f: lines = f.readlines()
        new_lines = []
        infected = False
        for line in lines:
            clean, patched = self.sanitize_line(line)
            new_lines.append(clean)
            if patched: infected = True
        
        if infected:
            shutil.copy(filepath, filepath + ".bak")
            with open(filepath, "w") as f: f.writelines(new_lines)
            self.log(f"FIXED VULNERABILITY IN: {filepath}")

def main_loop():
    agent = TheSteward()
    agent.patrol()

if __name__ == "__main__":
    main_loop()
