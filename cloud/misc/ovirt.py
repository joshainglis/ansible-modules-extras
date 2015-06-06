#!/usr/bin/env python

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
    - allows you to create new instances, either from scratch or an image, in addition to deleting or stopping instances on the oVirt/RHEV platform
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
    choices: ['present', 'absent', 'shutdown', 'started', 'restarted']
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
     - If not async, wait for the VM to provide its IP addresses before continuing (requires that VM image has "ovirt guest agent" installed)
    default: 'no'
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

TRIES = 0

# ------------------------------------------------------------------- #
# create connection with API
#
def connect(module):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :rtype: ovirtsdk.api.API
    """
    user = module.params['user']
    url = module.params['url']
    password = module.params['password']

    if not url.endswith('api'):
        url = '{}/api'.format(url.strip().rstrip('/'))

    try:
        api = API(url=url, username=user, password=password, insecure=True)
        api.test()
    except:
        module.fail_json(msg=u"Could not connect to server: {}".format(url))
    else:
        return api


def add_auth_key(key, user='root'):
    """
    :type key: str
    :type user: str
    :rtype : ovirtsdk.xml.params.Initialization
    """
    cloud_init = params.CloudInit(
        authorized_keys=params.AuthorizedKeys(
            authorized_key=[
                params.AuthorizedKey(
                    user=params.User(user_name=user),
                    key=key
                ),
            ]
        )
    )
    return params.Initialization(cloud_init=cloud_init)


def get_cloud_init(module):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :rtype: ovirtsdk.xml.params.Initialization
    """
    authorized_key_file = module.params['authorized_key_file']
    authorized_key_user = module.params['authorized_key_user']

    cloud_init = None
    if authorized_key_file:
        if os.path.isfile(authorized_key_file):
            try:
                with open(authorized_key_file, 'r') as f:
                    key = f.read()
            except IOError:
                module.fail_json(msg=u"Could not read the given authorized_key_file at {}".format(authorized_key_file))
            else:
                cloud_init = add_auth_key(key, authorized_key_user)
        else:
            module.fail_json(
                msg=(u"The provided authorized_key_file is not a file. "
                     u"Please specify the absolute path to the .pub key file")
            )
    return cloud_init


def add_tags(module, conn):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    tags = module.params['tags']

    if tags:
        new_tags = set([tag.strip().lower() for tag in tags.strip().replace(" ", "_").split(',')])

        try:
            existing_tags = set([tag.get_name() for tag in conn.tags.list()])
        except Exception:
            module.fail_json(msg=u"Could not get existing tags from server")
        else:
            tags_to_add = []
            for tag in new_tags:
                if tag in existing_tags:
                    tags_to_add.append(conn.tags.get(name=tag))
                else:
                    try:
                        tags_to_add.append(conn.tags.add(params.Tag(name=tag)))
                    except:
                        module.fail_json(msg=u"Failed to add tag to ovirt")
            return params.Tags(tag=tags_to_add)


def recurse(module, conn, func):
    """
    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    :type func: (ansible.module_utils.basic.AnsibleModule, ovirtsdk.api.API) -> bool
    """
    global TRIES
    poll_frequency = float(module.params['poll_frequency'])

    time.sleep(poll_frequency)
    TRIES -= 1
    return func(module, conn)


