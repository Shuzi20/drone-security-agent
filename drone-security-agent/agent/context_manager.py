from collections import Counter

class ContextManager:
    def __init__(self):
        self.frame_history = []
        self.alert_history = []

    def add_frame(self, frame):
        self.frame_history.append(frame)

    def add_alert(self, alert):
        self.alert_history.append(alert)

    def get_history_summary(self):
        if not self.frame_history:
            return "No previous frames."
        lines = []
        for f in self.frame_history[-5:]:
            lines.append(f"Frame {f['frame_id']} at {f['time']} ({f['location']}): {f['description'][:80]}")
        return "\n".join(lines)

    def get_patterns(self):
        patterns = []

        # Location frequency
        locations = [f["location"] for f in self.frame_history]
        location_counts = Counter(locations)
        for location, count in location_counts.items():
            if count >= 2:
                patterns.append(f"[PATTERN] {location} has triggered activity {count} times today — high risk zone")

        # Vehicle repeat
        vehicle_frames = [
            f for f in self.frame_history
            if "truck" in f["description"].lower() or "vehicle" in f["description"].lower()
        ]
        if len(vehicle_frames) >= 2:
            patterns.append(f"[PATTERN] Vehicle has appeared {len(vehicle_frames)} times today")

        # Person repeat
        person_frames = [
            f for f in self.frame_history
            if "person" in f["description"].lower()
        ]
        if len(person_frames) >= 2:
            patterns.append(f"[PATTERN] Person detected {len(person_frames)} times today — possible surveillance")

        return patterns

    def get_alert_counts(self):
        counts = Counter([a["severity"] for a in self.alert_history])
        return counts