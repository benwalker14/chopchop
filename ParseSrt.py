import pysrt
import re

def load_profanity_list():
    return ["badword1", "badword2", "badword3"]  # Replace with a more comprehensive list

def contains_profanity(text, profanity_list):
    for word in profanity_list:
        if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
            return True
    return False

def find_profanity_timecodes(srt_file, profanity_list):
    profanity_timecodes = []
    subs = pysrt.open(srt_file, encoding='iso-8859-1')
    
    for sub in subs:
        if contains_profanity(sub.text, profanity_list):
            start_time = sub.start.to_time()
            end_time = sub.end.to_time()
            profanity_timecodes.append((start_time, end_time))

    return profanity_timecodes

def main():
    srt_file = "example.srt"  # Replace with your SRT file
    profanity_list = load_profanity_list()
    profanity_timecodes = find_profanity_timecodes(srt_file, profanity_list)
    
    if profanity_timecodes:
        print("Profanity timecodes found:")
        for start, end in profanity_timecodes:
            print(f"{start} - {end}")
    else:
        print("No profanity found.")

if __name__ == "__main__":
    main()
