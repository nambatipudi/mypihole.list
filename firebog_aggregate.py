import requests
import re
import os
from bs4 import BeautifulSoup

def sanitize_filename(name):
    """Convert heading text to safe filename"""
    name = name.replace('&', 'and').lower()
    return re.sub(r'[^\w-]', '_', name).strip('_')

def split_large_file(filename, max_size_mb=99):
    """Split files larger than specified MB into chunks"""
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    if not os.path.exists(filename):
        return []

    file_size = os.path.getsize(filename)
    if file_size <= max_size:
        return [filename]

    print(f"Splitting {os.path.basename(filename)} ({file_size/1024/1024:.2f}MB)")
    part_num = 1
    current_size = 0
    current_lines = []
    base_name = os.path.splitext(filename)[0]
    output_files = []

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line_size = len(line.encode('utf-8'))
            if current_size + line_size > max_size:
                # Write current part
                part_filename = f"{base_name}_part{part_num}.txt"
                with open(part_filename, 'w', encoding='utf-8') as part_f:
                    part_f.writelines(current_lines)
                output_files.append(part_filename)
                print(f"Created {os.path.basename(part_filename)} ({current_size/1024/1024:.2f}MB)")
                part_num += 1
                current_lines = []
                current_size = 0
            current_lines.append(line)
            current_size += line_size

        # Write remaining lines
        if current_lines:
            part_filename = f"{base_name}_part{part_num}.txt"
            with open(part_filename, 'w', encoding='utf-8') as part_f:
                part_f.writelines(current_lines)
            output_files.append(part_filename)
            print(f"Created {os.path.basename(part_filename)} ({current_size/1024/1024:.2f}MB)")

    os.remove(filename)
    print(f"Removed original file: {os.path.basename(filename)}")
    return output_files

def process_category(heading, element, global_seen):
    """Process a single category and save its blocklist"""
    print(f"\n{'='*40}\nProcessing category: {heading}")
    urls = []
    skipped = []
    
    # Find all list items in this category
    for li in element.find_all('li'):
        if 'bdCross' in li.get('class', []):
            list_name = li.a.text.strip().rstrip(':')
            skipped.append(list_name)
            continue
        links = li.find_all('a')
        if len(links) >= 2:
            urls.append(links[1]['href'])
    
    # Show skipped lists
    if skipped:
        print(f"\n🚫 Skipped {len(skipped)} lists:")
        for name in skipped:
            print(f" - {name}")
    
    # Download and process lists
    category_domains = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            added = 0
            for line in response.text.splitlines():
                # Strip comments and whitespace
                clean_line = line.split('#', 1)[0].strip()
                if not clean_line:
                    continue
                
                # Add domain if not seen globally
                if clean_line not in global_seen:
                    category_domains.add(clean_line)
                    global_seen.add(clean_line)
                    added += 1
            print(f"✅ {os.path.basename(url)[:30]:<30} | Added {added} new domains")
        except Exception as e:
            print(f"❌ {os.path.basename(url)[:30]:<30} | Failed: {str(e)}")
    
    # Save category file
    if category_domains:
        base_filename = sanitize_filename(heading)
        filename = f"{base_filename}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(category_domains)))
        
        # Split if needed and get final filenames
        final_files = split_large_file(filename)
        print(f"\n📁 Final files for {heading}:")
        for fname in final_files:
            size = os.path.getsize(fname) / 1024 / 1024
            print(f" - {os.path.basename(fname)} ({size:.2f}MB)")
        return len(category_domains)
    else:
        print("⚠️ No new domains found for this category")
        return 0

# Main execution
if __name__ == "__main__":
    response = requests.get('https://firebog.net/')
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    target_headings = [
        'Suspicious Lists',
        'Advertising Lists',
        'Tracking & Telemetry Lists',
        'Malicious Lists',
        'Other Lists'
    ]

    global_seen = set()
    total_domains = 0

    for heading in target_headings:
        h2 = soup.find('h2', string=heading)
        if h2:
            ul = h2.find_next_sibling('ul')
            if ul:
                count = process_category(heading, ul, global_seen)
                total_domains += count
        else:
            print(f"⚠️ Warning: Heading '{heading}' not found in page")

    print("\n" + "="*40)
    print(f"Total unique domains across all lists: {total_domains}")
    print("All categories processed successfully!")