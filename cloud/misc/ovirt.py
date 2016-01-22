#!/usr/bin/python

# (c) 2013, Vincent Van der Kussen <vincent at vanderkussen.org>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: ovirt
author: '"Vincent Van der Kussen (@vincentvdk)" <vincent at vanderkussen.org>'
short_description: oVirt/RHEV platform management
description:
    - >
      allows you to create new instances, either from scratch or an image, in addition to deleting or stopping instances
      on the oVirt/RHEV platform
version_added: "1.4"
options:
  user:
    description:
     - the user to authenticate with
    default: null
    required: true
  url:
    description:
     - the url of the oVirt instance
    default: null
    required: true
  instance_name:
    description:
     - the name of the instance to use
    default: null
    required: true
    aliases: [ vmname ]
  password:
    description:
     - password of the user to authenticate with
    default: null
    required: true
    no_log: true
  image:
    description:
     - template to use for the instance
    default: null
    required: false
  resource_type:
    description:
     - whether you want to deploy an image or create an instance from scratch.
    default: null
    required: false
    choices: [ 'new', 'template' ]
  cluster:
    description:
     - deploy the image to this oVirt cluster
    default: null
    required: false
    aliases: [ zone ]
  instance_disksize:
    description:
     - size of the instance's disk in GB
    default: null
    required: false
    aliases: [ vm_disksize]
  instance_cpus:
    description:
     - the instance's number of cpu's
    default: 1
    required: false
    aliases: [ vmcpus ]
  instance_nic:
    description:
     - name of the network interface in oVirt/RHEV
    default: null
    required: false
    aliases: [ vmnic  ]
  instance_network:
    description:
     - the logical network the machine should belong to
    default: rhevm
    required: false
    aliases: [ vmnetwork ]
  instance_mem:
    description:
     - the instance's amount of memory in MB
    default: null
    required: false
    aliases: [ vmmem ]
  instance_type:
    description:
     - define if the instance is a server or desktop
    default: server
    required: false
    aliases: [ vmtype ]
    choices: [ 'server', 'desktop' ]
  disk_alloc:
    description:
     - define if disk is thin or preallocated
    default: thin
    required: false
    choices: [ 'thin', 'preallocated' ]
  disk_int:
    description:
     - interface type of the disk
    default: virtio
    required: false
    choices: [ 'virtio', 'ide' ]
  instance_os:
    description:
     - type of Operating System
    default: null
    required: false
    aliases: [ vmos ]
  instance_cores:
    description:
     - define the instance's number of cores
    default: 1
    required: false
    aliases: [ vmcores ]
  sdomain:
    description:
     - the Storage Domain where you want to create the instance's disk on.
    default: null
    required: false
  region:
    description:
     - the oVirt/RHEV datacenter where you want to deploy to
    default: null
    required: false
  state:
    description:
     - create, terminate or remove instances
    default: 'present'
    required: false
    choices: ['present', 'absent', 'shutdown', 'started', 'restart', 'cloud-init']
  authorized_key_file:
    description:
     - absolute path to the public key to be inserted into authorized keys on instantiation
    default: null
    required: false
    version_added: "2.0"
  authorized_key_user:
    description:
     - insert user key into authorized keys on instantiation
    default: 'root'
    required: false
    version_added: "2.0"
  authorized_key_user_groups:
    description:
     - Groups to associate to the user. comma separated list
    default: null
    required: false
    version_added: "2.0"
  tag:
    description:
     - comma separated list of tags
    default: null
    required: false
    version_added: "2.0"
  wait_for_state:
    description:
     - Normally all actions are asyncronous. This defines that we should wait for a machine state to be reached before we progress.
    default: null
    required: false
    version_added: "2.0"
  poll_frequency:
    description:
     - If we have set wait_for_state, this sets the poll_frequency (in seconds) at which to poll for the state of the VM
    default: 5
    required: false
    version_added: "2.0"
  poll_timeout:
    description:
     - If we have set wait_for_state, this specifies the maximum number of seconds to wait for before returning with a failure condition.
    default: 180
    required: false
    version_added: "2.0"
  custom_script:
    description:
      - A custom script to use with cloud-init. Must be an absolute path to a file
    default: null
    required: false
    version_added: "2.0"
  instance_host_name:
    description:
      - a hostname to apply to the instance
    default: null
    required: false
    version_added: "2.0"
  nic_name:
    description:
      - Name of the nic to apply a static ip address to
    default: null
    required: false
    version_added: "2.0"
  static_ip_address:
    description:
      - a static IP address to assign to the instance
    default: null
    required: false
    version_added: "2.0"
  static_netmask:
    description:
      - a static netmask address to assign to the instance
    default: null
    required: false
    version_added: "2.0"
  static_gateway:
    description:
      - a static gateway IP address to assign to the instance
    default: null
    required: false
    version_added: "2.0"

