
from yta_editor.tracks.items.gap import GapTrackItem
from yta_editor.tracks.items.transition import TransitionMode, TransitionTrackItem
from yta_video_frame_time.t_fraction import check_values_are_same
from yta_time_interval import TIME_INTERVAL_SYSTEM_LIMITS
from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from quicktions import Fraction
from typing import Union
from abc import ABC
from dataclasses import dataclass

import bisect


TrackItemType = Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem']
"""
The type that includes all the specific track item
types we can handle.
"""

@dataclass
class _TrackItemFound:
    """
    Dataclass just to hold the items we found in the
    items list, including the item but also the index.

    This dataclass is not for being stored within the
    `_TrackItems` list but to be returned when looking
    for specific items in the list.
    """

    def __init__(
        self,
        item: TrackItemType,
        index: int
    ):
        self.item: TrackItemType = item
        """
        The item found.
        """
        self.index: int = index
        """
        The index of the item found in the `items` list.
        """

@dataclass
class _TrackItems:
    """
    The list of items that exist in the track.

    This class will implement optimized ways of looking
    for items based on the time moments they have. The
    items inside will be always ordered by the `t_start`
    time moment.
    """

    @property
    def is_empty(
        self
    ) -> bool:
        """
        Boolean flag that indicates if the list is empty or
        not.
        """
        return len(self.items) == 0

    def __init__(
        self,
        track: Union['VideoTrack', 'AudioTrack']
    ):
        self.items: list[TrackItemType] = []
        """
        The list of items, that will be always initialized
        with a gap that lasts the whole duration.
        """
        # TODO: I don't know exactly how to handle this... What
        # if one of the items provided later doesn't belong to
        # this track (?)
        self._track: Union['VideoTrack', 'AudioTrack'] = track
        """
        The track of these items belong to.
        """

        self._fullfil_if_empty()

    """
    Internal but necessary and very important methods below.
    """

    def _recalculate_all(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        This method should be called when we add or remove
        any item from the track, so the track remains
        consistent, with the items ordered and with
        everything valid inside.
        """
        print('[OK] Ordering items')
        self._order_items()
        print('[OK] Relinking items')
        self._relink_items()
        print('[OK] Rebuilding gaps')
        self._rebuild_gaps()
        print('[OK] Merging consecutive gaps')
        self._merge_consecutive_gaps()
        print('[OK] Validating all the items inside')
        self._validate_items()
        print('[OK] Validate the transitions (if existing)')
        self._validate_transitions()

    def _fullfil_if_empty(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Fulfill the list with a gap that lasts the whole
        duration if the list is completely empty, as we
        always need to have one item inside.
        """
        if self.is_empty:
            self.items.append(
                GapTrackItem(
                    track = self._track,
                    t_start = 0,
                    duration = TIME_INTERVAL_SYSTEM_LIMITS[1],
                    item_in = None,
                    item_out = None
                )
            )

        return self
    
    def _validate_items(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Check that the `items` list is valid and all the items
        are consecutive, with no empty gap in between and with
        no overlappings.
        """
        # TODO: The list must be ordered
        for previous_item, current_item in zip(self.items, self.items[1:]):
            if previous_item.t_end != current_item.t_start:
                raise Exception(f'There is an item with "t_end={str(float(previous_item.t_end))}" and the next one with "t_start={str(float(current_item.t_start))}".')

        return self
    
    def _order_items(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Order the `items` list and ensures that all the items
        are ordered by the `t_start` field. This method will
        updated the `self.items` list.
        """
        self.items.sort(key = lambda item: item.t_start)

        return self
    
    def _relink_items(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Reset all the links in between the items that are in
        the list. One item will be the `item_in` of the next
        one, which will also be the `item_out` of that item
        that is inmediately before.
        """
        # 1. Order the items again based on the `t_start` field
        # self._reorder_items()

        # 2. Reset links
        prev = None
        for item in self.items:
            item.item_in = prev

            if prev:
                prev.item_out = item

            prev = item

        if prev:
            prev.item_out = None

        # 3. Regenerate gaps
        # self._rebuild_gaps()

        # 4. Validate transitions
        # self._validate_transitions()

    def _merge_consecutive_gaps(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        This method will merge the consecutive gaps existing
        in the items list, to combine them as a single but 
        longer one.
        """
        if self.is_empty:
            return

        merged = []
        current = self.items[0]

        for item in self.items[1:]:
            if (
                is_gap_track_item(current) and
                is_gap_track_item(item)
            ):
                # TODO: This should always happen. If it doesn't happen
                # is because we did something wrong...
                if item.t_start <= current.t_end:
                    # Combine gaps in one
                    current.shift_end_to(max(current.t_end, item.t_end))
                    # Point the 'item_out' to the next item's out
                    current.item_out = item.item_out
                    continue

            # No more consecutives to combine, just add
            merged.append(current)
            current = item

        # Add the last one pending and replace
        merged.append(current)
        self.items = merged

        return self

    def _rebuild_gaps(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Rebuild the gaps according to a change that has happened
        in some items, modifying the size of the gaps.
        """
        # TODO: Modify the time interval of any gap that doesn't
        # match the time moments of the track (that doesn't end
        # when the next item starts, or that ends after another
        # item has started)
        # No tiene sentido si hay menos de 2 items
        if len(self.items) < 2:
            return self
        
        # TODO: Should we build gaps in between elements that have
        # been shifted or something, leaving a time interval gap 
        # between the `t_start` of the first one and the `t_end`
        # of the second one (?)

        for i, item in enumerate(self.items):
            if not PythonValidator.is_instance_of(item, GapTrackItem):
                continue

            previous_item = (
                self.items[i - 1]
                if (i - 1) >= 0 else
                None
            )

            next_item = (
                self.items[i + 1]
                if (i + 1) < len(self.items) else
                None
            )

            # Set the time interval that is the right one
            if (
                previous_item is not None and
                item.t_start != previous_item.t_end
            ):
                # TODO: Use a 'item._set_t_start()' instead (?)
                #item._time_interval.with_start_and_end(previous_item.t_end, item.t_end)
                item._time_interval.t_start = previous_item.t_end

            if (
                next_item is not None and
                item.t_end != next_item.t_start
            ):
                # TODO: Use a 'item._set_t_end()' instead (?)
                #item._time_interval.with_start_and_end(item.t_start, next_item.t_start)
                item._time_interval.t_end = next_item.t_start

        # If we had 2 consecutive gaps, this method is fixing
        # the time gap if existing, but not combining them. 
        # Use the '_merge_consecutive_gaps' to do that.
        
        return self

    def _validate_transitions(
        self
    ) -> '_TrackItems':
        """
        *For internal use only*

        Check and validate the transitions that exist before any
        change to remove the ones that are not available now 
        according to the new changes.
        """
        # TODO: Maybe we don't need to raise exception but to
        # fix the time intervals of these transitions
        for i, item in enumerate(self.items):
            if not PythonValidator.is_instance_of(item, 'TransitionTrackItem'):
                continue

            if (
                i == 0 or
                i == len(self.items) - 1
            ):
                # I think this will never happen based on the
                # way the system is built
                raise Exception('Transition item cannot be the first or last item.')

            item_in = self.items[i - 1]
            item_out = self.items[i + 1]

            if item.item_in is not item_in:
                print(f'Transition item_in mismatch: expected index {i-1}, but transition.item_in is {item.item_in}.')
                # TODO: Remove any unexpected transition link
                item.item_in.transition_out = None
                self.remove_item(item)
                #raise Exception(f'Transition item_in mismatch: expected index {i-1}, but transition.item_in is {item.item_in}.')

            if item.item_out is not item_out:
                raise Exception(f'Transition item_out mismatch: expected index {i+1}, but transition.item_out is {item.item_out}.')

            if item_in.t_end != item.t_start:
                raise Exception(f'Transition start mismatch: item_in.t_end={float(item_in.t_end)} != transition.t_start={float(item.t_start)}')

            if item.t_end != item_out.t_start:
                raise Exception(f'Transition end mismatch: transition.t_end={float(item.t_end)} != item_out.t_start={float(item_out.t_start)}')
        
        return self
    
    def _shift_next_elements(
        self,
        item: TrackItemType,
        delta: Union[int, float, Fraction],
        do_include_item: bool = False
    ):
        """
        *For internal use only*

        Update the next elements of the given `item` by applying
        the `delta` time amount provided, that will make their
        time intervals be updated with that value. If the 
        `do_include_item` boolean parameter is True, the `item`
        itself will be also shifted (useful when you have deleted
        one item and want to shift the next ones).

        This method must be called when we are adding an item 
        that was longer than expected and we need to move the
        next items.
        """
        print(f'shifting next elements delta={str(float(delta))}')

        item = (
            item
            if do_include_item else
            item.item_out
        )

        while item is not None:
            # We just need to move the time interval, but the connections
            # and everything are the same because we just inserted
            # something that makes this 'shift' necessary
            item._shift_by(delta)
            item = item.item_out

    def _replace_item(
        self,
        index: int,
        items: Union[TrackItemType, list[TrackItemType]]
    ) -> '_TrackItems':
        """
        *For internal use only*

        Replace the item at the `index` position with the item
        or items given as `items` parameter.

        If any element of the `items` array provided is None it
        will be omitted.
        """
        ParameterValidator.validate_int_between('index', index, 0, len(self.items), do_include_upper_limit = False)

        items = (
            [items]
            if not PythonValidator.is_list(items) else
            items
        )

        # Replace the item at t with the new composition
        items_to_insert = [
            item
            for item in items
            if item is not None
        ]

        if len(items_to_insert) == 0:
            raise Exception('The amount of "items" provided that are not None is 0.')

        # TODO: Validate that t_start and t_end are congruent
        # TODO: Validate that the previous and next items
        # are ok according to the timing of this item
        self.items[index:index + 1] = items_to_insert

        return self
    
    """
    Internal but necessary and very important methods above.
    """

    def reset(
        self
    ):
        """
        Reset the items list by emptying it and adding a
        single gap item lasting the whole track duration.

        (!) This method should be called carefully as it
        will remove everything built before.
        """
        self.items = []
        self._fullfil_if_empty()

    def get_item(
        self,
        item: TrackItemType
    ) -> Union['_TrackItemFound', None]:
        """
        Get the `item` provided from the items list, if
        existing, but as a `_TrackItemFound` including the
        index, or `None` if it doesn't exist on the list.
        """
        try:
            index = self.items.index(item)

            return _TrackItemFound(
                item = item,
                index = index
            )
        except:
            return None

    def get_item_at(
        self,
        t: Union[int, float, Fraction]
    ) -> Union['_TrackItemFound', None]:
        """
        Get the item that is placed at the given `t` global
        time moment in this track.

        We will have always at least one item at that position
        because we fill empty gaps with the special gap item.
        """
        # TODO: This should not happen as we should always
        # have at least a gap that fulfills the whole track
        # items list
        t_starts = [
            i.t_start
            for i in self.items
        ]

        # TODO: What if 0 (?)
        index = bisect.bisect_right(t_starts, t)

        # TODO: Why this? Is it necessary (?)
        # TODO: I had to do this because it was becoming -1 in
        # some situations
        index = (
            index - 1
            if index > 0 else
            index
        )

        return _TrackItemFound(
            item = self.items[index],
            index = index
        )
    
    def get_items_at(
        self,
        t_start: Union[int, float, Fraction],
        t_end: Union[int, float, Fraction]
    ) -> list['_TrackItemFound']:
        """
        Get all the items that will take place in the time
        interval `[t_start, t_end]`.
        """
        t_starts = [
            i.t_start
            for i in self.items
        ]

        # First element with t_start > t1
        index = bisect.bisect_right(t_starts, t_end)

        result = []

        # Go backwards until we have no overlapping
        i = index - 1
        while i >= 0:
            item = self.items[i]

            if item.t_end <= t_start:
                # No more overlapping
                break

            result.append(item)
            i -= 1

        # Go forwards (just to make sure it is well done)
        i = index
        while i < len(self.items):
            item = self.items[i]

            if item.t_start >= t_end:
                # No more overlapping
                break

            if item.t_end > t_start:
                result.append(item)

            i += 1

        return result
    
    def get_items_after(
        self,
        t: Union[int, float, Fraction]
    ) -> list['_TrackItemFound']:
        """
        Get all the items whose `t_start` time moment is
        equal or greater than the `t` time moment provided.
        """
        item_at_t = self.get_item_at(t)

        current_index = item_at_t.index + 1
        items = []
        for item in self.items[item_at_t.index:]:
            items.append(
                object = _TrackItemFound(
                    item = item,
                    index = current_index
                )
            )
            current_index += 1

        return items
    
    def get_items_before(
        self,
        t: Union[int, float, Fraction]
    ) -> list['_TrackItemFound']:
        """
        Get all the items whose `t_start` time moment is lower 
        than the `t` time moment provided.
        """
        item_at_t = self.get_item_at(t)

        current_index = item_at_t.index - 1
        items = []
        for item in self.items[:item_at_t.index]:
            items.append(
                object = _TrackItemFound(
                    item = item,
                    index = current_index
                )
            )
            current_index -= 1

        return items
    
    """
    Important methods below
    """
    
    def add_item(
        self,
        item: TrackItemType,
        # TODO: Create a 'mode' instead
        do_force_add: bool = True
    ) -> '_TrackItems':
        """
        Add the `item` provided to the list, that will be added
        in the corresponding place according to the `t_start` time
        moment of that `item`.
        """
        item_at_t = self.get_item_at(item.t_start)

        # TODO: Implement the 'do_force_add' to force adding
        # the item if the 't' is occupied

        """
        Opciones:
        - (1) Insertar VÍDEO en GAP que termina antes que el siguiente
        elemento:
            *Podemos insertar sin problema, detectando si hace falta gap
            en la izquierda y/o en la derecha y construyendo el triplete
            correspondiente
        - (2) Insertar VÍDEO en GAP que termina después de que el siguiente elemento
        empiece:
            *Tenemos que desplazar el inicio del elemento que está a la derecha
            hasta el momento en el que terminaría el que queremos insertar (y
            propagar el cambio a los siguientes), y colocar un gap a la izquierda
            para rellenar si hace falta.
        - (3) Insertar VÍDEO en VÍDEO. Comprobar la estrategia, y si está
        forzada, convertir el 't' recibido en el 't_end' del VÍDEO que ya hay, y
        operar como el punto (1) o (2).
        """

        if is_gap_track_item(item_at_t.item):
            """
            (1) and (2) are being handled here, inserting in
            a gap
            """
            if is_gap_track_item(item):
                # Item to add is a gap
                # TODO: Is this possible? I think we will not add
                # gaps but use them with the 'replace'...
                print('we are adding a gap')

            if item.t_end > item_at_t.item.t_end:
                """
                (2) Our item ends when the next item has started
                so we need to shift the next item a bit to create
                the space needed and then set the triplet
                """
                # Shift it (and propagate) the amount of time we need
                """
                The GAP is now shifting in an special way considering
                if it is the last one (special one) or not, so we can
                shift it correctly. By now the strategy I am applying
                is to shift everything that is on the right just as it
                is, so everything keeps being the same and has to be
                modified manually to actually change.
                """
                delta = item.t_end - item_at_t.item.t_end
                self._shift_next_elements(item_at_t.item, delta)

            """
            Our item ends before or at the t_start of the next
            one so we can add it easy by creating a triplet
            of left and right gaps if needed and replace the
            previous item with that new one.

            I'll give you a nice example to understand 
            everything better. Imagine a gap from t=3 to t=6
            in which we want to place a video of duration=2:
            - (1) Set at t=3 - The triplet will be:
                [None, Video[3, 5], Gap[5, 6]]
            - (2) Set at t=3.5 - The triplet will be:
                [Gap[3, 3.5], Video[3.5, 5.5], Gap[5.5, 6]
            - (3) Set at t=4 - The triplet will be:
                [Gap[3, 4], Video[4, 6], None]

            Now imagine that the gap we have is from t=3 to
            t=5, with the same video with duration=2:
            - (1) Set at t=3 - The triplet will be:
                [None, Video[3, 5], None]
            """

            left_gap_item = (
                GapTrackItem(
                    track = item._track,
                    t_start = item_at_t.item.t_start,
                    duration = item.t_start - item_at_t.item.t_start,
                    # I'll set it when I have the left and the right
                    item_in = None,
                    item_out = None,
                )
                if item.t_start > item_at_t.item.t_start else
                None
            )

            right_gap_item = (
                GapTrackItem(
                    track = item._track,
                    t_start = item.t_end,
                    duration = item_at_t.item.t_end - item.t_end,
                    # I'll set it when I have the left and the right
                    item_in = None,
                    item_out = None,
                )
                if item.t_end < item_at_t.item.t_end else
                None
            )

            # Keep the old connections
            old_gap_item_in = item_at_t.item.item_in
            old_gap_item_out = item_at_t.item.item_out
            # Unlink the original (old) gap
            item_at_t.item.unset_item_in()
            item_at_t.item.unset_item_out()

            # Keep the connections according to the changes
            if left_gap_item is not None:
                left_gap_item.set_item_out(item, True)
            elif (old_gap_item_in is not None):
                item.set_item_in(old_gap_item_in)

            if right_gap_item is not None:
                right_gap_item.set_item_in(item, True)
            elif (old_gap_item_out is not None):
                item.set_item_out(old_gap_item_out)

            # Replace the item at t with the new composition
            self._replace_item(
                index = item_at_t.index,
                items = [left_gap_item, item, right_gap_item]
            )
        else:
            """
            (3) We are trying to insert something in a place in
            which we already have a video (and not a gap) so we
            need to, instead of that, insert it at the 't_end' of
            that existing video, and then move the rest of the
            items that are on the right the duration of the item
            we added
            """
            if not do_force_add:
                raise Exception('No gap in that place, so sorry by now!')
            
            item_at_t_item_out = item_at_t.item.item_out
            # Change the 't_start.item' to the 'item_at_t.item.t_end'
            print(f'@@@ shifting item to {str(float(item_at_t.item.t_end))}')
            item.shift_to(item_at_t.item.t_end)
            item_at_t.item.set_item_out(item)
            item.set_item_out(item_at_t_item_out)

            # Shift all the elements to the right
            self._shift_next_elements(item, item.duration)

            self._replace_item(
                index = item_at_t.index,
                items = [item_at_t.item, item]
            )

        # TODO: We need to recalculate the links, etc.
        self._recalculate_all()

        return self
    
    def remove_item(
        self,
        item: TrackItemType,
        # TODO: Maybe create a 'mode' and use the mode instead
        do_create_gap_instead: bool = True
    ) -> '_TrackItems':
        """
        Remove the `item` from the list. The item, if 
        existing and different to a gap, will be transformed
        into a gap if the `do_create_gap_instead` boolean
        parameter is True, or it will be removed completely
        if it is False.

        The list will have one item less but will keep
        being ordered by the `t_start` time moment.
        """
        item: _TrackItemFound = self.get_item(item)

        # TODO: This should not happen I think...
        if item is None:
            raise Exception('The "item" was not found, what did you send bro?')
        
        # TODO: Refactor this
        if do_create_gap_instead:
            gap_item = GapTrackItem(
                track = item.item._track,
                t_start = item.item.t_start,
                duration = item.item.duration,
                # I link these 'in' and 'out' before
                item_in = None,
                item_out = None
            )

            if item.item.item_in is not None:
                gap_item.set_item_in(item.item)

            if item.item.item_out is not None:
                gap_item.set_item_out(item.item)

            # Is this necessary? We will lose the instance...
            item.item.unset_item_in(False)
            item.item.unset_item_out(False)
            
            self._replace_item(
                index = item.index,
                items = [gap_item]
            )
        else:
            """
            We have some special cases, such as being the only item in
            the track, which, even being strange, should be replaced
            by a gap. But also being the first or the last item of the
            track are special situations.
            """
            # TODO: Remove the item and shift the next ones
            previous_item = item.item.item_in
            next_item = item.item.item_out

            self.items.pop(item.index)

            # TODO: Review this below, I think I have to use 'False'
            # to avoid infinite loops
            if previous_item is not None:
                previous_item.set_item_out(next_item)

            if next_item is not None:
                next_item.set_item_in(previous_item)

            # Just for security
            item.item.item_in = None
            item.item.item_out = None

            self._shift_next_elements(next_item, -item.item.duration, True)

        self._recalculate_all()

        return self
    
    def remove_item_at(
        self,
        t: Union[int, float, Fraction],
        # TODO: Maybe create a 'mode' and use the mode instead
        do_create_gap_instead: bool = True
    ) -> '_TrackItems':
        """
        Remove the item from the list that corresponds to
        the `t` time moment, which means that is being
        displayed at that time (the `t` is in between the
        `[t_start, t_end]` time interval). The item, if 
        existing and different to a gap, will be transformed
        into a gap if the `do_create_gap_instead` boolean
        parameter is True, or it will be removed completely
        if it is False.

        The list will have one item less but will keep
        being ordered by the `t_start` time moment.
        """
        item_at_t = self.get_item_at(t)

        return self.remove_item(
            item = item_at_t.item,
            do_create_gap_instead = do_create_gap_instead
        )
    


    # TODO: Working on this one below
    def add_transition(
        self,
        # TODO: We need to know the way to handle this 'type'
        # and maybe all the properties of the transition
        item_in: TrackItemType,
        item_out: TrackItemType,
        type: any = 'random',
        mode: TransitionMode = TransitionMode.TRIM,
        duration: Union[int, float, Fraction] = 1
    ) -> '_TrackItems':
        """
        Create a transition between the `item_in` and
        `item_out` provided of the given `type`, if
        possible, and place it as a new item in between
        those 2 items that have to be consecutive and
        valid.
        """
        item_in: _TrackItemFound = self.get_item(item_in)
        item_out: _TrackItemFound = self.get_item(item_out)

        if item_in is None:
            raise Exception('The "item_in" does not exist in the track.')
        
        if item_out is None:
            raise Exception('The "item_out" does not exist in the track')
        
        # TODO: Validate that 'item_in.item' is a video item
        # TODO: Validate that 'item_out.item' is a video item
        
        if (item_in.index + 1) != item_out.index:
            raise Exception('The "item_in" and "item_out" provided are not consecutive.')

        mode = TransitionMode.to_enum(mode)

        if (
            item_in.item.duration <= duration or
            item_out.item.duration <= duration
        ):
            raise Exception(f'The items for the transition must last more time than the duration of the transition requested (duration={str(float(duration))}), and these are the durations of the items: "item_in duration={str(float(item_in.item.duration))}" and the "item_out duration={str(float(item_out.item.duration))}".')

        """
        We will trim the affected clip items if needed and then
        we will insert the transition track item in between both
        so the 'item_out' clip is automatically shifted the
        amount of time needed to fit the transition item in
        between.

        The transition has different types (modes), and according
        to those modes we will modify the durations and time
        moments of the clips affected as I show below, considering
        this case `[ClipA] [Gap] [ClipB]`:

        - TRIM: `[ClipA_trimmed] [Transition] [ClipB_trimmed]`
        - FREEZE_TAIL: `[ClipA] [Transition] [ClipB_delayed]`
        - FREEZE_HEAD: `[ClipA] [Transition] [ClipB_delayed]`
        - FREEZE_BOTH: `[ClipA] [Transition] [ClipB_delayed]`

        As you can see, only with the 'TRIM' mode we have to trim
        the clips, and with all the other modes we only have to
        delay (shift) the 'item_out', which is the normal behaviour
        when inserting a new item after the 'item_in' and before
        the 'item_out'.
        """
        if mode in [TransitionMode.TRIM, TransitionMode.FREEZE_TAIL]:
            # Trim the end of 'item_in'
            self.shift_item_end_by(item_in.item, -duration)
        if mode in [TransitionMode.TRIM, TransitionMode.FREEZE_HEAD]:
            # Trim the start of 'item_out'
            """
            As we will use the first part of the 'item_out' clip
            for the transition, we need to adjust the media of
            that clip from the 't_start', but also the item itself
            from the 't_end' because we are trimming it in the
            track
            """
            self.shift_item_media_start_and_item_end_by(item_out.item, duration)

        print('pre adding transition item')

        # TODO: The 'TransitionTrackItem' needs to be like the
        # others

        """
        We use a time moment in between the 't_start' and the
        't_end' to make sure that it fits in the middle of the
        previous item so it is processed as it should be, using
        the 't_end' of the first element to be inserted there
        """
        t_start = (item_in.item.t_start + item_in.item.t_end) / 2

        transition_item: TransitionTrackItem = TransitionTrackItem(
            track = self._track,
            t_start = t_start,
            duration = duration,
            # TODO: The 'type' should be refactored
            type = type,
            mode = mode,
            # The 'item_in' and 'item_out' will be automatically set
            # according to the items that are previous and after the
            # transition time moment, and have been checked
            # previously. Including it here will make an infinite
            # loop as the next item would be referencing the
            # transition
            item_in = None,
            item_out = None
        )

        self.add_item(
            item = transition_item,
            do_force_add = True
        )

        return self
    
    def remove_transition(
        self,
        transition_item: 'TransitionTrackItem'
    ) -> '_TrackItems':
        """
        Remove the transition provided as `transition_item` from
        the track and readjust the items affected by that 
        transition. This means that if the transition was trimming
        the clips to be built, they will be enlarged again.
        """
        item_in = transition_item.item_in
        item_out = transition_item.item_out
        duration = transition_item.duration

        # Undone the changes the transition made to the
        # affected clips, if needed
        if transition_item.mode in [TransitionMode.TRIM]:
            # Enlarge the end of 'item_in'
            self.shift_item_end_by(item_in, duration)

            # Enlarge the start of 'item_out'
            """
            As we were using the first part of the 'item_out' clip
            for the transition, we need to adjust the media of 
            that clip from the 't_start', but also the item itself
            from the 't_end' because we trimmed it in the track
            """
            self.shift_item_media_start_and_item_end_by(item_out, -duration)

        self.remove_item(
            item = transition_item,
            do_create_gap_instead = False
        )

        # TODO: Do I really need this here (?)
        self._recalculate_all()

        return self
        

    """
    Methods related to shifting items
    """

    def shift_item_by(
        self,
        item: TrackItemType,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItems':
        """
        Shift the `item` provided the `delta` amount of time
        given.
        """
        if delta == 0:
            return self
        
        # TODO: Validate 'item'
        
        item.shift_by(delta)

        self._shift_next_elements(
            item = item,
            delta = delta,
            do_include_item = False
        )

        # TODO: Is this needed (?)
        self._recalculate_all()
        
        return self
    
    def shift_item_end_by(
        self,
        item: TrackItemType,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItems':
        """
        Shift the end of the `item` provided the `delta` amount
        of time given.
        """
        if delta == 0:
            return self
        
        # TODO: Validate 'item'
        
        item.shift_end_by(delta)

        self._shift_next_elements(
            item = item,
            delta = delta,
            do_include_item = False
        )

        # TODO: Is this needed (?)
        self._recalculate_all()
        
        return self
    
    def shift_item_media_start_and_item_end_by(
        self,
        item: TrackItemType,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItems':
        """
        Shift the start of the media associated to the `item`
        provided the `delta` amount of time given and the end
        of that `item` also that same amount of time.
        """
        if delta == 0:
            return self
        
        # TODO: Validate 'item'
        
        item.shift_media_start_and_item_end_by(delta)

        self._shift_next_elements(
            item = item,
            delta = delta,
            do_include_item = False
        )

        # TODO: Is this needed (?)
        self._recalculate_all()
        
        return self

class _Track(ABC):
    """
    TODO: This class should replace the old one.

    Abstract class to be inherited by the different
    track item classes we implement.
    """

    @property
    def t_end(
        self
    ) -> Fraction:
        """
        The maximum `t_end` time moment, which is the biggest `t_end`
        value of a non-gap track item.
        """
        for item in reversed(self.items.items):
            if not is_gap_track_item(item):
                return item.t_end
            
        return 0

    @property
    def fps(
        self
    ) -> float:
        """
        The fps of the track, which are the same than the timeline
        that includes this track.
        """
        return self._timeline.fps
    
    @property
    def audio_fps(
        self
    ) -> float:
        """
        The audio fps of the track, which are the same than the
        timeline that includes this track.
        """
        return self._timeline.audio_fps
    
    @property
    def is_muted(
        self
    ) -> bool:
        """
        Flag to indicate if the track is muted or
        not. Being muted means that no audio frames
        will be retured from this track.
        """
        return self._is_muted
    
    @property
    def _t_utils(
        self
    ) -> '_TUtils':
        """
        Shortcut to the timeline `_TUtils` instance to work
        with time moments according to the timeline fps.
        """
        return self._timeline._t_utils
    
    def __init__(
        self,
        timeline: 'Timeline',
        index: int,
    ):
        self._timeline: 'Timeline' = timeline
        """
        The timeline instance this track belongs to.
        """
        # TODO: Initialize with a 'GapTrackItem' that lasts the whole track instead
        self.items = _TrackItems(self)
        """
        The list of items this track contains, that will be
        always ordered according to the `t_start` time moment.
        """

        self.index: int = index
        """
        The index of the track within the timeline.
        """
        self._is_muted: bool = False
        """
        Internal flag to indicate if the track is
        muted or not.
        """

    def mute(
        self
    ) -> '_Track':
        """
        Set the track as muted so no audio frame will
        be played from this track.
        """
        self._is_muted = True

        return self

    def unmute(
        self
    ) -> '_Track':
        """
        Set the track as unmuted so the audio frames
        will be played as normal.
        """
        self._is_muted = False

        return self

    """
    Functionality related to the items below
    """
    def is_gap_at(
        self,
        t_start: Union[int, float, Fraction],
        t_end: Union[int, float, Fraction, None] = None
    ) -> bool:
        """
        Check if the if the `t_start` time moment provided is
        occupied by a `GapTrackItem` instance, if only the
        `t_start` parameter is provided, or if the whole time
        interval from `t_start` to `t_end` is occupied by the
        same `GapTrackItem` instance.
        """
        item_at_t = self.get_item_at(t_start).item
        is_gap = PythonValidator.is_instance_of(item_at_t, GapTrackItem)

        return (
            is_gap
            if t_end is None else
            (
                is_gap and
                item_at_t.t_start >= t_start and
                # TODO: Should this be '<=' or only '<' (?)
                item_at_t.t_end <= t_end
            )
        )

    def get_item_at(
        self,
        t: Union[int, float, Fraction]
    ) -> '_TrackItemFound':
        """
        Get the item that is placed at the given `t` global
        time moment in this track.

        We will have always at least one item at that position
        because we fill empty gaps with the special gap item.
        """
        return self.items.get_item_at(t)
    
    def add_video_item(
        self,
        media: 'VideoMedia',
        t: Union[int, float, Fraction],
        do_force_add: bool = True
    ) -> '_Track':
        """
        Create a video track item and set it in the `t` global
        time moment provided.
        """
        from yta_editor.tracks.items.abstract import TrackItemWithVideoMedia

        # TODO: Validate 'media'
        
        return self.items.add_item(
            item = TrackItemWithVideoMedia(
                track = self,
                t_start = t,
                media = media
            ),
            do_force_add = do_force_add
        )
    
    def remove_item(
        self,
        item: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem']
    ) -> '_Track':
        """
        Remove the item from the list. The item, if existing
        and different to a gap, will be transformed into a
        gap.
        
        The list will have one item less but will keep being
        ordered by the t_start time moment.
        """
        self.items.remove_item(item)

        return self
    
    def remove_item_at(
        self,
        t: Union[int, float, Fraction]
    ) -> '_Track':
        """
        Remove the item existing at the `t` time moment
        provided, that will turn it into a gap (if it is
        not already a gap).
        """
        self.items.remove_item_at(t)

        return self
    
    """
    Methods related to transitions below
    """
    def add_transition(
        self,
        # TODO: We need to know the way to handle this 'type'
        # and maybe all the properties of the transition
        item_in: TrackItemType,
        item_out: TrackItemType,
        type: any = 'random',
        mode: TransitionMode = TransitionMode.TRIM,
        duration: Union[int, float, Fraction] = 1
    ) -> '_Track':
        """
        Create a transition between the `item_in` and `item_out`
        provided of the given type, if possible, and place
        it as a new item in between those 2 items that have
        to be consecutive and valid.
        """
        self.items.add_transition(
            item_in = item_in,
            item_out = item_out,
            type = type,
            mode = mode,
            duration = duration
        )

        return self
    
    def remove_transition(
        self,
        transition_item: 'TransitionTrackItem'
    ) -> '_TrackItems':
        """
        Remove the transition provided as `transition_item` from
        the track and readjust the items affected by that 
        transition. This means that if the transition was trimming
        the clips to be built, they will be enlarged again.
        """
        self.items.remove_transition(
            transition_item = transition_item
        )

        return self
    
    """
    Here below you have all the methods related to shifting
    and moving the items.

    TODO: Maybe we should move these methods to the 
    TrackItems class instead.
    """
    def shift_item_by(
        self,
        item: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem'],
        delta: Union[int, float, Fraction]
    ) -> '_Track':
        """
        Remove the `item`, shift it the `delta` amount of time
        provided, and place it again in the track.
        """
        # TODO: Maybe valdiate some limits
        self.remove_item(item)
        item._shift_by(delta)
        self.items.add_item(item, True)

        return item
    
    def __str__(
        self
    ) -> str:
        """
        Stringify the instance by showing all the items.
        """
        return f'  - -   T   R   A   C   K   - - \n' + '\n'.join([
            f'[{str(int(index + 1))}] {item.__str__()}'
            for index, item in enumerate(self.items.items)
        ])
        
    
# TODO: This class has been created to wrap the methods
# to add transitions to the clips of a track due to its
# complexity. Maybe we will delete it as we are not
# handling the transitions as videos overlapping
class _TrackTransitionHandler:
    """
    *For internal use only*

    Class to handle the way we add transitions in between
    clips in a track.
    """

    @staticmethod
    def get_adjacent_medias_at(
        clips: list['Clip'],
        t: float
    ) -> tuple[Union['Clip', None], Union['Clip', None]]:
        """
        Get the 2 clips that are adjacent at the `t` time
        moment provided according to the given list of
        `clips`, or a tuple of None if there are no adjacent
        clips.
        """
        time_intervals = [
            (clip.t_start, clip.t_end)
            for clip in clips
        ]

        previous_index, next_index = _TrackTransitionHandler.get_adjacent_indexes_at(
            time_intervals = time_intervals,
            t = t
        )

        if (
            previous_index is None or
            next_index is None
        ):
            raise Exception(f'There are no adjacent medias at t={str(float(t))}')

        return (
            clips[previous_index],
            clips[next_index]
        )
    
    # TODO: This maybe should be somewhere else maybe
    def get_adjacent_indexes_at(
        time_intervals: list[tuple[float, float]],
        t: float
    ) -> Union[tuple[int, int], tuple[None, None]]:
        """
        Get the pair of indexes of the provided `time_invervals`
        list that are adjacent at the given `t` time moment (that
        must be exactly an `t_end` time moment).

        Returns
        -------
        (int, int) | (None, None)
            Indices of the adjacent ranges in the original list, or
            (None, None) if not found.
        """
        # Numbers are converted to float for comparison robustness
        t = float(t)
        # Keep the original index with the tuples
        indexed_ranges = list(enumerate(time_intervals))
        # Order by 't_start' without losing the original index
        sorted_ranges = sorted(indexed_ranges, key = lambda time_interval: float(time_interval[1][0]))

        for i in range(len(sorted_ranges) - 1):
            (idx_a, (_, end_a)) = sorted_ranges[i]
            (idx_b, (start_b, _)) = sorted_ranges[i + 1]

            previous_end_time = float(end_a)
            next_start_time = float(start_b)

            if _TrackTransitionHandler.are_adjacent_at(
                first_clip_end = previous_end_time,
                second_clip_start = next_start_time,
                t = t
            ):
                return (
                    idx_a,
                    idx_b
                )

        return (
            None,
            None
        )
    
    def are_adjacent_at(
        first_clip_end: float,
        second_clip_start: float,
        t: float
    ) -> bool:
        """
        Check if the `first_clip_end` and `second_clip_start`
        time moments provided are adjacent at the `t` time
        moment also given.
        """
        return (
            check_values_are_same(first_clip_end, second_clip_start)
            and check_values_are_same(t, first_clip_end)
        )

    @staticmethod
    def find_clips_overlapping_at_t(
        clips: list['Clip'],
        t: float
    ) -> tuple[Union['Clip', None], Union['Clip', None]]:
        """
        Find the list of 2 clips of the given `clips` list
        that are overlapping at the `t` time moment provided.

        This method will return a tuple including the
        previous and the next clips (that can be None if
        they are not overlapping).

        TODO: This will not happen because we don't accept
        overlapping clips in the same track. Remove it in the
        next commit.
        """
        prev_clip = None
        next_clip = None

        for clip in clips:
            if clip.t_end <= t:
                prev_clip = clip
            elif clip.t_start >= t:
                next_clip = clip
                break

        return (
            prev_clip,
            next_clip
        )
    
    @staticmethod
    def find_time_clips_overlap(
        previous_clip: 'Clip',
        next_clip: 'Clip'
    ) -> Union[tuple[float, float, float], None]:
        """
        Get the time interval in between the `previous_clip`
        and the `next_clip` provided are colliding, getting
        None if they are not colliding, or a tuple including:
        - `overlap_start`
        - `overlap_end`
        - `overlap_time`

        TODO: This will not happen because we don't accept
        overlapping clips in the same track. Remove it in the
        next commit.
        """
        # Overlapping time range
        overlap_start = max(previous_clip.t_start, next_clip.t_start)
        overlap_end = min(previous_clip.t_end, next_clip.t_end)

        if overlap_start >= overlap_end:
            # No overlap
            return None
            print("Advertencia: no hay solapamiento real, creando transición forzada.")
            overlap_start = t_start
            overlap_end = t_start + duration

        return (
            overlap_start,
            overlap_end,
            overlap_end - overlap_start
        )
    
class _TrackWithAudio(_Track):
    """
    Class that has the ability to obtain the
    audio frames from the source and must be
    inherited by those tracks that have audio
    (or video, that includes audio).
    """

    def __init__(
        self,
        # TODO: Where does it come from (?)
        audio_samples_per_frame: int,
        audio_layout: str,
        audio_format: str,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.audio_samples_per_frame: int = audio_samples_per_frame
        """
        The number of samples per audio frame.
        """
        self.audio_layout: str = audio_layout
        """
        The layout of the audio, that can be 'mono'
        or 'stereo'.
        """
        self.audio_format: str = audio_format
        """
        The format of the audio, that can be 's16',
        'flt', 'fltp', etc.
        """

    # TODO: This is not working well when
    # source has different fps
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        # TODO: Ignore this, we have the 'self.fps'
        video_fps: Union[int, float, Fraction] = None,
    ):
        """
        Get the sequence of audio frames that
        must be displayed at the 't' time 
        moment provided, which the collection
        of audio frames corresponding to the
        audio that is being played at that time
        moment.

        Remember, this 't' time moment provided
        is about the track, and we make the
        conversion to the actual audio 't' to
        get the frame.
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults
        frames = (
            TimelineDefaults().audio_empty
            if self.is_muted else
            # TODO: What if we find None here (?)
            self.get_item_at(t).item.get_audio_frames_at(t, self.fps)
        )

        for frame in frames:
            print('      HELLO       ')
            print(frame)
            if frame == []:
                print(f'   [ERROR] Audio frame t:{str(float(t))} not obtained.')
            yield frame

class _TrackWithVideo(_Track):
    """
    Class that has the ability to obtain the
    video frames from the source and must be
    inherited by those tracks that have video.
    """

    def __init__(
        self,
        size: tuple[int, int],
        **kwargs
    ):
        super().__init__(**kwargs)

        # TODO: This is not needed actually...
        self.size: tuple[int, int] = size
        """
        The size that the output video will have.
        """
        self._transitions: list['TransitionTrackItem'] = []
        """
        List of transitions that exist in the track and are
        joining adjacent videos.
        """

    def get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction]
    ) -> 'VideoFrameWrapped':
        """
        Get the frame that must be displayed at the
        `t_track` global time moment provided, which
        is a frame from the video that is being
        played at that time moment.

        The global `t_track` time moment provided will
        be transformed into the local `t_track` time
        moment for the specific track item located at
        that position to obtain the frame.
        """
        # TODO: What if the frame, that comes from
        # a video, doesn't have the expected size (?)
        return self.get_item_at(t_track).item._get_video_frame_at(t_track)

def is_gap_track_item(
    item: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem']
) -> bool:
    """
    Check if the `item` provided is an instance of a
    `GapTrackItem` or not.
    """
    return PythonValidator.is_instance_of(item, 'GapTrackItem')
    
"""
Note for the developers:
- When we are working with media and a track we need
to make sure that the time moment we are using matches
the fps of that track and it is a multiple of 1/fps to
be able to position that media properly.
"""