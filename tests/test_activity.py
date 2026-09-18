from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from urllib.error import URLError
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import update_activity as activity


NOW = datetime(2026, 9, 18, 12, tzinfo=timezone.utc)


def event(identifier="1", **overrides):
    item = {"id": identifier, "public": True, "actor": {"login": "scakki"},
            "repo": {"name": "RoLACLab/example"}, "type": "PushEvent",
            "created_at": (NOW - timedelta(days=1)).isoformat()}
    item.update(overrides)
    return item


class ActivityTests(unittest.TestCase):
    def test_only_public_work_by_this_user_in_this_org_is_selected(self):
        events = [event(), event("2", public=False), event("3", actor={"login": "colleague"}),
                  event("4", repo={"name": "RoLACLab-other/example"}),
                  event("5", type="WatchEvent"),
                  event("6", created_at=(NOW - timedelta(days=31)).isoformat()),
                  event("7", created_at=(NOW + timedelta(days=1)).isoformat())]
        result = activity.select_events(events, NOW)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["repo"], "RoLACLab/example")

    def test_case_insensitive_ownership_deduplication_and_order(self):
        recent = event("2", actor={"login": "SCAKKI"}, repo={"name": "rolaclab/new"},
                       created_at=NOW.isoformat())
        result = activity.select_events([event(), recent, recent], NOW)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["repo"], "rolaclab/new")

    def test_empty_window_does_not_claim_zero_lifetime_contributions(self):
        svg = activity.render_svg([], NOW)
        ET.fromstring(svg)
        self.assertIn("No public lab events in the current window", svg)
        self.assertIn("Checked 18 Sep 2026", svg)
        self.assertNotIn("0 contributions", svg)

    def test_svg_escapes_labels_and_counts_pushes_as_events(self):
        events = activity.select_events([event(repo={"name": "RoLACLab/<script>&"})], NOW)
        svg = activity.render_svg(events, NOW)
        ET.fromstring(svg)
        self.assertIn("&lt;script&gt;&amp;", svg)
        self.assertNotIn("<script>", svg)
        self.assertIn("Push events", svg)

    def test_fetch_paginates_public_endpoint_and_stops_at_end(self):
        with patch.object(activity, "urlopen") as request, patch.object(activity.json, "load") as load:
            load.side_effect = [[event(str(i)) for i in range(100)], [event("101")]]
            result = activity.fetch_events()
        self.assertEqual(len(result), 101)
        self.assertEqual(request.call_count, 2)
        self.assertTrue(all('/events/public?' in call.args[0].full_url for call in request.call_args_list))
        self.assertIn('page=2', request.call_args_list[1].args[0].full_url)

    def test_fetch_failure_retains_previous_card(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets").mkdir()
            card = root / "assets/rolac-activity.svg"
            card.write_text("last successful card")
            with patch.object(activity, "ROOT", root), patch.object(activity, "fetch_events", side_effect=URLError("offline")):
                with self.assertRaises(URLError):
                    activity.main()
            self.assertEqual(card.read_text(), "last successful card")


if __name__ == "__main__":
    unittest.main()