requirements:
  - "python >= 2.6"
  - "ovirt-engine-sdk-python"
'''
EXAMPLES = '''
# Basic example provisioning from image.

action: ovirt >
    user=admin@internal
    url=https://ovirt.example.com
    instance_name=ansiblevm04
    password=secret
    image=centos_64
    cluster=cluster01
    resource_type=template"

# Full example to create new instance from scratch
action: ovirt >
    instance_name=testansible
    resource_type=new
    instance_type=server
    user=admin@internal
    password=secret
    url=https://ovirt.example.com
    instance_disksize=10
    cluster=cluster01
    region=datacenter1
    instance_cpus=1
    instance_nic=nic1
    instance_network=rhevm
    instance_mem=1000
    disk_alloc=thin
    sdomain=FIBER01
    instance_cores=1
    instance_os=rhel_6x64
    disk_int=virtio
    authorized_key_file=/home/user/.ssh/id_rsa.pub
    authorized_key_user=root
    tags=test,ansible,jenkins
    async=False
    poll_frequency=5
    poll_timeout=180

# stopping an instance
action: ovirt >
    instance_name=testansible
    state=stopped
    user=admin@internal
    password=secret
    url=https://ovirt.example.com

# starting an instance
action: ovirt >
    instance_name=testansible
    state=started
    user=admin@internal
    password=secret
    url=https://ovirt.example.com
'''
RETURN = '''
instance_data:
  description: Information about the VM Instance
  returned: success
  type: dictionary
  contains:
    uuid:
      description: UUID of the instance
      returned: success
      type: string
      sample: af824696-bdc0-46de-b7f1-44c0302960cd
    id:
      description: ID of the instance
      returned: success
      type: string
      sample: af824696-bdc0-46de-b7f1-44c0302960cd
    image:
      description: Name of the instance's image
      returned: success
      type: string
      sample: rhel_7x64
    ips:
      description: UUID of the instance
      returned: success
      type: list
      sample: ["10.0.0.124"]
    name:
      description: Instance name
      returned: success
      type: string
      sample: ansiblevm04
    description:
      description: A description of the instance
      returned: success
      type: string
      sample: Some description
    status:
      description: UUID of the instance
      returned: success
      type: string
      sample: up
      choices: ['up', 'down', 'creating', 'starting', 'stopping', 'does_not_exist', 'unknown']
    cluster:
      description: The ovirt cluster the instance is running on
      returned: success
      type: string
      sample: local_cluster
    tags:
      description: Tags associated with the instance
      returned: success
      type: list
      sample: ["dev", "jenkins"]
    ovirt_guest_memory:
      description: Memory assigned to the VM
      returned: success
      type: int
      sample: 2056
    ovirt_guest_protected:
      description: Tags associated with the instance
      returned: success
      type: boolean
      sample: True
    ovirt_guest_nics:
      description: Tags associated with the instance
      returned: success
      type: dictionary
      contains:
        name:
          description: Name of the NIC
          returned: success
          type: string
          sample: eth0
        mac:
          description: Mac address of the NIC
          returned: success
          type: string
          sample: 01:23:45:67:89:ab
        machyphen:
          description: Hyphenated Mac address of the NIC
          returned: success
          type: string
          sample: 01-23-45-67-89-ab
        macupper:
          description: Uppercase Mac address of the NIC
          returned: success
          type: string
          sample: 01:23:45:67:89:AB
        machyphenupper:
          description: Uppercase Hyphenated Mac address of the NIC
          returned: success
          type: string
          sample: 01-23-45-67-89-AB
