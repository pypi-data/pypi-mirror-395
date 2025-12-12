def extract_event_data(inst, ID, frame):
    det = inst._detectors[ID]
    return det._frames[frame]
