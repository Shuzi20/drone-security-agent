class ContextManager:
    def __init__(self):
        self.frame_history = []
        self.alert_history = []
        self.feedback_log = []

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

    def get_false_positives(self):
        fp = [f for f in self.feedback_log if not f["correct"]]
        if not fp:
            return ""
        rules = list(set([f["rule"] for f in fp]))
        return f"Previously incorrect alerts for rules: {', '.join(rules)}. Be careful with these."