##!R:\Pipeline\App_VHQ\Python27x64\pythonw.exe
# coding:utf-8
import os, sys
import subprocess
from pprint import pprint as pp

banner = '''
ImageSeq-2-MP4 v001_01
Written by Patrick Woo patrickwoo@yahoo.com
date: 20190927

This tool converts an image sequence(s) into corresponding MP4 movie file(s).
Name of image sequence should follow this convention:
    <base_name>.####.ext

Usage:
    Drop a directory onto the file, and a MP4 file will be created for each unique sequence of images 
'''

print(banner)

# first argv is the python file path
if len(sys.argv) < 2:
    print ('This tool needs a path to an image sequence')
    sys.exit(1)

print('{} args passed in '.format(len(sys.argv)-1))
# pp(sys.argv[1:])

# -- config variables
path_djv = r'R:\Pipeline\App_VHQ\djv_win64\bin\djv_view.exe'
path_ffmpg = r'R:\Pipeline\_bin\ffmpeg.exe'
imgFormatsDict = ['jpg', 'jpeg', 'png', 'tif', 'exr', 'iff', 'psd', 'tga', 'bmp', 'gif', 'dpx']
framerate = 24

foundDjv = False
foundFfmp = False
if (os.path.exists(path_djv)):
    print('djv exists at {}'.format(path_djv))
    foundDjv = True
else:
    print('DJV not found at {}. Movie files will not play using DJV.')

if (os.path.exists(path_ffmpg)):
    print('ffmpeg exists at {}'.format(path_ffmpg))
    foundFfmp = True
else:
    print('The ffmpeg dependency does not exist. Terminating.')
    print('ffmpeg not found: {}'.format(path_ffmpg))
    sys.exit(1)


for this_seq in sys.argv[1:]:
    print ('this seq is {}'.format(this_seq))
    if not os.path.isdir(this_seq):
        print('\n\nNot a directory: {}'.format(this_seq))
        print('This tool currently only supports directory as an input argument. Please only use directories for now.\n\n')
        continue # skips to the next iteration in the for loop
    else:
        # a dir is specified, look for img seqs
        this_path = os.path.abspath(os.path.realpath(this_seq))
        flist = os.listdir(this_seq)
        # print('{} files in {} are'.format(len(flist), this_seq))
        # pp(flist)
        # reminder, os.path.splitext will split 'abc.jpg' into ['abc', '.jpg'] watch the '.'
        # filter the file lists to only include recognised image extensions
        flistFiltered = [x.replace('\\','/') for x in flist if os.path.splitext(x)[1][1:].lower() in imgFormatsDict]
        # print('{} files after filter'.format(len(flistFiltered)))
        # pp(flistFiltered)
        
        # right now our filenames are without path
        # later we can use os.path.realpath() to get the full path
        
        baseNamesList = [os.path.splitext(x)[0].rsplit('.')[0] for x in flistFiltered]
        # print('baseNamesList is')
        # pp(baseNamesList)
        baseNamesList = list(set(baseNamesList))
        print ('unique base names found: {}, {}'.format(len(baseNamesList), baseNamesList))
        for basename in baseNamesList:
            print('\n\n--== processing {} ==--'.format(basename))
            fseq = [x for x in flistFiltered if basename in x]
            # an fseq item should now be 'basename.1001'
            fseq.sort()
            # print ('fseq is')
            # pp(fseq)

            # ascertain the number padding in frame numbers
            numPadding = sum([len(os.path.splitext(x)[0].rsplit('.')[1]) for x in fseq])/len(fseq) # average across paddings in all frames
            # print('numpadding is {}'.format(numPadding))

            # get the min and max frame numbers
            # print([fseq[0], fseq[-1]])
            minMaxFramesList = [int(os.path.splitext(x)[0].rsplit('.')[1]) for x in [fseq[0], fseq[-1]]]
            # print('minMaxFramesList is {}'.format(minMaxFramesList))
            
            # take the first file's extension and use it to define the sequence's extension
            # again this will give us '.ext'
            imgExt = os.path.splitext(fseq[0])[1]
            imgExt = imgExt[1:]
            # formattedFilename will be something like: 'basename.%04d.png'
            formattedFilename = '{}.%0{}d.{}'.format(basename, numPadding, imgExt)
            # print(formattedFilename)
            # print('this_path is {}'.format( this_path ))
            # fseqFull = [os.path.join(this_path, x).replace('\\', '/') for x in fseq if os.path.exists(os.path.join(this_path, x))]
            # pp(fseqFull)
            formattedFilenameFull = os.path.join(this_path, formattedFilename)
            # print ('formattedFilenameFull is {}'.format(formattedFilenameFull))

            # output image to put in a path that is 1 level up from the img seq
            # we usually put movie files one level up from the hundreds of images
            mp4OutPath = '{}.mp4'.format(os.path.join(os.path.split(this_path)[0],basename))
            # print('mp4OutPath is {}'.format(mp4OutPath))

            # build ffmpeg command
            # -vf "pad= " will deal with width & height pixels, adding 1 to pixel count if original width/height cannot be divided by 2            
            ffmpgCmd = '{} -start_number {} -framerate {} -i {} -vf "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2" -hide_banner {}'.format(\
                        path_ffmpg, minMaxFramesList[0], framerate, formattedFilenameFull, mp4OutPath)
            print('ffmpgCmd is:\n{}'.format(ffmpgCmd))
            print('running ffmpeg now')
            
            # calling with os.system()
            os.system(ffmpgCmd)
            
            # calling with subprocess
            # try:
            #     subprocess.call([ffmpgCmd])
            # except OSError:
            #     print ('ERROR: ffmpeg raised errors!')
            print('\n--== Finished processing {} ==--'.format(basename))
        # end for basename in baseNamesList
# end for this_seq


# playback section after conversion

try:
    # if the creation fails, mp4OutPath will be undefined

    # specify the path to movie
    # foundDjv=False
    if foundDjv:
        # this will use djv to open the movie
        subprocess.call([path_djv, mp4OutPath])
    else:
        # using the shell to launch the default player, like passing a command to dos prompt in shell
        # the following will play the movie using the OS default player assigned to handle the file type
        os.system(mp4OutPath)
except:
    pass