# noinspection PyUnboundLocalVariable,PyBroadException
def create_vm(module, conn):
    """
    Create a VM instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """

    instance_name = module.params['instance_name']
    zone = module.params['zone']
    instance_disksize = module.params['instance_disksize']
    instance_nic = module.params['instance_nic']
    instance_network = module.params['instance_network']
    instance_mem = module.params['instance_mem']
    disk_alloc = module.params['disk_alloc']
    disk_int = module.params['disk_int']
    instance_os = module.params['instance_os']
    instance_type = module.params['instance_type']
    instance_cores = module.params['instance_cores']
    sdomain = module.params['sdomain']

    if disk_alloc == 'thin':
        vmparams = params.VM(
            name=instance_name,
            cluster=conn.clusters.get(name=zone),
            os=params.OperatingSystem(type_=instance_os),
            template=conn.templates.get(name="Blank"),
            memory=1024 * 1024 * int(instance_mem),
            cpu=params.CPU(topology=params.CpuTopology(cores=int(instance_cores))),
            type_=instance_type,
            initialization=get_cloud_init(module),
            tags=add_tags(module, conn)
        )
        vmdisk = params.Disk(
            size=1024 * 1024 * 1024 * int(instance_disksize),
            wipe_after_delete=True,
            sparse=True,
            interface=disk_int,
            type_="System",
            format='cow',
            storage_domains=params.StorageDomains(storage_domain=[conn.storagedomains.get(name=sdomain)]),
        )
        network_net = params.Network(name=instance_network)
        nic_net1 = params.NIC(name='nic1', network=network_net, interface='virtio')
    elif disk_alloc == 'preallocated':
        vmparams = params.VM(
            name=instance_name,
            cluster=conn.clusters.get(name=zone),
            os=params.OperatingSystem(type_=instance_os),
            template=conn.templates.get(name="Blank"),
            memory=1024 * 1024 * int(instance_mem),
            cpu=params.CPU(topology=params.CpuTopology(cores=int(instance_cores))),
            type_=instance_type,
            initialization=get_cloud_init(module),
            tags=add_tags(module, conn)
        )
        vmdisk = params.Disk(
            size=1024 * 1024 * 1024 * int(instance_disksize),
            wipe_after_delete=True,
            sparse=False,
            interface=disk_int,
            type_="System",
            format='raw',
            storage_domains=params.StorageDomains(storage_domain=[conn.storagedomains.get(name=sdomain)])
        )
        network_net = params.Network(name=instance_network)
        nic_net1 = params.NIC(name=instance_nic, network=network_net, interface='virtio')
    else:
        module.fail_json(msg=u"Invalid value for 'disk_alloc': {}".format(disk_alloc))

    try:
        conn.vms.add(vmparams)
    except:
        module.fail_json(msg=u"Error creating VM with specified parameters")
    vm = conn.vms.get(name=instance_name)
    try:
        vm.disks.add(vmdisk)
    except:
        vm_remove(module, conn)
        module.fail_json(msg=u"Error attaching disk")
    try:
        vm.nics.add(nic_net1)
    except:
        vm_remove(module, conn)
        module.fail_json(msg=u"Error adding nic")


def create_vm_template(module, conn):
    """
    Create an instance from a template

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    instance_name = module.params['instance_name']
    zone = module.params['zone']
    image = module.params['image']

    vmparams = params.VM(
        name=instance_name,
        cluster=conn.clusters.get(name=zone),
        template=conn.templates.get(name=image),
        disks=params.Disks(clone=True),
        initialization=get_cloud_init(module),
        tags=add_tags(module, conn)
    )
    conn.vms.add(vmparams)


def get_ips(module, conn):
    """
    get ip addresses from instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    :rtype: list[str]
    """
    instance_name = module.params['instance_name']

    try:
        ips = [ip.get_address() for ip in conn.vms.get(name=instance_name).get_guest_info().get_ips().get_ip()]
    except AttributeError:
        ips = []
    return ips



def vm_start(module, conn):
    """
    start instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    global TRIES
    instance_name = module.params['instance_name']
    async = module.boolean(module.params['async'])
    wait_for_ip = module.boolean(module.params['wait_for_ip'])

    state = vm_status(module, conn)

    if TRIES <= 0:
        module.fail_json(msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state))
    if state == 'does_not_exist':
        module.fail_json(msg=u"Cannot stop {} as it does not appear to exist on the server".format(instance_name))
    elif state == 'unknown':
        module.fail_json(msg=u"{} is in an unknown state.".format(instance_name))
    elif state in ['creating', 'starting', 'stopping']:
        return recurse(module, conn, vm_start)
    elif state == 'down':
        vm = conn.vms.get(name=instance_name)
        vm.start()
        if not async:
            return recurse(module, conn, vm_start)
    elif state == 'up':
        if wait_for_ip:
            ips = get_ips(module, conn)
            if not ips:
                return recurse(module, conn, vm_start)


def vm_stop(module, conn):
    """
    Stop instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    global TRIES
    instance_name = module.params['instance_name']
    async = module.boolean(module.params['async'])

    vm = conn.vms.get(name=instance_name)
    state = vm_status(module, conn)

    if TRIES <= 0:
        module.fail_json(msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state))
    if state == 'does_not_exist':
        module.fail_json(msg=u"Cannot stop {} as it does not appear to exist on the server".format(instance_name))
    elif state == 'unknown':
        module.fail_json(msg=u"{} is in an unknown state.".format(instance_name))
    elif state in ['creating', 'starting', 'stopping']:
        return recurse(module, conn, vm_stop)
    elif state == 'up':
        vm.stop()
        if not async:
            return recurse(module, conn, vm_stop)
    elif state == 'down':
        return True



def vm_restart(module, conn):
    """
    restart instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    stopped = vm_stop(module, conn)
    started = vm_start(module, conn)
    return stopped and started


