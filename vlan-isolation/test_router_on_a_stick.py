import subprocess
import pytest
from pathlib import Path
LAB_FILE = str(Path(__file__).resolve().parent / "router_on_a_stick.clab.yaml")
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
    container=(f"clab-router-on-a-stick-{node}")
    full= ["docker", "exec", container] + command.split()
    result = subprocess.run(full, capture_output=True, text=True)
    return result

def test_sales1_to_eng1():
    result=run("sales1","ping -c 3 192.168.20.10")
    assert result.returncode==0

def test_eng_to_sales():
    result=run("eng1","ping -c 3 192.168.10.10")
    assert result.returncode==0    

def test_router_sub_interfaceeth1_10():
    result=run("router","ip link show eth1.10")
    assert "eth1.10@eth1" in result.stdout

def test_router_sub_interfaceeth1_20():
    result=run("router","ip link show eth1.20")
    assert "eth1.20@eth1" in result.stdout

def test_switch1_router():
    result=run("sw1","bridge vlan show").stdout
    vlans = vlan_parser(result)
    assert vlans["eth3"] == [10, 20]

def test_switch2_pc():
    result=run("sw2","bridge vlan show").stdout
    vlans = vlan_parser(result)
    assert vlans["eth2"] == [20] 

def test_router_foreward_disable():
    try:
        disable_inter_vlan_routing = run("router", "sysctl -w net.ipv4.ip_forward=0")
        assert disable_inter_vlan_routing.returncode == 0
        ping_eng= run("sales1","ping -c 3 192.168.20.10")
        assert "100% packet loss" in ping_eng.stdout
        ping_sales= run("eng1","ping -c 3 192.168.10.10")
        assert "100% packet loss" in ping_sales.stdout
    finally:
        enable_inter_vlan_routing = run("router", "sysctl -w net.ipv4.ip_forward=1")
        assert enable_inter_vlan_routing.returncode == 0






def vlan_parser(result_vlan):
    vlan_list=result_vlan.strip().split("\n")[1:]
    port_dict={}
    current_port = None
    for i in vlan_list:
        fields = i.split()
        
        if fields[0].startswith("eth"):
            current_port=fields[0]
            port_dict[current_port] = [int(fields[1])]
            
        elif fields[0].isdigit():

           port_dict[current_port].append(int(fields[0]))
    return port_dict       

            
