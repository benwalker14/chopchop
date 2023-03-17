import re

def findBeepBoopTimes(filename):
    # Read SRT file content
    with open(filename, 'r') as file:
        fileContent = file.read()
    
    # Split file content into individual subtitle entries
    entries = fileContent.strip().split('\n\n')
    
    beepBoopTimes = []
    
    # Parse each subtitle entry and check for 'beep' or 'boop' in the text
    for entry in entries:
        # Split entry into lines and extract start time, end time, and text
        lines = entry.split('\n')
        startTime, endTime = map(timeToSeconds, lines[1].split(' --> '))
        text = '\n'.join(lines[2:])
        
        # Check if text contains 'beep' or 'boop'
        if re.search(r'\b(damn|bitch)\b', text, re.IGNORECASE):
            beepBoopTimes.append((startTime, endTime))
    
    return beepBoopTimes

def timeToSeconds(timeString):
    x = timeString[:8]
    # Convert h:m:s time string to total number of seconds
    h, m, s = map(int, x.split(':'))
    return h * 3600 + m * 60 + s

times = findBeepBoopTimes(r'C:\Users\Ben\Downloads\TheItalianJob.srt')
print(times)