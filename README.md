
# Firebog Aggregate

This Python script aggregates domain blocklists from the [Firebog](https://firebog.net/) website, processes them into categories, and saves them as text files. It ensures that duplicate domains are removed and splits large files into smaller chunks if necessary.

Use the following links to import lists to the pihole:
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/advertising_lists.txt
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/malicious_lists.txt
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/other_lists_part1.txt
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/other_lists_part2.txt
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/suspicious_lists.txt
https://raw.githubusercontent.com/nambatipudi/mypihole.list/refs/heads/main/tracking_and_telemetry_lists.txt


## Features

- Fetches blocklists from Firebog categories:
  - Suspicious Lists
  - Advertising Lists
  - Tracking & Telemetry Lists
  - Malicious Lists
  - Other Lists
- Removes duplicate domains across all categories.
- Splits large files into smaller chunks (default: 99 MB per file).
- Skips invalid or inaccessible lists.

## Requirements

- Python 3.7 or higher
- The following Python libraries:
  - `requests`
  - `beautifulsoup4`

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/firebog-aggregate.git
    cd firebog-aggregate
   ```

## Usage

Run the script using Python:
```sh
python firebog_aggregate.py
```

The script will:

1. Fetch blocklists from Firebog.
2. Process each category and save the domains into text files.
3. Split large files into smaller parts if they exceed the size limit.
 
#### Output Files
The script generates .txt files for each category, named after the category (e.g., suspicious_lists.txt). If a file exceeds 99 MB, it will be split into parts (e.g., suspicious_lists_part1.txt, suspicious_lists_part2.txt).

## Configuration
You can adjust the maximum file size for splitting by modifying the ``max_size_mb`` parameter in the ``split_large_file`` function.

#### Example Output
After running the script, you will see output like this:

```
========================================
Processing category: Suspicious Lists
✅ list1.txt                     | Added 100 new domains
✅ list2.txt                     | Added 50 new domains
📁 Final files for Suspicious Lists:
 - suspicious_lists.txt (0.15MB)

Processing category: Advertising Lists
🚫 Skipped 2 lists:
 - Example List 1
 - Example List 2
✅ list3.txt                     | Added 200 new domains
📁 Final files for Advertising Lists:
 - advertising_lists.txt (0.25MB)

========================================
Total unique domains across all lists: 350
All categories processed successfully!
```

#### Notes
* The script skips lists marked as "crossed out" on the Firebog website.
* If a list fails to download, it will be logged in the output.

