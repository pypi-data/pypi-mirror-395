"""
Unit tests for the AgentCardBuilder class.
"""

import pytest
from synqed.agent_card import AgentCardBuilder
from a2a.types import AgentCard, AgentSkill


class TestAgentCardBuilder:
    """Tests for the AgentCardBuilder class."""
    
    def test_basic_card_creation(self):
        """Test creating a basic agent card."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="A test agent",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        card = builder.build()
        
        assert isinstance(card, AgentCard)
        assert card.name == "Test Agent"
        assert card.description == "A test agent"
        assert card.version == "1.0.0"
        assert card.url == "http://localhost:8000"
    
    def test_add_skill(self):
        """Test adding skills to the card."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.add_skill(
            skill_id="cooking",
            name="Cooking",
            description="Prepare meals",
            tags=["food", "recipes"]
        )
        
        card = builder.build()
        
        assert len(card.skills) == 1
        assert card.skills[0].id == "cooking"
        assert card.skills[0].name == "Cooking"
        assert "food" in card.skills[0].tags
    
    def test_add_multiple_skills(self):
        """Test adding multiple skills."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.add_skill(
            skill_id="skill1",
            name="Skill 1",
            description="First skill",
            tags=["tag1"]
        ).add_skill(
            skill_id="skill2",
            name="Skill 2",
            description="Second skill",
            tags=["tag2"]
        )
        
        card = builder.build()
        
        assert len(card.skills) == 2
    
    def test_set_capabilities(self):
        """Test setting agent capabilities."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_capabilities(
            streaming=True,
            push_notifications=True,
            state_transition_history=True
        )
        
        card = builder.build()
        
        assert card.capabilities.streaming is True
        assert card.capabilities.push_notifications is True
        assert card.capabilities.state_transition_history is True
    
    def test_set_default_modes(self):
        """Test setting default input/output modes."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_default_input_modes(["application/json"])
        builder.set_default_output_modes(["text/html", "application/json"])
        
        card = builder.build()
        
        assert card.default_input_modes == ["application/json"]
        assert "text/html" in card.default_output_modes
    
    def test_add_interface(self):
        """Test adding additional interfaces."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.add_interface(
            url="http://localhost:8001",
            transport="GRPC"
        )
        
        card = builder.build()
        
        assert card.additional_interfaces is not None
        assert len(card.additional_interfaces) == 1
        assert card.additional_interfaces[0].url == "http://localhost:8001"
        assert card.additional_interfaces[0].transport == "GRPC"
    
    def test_set_provider(self):
        """Test setting provider information."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_provider(
            organization="Test Org",
            url="https://test.org"
        )
        
        card = builder.build()
        
        assert card.provider is not None
        assert card.provider.organization == "Test Org"
        assert card.provider.url == "https://test.org"
    
    def test_set_documentation_url(self):
        """Test setting documentation URL."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_documentation_url("https://docs.test.com")
        
        card = builder.build()
        
        assert card.documentation_url == "https://docs.test.com"
    
    def test_set_icon_url(self):
        """Test setting icon URL."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_icon_url("https://test.com/icon.png")
        
        card = builder.build()
        
        assert card.icon_url == "https://test.com/icon.png"
    
    def test_update_url(self):
        """Test updating the URL."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        builder.set_url("http://newhost:9000")
        
        card = builder.build()
        
        assert card.url == "http://newhost:9000"
    
    def test_fluent_interface(self):
        """Test that builder methods return self for chaining."""
        builder = AgentCardBuilder(
            name="Test Agent",
            description="Test",
            version="1.0.0",
            url="http://localhost:8000"
        )
        
        result = (builder
                 .add_skill("skill1", "Skill 1", "Test", ["tag"])
                 .set_capabilities(streaming=True)
                 .set_documentation_url("https://docs")
                 .set_icon_url("https://icon"))
        
        assert result is builder
        
        card = builder.build()
        assert len(card.skills) == 1
        assert card.capabilities.streaming is True

