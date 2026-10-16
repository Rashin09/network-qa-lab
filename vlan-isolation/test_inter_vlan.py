import pytest
import subprocess
from pathlib import Path
LAB_FILE = str(Path(__file__).resolve().parent / "inter_vlan.clab.yaml")
@pytest.fixture(autouse=True,scope="module")
def start_stop():
    containter_deploy_command=["sudo","containerlab","deploy","-t",LAB_FILE]           
    result=subprocess.run(containter_deploy_command,capture_output=True, text=True)
    if result.returncode !=0:
         pytest.fail(f"Lab Deployment Failed: {result.stderr}\n{result.stdout}")
    yield result
    containter_destroy_command=["sudo","containerlab","destroy","-t",LAB_FILE]
    result=subprocess.run(containter_destroy_command,capture_output=True, text=True)

def run(node,command):
    container=(f"clab-inter-vlan-{node}")
    full_command= ["docker", "exec",container]+command.split()
    result=subprocess.run(full_command, capture_output=True, text=True)
    return result

def test_ping_sales1_eng1():
    result=run("sales1","ping -c 2 -W 2 192.168.20.10")
    assert result.returncode == 0

def test_ping_eng1_sales1():
    result=run("eng1","ping -c 2 -W 2 192.168.10.10")
    assert result.returncode == 0


def test_inter_vlan_route():
    try :
        disable_vlan_routing=run("router", "sysctl -w net.ipv4.ip_forward=0")
        assert disable_vlan_routing.returncode==0 , disable_vlan_routing.stderr
        result1=run("sales1","ping -c 2 -W 2 192.168.20.10")
        result2=run("eng1","ping -c 2 -W 2 192.168.10.10")
        assert result1.returncode != 0
        assert result2.returncode != 0
    finally:    
        enable_vlan_routing=run("router", "sysctl -w net.ipv4.ip_forward=1")
        assert enable_vlan_routing.returncode ==0 , disable_vlan_routing.stderr




     
         