import pandas as pd

class PlayerOpponentMerger:
    """
    Merges player game logs with opponent defensive stats from team logs.
    """

    def __init__(self, player_df, team_df):
        self.player_df = player_df.copy()
        self.team_df = team_df.copy()

        self.player_df["PLAYER_TEAM_ABBR"] = self.player_df["MATCHUP"].str.extract(r"^([A-Z]{2,3})")
        self.team_df["TEAM_ABBR"] = self.team_df["MATCHUP"].str.extract(r"^([A-Z]{2,3})")

    def _prepare_opponent_table(self):
        return self.team_df[[
            "Game_ID",
            "TEAM_ABBR",
            "DEF_LAST10"
        ]].rename(columns={"TEAM_ABBR": "OPP_TEAM_ABBR"})

    def merge(self):
        opp_df = self._prepare_opponent_table()

        merged = self.player_df.merge(opp_df, on="Game_ID", how="left")

        merged = merged[merged["OPP_TEAM_ABBR"] != merged["PLAYER_TEAM_ABBR"]]

        return merged.reset_index(drop=True)