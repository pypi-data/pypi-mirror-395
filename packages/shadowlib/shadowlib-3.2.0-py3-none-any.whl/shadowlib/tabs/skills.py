"""
Skills tab module.
"""

from typing import Dict, List

from shadowlib.types.gametab import GameTab, GameTabs

# Ordered list of skill names (matching game order)
# Note: Also defined in state_builder.py to avoid circular import
SKILL_NAMES: List[str] = [
    "Attack",
    "Defence",
    "Strength",
    "Hitpoints",
    "Ranged",
    "Prayer",
    "Magic",
    "Cooking",
    "Woodcutting",
    "Fletching",
    "Fishing",
    "Firemaking",
    "Crafting",
    "Smithing",
    "Mining",
    "Herblore",
    "Agility",
    "Thieving",
    "Slayer",
    "Farming",
    "Runecrafting",
    "Hunter",
    "Construction",
    "Sailing",
]


class Skills(GameTabs):
    """
    Singleton skills tab operations class.

    Example:
        from shadowlib.tabs.skills import skills

        level = skills.getLevel("Attack")
    """

    TAB_TYPE = GameTab.SKILLS

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        """Actual initialization, runs once."""
        GameTabs.__init__(self)
        self._last_total_xp: int | None = None

    def _getSkillData(self, skill_name: str) -> Dict[str, int]:
        """
        Helper to get skill data from cache.

        Args:
            skill_name: Skill name (e.g., "Attack", "Fishing")

        Returns:
            Dict with 'level', 'xp', 'boosted_level'
        """
        from shadowlib.client import client

        # Get from cache
        data = client.cache.getAllSkills().get(skill_name)
        if data:
            return data

        # Default fallback
        return {"level": 1, "xp": 0, "boosted_level": 1}

    def getLevel(self, skill_name: str) -> int:
        """
        Get current boosted level for a skill.

        Args:
            skill_name: Skill name (e.g., "Attack", "Fishing")

        Returns:
            Current boosted skill level

        Example:
            attack_level = skills.getLevel("Attack")
            print(f"Attack level: {attack_level}")
        """
        return self._getSkillData(skill_name)["boosted_level"]

    def getRealLevel(self, skill_name: str) -> int:
        """
        Get real (unboosted) level for a skill.

        Args:
            skill_name: Skill name (e.g., "Attack", "Fishing")

        Returns:
            Real skill level without boosts

        Example:
            real_attack = skills.getRealLevel("Attack")
            print(f"Real attack level: {real_attack}")
        """
        return self._getSkillData(skill_name)["level"]

    def getExperience(self, skill_name: str) -> int:
        """
        Get experience for a skill.

        Args:
            skill_name: Skill name (e.g., "Attack", "Fishing")

        Returns:
            Experience amount

        Example:
            xp = skills.getExperience("Woodcutting")
            print(f"Woodcutting XP: {xp}")
        """
        return self._getSkillData(skill_name)["xp"]

    def getTotalLevel(self) -> int:
        """
        Get total level across all skills.

        Returns:
            Sum of all real skill levels

        Example:
            total = skills.getTotalLevel()
            print(f"Total level: {total}")
        """
        from shadowlib.client import client

        skills_data = client.cache.getAllSkills()
        return sum(data["level"] for data in skills_data.values())

    def getTotalExperience(self) -> int:
        """
        Get total experience across all skills.

        Returns:
            Total XP amount

        Example:
            total_xp = skills.getTotalExperience()
            print(f"Total XP: {total_xp}")
        """
        from shadowlib.client import client

        skills_data = client.cache.getAllSkills()
        return sum(data["xp"] for data in skills_data.values())

    def gainedXp(self) -> bool:
        """
        Check if XP was gained since last check.

        Returns:
            True if XP increased since last call to gainedXp() or waitXp()

        Example:
            if skills.gainedXp():
                print("XP gained!")
        """
        current_xp = self.getTotalExperience()

        # Initialize on first call
        if self._last_total_xp is None:
            self._last_total_xp = current_xp
            return False

        # Check if gained
        if current_xp > self._last_total_xp:
            self._last_total_xp = current_xp
            return True

        return False

    def waitXp(self, timeout: float = 5.0) -> bool:
        """
        Wait for XP gain with timeout.

        Args:
            timeout: Maximum time to wait in seconds (default: 5.0)

        Returns:
            True if XP was gained, False if timeout occurred

        Example:
            if skills.waitXp(timeout=10.0):
                print("XP gained!")
            else:
                print("No XP gained within timeout")
        """
        import time

        # Initialize baseline
        if self._last_total_xp is None:
            self._last_total_xp = self.getTotalExperience()

        # Check if already gained
        if self.gainedXp():
            return True

        # Wait for XP gain
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.gainedXp():
                return True
            time.sleep(0.05)

        return False


# Module-level singleton instance
skills = Skills()
