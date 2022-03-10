import time
from Entities import Activity, Comment, Kudoser, SegmentEffort, Split
from typing import List


class ActivityProcessor:

    def __init__(self, activity: Activity):
        self.activity = activity

    @staticmethod
    def _process_segment(segment: SegmentEffort, detailed: bool):
        if segment.pr_rank == 1:
            pr_suffix = "\U0001F947"
        elif segment.pr_rank == 2:
            pr_suffix = "\U0001F948"
        elif segment.pr_rank == 3:
            pr_suffix = "\U0001F949"
        else:
            pr_suffix = ""

        segment_pr = " {0}".format(pr_suffix) if segment.pr_rank is not None else ""
        segment_distance_km = round(segment.distance / 1000, 2)
        segment_distance_mi = round((segment.distance / 1000) * 0.6213712, 2)
        segment_time = time.gmtime(segment.moving_time)

        if segment.moving_time > 3599:
            segment_time_output = time.strftime("%H:%M:%S", segment_time)
        else:
            segment_time_output = time.strftime("%M:%S", segment_time)

        segment_pace_km_seconds = float(segment.moving_time) / float(segment_distance_km)
        segment_pace_km_time = time.gmtime(segment_pace_km_seconds)
        segment_pace_km_time_output = time.strftime("%M:%S", segment_pace_km_time)

        segment_pace_mi_seconds = float(segment.moving_time) / float(segment_distance_mi)
        segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
        segment_pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

        if detailed is False:
            return "{0} {1}  \n".format(segment.name, segment_pr)

        string_format = "| {0}{1} | {2} | {3}km / {4}mi | {5}min/km / {6}min/mi | {7} bpm | {8} bpm |  \n"

        return string_format.format(segment.name, segment_pr, segment_time_output,
                                    segment_distance_km, segment_distance_mi, segment_pace_km_time_output,
                                    segment_pace_mi_time_output, round(segment.average_heartrate),
                                    round(segment.max_heartrate))

    def _process_segments(self, activity: Activity, detailed: bool):
        segments_string = "### Segments  \n"

        if len(activity.segment_efforts) == 0:
            return "{0}No Segments  \n".format(segments_string)

        if detailed is True:
            segments_string += "| Segment | Time | Distance | Pace | Avg. Heart Rate | Max Heart Rate |  \n"
            segments_string += "| ----- | ----- | ----- | ----- | ----- | ----- |  \n"

        for s in activity.segment_efforts:
            segments_string += self._process_segment(s, detailed)

        return segments_string

    @staticmethod
    def _process_split(split: Split, metric: bool):
        moving_time = time.gmtime(split.moving_time)

        if split.moving_time > 3599:
            moving_time_output = time.strftime("%H:%M:%S", moving_time)
        else:
            moving_time_output = time.strftime("%M:%S", moving_time)

        speed = round(split.average_speed * 3.6, 2)
        if metric is False:
            speed = round(speed * 0.6213712, 2)

        if metric:
            speed_suffix = "kph"
        else:
            speed_suffix = "mph"

        return "| {0} | {1} | {2} {3} | {4} bpm |  \n".format(split.split, moving_time_output, speed,
                                                              speed_suffix, round(split.average_heartrate))

    def _process_splits(self, activity: Activity, metric: bool):
        splits_string = ""

        if metric:
            splits_string += "#### Kilometres  \n"
        else:
            splits_string += "#### Miles  \n"

        if metric and len(activity.splits_metric) > 0:
            splits = activity.splits_metric
        elif len(activity.splits_standard) > 0:
            splits = activity.splits_standard
        else:
            return "{0}No Splits  \n".format(splits_string)

        splits_string += "| Split | Time | Speed | Heart Rate |  \n"
        splits_string += "| ----- | ----- | ----- | ----- |  \n"

        for s in splits:
            splits_string += self._process_split(s, metric)

        return splits_string

    @staticmethod
    def _process_laps(activity: Activity):
        laps_string = "### Laps  \n"

        if len(activity.laps) < 2:
            return "{0}No Laps  \n".format(laps_string)

        laps_string += "| Lap | Time | Distance | Speed | Heart Rate |  \n"
        laps_string += "| ----- | ----- | ----- | ----- | ----- |  \n"

        for lap in activity.laps:
            moving_time = time.gmtime(lap.moving_time)
            if lap.moving_time > 3599:
                moving_time_output = time.strftime("%H:%M:%S", moving_time)
            else:
                moving_time_output = time.strftime("%M:%S", moving_time)

            lap_string_format = "| {0} | {1} | {2}m | {3}m/s avg / {4}m/s max | {5} bpm avg. / {6} bpm max  \n"
            laps_string += lap_string_format.format(lap.lap_index, moving_time_output, round(lap.distance),
                                                    round(lap.average_speed, 2), round(lap.max_speed, 2),
                                                    round(lap.average_heartrate), round(lap.max_heartrate))

        return laps_string

    @staticmethod
    def _process_distance_and_pace(activity: Activity):
        if activity.type == "Swim":
            distance_metric = round(activity.distance)
            distance_imper = round(activity.distance * 1.093613)
        else:
            distance_metric = round(activity.distance / 1000, 2)
            distance_imper = round((activity.distance / 1000) * 0.6213712, 2)

        pace_km_seconds = float(activity.moving_time) / float(distance_metric)
        pace_km_time = time.gmtime(pace_km_seconds)
        pace_km_time_output = time.strftime("%M:%S", pace_km_time)

        segment_pace_mi_seconds = float(activity.moving_time) / float(distance_imper)
        segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
        pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

        pace_m = round(float(distance_metric) / float(activity.moving_time), 2)

        if activity.type == "Swim":
            distance_string = "| **Distance:** | {0} metres | {1} yards |  \n".format(distance_metric, distance_imper)
            pace_string = "| **Pace:** | {0} m/s | |  \n".format(pace_m)
        else:
            distance_string = "| **Distance:** | {0}km | {1}mi |  \n".format(distance_metric, distance_imper)
            pace_string = "| **Pace:** | {0} min/km | {1} min/mi |  \n".format(pace_km_time_output, pace_mi_time_output)

        return distance_string, pace_string

    def _process_activity_details(self, activity: Activity):
        description = "{0}  \n".format(activity.description) if activity.description is not None else ""
        moving_time = time.gmtime(activity.moving_time)
        elapsed_time = time.gmtime(activity.elapsed_time)

        if activity.moving_time > 3599:
            moving_time_output = time.strftime("%H:%M:%S", moving_time)
        else:
            moving_time_output = time.strftime("%M:%S", moving_time)

        if activity.elapsed_time > 3599:
            elapsed_time_output = time.strftime("%H:%M:%S", elapsed_time)
        else:
            elapsed_time_output = time.strftime("%M:%S", elapsed_time)

        (distance_string, pace_string) = self._process_distance_and_pace(activity)

        avg_speed_kmh = round(activity.average_speed * 3.6, 2)
        avg_speed_mph = round(avg_speed_kmh * 0.6213712, 2)
        max_speed_kmh = round(activity.max_speed * 3.6, 2)
        max_speed_mph = round(max_speed_kmh * 0.6213712, 2)

        activity_details_string = "# {0}  \n".format(activity.name)
        activity_details_string += description
        activity_details_string += "|       |       |       |  \n"
        activity_details_string += "| ----- | ----- | ----- |  \n"
        activity_details_string += "| **Time:** | {0} moving | {1} total |  \n".format(moving_time_output,
                                                                                       elapsed_time_output)
        activity_details_string += distance_string
        activity_details_string += pace_string
        activity_details_string += "| **Avg. Speed:** | {0} kph | {1} mph |  \n".format(avg_speed_kmh, avg_speed_mph)
        activity_details_string += "| **Max Speed:** | {0} kph | {1} mph |  \n".format(max_speed_kmh, max_speed_mph)

        if activity.has_heartrate:
            activity_details_string += "| **Heart Rate:** | {0} bpm avg | {1} bpm max |  \n".format(
                round(activity.average_heartrate), round(activity.max_heartrate))

        if activity.map.polyline:
            activity_details_string += "  \n[{attachment}]"

        return activity_details_string

    def _process_comments(self, comments: List[Comment]):
        comment_string = '### Comments\n'
        for c in comments:
            comment_string += "**{0} {1}** {2}  \n".format(c.commenter_firstname, c.commenter_lastname,
                                                           c.text)

        return comment_string[:len(comment_string) - 2]

    def _process_kudos(self, kudos: List[Kudoser]):
        kudos_string = '### Got Kudos From\n'
        for k in kudos:
            kudos_string += "{0} {1} ".format(k.firstname, k.lastname)

        return kudos_string

    def process_activity(self, include_kudos, include_comments, segments, which_splits, include_laps):

        return_string = self._process_activity_details(self.activity)

        if include_kudos and self.activity.kudos:
            return_string += "  \n{0}".format(self._process_kudos(self.activity.kudos))

        if include_comments and self.activity.comments:
            return_string += "  \n{0}".format(self._process_comments(self.activity.comments))

        if segments.lower() == "simple":
            return_string += "  \n{0}".format(self._process_segments(self.activity, False))

        if segments.lower() == "detailed":
            return_string += "  \n{0}".format(self._process_segments(self.activity, True))

        if which_splits:
            return_string += "  \n### Splits"

            if which_splits.lower() == "km" or which_splits.lower() == "both":
                return_string += "  \n{0}".format(self._process_splits(self.activity, True))

            if which_splits.lower() == "mi" or which_splits.lower() == "both":
                return_string += "  \n{0}".format(self._process_splits(self.activity, False))

        if include_laps:
            return_string += "  \n{0}".format(self._process_laps(self.activity))

        return return_string
