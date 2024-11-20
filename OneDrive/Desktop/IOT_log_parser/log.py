import pandas as pd
import matplotlib.pyplot as plt
import json

def parse_log_file(log_file_path):
    parsed_entries = []
    with open(log_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                if line.startswith("{") and line.endswith("}"):
                    entry = json.loads(line)
                    parsed_entries.append(entry)
                else:
                    objects = line.split("}{")
                    for i, obj in enumerate(objects):
                        if i > 0:
                            obj = "{" + obj
                        if i < len(objects) - 1:
                            obj = obj + "}"
                        parsed_entries.append(json.loads(obj))
            except json.JSONDecodeError as e:
                print(f"Error parsing log entry: {e}")
                print(f"Malformed line: {line}")
                continue
    return parsed_entries

def visualize_data(data_entries):
    if not data_entries:
        print("No data to visualize.")
        return
    
    df = pd.DataFrame(data_entries)
    if 'event' in df.columns:
        event_counts = df['event'].value_counts()
        plt.figure(figsize=(10, 6))
        event_counts.plot(kind='bar', color='skyblue')
        plt.title('User Event Counts')
        plt.xlabel('Event')
        plt.ylabel('Count')
        plt.show()
    else:
        print("No 'event' column found in data.")

if __name__ == "__main__":
    log_file_path = "assignment_prod.log"
    parsed_data_entries = parse_log_file(log_file_path)
    print(f"Parsed {len(parsed_data_entries)} valid entries.")
    visualize_data(parsed_data_entries)