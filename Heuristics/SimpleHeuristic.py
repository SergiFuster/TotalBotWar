"""Defines a simple reward for the current `TotalBotWar.Players.Player.Player` given an
`TotalBotWar.Game.Observation.Observation` by using the current score difference."""


class SimpleHeuristic:
    """Defines a simple reward for the current `TotalBotWar.Players.Player.Player` given an
    `TotalBotWar.Game.Observation.Observation` by using the current score difference."""

# region Methods
    def get_reward(self, observation):
        """
        Returns a reward for the current `TotalBotWar.Players.Player.Player` given an
        `TotalBotWar.Game.Observation.Observation` by using the current health difference.
        :param observation: TotalBotWar.Game.Observation.Observation
        :return: float
        """
        team_0_health = self.get_team_health(observation, 0)
        team_1_health = self.get_team_health(observation, 1)

        return (team_0_health-team_1_health) if observation.turn == 0 else (team_1_health - team_0_health)

    def get_team_health(self, observation, team):
        health = 0
        if team == 0:
            for unit in observation.player_0_units:
                health += unit.health if unit.health > 0 else 0
        else:
            for unit in observation.player_1_units:
                health += unit.health if unit.health > 0 else 0
        return health
# endregion
