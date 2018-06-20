from flask import Flask, request, jsonify
import pyshipping
from pyshipping.package import Package
from pyshipping.binpack_simple import binpack
import json
from flask_cors import CORS
from cubspack import newPacker

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def main():
    data = request.get_json()
    coord = data["data"]
    binsize = data["binsize"]
    packages = []
    # for coordict in coord:
    # 	packages.append(Package([coordict["h"], coordict["w"], coordict["d"]]))
    # binobject = Package([binsize["h"], binsize["w"], binsize["d"]])
    # solution = binpack(packages, binobject)
    for coordict in coord:
    	packages.append((coordict["w"], coordict["h"], coordict["d"], coordict["id"]))
    binobject = [([binsize["w"], binsize["h"], binsize["d"]])]*3
    packer = newPacker()
    for package in packages:
    	packer.add_cub(*package[:-1],rid=package[-1])
    for binobj in binobject:
    	packer.add_bin(*binobj)
    packer.pack()
    packed = packer.cub_list()
    solution = {"nobin": len(packer),"data":{}}
    for box in packed:
    	solution["data"][box[7]] = {
    	"bin": box[0],
    	"x": box[1]+0.5*box[4],
    	"y": box[2]+0.5*box[5],
    	"z": box[3]+0.5*box[6],
    	}
    print(solution)
    return jsonify(solution)


if __name__ == "__main__":
    app.run()
