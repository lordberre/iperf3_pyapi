#!/usr/bin/env python3
# Version 0.01

import flask
import sys
import os
import json
from flask import Flask, request, jsonify
from uuid import UUID
import pprint
import iperf3
import time

app = flask.Flask(__name__)

# Enable verbose output
verbose = True

# Toggle validation of the json content
content_validation = True

# Do nothing but pretty print the JSON and quit
pretty_and_quit = False

# ...
iperf3_debug = True

# Create the UUID list
uuid_dict = {}

@app.route('/iperf3_api/<data>', methods=['GET', 'POST'])
def iperf3_api(data):
   dirpath = os.path.dirname(os.path.realpath(__file__))
   jsondefaultpath = os.path.join(dirpath, "/")
   jsonpath = sys.argv[1] if len(sys.argv) > 1 else jsondefaultpath
   content = request.json

# Check if the JSON is valid
   try:
      json_object = json.dumps(content)
   except ValueError:
      quit("Stopped processing due to error in JSON")

# Validate the UUID and store it for later use
   player_uuid = (content["uuid"]) 

   def validate_uuid(uuid_string):

      try:
         uuidcheck = UUID(uuid_string, version=4)
      except ValueError:
         return False
      return uuidcheck.hex == uuid_string.replace('-','')
   if validate_uuid(player_uuid):
      print("UUID is valid") if verbose else None

# Now save the uuid together with a timestamp so we can clean it up later
      if player_uuid in uuid_dict: # TODO
         quit("You already triggered a test recently, please wait a few more seconds")
      else:
         now = time.time()
         uuid_dict[player_uuid] = now
         print(player_uuid, "added to uuid dict:",(uuid_dict)) if verbose else None

   else:
      quit("Invalid UUID") 

# ...
   if pretty_and_quit:
      pprint.pprint(content)
      quit()

# Temp
   def return_error(values):
      return(print("stopped processing data due to error in:",values))

# Compare the UUID with what we know


# Parse iperf3 variables
   iperf3c = iperf3.Client()
   b00l = True
   iperf3c.port  = (content["iperf3_settings"]["port"])
   iperf3c.server_hostname = (content["iperf3_settings"]["ip"])
   iperf3c.reverse = (content["iperf3_settings"]["reverse"])
#iperf3c.ipversion = (content["iperf3_settings"]["ip_version"]) # Not supported in lib
   iperf3c.num_streams = (content["iperf3_settings"]["sessions"])
   iperf3c.duration = (content["iperf3_settings"]["duration"])
   init_in = (content["iperf3_settings"]["init"])

# Check if the data makes sense from what we just learned
   if content_validation:
      for ints in (iperf3c.port,iperf3c.num_streams,iperf3c.duration):
         return_error(ints) if not isinstance(ints, int) else print(ints,"check passed") if verbose else None
      for strings in (iperf3c.server_hostname):
         return_error(strings) if not isinstance(strings, str) else print(strings,"check passed") if verbose else None
         return_error(init_in) if init_in != 'start' else print("init var is OK") if verbose else None
      for bools in (iperf3c.reverse,b00l):
         return_error(bools) if not isinstance(bools, bool) else print(bools,"check passed") if verbose else None
   
   print('Connecting to {0}:{1}'.format(iperf3c.server_hostname, iperf3c.port))
   if init_in == 'start':
      result = iperf3c.run()
      if result.error:
         print(result.error)
         return result.error
               
      else:
         return result.text
         if verbose:
            print('')
            print('Test completed:')
            print('  started at         {0}'.format(result.time))
            print('  bytes transmitted  {0}'.format(result.sent_bytes))
            print('  retransmits        {0}'.format(result.retransmits))
            print('  avg cpu load       {0}%\n'.format(result.local_cpu_total))
            print('  MegaBytes per second (MB/s)  {0}'.format(result.sent_MB_s))

# Store general vars for later use
         remoteid = (content["cm_info"]["remoteid"])
         playerid = (content["cm_info"]["playerid"])
         cmts = (content["cm_info"]["cmts"])
         model = (content["cm_info"]["model"])

# Run the daemon
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8001, debug = True)

# Keep the uuid list  # TODO
