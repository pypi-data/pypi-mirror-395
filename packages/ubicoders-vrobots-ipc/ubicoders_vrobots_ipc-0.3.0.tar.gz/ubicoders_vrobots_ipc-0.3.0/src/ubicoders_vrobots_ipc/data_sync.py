class DataSynchronizer:
    def __init__(self, camera_keys):
        self.camera_keys = camera_keys
        self.state_buffer = []
        self.pending_images = {key: None for key in camera_keys}
        self.synced_data = None

    def watch(self, state, new_images):
        if state:
            self.state_buffer.append(state)
        
        for key, img in new_images.items():
            if img is not None and key in self.pending_images:
                self.pending_images[key] = img
        
        # Check if all images are present
        if all(self.pending_images[k] is not None for k in self.camera_keys):
            # Check timestamps
            first_ts = self.pending_images[self.camera_keys[0]].ts
            all_match = True
            for k in self.camera_keys[1:]:
                if abs(self.pending_images[k].ts - first_ts) > 1e-6:
                    all_match = False
                    break
            
            if all_match:
                # Find matching state
                matched_state = None
                found_idx = -1
                for i, s in enumerate(self.state_buffer):
                    if abs(s.timestamp - first_ts) < 1e-6:
                        matched_state = s
                        found_idx = i
                        break
                
                if matched_state:
                    img_data = {k: self.pending_images[k].image_data for k in self.camera_keys}
                    self.synced_data = (matched_state, img_data)
                    
                    # Clean up buffer
                    self.state_buffer = self.state_buffer[found_idx+1:]
                    # Clear pending images
                    for k in self.camera_keys:
                        self.pending_images[k] = None

    def match(self):
        return self.synced_data is not None

    def get_data(self):
        data = self.synced_data
        self.synced_data = None
        return data