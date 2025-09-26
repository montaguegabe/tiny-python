"""Test the example from the README to ensure it works correctly."""

from dataclasses import dataclass
from typing import List, Optional

from tiny_python import tiny_eval_last, tiny_exec


def test_readme_organization_example():
    """Test the organization example from the README."""

    # Define dataclasses that model an organization
    @dataclass
    class Person:
        name: str
        role: str
        team: Optional["Team"] = None

    @dataclass
    class Team:
        name: str
        description: str
        leader: Optional[Person] = None
        members: List[Person] = None

        def __post_init__(self):
            if self.members is None:
                self.members = []

    @dataclass
    class Project:
        title: str
        team: Team
        budget: float
        priority: int

    # Use tiny_exec to safely execute code that builds complex structures
    code = """
# Create team members
alice = Person("Alice", "Engineer")
bob = Person("Bob", "Designer")
charlie = Person("Charlie", "Manager")

# Create a team with a leader
dev_team = Team("Development Team", "Builds awesome products", charlie)
dev_team.members = [alice, bob, charlie]

# Set team references (creating cycles)
alice.team = dev_team
bob.team = dev_team
charlie.team = dev_team

# Create a project for this team
project = Project("New Website", dev_team, 50000.0, 1)

# Calculate some metrics
team_size = len(dev_team.members)
budget_per_person = project.budget / team_size
high_priority = project.priority == 1

# Store results in a summary
summary = {
    "project_name": project.title,
    "team_leader": dev_team.leader.name,
    "team_size": team_size,
    "budget_per_person": budget_per_person,
    "is_high_priority": high_priority
}
"""

    # Execute the code safely with the allowed dataclasses
    result = tiny_exec(code, allowed_classes=[Person, Team, Project])

    # Verify the summary was created correctly
    assert "summary" in result
    summary = result["summary"]
    assert summary["project_name"] == "New Website"
    assert summary["team_leader"] == "Charlie"
    assert summary["team_size"] == 3
    assert abs(summary["budget_per_person"] - 16666.67) < 0.01
    assert summary["is_high_priority"] is True

    # Verify the team structure
    assert "dev_team" in result
    dev_team = result["dev_team"]
    assert isinstance(dev_team, Team)
    assert dev_team.name == "Development Team"
    assert dev_team.description == "Builds awesome products"
    assert dev_team.leader.name == "Charlie"
    assert len(dev_team.members) == 3

    # Verify individual people
    assert "alice" in result
    assert "bob" in result
    assert "charlie" in result

    alice = result["alice"]
    bob = result["bob"]
    charlie = result["charlie"]

    assert isinstance(alice, Person)
    assert isinstance(bob, Person)
    assert isinstance(charlie, Person)

    assert alice.name == "Alice"
    assert alice.role == "Engineer"
    assert bob.name == "Bob"
    assert bob.role == "Designer"
    assert charlie.name == "Charlie"
    assert charlie.role == "Manager"

    # Verify circular references work
    assert alice.team is dev_team
    assert bob.team is dev_team
    assert charlie.team is dev_team
    assert dev_team.leader is charlie

    # Verify the project
    assert "project" in result
    project = result["project"]
    assert isinstance(project, Project)
    assert project.title == "New Website"
    assert project.team is dev_team
    assert project.budget == 50000.0
    assert project.priority == 1

    # Verify calculated values
    assert result["team_size"] == 3
    assert abs(result["budget_per_person"] - 16666.67) < 0.01
    assert result["high_priority"] is True


def test_readme_simple_math_example():
    """Test the simple math example from the README."""
    last_value = tiny_eval_last("2 + 3 * 4")
    assert last_value == 14


def test_readme_members_initialization():
    """Test that the Team.members initialization works correctly."""

    @dataclass
    class Person:
        name: str
        role: str

    @dataclass
    class Team:
        name: str
        description: str
        leader: Optional[Person] = None
        members: List[Person] = None

        def __post_init__(self):
            if self.members is None:
                self.members = []

    code = """
# Create a team without specifying members initially
team1 = Team("Team One", "First team")

# Create a team with members specified
leader = Person("Leader", "Manager")
team2 = Team("Team Two", "Second team", leader, [leader])
team2_member_count = len(team2.members)
"""

    result = tiny_exec(code, allowed_classes=[Person, Team])

    # Team 1 should have None for members since __post_init__ isn't called
    assert result["team1"].members is None

    # Team 2 should have the specified member
    assert result["team2_member_count"] == 1
    assert len(result["team2"].members) == 1
    assert result["team2"].members[0].name == "Leader"
