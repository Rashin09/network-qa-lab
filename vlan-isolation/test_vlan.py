import subprocess
import pytest
from pathlib import Path
LAB_FILE = str(Path(__file__).resolve().parent / "vlan.clab.yml")

@pytest.fixture(autouse=True,scope="module")
def start_stop():
    containter_deploy_command=["sudo","containerlab","deploy","-t",LAB_FILE]           
    result=subprocess.run(containter_deploy_command,capture_output=True, text=True)
    if result.returncode !=0:
         pytest.fail(f"Lab Deployement Failed: {result.stderr} {result.stdout}")
    yield result
    containter_destroy_command=["sudo","containerlab","destroy","-t",LAB_FILE]
    result=subprocess.run(containter_destroy_command,capture_output=True, text=True)


def run(node, command):
    container=(f"clab-vlan-{node}")
    full= ["docker", "exec", container] + command.split()
    result = subprocess.run(full, capture_output=True, text=True)
    return result

def test_same_vlan_hosts_can_ping():
    result = run("sales1","ping -c 2 -W 2 10.0.0.3")
    assert result.returncode ==0

def test_different_vlan_hosts_cannot_ping():
    result = run("sales1","ping -c 2 -W 2 10.0.0.2")
    assert result.returncode !=0
    assert "100% packet loss" in result.stdout

def get_switch_vlan_text():
    result=run("sw1","bridge vlan show")
    return result.stdout

def parse_vlans(vlan_string):
    vlan_mapping={}
    for line in vlan_string.strip().split("\n"):
        part=line.split()
        port=part[0]
        vlan_id=part[1]
        if "eth" in part[0]:
            vlan_mapping[port]=int(vlan_id)

    return vlan_mapping


def test_switch_ports_are_in_expected_vlans():
    expected_vlans={'eth1': 10, 'eth2': 20, 'eth3': 10}
    assert expected_vlans==parse_vlans(get_switch_vlan_text())


    
    
    