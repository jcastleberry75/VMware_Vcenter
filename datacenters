import atexit
import requests
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
import logging
import platform
import subprocess
import re

if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()


def custom_logger(log_file_name):
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(logging.DEBUG)
    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers

    extra_fields = {'thread_id': 'THREAD-ID:',
                    'function_name': 'FUNCTION:'}
    formatter = logging.Formatter('%(asctime)s'
                                  ' [%(levelname)s]'
                                  ' %(processName)s'
                                  ' %(process)s'
                                  ' (%(threadName)s)'
                                  ' %(thread_id)s'
                                  ' %(thread)d'
                                  ' %(function_name)s'                                  
                                  ' %(funcName)s'
                                  ' %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    l = logging.LoggerAdapter(logger, extra_fields)
    return l


logger = custom_logger("pyvmomi_client.log")
logger.info("""PROGRAM START""")


def error_handler(error):
    """
    Handles KeyErrors and
    :param error: error that has been raised
    :return: str
    """
    error_msg = str(error)
    logger.error("The following error has occured")
    logger.error(error_msg)
    logger.error("The ITAM record will not be created.")
    support_contact = """Please contact Jay Castleberry for assistance"""
    logger.error(support_contact)


# Determine platform operating system
op_system = platform.system().lower()
logger.info(f"""Operating System: {op_system}""")


def ping_parser(s, o):
    """

    :param s: string to parse
    :param o: operating system
    :return: str
    """
    patterns = ["[[].+[]]", "[(].+[)]"]
    search_pattern = patterns[0] if o == 'windows' else patterns[1]
    if o == 'windows':
        parse_result = re.search(search_pattern, s).group(0).split(" ")[0].replace("[", "").replace("]", "")
    else:
        parse_result = re.search(search_pattern, s).group(0).split(" ")[0].replace("(", "").replace(")", "")
    return parse_result


def shell_command(command):
    """
    Sends shell command
    :param command: The cli command to send
    :return: decoded strings for display
    """
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as p:
        logger.info(f"""Executing shell command: {command}""")
        shell_rsp = p.stdout.read()
        decode_rsp = shell_rsp.decode()
        (str(decode_rsp))
        logger.info(decode_rsp)
        return decode_rsp


def ping(host):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    ping_command = f"""ping {param} 1 {host}"""
    rsp = shell_command(ping_command)
    ip_result = ping_parser(rsp, op_system)
    return ip_result


def get_ip_addresses():
    vcenter_names = ["foo", "foo2"]

    logger.info(f""""Vcenter list: {vcenter_names}""")

    vcenter_ips = {}
    logger.info("*** BEGIN VCENTER PINGS ***")
    for v in vcenter_names:
        try:
            vcenter_name = v
            vcenter_ip = ping(v)
            logger.info(f"""Obtained IP Address for {v}: {vcenter_ip}""")
            vcenter_ips[vcenter_name] = vcenter_ip

        except (OSError, SystemError, Exception) as err:
            error_handler(err)

    logger.info("*** END VCENTER PINGS ***")
    logger.info(f"""Vcenter Ping Results: {vcenter_ips}""")
    return vcenter_ips

vcenters = get_ip_addresses()
logger.info(f"""Discovered Vcenter IPs : {vcenters}""")


def get_obj(content, vim_type, name=None):
    container = content.viewManager.CreateContainerView(content.rootFolder, vim_type, True)
    if name:
        for c in container.view:
            if c.name == name:
                obj = c
                return [obj]
    else:
        return container.view


def sizeof_fmt(num):
    """
    Returns the human readable version of a file size
    :param num:
    :return:
    """
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def generate_datastore_info(ds_obj, v, i):
    summary = ds_obj.summary
    clean_name = summary.name.replace(" ", "")
    ds_capacity = summary.capacity
    ds_freespace = summary.freeSpace
    ds_uncommitted = summary.uncommitted if summary.uncommitted else 0
    ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
    vcenter_name = v
    vcenter_ip = i
    datastore_name = clean_name
    # datastore_capacity = sizeof_fmt(summary.capacity)
    # datastore_provisioned = sizeof_fmt(ds_provisioned)
    # datastore_freespace = sizeof_fmt(summary.freeSpace)
    datastore_capacity = summary.capacity
    datastore_provisioned = ds_provisioned
    datastore_freespace = summary.freeSpace
    data = [vcenter_name, vcenter_ip, datastore_name, datastore_capacity, datastore_provisioned, datastore_freespace]
    return data


def get_storage_data(vcenter_name, ip):
    u_name = r"NAME"
    u_pass = r"PASS"
    si = SmartConnectNoSSL(
        host=ip,
        user=u_name,
        pwd=u_pass,
        port=443
        )
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    # Get list of ds mo
    ds_obj_list = get_obj(content, [vim.Datastore])
    data = []
    for ds in ds_obj_list:
        d = generate_datastore_info(ds, vcenter_name, ip)
        # logger.info(d)
        data.append(d)
    return data

for k, v in vcenters.items():
    vc_name = k
    # logger.info(f"""Getting data for {k}, {v}""")
    vcenter_storage_data = get_storage_data(k, v)
    print(f"Data for {vc_name} ")
    print(vcenter_storage_data)
