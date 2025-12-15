import json

class JoltRequestBuilder:
    
    @staticmethod
    def auth(username: str, password: str) -> str:
        request = {
            "op": "auth",
            "user": username,
            "pass": password
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def subscribe(topic: str) -> str:
        request = {
            "op": "subscribe",
            "topic": topic
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def unsubscribe(topic: str) -> str:
        request = {
            "op": "unsubscribe",
            "topic": topic
        }
        return json.dumps(request) + "\n"
    
    @staticmethod
    def publish(topic: str, data: str) -> str:
        request = {
            "op": "publish",
            "topic": topic,
            "data": data
        }
        return json.dumps(request) + "\n"
        
    @staticmethod
    def ping() -> str:
        request = {"op": "ping"}
        return json.dumps(request) + "\n"