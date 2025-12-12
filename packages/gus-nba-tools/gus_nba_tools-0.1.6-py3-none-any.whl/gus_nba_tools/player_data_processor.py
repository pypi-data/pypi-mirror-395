
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog

class PlayerGameProcessor:
    """
    Processes a rookie player's game logs for a given NBA season.
    Adds features:
    - Opponent team code
    - Home/Away
    - Consecutive away streak
    - Rolling 5-game averages for PTS, MIN, USG, FG%
    - Back-to-back indicator
    """

    def __init__(self, player_name, season):
        self.player_name = player_name
        self.season = season
        self.player_id = self._get_player_id()

    def _get_player_id(self):
        all_players = players.get_players()
        try:
            return next(p['id'] for p in all_players if p['full_name'] == self.player_name)
        except StopIteration:
            raise ValueError(f"Player not found: {self.player_name}")
    
    def _home_away(self, matchup):
        return 0 if "vs." in matchup else 1

    def _away_streak(self, away_column):
        streaks = []
        streak = 0
        for value in away_column:
            if value == 1:  # away
                streak += 1
            else:
                streak = 0
            streaks.append(streak)
        return streaks

    def _usage(self, df):
        # Possession approximation
        return (df['FGA'] + 0.44 * df['FTA']) / df['MIN']

    def _rolling_feature(self, series, window=5):
        return series.rolling(window).mean().shift(1)  # shift prevents leakage

    def process(self):
        gamelog = playergamelog.PlayerGameLog(player_id=self.player_id, season=self.season)
        df = gamelog.get_data_frames()[0]

        df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
        df = df.sort_values('GAME_DATE')

        df['OPP'] = df['MATCHUP'].apply(lambda x: x.split(" ")[-1])

        df['AWAY'] = df['MATCHUP'].apply(self._home_away)

        df['AWAY_STREAK'] = self._away_streak(df['AWAY'])

        df['USG'] = self._usage(df)

        df['PTS_5'] = self._rolling_feature(df['PTS'])
        df['MIN_5'] = self._rolling_feature(df['MIN'])
        df['USG_5'] = self._rolling_feature(df['USG'])
        df['FG_PCT_5'] = self._rolling_feature(df['FG_PCT'])

        df["REST_DAYS"] = df["GAME_DATE"].diff().dt.days

        df["BACK_TO_BACK"] = (df["REST_DAYS"] == 1).astype(int)
        
        return df.reset_index(drop=True)
