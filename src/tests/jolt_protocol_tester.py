import socket
import json
import time

def test_protocol(host='127.0.0.1', port=8080):
    print("="*60)
    print("Jolt Protocol Tester")
    print("="*60)
    print(f"\nConnecting to {host}:{port}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((host, port))
        print("✓ Connected!\n")
        
        tests = [
            ("Test 1: op=ping", {"op": "ping"}),
            ("Test 2: command=ping", {"command": "ping"}),
            ("Test 3: command=ping", {"command": "ping"}),
            ("Test 4: action=ping", {"action": "ping"}),
            ("Test 5: op=sub with topic", {"op": "sub", "topic": "test"}),
            ("Test 6: command=sub with topic", {"command": "sub", "topic": "test"}),
            ("Test 7: op=subscribe with topic", {"op": "subscribe", "topic": "test"}),
            ("Test 8: command=subscribe with topic", {"command": "subscribe", "topic": "test"}),
        ]
        
        for test_name, data in tests:
            print(f"\n{test_name}")
            print(f"  Sending: {json.dumps(data)}")
            
            message = json.dumps(data) + "\n"
            sock.sendall(message.encode('utf-8'))
            
            time.sleep(0.2)
            sock.settimeout(1.0)
            try:
                response = sock.recv(4096).decode('utf-8').strip()
                if response:
                    print(f"  Response: {response}")
                    
                    try:
                        resp_data = json.loads(response)
                        if resp_data.get('ok') is True:
                            print(f"  ✓ SUCCESS! This format works!")
                        elif resp_data.get('ok') is False:
                            print(f"  ✗ Error: {resp_data.get('error', 'unknown')}")
                    except:
                        pass
                else:
                    print(f"  (no response)")
            except socket.timeout:
                print(f"  (timeout)")
            except Exception as e:
                print(f"  Error: {e}")
        
        print("\n" + "="*60)
        print("Testing complete!")
        print("="*60)
        
    except ConnectionRefusedError:
        print("✗ Connection refused - is the broker running?")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        sock.close()

if __name__ == '__main__':
    test_protocol()