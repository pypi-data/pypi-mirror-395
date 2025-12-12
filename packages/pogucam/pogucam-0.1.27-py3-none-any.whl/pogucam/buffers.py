
import numpy as np
# ================================================================================
# jsut store uint +info
# --------------------------------------------------------------------------------

class FastAccumBuffer:
    def __init__(self, max_frames, shape=(640, 480, 3)):
        self.max_frames = max_frames
        self.shape = shape
        self._init_buffer()
        self._last_retrieved_idx = -1 #???
        self.previous_sum_frames = None
        #self._saturated_pixel_count = 0
        self._saturated_pixel_count = np.zeros(3, dtype=int)

    def _init_buffer(self):
        self.cube = np.empty((self.max_frames, *self.shape), dtype=np.uint8)
        self.info = [None] * self.max_frames
        self.idx = 0
        self.count = 0
        self._last_retrieved_idx = -1 #???
        self.previous_sum_frames = None
        #self._saturated_pixel_count = 0
        self._saturated_pixel_count = np.zeros(3, dtype=int)

    def add(self, img: np.ndarray, info: dict):
        """
        inconsistent shapes reset the buffer
        """
        if img.dtype != np.uint8 or img.shape != self.shape:
            self.shape = img.shape
            self._init_buffer()
        if self.cube.shape[0] != self.max_frames:
            self._init_buffer()
        self.cube[self.idx] = img
        self.info[self.idx] = info
        self.idx = (self.idx + 1) % self.max_frames
        self.count = min(self.count + 1, self.max_frames)

    def get_last_img(self):
        if self.count == 0:
            return None
        last_idx = (self.idx - 1) % self.max_frames
        return self.cube[last_idx]

    def new_sum_available(self):
        return self.idx == self.max_frames - 1
        # True if buffer has wrapped around since last sum_images() call
        if self.count < self.max_frames:
            return False
        return self.idx != self._last_retrieved_idx # ???

    def get_previous_sum_frames(self):
        #print("i... prev buffers")
        return self.previous_sum_frames

    def get_sum_frames(self):
        if self.count == 0:
            self._saturated_pixel_count = 0
            return None
        #print("!... SUM")
        summed = np.sum(self.cube[:self.count].astype(np.uint16), axis=0)
        saturated_mask = summed > 255#
        #Count saturation per channel
        self._saturated_pixel_count = np.array([
            np.count_nonzero(saturated_mask[:, :, c]) for c in range(3)
        ])
        #self._saturated_pixel_count = np.count_nonzero(saturated_mask)
        np.clip(summed, 0, 255, out=summed)
        self._last_retrieved_idx = self.idx # ???
        #prev = self.previous_sum_frames
        curr = summed.astype(np.uint8)
        self.previous_sum_frames = curr
        return curr# summed.astype(np.uint8)

    def get_avg_frames(self):
        """
        untested averaged frame
        """
        if self.count == 0:
            return None
        avg = np.mean(self.cube[:self.count].astype(np.float32), axis=0)
        avg = np.clip(avg, 0, 255).astype(np.uint8)
        self.previous_sum_frames = avg
        return avg



    def get_saturated_pixel_count(self):
        return self._saturated_pixel_count

    def get_max_frames(self):
        return self.max_frames

    def set_max_frames(self, max_frames):
        """
        reset the buffer
        """
        if max_frames != self.max_frames:
            self.max_frames = max_frames
            self._init_buffer()

    def __iter__(self):
        """
        returns image,info_dict
        """
        for i in range(self.count):
            yield self.cube[(self.idx - self.count + i) % self.max_frames], self.info[(self.idx - self.count + i) % self.max_frames]

    def __len__(self):
        return self.count




# ==========================================================================================
#  CLASS     SLOW  level 2  - averaging buffer.....
# ------------------------------------------------------------------------------------------


class AccumBuffer:
    def __init__(self, frame=None, img_dtype=np.uint8):
        self.frame = frame
        self.img = type('img', (), {'dtype': img_dtype})()
        self.accum_buffer_size = 0
        self.accum_buffer = []
        self.accum_count = 0
        self.accum_index = 0
        self.running_sum = None

    def is_accum_index_at_end(self):
        return self.accum_index >= self.accum_buffer_size - 1

    def get_current_size(self):
        return self.accum_count

    def get_max_buffer_size(self):
        return self.accum_buffer_size

    def clear_buffer(self, some_frame):
        self.accum_buffer = np.zeros((self.accum_buffer_size, *some_frame.shape), dtype=self.img.dtype)
        self.accum_count = 0
        self.accum_index = 0
        self.running_sum = np.zeros(some_frame.shape, dtype=np.float64)

    def get_frame_shape(self):
        if self.frame is not None:
            return self.frame.shape
        else:
            return None

    def define_accum_buffer(self, n):
        if self.frame is None:
            return False
        if (n == self.accum_buffer_size) and (len(self.accum_buffer) > 1):
            return True
        self.accum_buffer_size = n
        self.accum_buffer = np.zeros((self.accum_buffer_size, *self.frame.shape), dtype=self.img.dtype)
        self.accum_count = 0
        self.accum_index = 0
        self.running_sum = np.zeros(self.frame.shape, dtype=np.float64)
        return True

    def add_to_accum_buffer(self, frame):
        if len(self.accum_buffer) < 1:
            return False
        if self.accum_count < self.accum_buffer_size:
            self.running_sum += frame
            self.accum_buffer[self.accum_index] = frame
            self.accum_count += 1
        else:
            oldest_frame = self.accum_buffer[self.accum_index]
            if frame.shape != oldest_frame.shape:
                return False
            self.running_sum += frame.astype(np.float64) - oldest_frame.astype(np.float64)
            self.accum_buffer[self.accum_index] = frame
        self.accum_index = (self.accum_index + 1) % self.accum_buffer_size
        return True

    def get_mean_accum_buffer(self):
        if self.accum_count == 0:
            return None
        rimg = self.running_sum / self.accum_count
        return rimg.astype(np.uint8)

    def order_accum_buffer_frames(self):
        if self.accum_count < self.accum_buffer_size:
            frames_ordered = self.accum_buffer[:self.accum_count]
        else:
            frames_ordered = np.concatenate((self.accum_buffer[self.accum_index:], self.accum_buffer[:self.accum_index]))
        for frame in frames_ordered:
            yield frame