'''

import time
try:
    # noinspection PyUnresolvedReferences
    from ovirtsdk.api import API
    # noinspection PyUnresolvedReferences
    from ovirtsdk.xml import params

    HAS_LIB = True
except ImportError:
    HAS_LIB = False

#OVIRT_STATE_MAP = dict(
#    unassigned='unknown',
#    down='down',
#    up='up',
#    powering_up='starting',
#    paused='down',
#    migrating_from='creating',
#    migrating_to='creating',
#    unknown='unknown',
#    not_responding='unknown',
#    wait_for_launch='starting',
#    reboot_in_progress='starting',
#    saving_state='stopping',
#    restoring_state='starting',
#    suspended='down',
#    image_illegal='unknown',
#    image_locked='creating',
#    powering_down='stopping',
#)

OVIRT_VALID_STATES = [
    'up',
    'down',
    'starting',
    'unknown',
    'stopping',
    'creating',
]



class OvirtConnection(object):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    :type tries: int
    :type cloud_init_run: bool
    :type cloud_init_started: bool
    :type cloud_init_completed: bool
    """

    def __init__(self, module):
        self.module = module
        self.conn = None
        self.tries = int(module.params['poll_timeout'])
        self.cloud_init_started = False
        self.cloud_init_completed = False

    def __enter__(self):
        """
        :rtype : OvirtConnection
        """
        self.conn = self.connect()
        return self

    # noinspection PyUnusedLocal,PyBroadException
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.disconnect()
        except:
            pass

    # noinspection PyBroadException
    def connect(self):
        """
        :rtype: ovirtsdk.api.API
        """
        user = self.module.params['user']
        url = self.module.params['url']
        password = self.module.params['password']

        if not url.endswith('api'):
            url = '{}/api'.format(url.strip().rstrip('/'))

        try:
            api = API(url=url, username=user, password=password, insecure=True, debug=False)
            api.test(throw_exception=True)
        except:
            self.module.fail_json(msg=u"Could not connect to server: {}".format(url))
        else:
            return api

    def _get_auth_key(self):
        """
        :rtype : str
        """
        authorized_key_file = self.module.params['authorized_key_file']

        if authorized_key_file is not None:
            if os.path.isfile(authorized_key_file):
                try:
                    with open(authorized_key_file, 'r') as f:
                        return f.read()
                except IOError:
                    self.module.fail_json(
                        msg=u"Could not read the given authorized_key_file at {}".format(authorized_key_file)
                    )
            else:
                self.module.fail_json(
                    msg=u"authorized_key_file must be an absolute path to a public key file"
                )

    def _get_custom_script(self):
        """
        :rtype : str
        """
        custom_script = self.module.params['custom_script']

        if custom_script is not None:
            if os.path.isfile(custom_script):
                try:
                    with open(custom_script, 'r') as f:
                        return f.read()
                except IOError:
                    self.module.fail_json(
                        msg=u"Could not read the given custom script file at {}".format(custom_script)
                    )
            else:
                return custom_script

    def _cloud_init_network(self):
        """
        :rtype: ovirtsdk.xml.params.NetworkConfiguration
        """
        nic_name = self.module.params['nic_name']
        static_ip_address = self.module.params['static_ip_address']
        static_netmask = self.module.params['static_netmask']
        static_gateway = self.module.params['static_gateway']

        if all([nic_name, static_ip_address, static_netmask, static_gateway]):
            return params.NetworkConfiguration(
                nics=params.Nics(nic=[
                    params.NIC(
                        name=nic_name,
                        boot_protocol="STATIC",
                        on_boot=True,
                        network=params.Network(
                            ip=params.IP(
                                address=static_ip_address,
                                netmask=static_netmask,
                                gateway=static_gateway
                            )
                        )
                    )
                ])
            )

    def _cloud_init_user_groups(self):
        user_groups = self.module.params['authorized_key_user_groups']
        if user_groups is not None:
            return params.Groups(
                group=[params.Group(name=group.strip()) for group in user_groups.lower().strip().split(',')]
            )

    def _cloud_init_user(self):
        authorized_key_user = self.module.params['authorized_key_user']
        if authorized_key_user is not None:
            return params.Users(
                user=[
                    params.User(
                        user_name=authorized_key_user,
                        groups=self._cloud_init_user_groups()
                    )
                ]
            )

    def _generate_cloud_init(self):
        """
        :rtype : ovirtsdk.xml.params.Initialization
        """

        authorized_key_user = self.module.params['authorized_key_user']
        instance_host_name = self.module.params['instance_host_name']

        script = self._get_custom_script()
        key = self._get_auth_key()
        network = self._cloud_init_network()

        files = None
        auth_key = None

        if script is not None:
            files = params.Files(
                file=[params.File(name="/tmp/_vmcustomscript", content=script, type_="PLAINTEXT")]
            )

        if key is not None:
            auth_key = params.AuthorizedKeys(
                authorized_key=[
                    params.AuthorizedKey(
                        user=params.User(user_name=authorized_key_user),
                        key=key
                    ),
                ]
            )

        cloud_init = params.CloudInit(
            host=instance_host_name,
            files=files,
            authorized_keys=auth_key,
            network_configuration=network,
            regenerate_ssh_keys=True,
            users=self._cloud_init_user()
        )
        return params.Initialization(cloud_init=cloud_init)

    def get_cloud_init(self):
        """
        :rtype: ovirtsdk.xml.params.Initialization
        """
        return self._generate_cloud_init()

    # noinspection PyBroadException
    def add_tags(self):
        """
        :rtype: list[ovirtsdk.infrastructure.brokers.Tag]
        """
        tags = self.module.params['tags']

        if tags:
            new_tags = set([tag.strip().lower() for tag in tags.strip().replace(" ", "_").split(',')])

            try:
                existing_tags = set([tag.get_name() for tag in self.conn.tags.list()])
            except Exception:
                self.module.fail_json(msg=u"Could not get existing tags from server")
            else:
                tags_to_add = []
                for tag in new_tags:
                    if tag not in existing_tags:
                        try:
                            self.conn.tags.add(params.Tag(name=tag))
                        except:
                            self.module.fail_json(msg=u"Failed to add tag '{}' to ovirt".format(tag))
                    try:
                        infra_tag = self.conn.tags.get(name=tag)
                        tags_to_add.append(infra_tag)
                    except:
                        self.module.fail_json(msg=u"Failed to get tag '{}' from ovirt".format(tag))
                return tags_to_add

    # noinspection PyUnboundLocalVariable,PyBroadException
    def create_vm(self):
        """
        Create a VM instance
        """
        instance_name = self.module.params['instance_name']
        cluster = self.module.params['cluster']
        instance_disksize = self.module.params['instance_disksize']
        # instance_nic = self.module.params['instance_nic']
        instance_network = self.module.params['instance_network']
        instance_mem = self.module.params['instance_mem']
        disk_alloc = self.module.params['disk_alloc']
        disk_int = self.module.params['disk_int']
        instance_os = self.module.params['instance_os']
        instance_type = self.module.params['instance_type']
        instance_cores = self.module.params['instance_cores']
        sdomain = self.module.params['sdomain']

        vmparams = params.VM(
            name=instance_name,
            cluster=self.conn.clusters.get(name=cluster),
            os=params.OperatingSystem(type_=instance_os),
            template=self.conn.templates.get(name="Blank"),
            memory=1024 * 1024 * int(instance_mem),
            cpu=params.CPU(topology=params.CpuTopology(cores=int(instance_cores))),
            type_=instance_type,
        )

        network_net = params.Network(name=instance_network)
        nic_net1 = params.NIC(name='nic1', network=network_net, interface='virtio')

        if disk_alloc == 'thin':
            vmdisk = params.Disk(
                size=1024 * 1024 * 1024 * int(instance_disksize),
                wipe_after_delete=True,
                sparse=True,
                interface=disk_int,
                type_="System",
                format='cow',
                storage_domains=params.StorageDomains(storage_domain=[self.conn.storagedomains.get(name=sdomain)]),
            )
        elif disk_alloc == 'preallocated':
            vmdisk = params.Disk(
                size=1024 * 1024 * 1024 * int(instance_disksize),
                wipe_after_delete=True,
                sparse=False,
                interface=disk_int,
                type_="System",
                format='raw',
                storage_domains=params.StorageDomains(storage_domain=[self.conn.storagedomains.get(name=sdomain)])
            )
        else:
            self.module.fail_json(msg=u"Invalid value for 'disk_alloc': {}".format(disk_alloc))

        try:
            self.conn.vms.add(vmparams)
        except:
            self.module.fail_json(msg=u"Error creating VM with specified parameters")
        vm = self.conn.vms.get(name=instance_name)
        try:
            vm.disks.add(vmdisk)
        except:
            self.vm_remove()
            self.module.fail_json(msg=u"Error attaching disk")
        try:
            vm.nics.add(nic_net1)
        except:
            self.vm_remove()
            self.module.fail_json(msg=u"Error adding nic")
        if self.add_tags() is not None:
            for tag in self.add_tags():
                self.conn.vms.get(name=instance_name).tags.add(tag)

    def create_vm_template(self):
        """
        Create an instance from a template
        """
        instance_name = self.module.params['instance_name']
        cluster = self.module.params['cluster']
        image = self.module.params['image']

        vmparams = params.VM(
            name=instance_name,
            cluster=self.conn.clusters.get(name=cluster),
            template=self.conn.templates.get(name=image),
            disks=params.Disks(clone=True),
        )
        try:
            self.conn.vms.add(vmparams)
            if self.add_tags() is not None:
                for tag in self.add_tags():
                    self.conn.vms.get(name=instance_name).tags.add(tag)
        except:
            raise self.module.fail_json(msg=u'error adding template {}'.format(image))

    # noinspection PyBroadException
    def instantiate(self):
        instance_name = self.module.params['instance_name']
        image = self.module.params['image']
        resource_type = self.module.params['resource_type']

        if resource_type == 'template':
            try:
                self.create_vm_template()
            except Exception as e:
                self.module.fail_json(msg=u'error deploying from template {} - {}'.format(image, e))
        elif resource_type == 'new':
            try:
                self.create_vm()
            except:
                self.module.fail_json(msg=u"Failed to create VM: {}".format(instance_name))
        else:
            self.module.fail_json(msg=u"You did not specify a resource type")

    def get_ips(self):
        """
        get ip addresses from instance
        :rtype: list[str]
        """
        instance_name = self.module.params['instance_name']

        try:
            ips = [ip.get_address() for ip in self.conn.vms.get(name=instance_name).get_guest_info().get_ips().get_ip()]
        except AttributeError:
            ips = []
        return ips

    def get_instance_data(self):
        """
        :rtype: dict
        """
        instance_name = self.module.params['instance_name']
        inst = self.conn.vms.get(name=instance_name)

        if inst is None:
            return {}

        ips = self.get_ips()
        tags = [x.get_name() for x in inst.get_tags().list()]

        niclist = inst.get_nics().list()
        ovirt_guest_nics = []
        for nic in niclist:
            ovirt_guest_nics.append({
                'name': nic.get_name(),
                'mac': nic.get_mac().get_address(),
                'machyphen': nic.get_mac().get_address().replace(':', '-'),
                'macupper': nic.get_mac().get_address().upper(),
                'machyphenupper': nic.get_mac().get_address().upper().replace(':', '-'),
            })

        return {
            'uuid': inst.get_id(),
            'id': inst.get_id(),
            'image': inst.get_os().get_type(),
            'machine_type': inst.get_instance_type(),
            'ips': ips,
            'name': inst.get_name(),
            'description': inst.get_description(),
            'status': inst.get_status().get_state(),
            'cluster': self.conn.clusters.get(id=inst.get_cluster().get_id()).get_name(),
            'tags': tags,
            'ansible_ssh_host': ips[0] if len(ips) > 0 else None,
            'ovirt_guest_memory': inst.get_memory(),
            'ovirt_guest_protected': inst.get_delete_protected(),
            'ovirt_guest_nics': ovirt_guest_nics,
        }

    def vm_cloud_init(self):
        """
        :rtype : bool
        """
        instance_name = self.module.params['instance_name']

        current_state = self.vm_status()
        if current_state == 'down':
            vm = self.conn.vms.get(name=instance_name)
            if not self.cloud_init_started:
                vm.start(action=params.Action(vm=params.VM(initialization=self.get_cloud_init())))
                self.cloud_init_started = True
            else:
                vm.start()
                self.cloud_init_completed = True
            return True
        else:
            self.module.fail_json(
                msg=u"Machine {} is in state '{}'. Will not cloud init as you should investigate this".format(current_state ,instance_name)
            )

    def vm_start(self):
        """
        start instance
        :rtype : bool
        """
        instance_name = self.module.params['instance_name']

        current_state = self.vm_status()

        if current_state == 'down':
            vm = self.conn.vms.get(name=instance_name)
            vm.start()
            return True
        elif current_state == 'up':
            return False
        else:
            self.module.fail_json(
                msg=u"Machine {} is in state '{}'. Will not start as you should investigate this".format(current_state ,instance_name)
            )

    def vm_stop(self):
        """
        Stop instance
        :rtype : bool
        """
        instance_name = self.module.params['instance_name']

        vm = self.conn.vms.get(name=instance_name)
        current_state = self.vm_status()

        if current_state == 'up':
            vm.stop()
            return True
        elif current_state == 'down':
            return False
        else:
            self.module.fail_json(
                msg=u"Machine {} is in state '{}'. Will not stop as you should investigate this".format(current_state ,instance_name)
            )

    def vm_restart(self):
        """
        restart instance
        :rtype : bool
        """
        stopped = self.vm_stop()
        started = self.vm_start()
        return stopped and started

    def vm_remove(self):
        """
        remove an instance
        :rtype : bool
        """
        instance_name = self.module.params['instance_name']

        vm = self.conn.vms.get(name=instance_name)
        current_state = self.vm_status()

        if current_state == 'does_not_exist':
            return True
        elif current_state == 'down':
            vm.delete()
            return True
        else:
            self.module.fail_json(
                msg=u"Machine {} is in state '{}'. Will not remove as you should investigate this".format(current_state ,instance_name)
            )

    def vm_status(self):
        """
        Get the VMs status
        :rtype : bool
        """
        instance_name = self.module.params['instance_name']

        if instance_name not in set([vm.get_name() for vm in self.conn.vms.list()]):
            status = 'does_not_exist'
        else:
            # status = OVIRT_STATE_MAP.get(self.conn.vms.get(name=instance_name).get_status().get_state(), 'unknown')
            status = self.conn.vms.get(name=instance_name).get_status().get_state()
        return status

    def get_vm(self):
        """
        Get VM object and return it's name if object exists
        :rtype : str
        """
        instance_name = self.module.params['instance_name']
        vm = self.conn.vms.get(name=instance_name)

        return "empty" if vm is None else vm.get_name()

    def finish(self, changed, msg):
        """
        :type changed: bool
        :type msg: str
        """
        # Close the connection?
        self.module.exit_json(
            changed=changed,
            msg=msg,
            instance_data=self.get_instance_data()
        )

    def wait_for_state(self, state):
        """
        :type state: str
        """
        freq = self.module.params['poll_frequency']
        timeout = self.module.params['poll_timeout']
        elapsed = 0
        while elapsed < timeout:
            # Check the machine state
            current_state = self.vm_status()
            print('%s %s' % (current_state, elapsed))
            if state == current_state:
                return
            elapsed += freq
            time.sleep(freq)
        self.module.fail_json(msg=u'Waited for %s and state %s was not reached. Machine is in state %s' % (timeout, state, current_state ))


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'shutdown', 'started', 'restart', 'cloud-init']
            ),
            user=dict(
                type='str',
                required=True
            ),
            url=dict(
                type='str',
                required=True
            ),
            instance_name=dict(
                type='str',
                required=True,
                aliases=['instance_name']
            ),
            password=dict(
                type='str',
                required=True,
                no_log=True
            ),
            image=dict(
                type='str',
            ),
            resource_type=dict(
                type='str',
                choices=['new', 'template']
            ),
            cluster=dict(
                type='str',
                aliases=['zone']
            ),
            instance_disksize=dict(
                type='str',
                aliases=['vm_disksize']
            ),
            instance_cpus=dict(
                type='str',
                default=1,
                aliases=['instance_cpus']
            ),
            instance_nic=dict(
                type='str',
                aliases=['instance_nic']
            ),
            instance_network=dict(
                type='str',
                default='rhevm',
                aliases=['instance_network']
            ),
            instance_mem=dict(
                type='str',
                aliases=['instance_mem']
            ),
            instance_type=dict(
                type='str',
                default='server',
                aliases=['instance_type'],
                choices=['server', 'desktop']
            ),
            disk_alloc=dict(
                type='str',
                default='thin',
                choices=['thin', 'preallocated']
            ),
            disk_int=dict(
                type='str',
                default='virtio',
                choices=['virtio', 'ide']
            ),
            instance_os=dict(
                type='str',
                aliases=['instance_os']
            ),
            instance_cores=dict(
                type='str',
                default=1,
                aliases=['instance_cores']
            ),
            sdomain=dict(
                type='str',
            ),
            region=dict(
                type='str',
            ),
            authorized_key_file=dict(
                type='str',
            ),
            authorized_key_user=dict(
                type='str',
                default='root'
            ),
            authorized_key_user_groups=dict(
                type='str',
                default=None
            ),
            tags=dict(
                type='str',
            ),
            wait_for_state=dict(
                type='str',
                default=None
            ),
            poll_frequency=dict(
                type='float',
                default=5.0
            ),
            poll_timeout=dict(
                type='int',
                default=180
            ),
            custom_script=dict(
                type='str',
                default=None,
            ),
            instance_host_name=dict(
                type='str',
                default=None,
            ),
            nic_name=dict(
                type='str',
                default=None
            ),
            static_ip_address=dict(
                type='str',
                default=None
            ),
            static_netmask=dict(
                type='str',
                default=None
            ),
            static_gateway=dict(
                type='str',
                default=None
            ),
        ),
    )

    if not HAS_LIB:
        module.fail_json(msg=u'ovirt-engine-sdk-python required for this module')

    state = module.params['state']
    instance_name = module.params['instance_name']
    image = module.params['image']
    resource_type = module.params['resource_type']
    wait_for_state = module.params['wait_for_state']
    # Check that the wait_for_state is a valid state
    if wait_for_state is not None and wait_for_state not in OVIRT_VALID_STATES:
        module.fail_json(msg=u'Requested wait_for_state with invalid state.')

    # Going to need to tottaly rewrite these ....
    with OvirtConnection(module) as ovirt:
        initial_status = ovirt.vm_status()
        changed = False
        # error = False
        msg = u'No action was taken'

        if state == 'present':
            if initial_status == "does_not_exist":
                ovirt.instantiate()
                if resource_type == 'template':
                    changed=True
                    msg = u"deployed VM {} from template {}".format(instance_name, image)
                elif resource_type == 'new':
                    changed = True
                    msg = u"deployed VM {} from scratch".format(instance_name)
            else:
                changed = False
                msg = u"VM {} already exists".format(instance_name)

        elif state == 'started':
            if initial_status == 'up': # and (not wait_for_ip or (wait_for_ip and ovirt.get_ips())):
                changed = False
                msg = u"VM {} is already running".format(instance_name)
            else:
                ovirt.vm_start()
                changed = True
                msg = u"VM {0:s} started".format(instance_name)
        elif state == 'cloud-init':
            ovirt.vm_cloud_init()
            changed = True
            msg = u"VM {0:s} started".format(instance_name)
        elif state == 'shutdown':
            if initial_status == 'down':
                changed = False
                msg = u"VM {0:s} is already shutdown".format(instance_name)
            else:
                ovirt.vm_stop()
                changed = True
                msg = u"VM {} is shutting down".format(instance_name)
        elif state == 'restart':
            if initial_status == 'up':
                ovirt.vm_restart()
                changed = True
                msg = u"VM {0:s} is restarted".format(instance_name)
            else:
                ovirt.vm_restart()
                changed = True
                msg = u"VM {0:s} was started".format(instance_name)
        elif state == 'absent':
            if initial_status == 'does_not_exist':
                changed = False
                msg = u"VM {0:s} does not exist".format(instance_name)
            else:
                ovirt.vm_remove()
                changed = True
                msg = u"VM {0:s} removed".format(instance_name)
        if wait_for_state is not None:
            #  wait for the action ...
            ovirt.wait_for_state(state=wait_for_state)
        ovirt.finish(changed, msg)

# import module snippets
from ansible.module_utils.basic import *

main()