def vm_remove(module, conn):
    """
    remove an instance

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    global TRIES
    instance_name = module.params['instance_name']
    async = module.boolean(module.params['async'])

    vm = conn.vms.get(name=instance_name)
    state = vm_status(module, conn)

    if TRIES <= 0:
        module.fail_json(msg=u"Ran out of poll_tries. {} is currently in state: '{}'".format(instance_name, state))
    if state == 'does_not_exist':
        return True
    elif state == 'unknown':
        vm.delete()
        return True if async else recurse(module, conn, vm_remove)
    elif state in ['creating', 'starting', 'stopping']:
        return recurse(module, conn, vm_remove)
    elif state == 'up':
        vm_stop(module, conn)
        return recurse(module, conn, vm_remove)
    elif state == 'down':
        vm.delete()
        return True if async else recurse(module, conn, vm_remove)


def vm_status(module, conn):
    """
    Get the VMs status

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    instance_name = module.params['instance_name']

    if instance_name not in set([vm.get_name() for vm in conn.vms.list()]):
        status = 'does_not_exist'
    else:
        status = OVIRT_STATE_MAP.get(conn.vms.get(name=instance_name).get_status().get_state(), 'unknown')
    return status


def get_vm(module, conn):
    """
    Get VM object and return it's name if object exists

    :type module: ansible.module_utils.basic.AnsibleModule
    :type conn: ovirtsdk.api.API
    """
    instance_name = module.params['instance_name']
    vm = conn.vms.get(name=instance_name)

    return "empty" if vm is None else vm.get_name()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                type='str',
                default='present',
                choices=['present', 'absent', 'shutdown', 'started', 'restart']
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
        ),
    )

    if not HAS_LIB:
        module.fail_json(msg=u'ovirtsdk required for this module')

    state = module.params['state']
    instance_name = module.params['instance_name']
    image = module.params['image']
    resource_type = module.params['resource_type']

    global TRIES
    TRIES = int(module.params['poll_tries'])

    # initialize connection
    try:
        connection = connect(module)
    except:
        module.fail_json(msg=u"error connecting to the oVirt API")
    else:
        initial_status = vm_status(module, connection)

        def instantiate():
            if resource_type == 'template':
                try:
                    create_vm_template(module, connection)
                except:
                    module.fail_json(msg=u'error adding template {}'.format(image))
            elif resource_type == 'new':
                try:
                    create_vm(module, connection)
                except:
                    module.fail_json(u"Failed to create VM: {}".format(instance_name))
            else:
                module.fail_json(msg=u"You did not specify a resource type")

        if state == 'present':
            if initial_status == "does_not_exist":
                instantiate()
                if resource_type == 'template':
                    module.exit_json(
                        changed=True,
                        msg=u"deployed VM {} from template {}".format(instance_name, image),
                        ips=get_ips(module, connection)
                    )
                elif resource_type == 'new':
                    module.exit_json(
                        changed=True,
                        msg=u"deployed VM {} from scratch".format(instance_name),
                        ips=get_ips(module, connection)
                    )
            else:
                module.exit_json(
                    changed=False,
                    msg=u"VM {} already exists".format(instance_name),
                    ips=get_ips(module, connection)
                )

        if state == 'started':
            if initial_status == 'up':
                module.exit_json(
                    changed=False,
                    msg=u"VM {} is already running".format(instance_name),
                    ips=get_ips(module, connection)
                )
            else:
                if initial_status == 'does_not_exist':
                    instantiate()
                vm_start(module, connection)
                module.exit_json(
                    changed=True,
                    msg=u"VM {0:s} started".format(instance_name),
                    ips=get_ips(module, connection)
                )

        if state == 'shutdown':
            if initial_status == 'down':
                module.exit_json(
                    changed=False,
                    msg=u"VM {0:s} is already shutdown".format(instance_name),
                    ips=get_ips(module, connection)
                )
            else:
                if initial_status == 'does_not_exist':
                    instantiate()
                vm_stop(module, connection)
                module.exit_json(
                    changed=True,
                    msg=u"VM {} is shutting down".format(instance_name),
                    ips=get_ips(module, connection)
                )

        if state == 'restart':
            if initial_status == 'up':
                vm_restart(module, connection)
                module.exit_json(
                    changed=True,
                    msg=u"VM {0:s} is restarted".format(instance_name),
                    ips=get_ips(module, connection)
                )
            else:
                if initial_status == 'does_not_exist':
                    instantiate()
                vm_restart(module, connection)
                module.exit_json(
                    changed=True,
                    msg=u"VM {0:s} was started".format(instance_name),
                    ips=get_ips(module, connection)
                )

        if state == 'absent':
            if initial_status == 'does_not_exist':
                module.exit_json(
                    changed=False,
                    msg=u"VM {0:s} does not exist".format(instance_name),
                    ips=[]
                )
            else:
                vm_remove(module, connection)
                module.exit_json(
                    changed=True,
                    msg=u"VM {0:s} removed".format(instance_name),
                    ips=[]
                )

# import module snippets
from ansible.module_utils.basic import *

main()
