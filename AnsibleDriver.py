import os
import json
from prettytable import PrettyTable

from Common import *

ASB_PLAY_BIN = "ansible-playbook"
LIST_TMP_FILE_PATH = "/tmp/ec2_instance_info.log"

PLAYBOOK_PATH_DICTIONARY = {
  'list' : "list_instances/print_info.yml",
  'upload' : "upload/upload.yml"
}

def list_instances(args):
  if len(args) < 1:
    print("Error: missing parameters")
    print("Parameter list: [tag:value]")
    return -ECODE_MISSING_PARAM

  tag_key = args[0].split(':')[0]
  tag_value = args[0].split(':')[1]

  target_playbook = os.getcwd() + '/' + PLAYBOOK_PATH_DICTIONARY['list']
  command = "%s %s" % (ASB_PLAY_BIN, target_playbook)
  ret_val = os.system(command)

  if ret_val > 0:
    return -ret_val

  tab_header = ['Instance Name', 'Private IP', 'Public IP', 'Status', 'Tags']
  tab = PrettyTable(tab_header)

  print("[Instance Information] - %s" % args[0])
  with open(LIST_TMP_FILE_PATH) as ec2_info_file:
    ec2_info_list = json.load(ec2_info_file)
    for ec2_info in ec2_info_list:
      if tag_key in ec2_info['tags'] and ec2_info['tags'][tag_key] == tag_value:
        inst_info_row = []

        inst_info_row.append(ec2_info['tags']['Name'])
        inst_info_row.append(ec2_info['private_ip_address'])
        inst_info_row.append(ec2_info['public_ip_address'])
        inst_info_row.append(ec2_info['state']['name'])
        inst_info_row.append(json.dumps(dict(sorted(ec2_info['tags'].items()))))

        tab.add_row(inst_info_row)

  print(tab)
  return ret_val



def 



def upload_to_hosts(args):
#  print(args)

  if len(args) < 3:
    print("Error: missing parameters")
    print("Parameter list: [tag:value] [src file path(local)] [dest. file path(remote)]")
    return -ECODE_MISSING_PARAM

  tag_key = args[0].split(':')[0]
  tag_value = args[0].split(':')[1]
  source_file = args[1]
  dest_path = args[2]

  target_host_group = "_%s_%s" % (tag_key, tag_value)

  print("Upload file(s) to hosts: %s" % target_host_group)
  print("Source file: %s" % source_file)
  print("Destination path: %s" % dest_path)

  target_playbook = os.getcwd() + '/' + PLAYBOOK_PATH_DICTIONARY['upload']
  extra_parameters = "target_host=%s src_file=%s dest_path=%s" % (target_host_group, source_file, dest_path)

  command = "%s %s -e \"%s\"" % (ASB_PLAY_BIN, target_playbook, extra_parameters)

  #print(command)
  ret_val = os.system(command)

  return ret_val

