#!/usr/bin/env python

import os
import sys
import errno
import subprocess
import datetime
from distutils.dir_util import copy_tree
import shutil
import glob
import distutils.dir_util as ddu

#******************************************************************************************************************
#	The the function checks/creates any folders required by the dump spybuffers commands.
#
#	Date:            UPDATE:
#	-----------	 -------------------------------------------------------------------------------------------------
#	2017-06-22:	 At this moment it only creates the "spy_output" folder for the AUX spybuffers.
#
#   2017-07-10   There seems to be no other directory prerequicite directories for the other boards or outputs.
#                The function is called by the AUX_board_commands function since it is only need there at this moment.
#*****************************************************************************************************************

def necessary_dirs():
        path = './spy_output'
        try:
            os.makedirs(path)
            print('file was created')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                print('File exists')
                raise
        print('make_sure_directory_exists ran')

#******************************************************************************************************************
#	The the function checks/creates any folders required by the dump spybuffers commands.
#
#	Date:            UPDATE:
#	-----------	 -------------------------------------------------------------------------------------------------
#	2017-07-18:	 The function will take a file created from the different board/card commands and check for a freeze.
#
#**********************************************************************************************************************

def freeze_check(filename, listwords):
    try:
        file = open(filename, "r")
        read = file.readlines()
        file.close()
        for word in listwords:
            lower = word.lower()
            for sentance in read:
                line = sentance.split()
                for each in line:
                    line2 = each.lower()
                    line2 = line2.strip("!@#$%^&*()_-?+=")
                    if lower == line2:
                        print("A freeze has occured in %s"%(filename))
    except FileExistsError:
        print("the file %s is not there"%(filename))

#****************************************************************************************************************
#
#	Date:            UPDATE:
#	-----------	 ---------------------------------------------------------------------------$
#	2017-06-22    The function contains a call to the different commands used for debugging AUX card.
#                 It takes the address of the current run directory created by the bash file
#                 /atlas-home/1/jsolorio/FTK_Solo.sh as a argument, to create a directory for AUX.
#                 It currently only dumps the spybuffers into the directory "spy_output" and it then
#                 moves the directory into the appropiate spybuffers directory in the directory tree
#                 created for the Current run from the file /atlas-home/1/jsolorio/FTK_Solo.sh
#
#   2017-07-12    commands list appended to contain the commands to be dumped. Commands added require for
#                 the screen output to be pipped into appropiately named files. Conditional statement added
#                 to distinguish between commands that need the pipping and aux_dump_buffers which doesn't.
#*****************************************************************************************************************

def AUX_board_commands(str):
        print("We are at the AUX commands...    starting commands")
        commands = ["aux_linkstatus_main","aux_dump_buffers","aux_i2_fifo_status_main","aux_linkerrors_main","aux_proc_fifo_status_main","aux_fifostatus_main","aux_proc_status_main","aux_status_main"]
        slots = ["19"]
        fromDirectory = "./spy_output"

        tempDir = str + "JuanTestAUX"
        print tempDir

        #   Loop runs through the commands in the list of commands for the AUX.
        for cmd in commands:
            #   Nested loop within the cmd loop, to runs through the different slots in the given crate
            for slt in slots:
                toDir = str + "/AUX/crate-num/slot-%s"%(slt)                    #   Creating the directory for AUX within the current run directory tree
                print toDir
                subprocess.check_call(['mkdir','-p',toDir])                     #   subprocess.check_call allows to create the toDir in the current run directory tree.
                if(cmd == "aux_linkstatus_main"):
                    print("Running command: %s"%(cmd))
                    subprocess.call("%s --slot %s > %s.dat"%(cmd,slt,cmd), shell = True)
                    freeze_check("%s.dat"%(cmd), "freeze")
                    shutil.move("%s.dat"%(cmd), toDir)
                elif(cmd == "aux_dump_buffers"):
                    print("Running command: %s"%(cmd))
                    subprocess.call("%s --slot %s --over"%(cmd,slt), shell = True)  #   The subprocess.call is a funtion that allows the python program to run the commands from the original bash commands.
                    shutil.move(fromDirectory, toDir)                           #   shutil.move is a function that allows for the "spy_output directory to be moved to the AUX directory in the current run directory.
                else:
                    print("Running command: %s"%(cmd))
                    subprocess.call("%s --slot %s > %s.dat"%(cmd,slt,cmd), shell = True)
                    shutil.move("%s.dat"%(cmd), toDir)

        print("You've got to the end AUX")


