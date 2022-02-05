import time

class ActivityProcessor:

    def __init__(self, activity, kudos, comments):
        self.activity = activity
        self.kudos = kudos
        self.comments = comments

    def _process_segment(self, segment, detailed):
        if segment["pr_rank"] == 1:
            pr_suffix = "\U0001F947"
        elif segment["pr_rank"] == 2:
            pr_suffix = "\U0001F948"
        elif segment["pr_rank"] == 3:
            pr_suffix = "\U0001F949"
        else:
            pr_suffix = ""

        segment_pr = " {0}".format(pr_suffix) if segment["pr_rank"] is not None else ""
        segment_distance_km = round(segment["distance"] / 1000, 2)
        segment_distance_mi = round((segment["distance"] / 1000) * 0.6213712, 2)
        segment_time = time.gmtime(segment["moving_time"])

        if segment["moving_time"] > 3599:
            segment_time_output = time.strftime("%H:%M:%S", segment_time)
        else:
            segment_time_output = time.strftime("%M:%S", segment_time)

        segment_pace_km_seconds = float(segment["moving_time"]) / float(segment_distance_km)
        segment_pace_km_time = time.gmtime(segment_pace_km_seconds)
        segment_pace_km_time_output = time.strftime("%M:%S", segment_pace_km_time)

        segment_pace_mi_seconds = float(segment["moving_time"]) / float(segment_distance_mi)
        segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
        segment_pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

        if detailed is False:
            return "{0} {1}  \n".format(segment["name"], segment_pr)

        string_format = "| {0}{1} | {2} | {3}km / {4}mi | {5}min/km / {6}min/mi | {7} bpm | {8} bpm |  \n"

        return string_format.format(segment["name"], segment_pr, segment_time_output,
                                    segment_distance_km, segment_distance_mi, segment_pace_km_time_output,
                                    segment_pace_mi_time_output, round(segment["average_heartrate"]),
                                    round(segment["max_heartrate"]))

    def _process_segments(self, activity, detailed):
        segments_string = "### Segments  \n"

        if detailed is True:
            segments_string += "| Segment | Time | Distance | Pace | Avg. Heart Rate | Max Heart Rate |  \n"
            segments_string += "| ----- | ----- | ----- | ----- | ----- | ----- |  \n"

        for s in activity["segment_efforts"]:
            segments_string += self._process_segment(s, detailed)

        return segments_string

    def _process_split(self, split, metric):
        moving_time = time.gmtime(split["moving_time"])

        if split["moving_time"] > 3599:
            moving_time_output = time.strftime("%H:%M:%S", moving_time)
        else:
            moving_time_output = time.strftime("%M:%S", moving_time)

        speed = round(split["average_speed"] * 3.6, 2)
        if metric is False:
            speed = round(speed * 0.6213712, 2)

        if metric:
            speed_suffix = "kph"
        else:
            speed_suffix = "mph"

        return "| {0} | {1} | {2} {3} | {4} bpm |  \n".format(split["split"], moving_time_output, speed,
                                                              speed_suffix, round(split["average_heartrate"]))

    def _process_splits(self, activity, metric):
        splits_string = ""

        if metric:
            splits_string += "#### Kilometres  \n"
            splits = activity["splits_metric"]
        else:
            splits_string += "#### Miles  \n"
            splits = activity["splits_standard"]

        splits_string += "| Split | Time | Speed | Heart Rate |  \n"
        splits_string += "| ----- | ----- | ----- | ----- |  \n"

        for s in splits:
            splits_string += self._process_split(s, metric)

        return splits_string

    def _process_activity_details(self, activity):
        description = "{0}  \n".format(activity["description"]) if activity["description"] is not None else ""
        distance_km = round(activity["distance"] / 1000, 2)
        distance_mi = round((activity["distance"] / 1000) * 0.6213712, 2)
        moving_time = time.gmtime(activity["moving_time"])
        elapsed_time = time.gmtime(activity["elapsed_time"])

        if activity["moving_time"] > 3599:
            moving_time_output = time.strftime("%H:%M:%S", moving_time)
        else:
            moving_time_output = time.strftime("%M:%S", moving_time)

        if activity["elapsed_time"] > 3599:
            elapsed_time_output = time.strftime("%H:%M:%S", elapsed_time)
        else:
            elapsed_time_output = time.strftime("%M:%S", elapsed_time)

        pace_km_seconds = float(activity["moving_time"]) / float(distance_km)
        pace_km_time = time.gmtime(pace_km_seconds)
        pace_km_time_output = time.strftime("%M:%S", pace_km_time)

        segment_pace_mi_seconds = float(activity["moving_time"]) / float(distance_mi)
        segment_pace_mi_time = time.gmtime(segment_pace_mi_seconds)
        pace_mi_time_output = time.strftime("%M:%S", segment_pace_mi_time)

        avg_speed_kmh = round(activity["average_speed"] * 3.6, 2)
        avg_speed_mph = round(avg_speed_kmh * 0.6213712, 2)
        max_speed_kmh = round(activity["max_speed"] * 3.6, 2)
        max_speed_mph = round(max_speed_kmh * 0.6213712, 2)

        activity_details_string = "# {0}  \n".format(activity["name"])
        activity_details_string += description
        activity_details_string += "|       |       |       |  \n"
        activity_details_string += "| ----- | ----- | ----- |  \n"
        activity_details_string += "| **Time:** | {0} moving | {1} total |  \n".format(moving_time_output,
                                                                                       elapsed_time_output)
        activity_details_string += "| **Distance:** | {0}km | {1}mi |  \n".format(distance_km, distance_mi)
        activity_details_string += "| **Pace:** | {0} min/km | {1} min/mi |  \n".format(pace_km_time_output,
                                                                                        pace_mi_time_output)
        activity_details_string += "| **Avg. Speed:** | {0} kph | {1} mph |  \n".format(avg_speed_kmh, avg_speed_mph)
        activity_details_string += "| **Max Speed:** | {0} kph | {1} mph |  \n".format(max_speed_kmh, max_speed_mph)

        if activity["has_heartrate"]:
            activity_details_string += "| **Heart Rate:** | {0} bpm avg | {1} bpm max |  \n".format(
                round(activity["average_heartrate"]), round(activity["max_heartrate"]))

        activity_details_string += "  \n[{attachment}]"

        return activity_details_string

    def _process_comments(self, comments):
        comment_string = '### Comments\n'
        for c in comments:
            comment_string += "**{0} {1}** {2}  \n".format(c["athlete"]["firstname"], c["athlete"]["lastname"],
                                                           c["text"])

        return comment_string[:len(comment_string) - 2]

    def _process_kudos(self, kudos):
        kudos_string = '### Got Kudos From\n'
        for k in kudos:
            kudos_string += "{0} {1} ".format(k["firstname"], k["lastname"])

        return kudos_string

    def process_activity(self, include_kudos, include_comments, segments, which_splits):
        return_string = self._process_activity_details(self.activity)

        if include_kudos and self.kudos:
            return_string += "  \n{0}".format(self._process_kudos(self.kudos))

        if include_comments and self.comments:
            return_string += "  \n{0}".format(self._process_comments(self.comments))

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

        return return_string
