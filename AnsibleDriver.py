import os
import json
from prettytable import PrettyTable

from Common import *
import ArgumentProcessor

LIST_TMP_FILE_PATH = "/tmp/ec2_instance_info.log"


def error_missing_parameter(arg_list):
  print("Error: missing parameters")
  param_list_str = "Parameter list: "
  for a in arg_list:
    param_list_str += "[%s]" % a
  print(param_list_str)
  return -ECODE_MISSING_PARAM



def list_instances(args):
  if len(args) < 1:
    return error_missing_parameter(["tag:value"])

  tag_key, tag_value = ArgumentProcessor.get_key_and_value(args[0])
  
  extra_vars = dict()
  extra_vars["tag_key"] = tag_key
  extra_vars["tag_value"] = tag_value

  command = ArgumentProcessor.generate_command('list', extra_vars)
  
  ret_val = os.system(command)

  if ret_val > 0:
    print("Failed to run command")
    return -ret_val

  tab_header = ['Instance Name', 'Private IP', 'Public IP', 'Status', 'Tags']
  tab = PrettyTable(tab_header)

  print("[Instance Information] - %s" % args[0])
  with open(LIST_TMP_FILE_PATH) as ec2_info_file:
    ec2_info_list = json.load(ec2_info_file)
    for ec2_info in ec2_info_list:
      inst_info_row = []
      inst_info_row.append(ec2_info['tags']['Name'])
      inst_info_row.append(ec2_info['private_ip_address'])
      inst_info_row.append(ec2_info['public_ip_address'])
      inst_info_row.append(ec2_info['state']['name'])
      inst_info_row.append(json.dumps(dict(sorted(ec2_info['tags'].items()))))

      tab.add_row(inst_info_row)

  print(tab)
  return -ret_val

def deploy_webserver(args):
  if len(args) < 2:
    return error_missing_parameter(["tag:value", "appName"])

  extra_vars = dict()
  extra_vars["target_host"] = ArgumentProcessor.get_host_group_name(args[0])
  extra_vars["app_name"] = args[1]

  command = ArgumentProcessor.generate_command('deploy', extra_vars)

  ret_val = os.system(command)

  return -ret_val


def change_instance_type(args):
  if len(args) < 2:
    return error_missing_parameter(["tag:value", "instance type"])

  tag_key, tag_value = ArgumentProcessor.get_key_and_value(args[0])

  extra_vars = dict()
  extra_vars["tag_key"] = tag_key
  extra_vars["tag_value"] = tag_value
  extra_vars["target_type"] = args[1]

  command = ArgumentProcessor.generate_command('change-type', extra_vars)

  ret_val = os.system(command)

  return -ret_val


def register_to_load_balancer(args):
  if len(args) < 2:
    return error_missing_parameter(["tag:value", "target group name"])

  tag_key, tag_value = ArgumentProcessor.get_key_and_value(args[0])

  extra_vars = dict()
  extra_vars["tag_key"] = tag_key
  extra_vars["tag_value"] = tag_value
  extra_vars["target_group_name"] = args[1]

  command = ArgumentProcessor.generate_command('register', extra_vars)

  ret_val = os.system(command)

  return -ret_val


def deregister_from_load_balancer(args):
  if len(args) < 2:
    return error_missing_parameter(["tag:value", "target group name"])

  tag_key, tag_value = ArgumentProcessor.get_key_and_value(args[0])

  extra_vars = dict()
  extra_vars["tag_key"] = tag_key
  extra_vars["tag_value"] = tag_value
  extra_vars["target_group_name"] = args[1]

  command = ArgumentProcessor.generate_command('deregister', extra_vars)

  ret_val = os.system(command)

  return -ret_val


def upload_to_hosts(args):
  if len(args) < 3:
    return error_missing_parameter(
      ["tag:value", 
      "src file path(local)", 
      "dest. file path(remote)"]
      )

  extra_vars = dict()
  extra_vars["target_host"] = ArgumentProcessor.get_host_group_name(args[0])
  extra_vars["src_file"] = args[1]
  extra_vars["dest_path"] = args[2]

  print("Upload file(s) to hosts: %s" % extra_vars["target_host"])
  print("Source file: %s" % extra_vars["src_file"])
  print("Destination path: %s" % extra_vars["dest_path"])

  command = ArgumentProcessor.generate_command('upload', extra_vars)

  ret_val = os.system(command)

  return -ret_val

def print_args(args):
  print(args)
