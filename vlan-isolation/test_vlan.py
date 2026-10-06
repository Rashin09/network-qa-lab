import subprocess

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
parse_vlans(get_switch_vlan_text())

def test_switch_ports_are_in_expected_vlans():
    expected_vlans={'eth1': 10, 'eth2': 20, 'eth3': 10}
    assert expected_vlans==parse_vlans(get_switch_vlan_text())


    
    
    