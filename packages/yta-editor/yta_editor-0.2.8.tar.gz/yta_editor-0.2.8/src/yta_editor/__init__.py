"""
Our awesome editor module in which we
have all the classes that interact with
it and make it possible.

An editor includes a single timeline,
built by tracks, in which we place media
elements and we are able to apply effects
to them.

Here is a brief explanation about the
hierarchy:

- The editor has a timeline.
- The timeline has audio and video tracks
(that can handle when we play or not the
audio and video).
- The tracks have parts, that are virtual
items to simplify the way we combine 
tracks. Those parts include media 
instances. The tracks have priorities
ones against the others.
- The media instances have a time range
in which they must be played within the
track (within the timeline). Those media
instances have the start and end time
range for the media source and can apply
effects to the frames.
- The media sources are just the way we
obtain the frames for the specific media
items (read a file, constant color, etc.).
"""

def main():
    from yta_editor.tests import video_modified_stored

    video_modified_stored()


if __name__ == '__main__':
    main()