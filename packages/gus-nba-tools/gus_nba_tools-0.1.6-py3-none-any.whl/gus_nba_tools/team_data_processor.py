import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog

class TeamDataProcessor:
    """
    Loads NBA team logs for a season and computes:
      - PTS_ALLOWED (opponent points)
      - DEF_LAST10 (rolling defensive average)
    Usage:
        processor = TeamDataProcessor("2023")
        df = processor.process()
    """

    def __init__(self, season):
        self.season = season
        self.team_ids = [t["id"] for t in teams.get_teams()]

    def _load_team_logs(self):
        frames = []
        for tid in self.team_ids:
            df = teamgamelog.TeamGameLog(
                team_id=tid,
                season=self.season
            ).get_data_frames()[0]

            df["TEAM_ID"] = tid
            frames.append(df)

        return pd.concat(frames, ignore_index=True)

    def _add_pts_allowed(self, df):
        opp = df[["Game_ID", "TEAM_ID", "PTS"]].rename(
            columns={"TEAM_ID": "OPP_TEAM_ID", "PTS": "PTS_ALLOWED"}
        )

        merged = df.merge(opp, on="Game_ID")
        merged = merged[merged["TEAM_ID"] != merged["OPP_TEAM_ID"]]

        return merged

    def _add_def_last10(self, df):
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
        df = df.sort_values(["TEAM_ID", "GAME_DATE"])

        df["DEF_LAST10"] = (
            df.groupby("TEAM_ID")["PTS_ALLOWED"]
              .rolling(window=10, min_periods=5)
              .mean()
              .shift(1)
              .reset_index(level=0, drop=True)
        )

        return df

    def process(self):
        df = self._load_team_logs()
        df = self._add_pts_allowed(df)
        df = self._add_def_last10(df)
        return df.reset_index(drop=True)
