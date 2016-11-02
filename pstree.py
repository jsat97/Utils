#!/usr/local/bin/python3
import os, sys
# -c on OS X to get only name of command 
if os.uname()[0] == 'Darwin':
  PS_COMMAND = "ps caxo pid,ppid,comm"
  # linux
else:
  PS_COMMAND = "ps axo pid,ppid,comm"

PID_INDEX = 0
PPID_INDEX = 1
COMM_INDEX = 2
nskip = 1

def print_proc(pid, indent):
  # print the parent
  if pid == "1" : 
    indent_str = indent
  else:
    indent_str = indent + "-"

  print("%s %s %s" %(indent_str, pid, proc_dict[pid]["comm"]))
  # if pid has no children return
  if not pid in proc_child_dict: return
  indent +=  "\t" + "|"
  # iterate the list of children for pid    
  for child_pid in proc_child_dict[pid]:
    #print("%s |- %s %s %s" %(indent, child_pid, proc_dict[child_pid]["ppid"], proc_dict[child_pid]["comm"]))
    # keep descending the tree until there are no more children
    print_proc(child_pid, indent) 

if __name__ == "__main__":
  global proc_dict, proc_child_dict
  proc_dict = {}
  proc_child_dict = {}
  no_lines = 0

  for line in os.popen(PS_COMMAND, "r"):
    no_lines += 1
    if no_lines <= nskip: continue
    line_list = line.strip().split()
    pid = line_list[PID_INDEX]      
    ppid = line_list[PPID_INDEX]      
    proc_dict[pid] = {"pid":line_list[PID_INDEX], "ppid":line_list[PPID_INDEX], "comm":line_list[COMM_INDEX]}
    # add it to the list of children for its parent
    if ppid in proc_child_dict:
      proc_child_dict[ppid].append(pid)   
    else:      
      proc_child_dict[ppid] = []
      proc_child_dict[ppid].append(pid)   
  print_proc("1", "")
