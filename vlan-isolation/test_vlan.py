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