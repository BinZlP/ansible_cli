import os

ASB_PLAY_BIN = "ansible-playbook"

PLAYBOOK_PATH_DICTIONARY = {
  'list' : "list_instances/print_info.yml",
  'deploy' : "deploy_webserver/deploy.yml",
  'change-type' : "change_type/change_type.yml",
  'register' : "register_to_lb/registration.yml",
  'deregister' : "register_to_lb/deregistration.yml",
  'upload' : "upload/upload.yml"
}

def get_key_and_value(kv_str):
  tag_key = kv_str.split(':')[0]
  tag_value = kv_str.split(':')[1]
  return tag_key, tag_value


def get_host_group_name(kv_str): 
  tag_key = kv_str.split(':')[0]
  tag_value = kv_str.split(':')[1]
  target_host_group = "_%s_%s" % (tag_key, tag_value)
  return target_host_group


def generate_command(command, extra_var_dict):
  recipe="%s %s -e \"%s\""
  target_playbook = os.getcwd()
  target_playbook += '/' + PLAYBOOK_PATH_DICTIONARY[command]
  
  extra_var_string = ""
  for k, v in extra_var_dict.items():
    extra_var_string += "%s=%s " % (k,v)
  
  return recipe % (ASB_PLAY_BIN, target_playbook, extra_var_string)


