"""
Manual tests that are working and are interesting
to learn about the code, refactor and build
classes.

TODO: Remove this class when finished and the
call from the '__init__.py' main file.
"""

IMAGE_FILENAME = 'test_files/mobile_alpha.png'
"""
Filename of an image that has transparency
and its size is 1280x720.
"""

def test_save_image_media():
    from yta_editor.media.video import VideoImageMedia
    from yta_editor.utils import VideoUtils

    output_filename = 'test_files/test_media_image.mov'

    # Transforming an image with alpha layer and
    # transparent pixels into a video with that
    # same transparency
    VideoImageMedia(
        filename = IMAGE_FILENAME,
        duration = 1.0
    ).save_as(
        output_filename = output_filename,
        video_pixel_format = 'argb',
        video_codec = 'qtrle'
    )

    print(VideoUtils.video.alpha.file_has_transparent_pixels(output_filename))

def timeline_to_render():
    from yta_editor.timeline import Timeline
    from yta_editor.media.video import VideoFileMedia, VideoImageMedia

    timeline = Timeline()

    VIDEO_PATH_60FPS = 'test_files/test_1.mp4'
    IMAGE_PATH = 'test_files/test_image_1920x1080.webp'

    video_60fps_1_5s = VideoFileMedia(
        filename = VIDEO_PATH_60FPS,
        t_start = 0.25,
        t_end = 1.75
    )
    video_60fps_1s = VideoFileMedia(
        filename = VIDEO_PATH_60FPS,
        t_start = 0.25,
        t_end = 1.25
    )
    clip_b = VideoImageMedia(
        filename = IMAGE_PATH,
        duration = 3,
        size = video_60fps_1_5s.size
    )

    track = timeline.tracks[0]

    track.add_video_item(
        # TODO: We always have to use a 'copy' of the media or
        # the changes we make on them will be applied to the
        # other instances, which is not what we want. We only
        # have to use the same 'source' for the different
        # medias that use it
        media = video_60fps_1s.copy,
        t = 0.33,
        do_force_add = True
    )

    track.add_video_item(
        # TODO: We always have to use a 'copy' of the media or
        # the changes we make on them will be applied to the
        # other instances, which is not what we want. We only
        # have to use the same 'source' for the different
        # medias that use it
        #media = clip_b.copy,
        media = video_60fps_1s.copy,
        t = 1,
        do_force_add = True
    )

    track.add_transition(
        item_in = track.get_item_at(0.4).item,
        item_out = track.get_item_at(1.4).item,
        mode = 'freeze_tail',
        duration = 0.5
    )

    timeline.render('test_files/timeline_to_render.mp4')

