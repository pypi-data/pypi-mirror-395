from django import dispatch

# Signal sent when presence changes in a room
# Arguments: room (Room instance), added (bool), removed (bool), bulk_change (bool)
presence_changed = dispatch.Signal()
