import json

class JoltRequestBuilder:
    
    @staticmethod
    def auth(username: str, password: str) -> str:
        request = {
            "command": "auth",
            "user": username,
            "pass": password
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def subscribe(topic: str) -> str:
        request = {
            "command": "sub",
            "topic": topic
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def unsubscribe(topic: str) -> str:
        request = {
            "command": "unsub",
            "topic": topic
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def publish(topic: str, data: str) -> str:
        request = {
            "command": "pub",
            "topic": topic,
            "data": data
        }
        return json.dumps(request) + "\n"
        
    @staticmethod
    def ping() -> str:
        request = {"command": "ping"}
        return json.dumps(request) + "\n"