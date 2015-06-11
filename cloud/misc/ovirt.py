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
  zone:
    description:
     - deploy the image to this oVirt cluster
    default: null
    required: false
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
    choices: ['present', 'absent', 'shutdown', 'started', 'restarted', 'cloud-init']
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
  tag:
    description:
     - comma separated list of tags
    default: null
    required: false
    version_added: "2.0"
  async:
    description:
     - If True, just send command to server. If false, wait for the correct state before continuing (Idempotent)
    default: 'yes'
    required: false
    version_added: "2.0"
  poll_frequency:
    description:
     - If not async, this sets the poll_frequency (in seconds) at which to poll for the state of the VM
    default: 5
    required: false
    version_added: "2.0"
  poll_tries:
    description:
     - If not async, this specifies the maximum number of times to poll before exiting
    default: 100
    required: false
    version_added: "2.0"
  wait_for_ip:
    description:
     - >
       If not async, wait for the VM to provide its IP addresses before continuing (requires that VM image has "ovirt
       guest agent" installed)
    default: 'no'
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
    zone=cluster01 
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
    zone=cluster01 
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
    poll_tries=100
    wait_for_ip=True

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
            choices: ['up', 'down', 'creating', 'starting' 'stopping', 'does_not_exist', 'unknown']
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
'''

try:
    # noinspection PyUnresolvedReferences
    from ovirtsdk.api import API
    # noinspection PyUnresolvedReferences
    from ovirtsdk.xml import params

    HAS_LIB = True
except ImportError:
    HAS_LIB = False

OVIRT_STATE_MAP = dict(
    unassigned='unknown',
    down='down',
    up='up',
    powering_up='starting',
    paused='down',
    migrating_from='creating',
    migrating_to='creating',
    unknown='unknown',
    not_responding='unknown',
    wait_for_launch='starting',
    reboot_in_progress='starting',
    saving_state='stopping',
    restoring_state='starting',
    suspended='down',
    image_illegal='unknown',
    image_locked='creating',
    powering_down='stopping',
)


class OvirtConnection(object):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """

    def __init__(self, module):
        self.module = module
        self.conn = self.connect()
        self.tries = int(module.params['poll_tries'])
        self.cloud_init_run = False

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
            api = API(url=url, username=user, password=password, insecure=True)
            api.test(throw_exception=True)
        except:
            self.module.fail_json(msg=u"Could not connect to server: {}".format(url))
        else:
            return api

    def _get_auth_key(self):
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
        script_file = self.module.params['script_file']

        if script_file is not None:
            if os.path.isfile(script_file):
                try:
                    with open(script_file, 'r') as f:
                        return f.read()
                except IOError:
                    self.module.fail_json(
                        msg=u"Could not read the given custom script file at {}".format(script_file)
                    )
            else:
                self.module.fail_json(
                    msg=u"custom_script must be an absolute path to a file"
                )

    def _generate_cloud_init(self):
        """
        :rtype : ovirtsdk.xml.params.Initialization
        """

        authorized_key_user = self.module.params['authorized_key_user']
        instance_host_name = self.module.params['instance_host_name']

        script = self._get_custom_script()
        key = self._get_auth_key()

        cloud_init = params.CloudInit(
            host=instance_host_name,
            files=params.Files(
                file=[params.File(name="/tmp/_vmcustomscript", content=script, type_="PLAINTEXT")]
            ),
            authorized_keys=params.AuthorizedKeys(
                authorized_key=[
                    params.AuthorizedKey(
                        user=params.User(user_name=authorized_key_user),
                        key=key
                    ),
                ]
            )
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

    def recurse(self, func):
        """
        :type func: (OvirtConnection) -> bool
        :rtype: bool
        """
        poll_frequency = float(self.module.params['poll_frequency'])

        time.sleep(poll_frequency)
        self.tries -= 1
        return func()

    # noinspection PyUnboundLocalVariable,PyBroadException
    def create_vm(self):
        """
        Create a VM instance
        """
        instance_name = self.module.params['instance_name']
        zone = self.module.params['zone']
        instance_disksize = self.module.params['instance_disksize']
        instance_nic = self.module.params['instance_nic']
        instance_network = self.module.params['instance_network']
        instance_mem = self.module.params['instance_mem']
        disk_alloc = self.module.params['disk_alloc']
        disk_int = self.module.params['disk_int']
        instance_os = self.module.params['instance_os']
        instance_type = self.module.params['instance_type']
        instance_cores = self.module.params['instance_cores']
        sdomain = self.module.params['sdomain']

        if disk_alloc == 'thin':
            vmparams = params.VM(
                name=instance_name,
                cluster=self.conn.clusters.get(name=zone),
                os=params.OperatingSystem(type_=instance_os),
                template=self.conn.templates.get(name="Blank"),
                memory=1024 * 1024 * int(instance_mem),
                cpu=params.CPU(topology=params.CpuTopology(cores=int(instance_cores))),
                type_=instance_type,
            )
            vmdisk = params.Disk(
                size=1024 * 1024 * 1024 * int(instance_disksize),
                wipe_after_delete=True,
                sparse=True,
                interface=disk_int,
                type_="System",
                format='cow',
                storage_domains=params.StorageDomains(storage_domain=[self.conn.storagedomains.get(name=sdomain)]),
            )
            network_net = params.Network(name=instance_network)
            nic_net1 = params.NIC(name='nic1', network=network_net, interface='virtio')
        elif disk_alloc == 'preallocated':
            vmparams = params.VM(
                name=instance_name,
                cluster=self.conn.clusters.get(name=zone),
                os=params.OperatingSystem(type_=instance_os),
                template=self.conn.templates.get(name="Blank"),
                memory=1024 * 1024 * int(instance_mem),
                cpu=params.CPU(topology=params.CpuTopology(cores=int(instance_cores))),
                type_=instance_type,
            )
            vmdisk = params.Disk(
                size=1024 * 1024 * 1024 * int(instance_disksize),
                wipe_after_delete=True,
                sparse=False,
                interface=disk_int,
                type_="System",
                format='raw',
                storage_domains=params.StorageDomains(storage_domain=[self.conn.storagedomains.get(name=sdomain)])
            )
            network_net = params.Network(name=instance_network)
            nic_net1 = params.NIC(name=instance_nic, network=network_net, interface='virtio')
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
        for tag in self.add_tags():
            self.conn.vms.get(name=instance_name).tags.add(tag)

    def create_vm_template(self):
        """
        Create an instance from a template
        """
        instance_name = self.module.params['instance_name']
        zone = self.module.params['zone']
        image = self.module.params['image']

        vmparams = params.VM(
            name=instance_name,
            cluster=self.conn.clusters.get(name=zone),
            template=self.conn.templates.get(name=image),
            disks=params.Disks(clone=True),
        )
        self.conn.vms.add(vmparams)
        for tag in self.add_tags():
            self.conn.vms.get(name=instance_name).tags.add(tag)

    # noinspection PyBroadException
    def instantiate(self):
        instance_name = self.module.params['instance_name']
        image = self.module.params['image']
        resource_type = self.module.params['resource_type']

        if resource_type == 'template':
            try:
                self.create_vm_template()
            except:
                self.module.fail_json(msg=u'error adding template {}'.format(image))
        elif resource_type == 'new':
            try:
                self.create_vm()
            except:
                self.module.fail_json(u"Failed to create VM: {}".format(instance_name))
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
                'name' : nic.get_name(),
                'mac' : nic.get_mac().get_address(),
                'machyphen' : nic.get_mac().get_address().replace(':', '-'),
                'macupper' : nic.get_mac().get_address().upper(),
                'machyphenupper' : nic.get_mac().get_address().upper().replace(':', '-'),
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
            'ovirt_guest_memory' : inst.get_memory(),
            'ovirt_guest_protected' : inst.get_delete_protected(),
            'ovirt_guest_nics' : ovirt_guest_nics

        }



    def vm_cloud_init(self):
        instance_name = self.module.params['instance_name']
        async = self.module.boolean(self.module.params['async'])
        wait_for_ip = self.module.boolean(self.module.params['wait_for_ip'])

        state = self.vm_status()

        if self.tries <= 0:
            self.module.fail_json(
                msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state)
            )
        if state == 'does_not_exist':
            self.instantiate()
            return self.recurse(self.vm_cloud_init)
        elif state == 'unknown':
            self.module.fail_json(msg=u"{} is in an unknown state.".format(instance_name))
        elif state in ['creating', 'starting', 'stopping']:
            return self.recurse(self.vm_cloud_init)
        elif state == 'down':
            vm = self.conn.vms.get(name=instance_name)
            vm.start(action=params.Action(params.VM(initialization=self.get_cloud_init())))
            self.cloud_init_run = True
            if not async:
                return self.recurse(self.vm_cloud_init)
        elif state == 'up':
            if not self.cloud_init_run:
                self.vm_stop()
                self.recurse(self.vm_cloud_init)
            else:
                self.cloud_init_run = False
                if wait_for_ip:
                    ips = self.get_ips()
                    if not ips:
                        return self.recurse(self.vm_cloud_init)

    def vm_start(self):
        """
        start instance
        """
        instance_name = self.module.params['instance_name']
        async = self.module.boolean(self.module.params['async'])
        wait_for_ip = self.module.boolean(self.module.params['wait_for_ip'])

        state = self.vm_status()

        if self.tries <= 0:
            self.module.fail_json(
                msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state)
            )
        if state == 'does_not_exist':
            self.instantiate()
            return self.recurse(self.vm_start)
        elif state == 'unknown':
            self.module.fail_json(msg=u"{} is in an unknown state.".format(instance_name))
        elif state in ['creating', 'starting', 'stopping']:
            return self.recurse(self.vm_start)
        elif state == 'down':
            vm = self.conn.vms.get(name=instance_name)
            vm.start()
            if not async:
                return self.recurse(self.vm_start)
        elif state == 'up':
            if wait_for_ip:
                ips = self.get_ips()
                if not ips:
                    return self.recurse(self.vm_start)

    def vm_stop(self):
        """
        Stop instance
        """
        instance_name = self.module.params['instance_name']
        async = self.module.boolean(self.module.params['async'])

        vm = self.conn.vms.get(name=instance_name)
        state = self.vm_status()

        if self.tries <= 0:
            self.module.fail_json(
                msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state)
            )
        if state == 'does_not_exist':
            self.instantiate()
            return self.recurse(self.vm_stop)
        elif state == 'unknown':
            self.module.fail_json(msg=u"{} is in an unknown state.".format(instance_name))
        elif state in ['creating', 'starting', 'stopping']:
            return self.recurse(self.vm_stop)
        elif state == 'up':
            vm.stop()
            if not async:
                return self.recurse(self.vm_stop)
        elif state == 'down':
            return True

    def vm_restart(self):
        """
        restart instance
        """
        stopped = self.vm_stop()
        started = self.vm_start()
        return stopped and started

    def vm_remove(self):
        """
        remove an instance
    
        """
        instance_name = self.module.params['instance_name']
        async = self.module.boolean(self.module.params['async'])

        vm = self.conn.vms.get(name=instance_name)
        state = self.vm_status()

        if self.tries <= 0:
            self.module.fail_json(
                msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state)
            )
        if state == 'does_not_exist':
            return True
        elif state == 'unknown':
            vm.delete(action=params.Action(force=True))
            return True if async else self.recurse(self.vm_remove)
        elif state in ['creating', 'starting', 'stopping']:
            return self.recurse(self.vm_remove)
        elif state == 'up':
            self.vm_stop()
            return self.recurse(self.vm_remove)
        elif state == 'down':
            vm.delete()
            return True if async else self.recurse(self.vm_remove)

    def vm_status(self):
        """
        Get the VMs status
        """
        instance_name = self.module.params['instance_name']

        if instance_name not in set([vm.get_name() for vm in self.conn.vms.list()]):
            status = 'does_not_exist'
        else:
            status = OVIRT_STATE_MAP.get(self.conn.vms.get(name=instance_name).get_status().get_state(), 'unknown')
        return status

    def get_vm(self):
        """
        Get VM object and return it's name if object exists
        """
        instance_name = self.module.params['instance_name']
        vm = self.conn.vms.get(name=instance_name)

        return "empty" if vm is None else vm.get_name()

    def finish(self, changed, msg):
        """
        :type changed: bool
        :type msg: str
        """
        self.module.exit_json(
            changed=changed,
            msg=msg,
            instance_data=self.get_instance_data()
        )


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
            zone=dict(
                type='str',
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
            tags=dict(
                type='str',
            ),
            async=dict(
                type='bool',
                default=True,
                choices=BOOLEANS
            ),
            poll_frequency=dict(
                type='float',
                default=5.0
            ),
            poll_tries=dict(
                type='int',
                default=100
            ),
            wait_for_ip=dict(
                type='bool',
                default=False,
                choices=BOOLEANS
            ),
            custom_script=dict(
                type='str',
                default=None,
            ),
            instance_host_name=dict(
                type='str',
                default=None,
            ),
        ),
    )

    if not HAS_LIB:
        module.fail_json(msg=u'ovirt-engine-sdk-python required for this module')

    state = module.params['state']
    instance_name = module.params['instance_name']
    image = module.params['image']
    resource_type = module.params['resource_type']
    wait_for_ip = module.boolean(module.params['wait_for_ip'])

    ovirt = OvirtConnection(module)

    initial_status = ovirt.vm_status()

    if state == 'present':
        if initial_status == "does_not_exist":
            ovirt.instantiate()
            if resource_type == 'template':
                ovirt.finish(
                    changed=True,
                    msg=u"deployed VM {} from template {}".format(instance_name, image),
                )
            elif resource_type == 'new':
                ovirt.finish(
                    changed=True,
                    msg=u"deployed VM {} from scratch".format(instance_name),
                )
        else:
            ovirt.finish(
                changed=False,
                msg=u"VM {} already exists".format(instance_name),
            )

    if state == 'started':
        if initial_status == 'up' and (not wait_for_ip or (wait_for_ip and ovirt.get_ips())):
            ovirt.finish(
                changed=False,
                msg=u"VM {} is already running".format(instance_name),
            )
        else:
            ovirt.vm_start()
            ovirt.finish(
                changed=True,
                msg=u"VM {0:s} started".format(instance_name),
            )

    if state == 'cloud-init':
        ovirt.vm_cloud_init()
        ovirt.finish(
            changed=True,
            msg=u"VM {0:s} started".format(instance_name),
        )

    if state == 'shutdown':
        if initial_status == 'down':
            ovirt.finish(
                changed=False,
                msg=u"VM {0:s} is already shutdown".format(instance_name),
            )
        else:
            ovirt.vm_stop()
            ovirt.finish(
                changed=True,
                msg=u"VM {} is shutting down".format(instance_name),
            )

    if state == 'restart':
        if initial_status == 'up':
            ovirt.vm_restart()
            ovirt.finish(
                changed=True,
                msg=u"VM {0:s} is restarted".format(instance_name),
            )
        else:
            ovirt.vm_restart()
            ovirt.finish(
                changed=True,
                msg=u"VM {0:s} was started".format(instance_name),
            )

    if state == 'absent':
        if initial_status == 'does_not_exist':
            ovirt.finish(
                changed=False,
                msg=u"VM {0:s} does not exist".format(instance_name),
            )
        else:
            ovirt.vm_remove()
            ovirt.finish(
                changed=True,
                msg=u"VM {0:s} removed".format(instance_name),
            )

# import module snippets
from ansible.module_utils.basic import *

main()
