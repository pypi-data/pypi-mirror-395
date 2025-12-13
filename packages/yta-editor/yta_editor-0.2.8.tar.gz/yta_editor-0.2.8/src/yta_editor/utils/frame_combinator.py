"""
TODO: I don't like the name nor the
location of this file, but it is here
to encapsulate some functionality 
related to combining video frames.

Module to contain methods that combine
video frames. Call them with the 2
frames you want to combine and you 
will get the combined frame as return.
"""
from av.audio.resampler import AudioResampler
from av.audio.frame import AudioFrame

import numpy as np


# TODO: There was a 'VideoFrameCombinator'
# class here, but it is now in
# 'yta_numpy.rgba.combinator'

class AudioFrameCombinator:
    """
    Class to wrap the functionality related
    to combine different audio frames.
    """

    @staticmethod
    def sum_tracks_frames(
        tracks_frames: list[AudioFrame],
        sample_rate: int = 44100,
        layout: str = 'stereo',
        format: str = 'fltp',
        do_normalize: bool = True
    ) -> AudioFrame:
        """
        Sum all the audio frames from the different
        tracks that are given in the 'tracks_frames'
        list (each column is a single audio frame of
        a track). This must be a list that should 
        come from a converted matrix that was
        representing each track in a row and the
        different audio frames for that track on each
        column.

        This method is to sum audio frames of one
        specific 't' time moment of a video.

        The output will be the sum of all the audio
        frames and it will be normalized to avoid
        distortion if 'do_normalize' is True (it is
        recommended).
        """
        if len(tracks_frames) == 0:
            raise Exception('The "tracks_frames" list of audio frames is empty.')
        
        arrays = []
        resampler: AudioResampler = AudioResampler(
            format = format,
            layout = layout,
            rate = sample_rate
        )

        for track_frame in tracks_frames:
            # Resample to output format
            # TODO: What if the resampler creates more
            # than one single frame? I don't know what
            # to do... I'll see when it happens
            print(track_frame)
            track_frame = resampler.resample(track_frame)
            
            if len(track_frame) > 1:
                print('[ ! ]   The resampler has given more than 1 frame...')

            track_frame_array = track_frame[0].to_ndarray()

            # Transform to 'float32' [-1, 1]
            # TODO: I think this is because the output
            # is 'fltp' but we have more combinations
            # so this must be refactored
            if track_frame_array.dtype == np.int16:
                track_frame_array = track_frame_array.astype(np.float32) / 32768.0
            elif track_frame_array.dtype != np.float32:
                track_frame_array = track_frame_array.astype(np.float32)

            # Mono to stereo if needed
            # TODO: What if source is 'stereo' and we
            # want mono (?)
            if (
                track_frame_array.shape[0] == 1 and
                layout == 'stereo'
            ):
                track_frame_array = np.repeat(track_frame_array, 2, axis = 0)

            arrays.append(track_frame_array)

        # Same length and fill with zeros if needed
        max_len = max(a.shape[1] for a in arrays)
        stacked = []
        for a in arrays:
            # TODO: Again, this 'float32' is because output
            # is 'fltp' I think...
            buf = np.zeros((a.shape[0], max_len), dtype = np.float32)
            buf[:, :a.shape[1]] = a
            stacked.append(buf)

        """
        All this below is interesting to avoid
        distortion or things like that, but it
        is actually making the volume decrease
        in these items we combine the frames,
        so we are facing a higher volume in the
        segments in which we have one single
        audio and different volumes when more
        than one are being played together...

        Thats why I have this code commented by
        now.
        """
        if False:
            # We attenuate the audios
            # attenuation_gain = 1.0 / math.sqrt(len(arrays))
            # arrays = [
            #     arr * attenuation_gain
            #     for arr in arrays
            # ]

            # Sum all the sounds
            mix = np.sum(stacked, axis = 0)

            # if do_normalize:
            #     # Avoid distortion and saturation
            #     mix /= len(stacked)

            # # Avoid clipping
            # mix = np.clip(mix, -1.0, 1.0)
        else:
            mix = np.sum(stacked, axis = 0)

        out = AudioFrame.from_ndarray(
            array = mix,
            format = format,
            layout = layout
        )
        out.sample_rate = sample_rate

        return out