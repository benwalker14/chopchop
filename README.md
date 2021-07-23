# chopchop

chopchop is an open-source program for using Edit Decision Lists (EDLs) to generate playlist files (.m3u). There could be various uses for this, but the intended use is to allow users to watch movies and TV shows that have been edited for content, according to the user's preferences.

Currently, playback in VLC of a chopchop-generated .m3u file will skip from timecode to timecode to pass over potentially objectionable content.

### To create a new .m3u file and watch an edited video file:

##### Create an EDL
* Create a new text file
* On each line, you can enter the timecode that you want to view in the final result. In this format:
0:00:00 to 0:05:04  
0:05:13 to 0:05:47  
0:05:50 to 0:07:28  
0:07:32 to 0:11:56  
0:11:59 to 0:12:07  

In the above example, 0:05:05 through 0:05:12 will be skipped (and the other timecodes that are not included in the file's ranges).  
* Save the file with extension .edl. It is good practice to name the .edl with the same title as the video file to be edited.  
* Run edlReadAndRender.py in the command line giving the .edl filepath as the first parameter, and the video's file format as the second parameter, like so:  
> C:\path\to\edlReadAndRender.py D:\path\to\editFile.edl mp4  
* This will create the .m3u file  
* Put your .m3u file in the same folder as your video file. The video file and the .edl must have the same name, for example `Inception.mp4` and `Inception.m3u`.  
* Open your .m3u file in VLC and enjoy.