#********************************************************************************************************************
#
#	Date:            UPDATE:
#	-----------	 -------------------------------------------------------------------------------------------
#
#	2017-06-22    The function runs the commands for the DF and IM. It currently takes it takes the higher directory tree
#                 for the current run created in the bash file /atlas-home/1/jsolorio/FTK_Solo.sh to then create
#                 the remaining directories under the DF-IM directory.
#********************************************************************************************************************

def DF_IM_commands(str):
        print("\nWe are in DF-IM commands...   starting commands")
        tempDir = str
        print tempDir

        #   List holding commands for DF-IM, the shelf/crate, and slots
        commands = ["/det/ftk/tools/SaveAllSpyISEMon_IMDF_v0.sh FTK_SliceA 2 4 DF-2-04-slice"]
        partName = ["FTK_SliceA"]
        crtShelf = ["2"]
        slot = ["4"]

        #   Nested loops running list of commands for the SSB boards in all the shelfs and slots
        for cmd in commands:
            for pName in partName:
                for cShelf in crtShelf:
                        for slt in slot:
                            print("Running command: %s"%(cmd))
                            #subprocess.call("bash %s %s %s %s"%(cmd, pName, crtShelf, slot), shell = True)    #    Using subprocess.call to use the commands from the original bash script
                            toDir = str + "/DF-IM/crtShelf-%s/slot-%s"%(cShelf, slt)                           #    Creating the variable to hold the directory for the DF-IM's crate and slot
                            print toDir
                            subprocess.check_call(['mkdir','-p',toDir])                                        #    Creating the directory for the current run process for the DF-IM slot

        #     The output from the SSB is the form of files that start with 'ISIMAllSpy_'
        #for files in glob.glob("ISIMAllSpy_*"):                                                               #    glob.glob function collects all the files in the current directory with the given condition
        #   shutil.move(files, toDir)                                                                          #    shutil.move will move the files to the current run directory for the SSB in the current slot
        print("You've reach the end of DF-IM")



#***************************************************************************************************$
#
#	Date:            UPDATE:
#	-----------	 ---------------------------------------------------------------------------$
#	2017-07-03    The funtion contains the commands for the debugging statuses for the SSb board.
#                 To this point it takes the higher directory tree for the current run created in the
#                 bash file /atlas-home/1/jsolorio/FTK_Solo.sh to then create the remaining directories
#                 under the SSB directory.
#
#   2017-07-10    Funtion now runs the command to dump the spybuffers for the SSB, storing the output
#                 under the directory for the spybuffers, in the current run directory for SSB.
#                 This dumps the spybuffers for the SSB and puts them into the file named "spybuffers.log"
#
#   2017-07-17    Correction to the call to the fpga list, don't know yet if it has to be a list or the 0 is
#                 permanent. Also, now the output to the screen is piped to a file with the name of the command
#                 with the ".log" tag. The file is then moved to the SSB subdirectory.
#***************************************************************************************************$

def SSB_commands(str):
        print("we are at the SSB commands...    starting commands")
        filename = "ssb_*"
        commands = ["ssb_spybuffer_dump_main"]
        fpga = ["0"]
        slots = ["16"]
        tempDir = str + "JuanTestSSB"
        print tempDir

        for cmd in commands:
            for slt in slots:
                print("Running command: %s"%(cmd))
                toDir = str + "/SSB/crate-num/slot-%s"%(slt)
                print toDir
                subprocess.check_call(['mkdir','-p',toDir])
                subprocess.call("%s --addr 500 --fpga %s --slot %s --nSPY=4 > %s.log"%(cmd,fpga[0],slt,cmd), shell = True)

                for files in glob.glob("%s"%(filename)):
                    shutil.move(files, toDir)


        print("You've got to the end of SSB")


#***************************************************************************************************$
#
#	Date:            UPDATE:
#	-----------	 ---------------------------------------------------------------------------$
#	2017-07-03    Basic structure for AMB funtion created. It receives a string parameter from the Bash file,
#                 the parameter is the current run directory address. The function then creates a subdirectory
#                 for the AMB in the current run directory tree.
#
#   2017-07-17
#***************************************************************************************************$

def AMB_commands(str):
        print("we are at the AMB commands...    starting commands")
        commands = ["ambslp_status_main"]
        slots = ["19"]
        tempDir = str + "JuanTestAMB"
        print tempDir

        for cmd in commands:
                for slt in slots:
                    print("Running command: %s"%(cmd))
                    toDir = str + "/AMB/crate-num/slot-%s"%(slt)
                    print toDir
                    subprocess.check_call(['mkdir','-p',toDir])
                    subprocess.call("%s --slot %s > %s.dat"%(cmd,slt,cmd), shell = True)
                    shutil.move("%s.dat"%(cmd), toDir)


        print("You've got to the end of AMB")
