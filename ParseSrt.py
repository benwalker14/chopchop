import pysrt
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import timedelta

def find_non_profanity_timecodes(srt_file, profanity_list):
    safe_timecodes = []
    subs = pysrt.open(srt_file, encoding='iso-8859-1')

    # Initialize the end of the last safe period to the start of the video
    last_safe_end = timedelta()

    for sub in subs:
        if contains_profanity(sub.text, profanity_list):
            # Add the time period from the end of the last safe period to the start of the profanity
            safe_timecodes.append((last_safe_end, sub.start.to_time()))

            # Update the end of the last safe period to the end of the current profanity
            last_safe_end = sub.end.to_time()

    # Add the final safe period from the end of the last profanity to the end of the video
    # This assumes the end of the video is the same as the end of the last subtitle
    safe_timecodes.append((last_safe_end, subs[-1].end.to_time()))

    return safe_timecodes

def load_profanity_list():
    return ["fuck", "shit", "jesus", "christ", "my god", "my god", "bitch", "bastard", "cunt", "faggot", "dammit", "damn"]  # Replace with a more comprehensive list

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
    # Hide the main tkinter window
    Tk().withdraw()

    # Open the file dialog and get the path to the selected file
    srt_file = askopenfilename(filetypes=[("SRT files", "*.srt")])

    # Proceed only if a file is selected
    if srt_file:
        profanity_list = load_profanity_list()
        safe_timecodes = find_non_profanity_timecodes(srt_file, profanity_list)

        if safe_timecodes:
            print("Safe timecodes found:")
            for start, end in safe_timecodes:
                print(f"{start} to {end}")
        else:
            print("No safe periods found.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()