def video_modified_stored():
    timeline_to_render()

    return
    # TODO: Test a Timeline above this

    # test_opengl_transition()

    # return

    # test_transition()

    # return

    # test_save_image_media()

    # return

    # This path below was trimmed in an online platform
    # and seems to be bad codified and generates error
    # when processing it, but it is readable in the
    # file explorer...
    #VIDEO_PATH = 'test_files/test_1_short_broken.mp4'
    # This is short but is working well
    VIDEO_PATH = 'test_files/test_1_short_2.mp4'
    AUDIO_PATH = 'test_files/test_audio.mp3'
    # Long version below, comment to test faster
    #VIDEO_PATH = 'test_files/test_1.mp4'
    OUTPUT_PATH = 'test_files/output.mp4'
    # TODO: This has to be dynamic, but
    # according to what (?)
    NUMPY_FORMAT = 'rgb24'
    # TODO: Where do we obtain this from (?)
    VIDEO_CODEC_NAME = 'libx264'
    # TODO: Where do we obtain this from (?)
    PIXEL_FORMAT = 'yuv420p'

    from yta_editor.media.video import VideoFileMedia
    from yta_editor.media.audio import AudioFileMedia
    from yta_editor.timeline import Timeline

    # TODO: This test below is just to validate
    # that it is cropping and placing correctly
    # but the videos are only in one track
    # video = Video(VIDEO_PATH, 0.25, 0.75)
    # timeline = Timeline()
    # timeline.add_video(Video(VIDEO_PATH, 0.25, 1.0), 0.5)
    # # This is successfully raising an exception
    # #timeline.add_video(Video(VIDEO_PATH, 0.25, 0.75), 0.6)
    # timeline.add_video(Video(VIDEO_PATH, 0.25, 0.75), 1.75)
    # timeline.add_video(Video('C:/Users/dania/Downloads/Y2meta.app-TOP 12 SIMPLE LIQUID TRANSITION _ GREEN SCREEN TRANSITION PACK-(1080p60).mp4', 4.0, 5.0), 3)
    # # timeline.add_video(Video('C:/Users/dania/Downloads/Y2meta.app-10 Smooth Transitions Green Screen Template For Kinemaster, Alight Motion, Filmora, premiere pro-(1080p).mp4', 2.25, 3.0), 3)
    # timeline.render(OUTPUT_PATH)

    # # Testing concatenating
    # timeline = Timeline()
    # # When you concat like this, some of the
    # # videos have frames that cannot be accessed
    # # and I don't know why...
    # timeline.add_video(Video('test_files/glitch_rgb_frame.mp4'))
    # timeline.add_video(Video('test_files/output.mp4'))
    # timeline.add_video(Video('test_files/output_render.mp4'))
    # timeline.add_video(Video('test_files/strange_tv_frame.mp4'))
    # timeline.add_video(Video('test_files/test_1.mp4'))
    # timeline.add_video(Video('test_files/test_1_short_2.mp4'))
    # timeline.add_video(Video('test_files/test_audio_1st_track_solo_v0_0_15.mp4'))
    # timeline.add_video(Video('test_files/test_audio_2nd_track_solo_v0_0_15.mp4'))
    # timeline.add_video(Video('test_files/test_audio_combined_tracks_v0_0_015.mp4'))
    # timeline.add_video(Video('test_files/test_audio_combined_v0_0_15.mp4'))
    # timeline.add_video(Video('test_files/test_blend_add_v0_0_16.mp4'))
    # timeline.add_video(Video('test_files/test_blend_difference_v0_0_16.mp4'))
    # timeline.add_video(Video('test_files/test_blend_multiply_v0_0_16.mp4'))
    # timeline.add_video(Video('test_files/test_blend_overlay_v0_0_16.mp4'))
    # timeline.add_video(Video('test_files/test_blend_screen_v0_0_16.mp4'))
    # timeline.add_video(Video('test_files/test_combine_skipping_empty_using_priority_v0_0_18.mp4'))
    # timeline.add_video(Video('test_files/test_ok_v0_0_13.mp4'))

    # timeline.render('test_files/concatenated.mp4')

    # from yta_video_pyav.media import ImageMedia, ColorMedia

    # image_media = ImageMedia('test_files/mobile_alpha.png', 0, 1).save_as('test_files/test_image.mp4')

    # color_media = ColorMedia('random', 0, 1).save_as('test_files/test_color.mp4')

    # return

    # TODO: This test will add videos that
    # must be played at the same time

    # from yta_video_ffmpeg.handler import FfmpegHandler

    # ffmpeg_handler = FfmpegHandler()

    # # ffmpeg_handler.video.encoding.to_dnxhr(VIDEO_PATH, 'test_files/video_dnxhr.mov')
    # # ffmpeg_handler.video.encoding.to_prores(VIDEO_PATH, 'test_files/video_prores.mov')
    # # ffmpeg_handler.video.encoding.to_mjpeg(VIDEO_PATH, 'test_files/video_mjpeg.mov')

    # ffmpeg_handler.video.trim_fast(VIDEO_PATH, 0.25, 0.75, 'test_files/trimmed_fast.mp4')
    # ffmpeg_handler.video.trim_accurate(VIDEO_PATH, 0.25, 0.75, 'test_files/trimmed_accurate.mp4')
    # ffmpeg_handler.audio.trim_fast(AUDIO_PATH, 0.25, 1.75, 'test_files/trimmed_fast.mp3')
    # ffmpeg_handler.audio.trim_accurate(AUDIO_PATH, 0.25, 1.75, 'test_files/trimmed_accurate.mp3')

    # return


    # audio = Audio(AUDIO_PATH, 3, 6).save_as('test_files/output.mp3')

    # return

    # TODO: Testing overlaying with alpha layer

    # import av
    # for name in av.codecs_available:
    #     print(name)
    # exit()
    # import av
    # qtrle = av.codec.Codec('qtrle', 'r')  # 'r' = decode/read
    # print("is_decoder:", qtrle.is_decoder)
    # print("is_encoder:", qtrle.is_encoder)
    # print("type:", qtrle.type)
    # exit()

    # TODO: Transform non-alpha transition into
    # a alpha transition
    def non_alpha_transition_to_alpha_transition():
        from yta_video_pyav.writer import VideoWriter
        from yta_video_frame_time.t_fraction import get_ts

        video_alpha = VideoFileMedia('test_files/alpha_transition.mp4')

        writer = VideoWriter('test_files/alpha_transition.mov')
        # 'prores_ks' and 'yuva444p10le' write but not seen

        """
        To transform a non-alpha transition in 
        an alpha transition, use this:
        - codec: 'libvpx-vp9'
        - extension: '.webm'
        - pixel_format: 'yuva420p'
        """

        """
        'libvpx-vp9' and 'yuva420p' with '.webm'
        is written but even when the array has an
        alpha layer, the result is 'yuv420p' with
        the alpha metadata, but not including it.
        """

        """
        'qtrle' and 'argb' with '.mov' is working
        and writting the video correctly with the
        alpha layer, but then I cannot read it
        properly...
        """
        
        writer.set_video_stream(
            codec_name = 'qtrle', # video_alpha.codec_name, # 'libx264'
            fps = video_alpha.fps,
            size = video_alpha.size,
            pixel_format = 'argb'
        )

        # TODO: By now I'm omitting the audio
        # writer.set_audio_stream(
        #     codec_name = self.audio_codec,
        #     fps = self.audio_fps
        # )
        import numpy as np
        from av.video.frame import VideoFrame

        for t in get_ts(0, video_alpha.t_end, video_alpha.fps):
            frame = video_alpha.get_video_frame_at_t(t)

            # TODO: Why isn't this frame available if
            # I can see it in the original one (?)
            if frame is None:
                print(f'Frame at "t={str(t)}" is None (not available).')
                continue

            # To RGB
            rgb = frame.to_ndarray(format = 'rgb24')

            threshold = 30

            # Maximum brightness per pixel
            # brightness = np.max(rgb, axis=-1)  # valor más alto de R,G,B
            # mask = (brightness > threshold).astype(np.uint8) * 255
            # alpha = mask[..., None]

            # Pure black only
            # Create alpha: 0 when black, 255 when other
            # mask = np.any(rgb != [0, 0, 0], axis = -1).astype(np.uint8) * 255
            # alpha = mask[..., None]  # (H, W, 1)

            # With euclidean distance
            dist = np.linalg.norm(rgb.astype(np.int16), axis=-1)
            mask = (dist > threshold).astype(np.uint8) * 255
            alpha = mask[..., None]

            # To RGBA
            rgba = np.concatenate([rgb, alpha], axis = -1)

            # Create to write
            out_frame = VideoFrame.from_ndarray(rgba, format = 'rgba')
            #out_frame = out_frame.reformat(format = 'yuva420p')
            #out_frame.pict_type = 'NONE'

            # Codificar y muxear
            writer.mux_video_frame(
                frame = out_frame
            )

        writer.mux_video_frame(None)
        writer.output.close()

    #non_alpha_transition_to_alpha_transition()

    #return

    """
    Reading frames from .mov directly
    """
    # import av
    # import numpy as np

    # # Abrimos el archivo .mov con qtrle
    # container = av.open("test_files/alpha_transition.mov")

    # # Seleccionamos el primer stream de video
    # video_stream = container.streams.video[0]

    # for frame in container.decode(video_stream):
    #     # Forzamos conversión del frame a 'rgba'
    #     rgba_frame = frame.reformat(format="rgba")

    #     # Lo pasamos a un numpy array (H, W, 4)
    #     img = rgba_frame.to_ndarray()

    #     print(img.shape, img.dtype)  # Ej: (480, 640, 4) uint8

    # exit()

    # IMAGE_WITH_ALPHA = 'test_files/mobile_alpha.png'

    # from yta_editor.media.video import VideoImageMedia, VideoColorMedia

    # timeline = Timeline(
    #     video_codec = 'qtrle',
    #     video_pixel_format = 'argb'
    # )

    # #video_alpha = VideoFileMedia('test_files/alpha_transition_euclidean_distance_30.mov')
    # video_alpha = VideoImageMedia(IMAGE_WITH_ALPHA, 1, size = (1280, 720), do_include_alpha = True)
    # # I manually force the video_alpha size
    # # that has that size due to the image
    # #video_image = VideoImageMedia('test_files/background_1920_1080.jpg', 1, size = (1280, 720), do_include_alpha = True)
    # video_color = VideoColorMedia('notworkingyet', 1, size = (1280, 720), transparency = 0.1)

    # timeline.add_video(video_alpha, 0.2)
    # timeline.add_video(video_color, 0.0, 1)

    # timeline.render(OUTPUT_PATH.replace('.mp4', '.mov'), output_format = 'argb')

    # return

    def transition_to_alpha(
        filename: str,
        output_filename: str
    ):
        """
        Save the provided transition 'filename' file
        to a video file with the alpha layer.

        Perfect to download from AlphaPediaYT and
        transform into clips with alpha, using the
        chromakey, and using them as transitions.
        """
        from yta_video_pyav.reader.filter.dataclass import GraphFilters

        video = VideoFileMedia(
            filename = filename,
            video_filters = [
                GraphFilters.video.chromakey(
                    hex_color = '0x000000'
                )
            ]
        )

        video.save_as(
            output_filename = output_filename,
            video_size = video.size,
            video_fps = video.fps,
            #video_codec = video.codec_name, # that supports alpha
            video_codec = 'prores_ks',
            #video_pixel_format = video.pixel_format, # with alpha
            video_pixel_format = 'yuva444p10le',
            audio_codec = video.audio_codec_name,
            audio_sample_rate = video.audio_fps,
            audio_format = video.audio_format,
            audio_layout = video.audio_layout
        )

    # transition_to_alpha(
    #     filename = 'test_files/alpha_crocodile_transition.mp4',
    #     output_filename = 'test_files/alpha_transition_automated.mov'
    # )

    # return

    test_timeline_simpsons()

    return

    # Track 1
    timeline.add_video(Video(VIDEO_PATH, 0.25, 1.0), 0.75, track_index = 0)
    timeline.add_video(Video(simpsons_60fps, 1.5, 2.0), 3.0, track_index = 0)
    timeline.add_video(Video(VIDEO_PATH, 0.5, 1.0), 2.0, track_index = 0)

    #timeline.tracks[0].mute()

    # Track 2
    timeline.add_video(Video(VIDEO_PATH, 0.5, 1.0), 2.7, track_index = 1)
    timeline.add_video(Video(simpsons_60fps, 5.8, 7.8), 0.6, track_index = 1)
    # 30fps
    # timeline.add_video(Video('C:/Users/dania/Downloads/Y2meta.app-TOP 12 SIMPLE LIQUID TRANSITION _ GREEN SCREEN TRANSITION PACK-(1080p60).mp4', 0.25, 1.5), 0.25, do_use_second_track = True)
    # 29.97fps
    # timeline.add_video(Video('C:/Users/dania/Downloads/Y_una_porra_los_simpsons_castellano.mp4', 5.8, 6.8), 3.6, do_use_second_track = True)
    
    timeline.render(OUTPUT_PATH)

    return

    Video(VIDEO_PATH, 0.25, 0.75).save_as(OUTPUT_PATH)

    return