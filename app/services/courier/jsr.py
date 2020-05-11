# -*- coding: utf-8 -*-
# Json Master
import flask
import json
import os

class JsonMaster():
    def getJson(filename: str):
        with open(filename, "r") as file:
            return json.load(file)
    
    def htmlify(data: dict, activated: list = [], attr: dict = {}) -> dict:
        
        def recursive(data: dict, item) -> str:
            if item == "end": return ""
            html = ""
            if data[item]["tag"] is not None:
                html += f"<{data[item]['tag']} "
                for i in data[item]["attr"]:
                    html += f" {i}='{data[item][i]}' "
                html += ">"
                if data[item]["next"] != "end": html += recursive(data, data[item]["next"])
                html += f"</{data[item]['tag']}>"
            else:
                for i in data[item]["attr"]:
                    html += f"{data[item][i]} "
                    if data[item]["next"] != "end": html += recursive(data, data[item]["next"])
            return html
        
        def linear(data: dict, item) -> str:
            if item == "end": return ""
            html = ""
            for i in data[item]["attr"]:
                html += data[item][i]
            return html
        
        html = {}
        if not "queue" in data: return {}
        html["queue"] = data["queue"]
        html["signature"] = data["signature"]
        
        # activeted rebuild
        
        for item in activated:
            if item in data["activable"]:
                for block in data[item]["activated"]:
                    # print(block, "is activated")
                    data[item][block] = data[item]["activated"][block]
        # print(data)
        
        
        if data["method"] == "R": # recursive
            for item in data["queue"]:
                html[item] = recursive(data[item], data[item]["first"])
        
        elif data["method"] == "L": # linear
            for item in data["queue"]:
                html[item] = linear(data, item)
        
        elif data["method"] == "T": # file-template
            for item in data["queue"]:
                html[item] = flask.render_template(data[item], attr=attr)
            
        return html
    
    def htmlifyFile(filename, attr={}) -> dict:
        return JsonMaster.htmlify(
            JsonMaster.getJson(filename),
            (attr["activated"] if "activated" in attr else []),
            (attr["attr"] if "attr" in attr else {})
        )

if __name__ == "__main__":
    
    #print(os.listdir("../../../templates/json-templates"))
    print(JsonMaster.htmlifyFile("../../../templates/json-templates/user-bar.json", {} ))