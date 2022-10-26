import os

ASB_PLAY = "ansible-playbook"

PLAYBOOK_PATH_DICTIONARY = {
  'upload' : "upload/upload.yml"
}

def upload_to_hosts(args):
  print(args)

  if len(args) < 3:
    print("Error: missing parameters")
    print("Parameter list: [tag:value] [src file path(local)] [dest. file path(remote)]")
    return -1

  tag_key = args[0].split(':')[0]
  tag_value = args[0].split(':')[1]
  source_file = args[1]
  dest_path = args[2]

  target_host_group = "_%s_%s" % (tag_key, tag_value)

  print("Running ansible playbook - %s" % target_host_group)
  print("Source file: %s" % source_file)
  print("Destination path: %s" % dest_path)

  target_playbook = os.getcwd()+'/'+PLAYBOOK_PATH_DICTIONARY['upload']
  extra_parameters = "target_host=%s src_file=%s dest_path=%s" % (target_host_group, source_file, dest_path)

  command = "%s %s -e \"%s\"" % (ASB_PLAY, target_playbook, extra_parameters)

  #print(command)
  os.system(command)

  return 0

