"""
Unit tests for conversation history system
Tests conversation CRUD operations, message saving, and role isolation
"""
import pytest
from httpx import AsyncClient
from datetime import datetime
from bson import ObjectId

# Test data
TEST_USER_STUDENT = {
    "email": "test_student_conv@example.com",
    "password": "testpass123",
    "full_name": "Test Student Conversation",
    "role": "student"
}

TEST_USER_TEACHER = {
    "email": "test_teacher_conv@example.com",
    "password": "testpass123",
    "full_name": "Test Teacher Conversation",
    "role": "teacher"
}

TEST_USER_2 = {
    "email": "test_student2_conv@example.com",
    "password": "testpass123",
    "full_name": "Test Student 2",
    "role": "student"
}


@pytest.fixture
async def student_token(client: AsyncClient):
    """Get authentication token for test student"""
    # Register
    await client.post("/auth/register", json=TEST_USER_STUDENT)
    
    # Login
    response = await client.post("/auth/login", json={
        "email": TEST_USER_STUDENT["email"],
        "password": TEST_USER_STUDENT["password"]
    })
    
    data = response.json()
    return data["access_token"]


@pytest.fixture
async def teacher_token(client: AsyncClient):
    """Get authentication token for test teacher"""
    # Register
    await client.post("/auth/register", json=TEST_USER_TEACHER)
    
    # Login
    response = await client.post("/auth/login", json={
        "email": TEST_USER_TEACHER["email"],
        "password": TEST_USER_TEACHER["password"]
    })
    
    data = response.json()
    return data["access_token"]


@pytest.fixture
async def student2_token(client: AsyncClient):
    """Get authentication token for second test student"""
    # Register
    await client.post("/auth/register", json=TEST_USER_2)
    
    # Login
    response = await client.post("/auth/login", json={
        "email": TEST_USER_2["email"],
        "password": TEST_USER_2["password"]
    })
    
    data = response.json()
    return data["access_token"]


class TestConversationCreation:
    """Test automatic conversation creation when asking questions"""
    
    @pytest.mark.asyncio
    async def test_first_question_creates_conversation(self, client: AsyncClient, student_token: str):
        """Test that asking the first question creates a new conversation"""
        # Clear any existing conversations
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Ask a question
        response = await client.post(
            "/assistant/ask",
            json={"question": "What is Python?"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        assert "answer" in response.json()
        
        # Check that conversation was created
        conv_response = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert conv_response.status_code == 200
        conversations = conv_response.json()
        assert len(conversations) == 1
        assert conversations[0]["messageCount"] == 2  # user + assistant
    
    @pytest.mark.asyncio
    async def test_second_question_appends_to_conversation(self, client: AsyncClient, student_token: str):
        """Test that subsequent questions append to existing conversation"""
        # Clear conversations
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Ask first question
        await client.post(
            "/assistant/ask",
            json={"question": "What is Python?"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Ask second question
        await client.post(
            "/assistant/ask",
            json={"question": "What is JavaScript?"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Check conversations
        conv_response = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        conversations = conv_response.json()
        assert len(conversations) == 1
        assert conversations[0]["messageCount"] == 4  # 2 questions + 2 answers
    
    @pytest.mark.asyncio
    async def test_message_structure(self, client: AsyncClient, student_token: str):
        """Test that messages have correct structure"""
        # Clear conversations
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Ask question
        question_text = "Test question for structure"
        await client.post(
            "/assistant/ask",
            json={"question": question_text},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get conversation
        conv_list = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        conv_id = conv_list.json()[0]["_id"]
        
        conv_response = await client.get(
            f"/assistant/conversation/{conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        conversation = conv_response.json()
        messages = conversation["messages"]
        
        # Check user message
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == question_text
        assert "timestamp" in messages[0]
        
        # Check assistant message
        assert messages[1]["role"] == "assistant"
        assert len(messages[1]["content"]) > 0
        assert "timestamp" in messages[1]


class TestConversationRetrieval:
    """Test retrieving conversations"""
    
    @pytest.mark.asyncio
    async def test_get_all_conversations(self, client: AsyncClient, student_token: str):
        """Test getting all conversations for a user"""
        # Clear and create test data
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Create multiple conversations
        await client.post(
            "/assistant/ask",
            json={"question": "Question 1"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        response = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        conversations = response.json()
        assert len(conversations) >= 1
        assert all("_id" in conv for conv in conversations)
        assert all("messageCount" in conv for conv in conversations)
    
    @pytest.mark.asyncio
    async def test_get_specific_conversation(self, client: AsyncClient, student_token: str):
        """Test getting a specific conversation by ID"""
        # Clear and create test conversation
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        await client.post(
            "/assistant/ask",
            json={"question": "Test question"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get conversation ID
        conv_list = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        conv_id = conv_list.json()[0]["_id"]
        
        # Get specific conversation
        response = await client.get(
            f"/assistant/conversation/{conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        conversation = response.json()
        assert conversation["_id"] == conv_id
        assert "messages" in conversation
        assert len(conversation["messages"]) >= 2
    
    @pytest.mark.asyncio
    async def test_get_invalid_conversation_id(self, client: AsyncClient, student_token: str):
        """Test getting conversation with invalid ID"""
        response = await client.get(
            "/assistant/conversation/invalid_id",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 400
        assert "Invalid conversation ID" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_conversation(self, client: AsyncClient, student_token: str):
        """Test getting conversation that doesn't exist"""
        fake_id = str(ObjectId())
        
        response = await client.get(
            f"/assistant/conversation/{fake_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestConversationDeletion:
    """Test deleting conversations"""
    
    @pytest.mark.asyncio
    async def test_delete_single_conversation(self, client: AsyncClient, student_token: str):
        """Test deleting a single conversation"""
        # Create conversation
        await client.post(
            "/assistant/ask",
            json={"question": "To be deleted"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get conversation ID
        conv_list = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        initial_count = len(conv_list.json())
        conv_id = conv_list.json()[0]["_id"]
        
        # Delete conversation
        response = await client.delete(
            f"/assistant/conversation/{conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()
        
        # Verify deletion
        conv_list_after = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert len(conv_list_after.json()) == initial_count - 1
    
    @pytest.mark.asyncio
    async def test_clear_all_conversations(self, client: AsyncClient, student_token: str):
        """Test clearing all conversations"""
        # Create multiple conversations
        for i in range(3):
            await client.post(
                "/assistant/ask",
                json={"question": f"Question {i}"},
                headers={"Authorization": f"Bearer {student_token}"}
            )
        
        # Clear all
        response = await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == 200
        assert "cleared" in response.json()["message"].lower()
        
        # Verify all deleted
        conv_list = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert len(conv_list.json()) == 0
    
    @pytest.mark.asyncio
    async def test_delete_message_from_conversation(self, client: AsyncClient, student_token: str):
        """Test deleting a specific message from conversation"""
        # Clear and create conversation with multiple messages
        await client.delete(
            "/assistant/conversations/clear",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        await client.post(
            "/assistant/ask",
            json={"question": "Question 1"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        await client.post(
            "/assistant/ask",
            json={"question": "Question 2"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get conversation
        conv_list = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        conv_id = conv_list.json()[0]["_id"]
        
        # Get initial message count
        conv_response = await client.get(
            f"/assistant/conversation/{conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        initial_message_count = len(conv_response.json()["messages"])
        
        # Delete message at index 0
        delete_response = await client.delete(
            f"/assistant/conversation/{conv_id}/message/0",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert delete_response.status_code == 200
        
        # Verify message was deleted
        conv_after = await client.get(
            f"/assistant/conversation/{conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert len(conv_after.json()["messages"]) == initial_message_count - 1


class TestRoleIsolation:
    """Test that users can only access their own conversations"""
    
    @pytest.mark.asyncio
    async def test_user_cannot_see_other_user_conversations(
        self, 
        client: AsyncClient, 
        student_token: str,
        student2_token: str
    ):
        """Test that User A cannot see User B's conversations"""
        # User 1 creates conversation
        await client.post(
            "/assistant/ask",
            json={"question": "User 1 question"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get User 1's conversation ID
        conv_list_user1 = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        user1_conv_id = conv_list_user1.json()[0]["_id"]
        
        # User 2 tries to access User 1's conversation
        response = await client.get(
            f"/assistant/conversation/{user1_conv_id}",
            headers={"Authorization": f"Bearer {student2_token}"}
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_user_cannot_delete_other_user_conversations(
        self,
        client: AsyncClient,
        student_token: str,
        student2_token: str
    ):
        """Test that User A cannot delete User B's conversations"""
        # User 1 creates conversation
        await client.post(
            "/assistant/ask",
            json={"question": "User 1 question"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get User 1's conversation ID
        conv_list_user1 = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        user1_conv_id = conv_list_user1.json()[0]["_id"]
        
        # User 2 tries to delete User 1's conversation
        response = await client.delete(
            f"/assistant/conversation/{user1_conv_id}",
            headers={"Authorization": f"Bearer {student2_token}"}
        )
        
        assert response.status_code == 404
        
        # Verify User 1's conversation still exists
        verify_response = await client.get(
            f"/assistant/conversation/{user1_conv_id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert verify_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_teacher_and_student_separate_conversations(
        self,
        client: AsyncClient,
        student_token: str,
        teacher_token: str
    ):
        """Test that teachers and students have separate conversation spaces"""
        # Student creates conversation
        await client.post(
            "/assistant/ask",
            json={"question": "Student question"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Teacher creates conversation
        await client.post(
            "/assistant/ask",
            json={"question": "Teacher question"},
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        
        # Get student conversations
        student_convs = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        # Get teacher conversations
        teacher_convs = await client.get(
            "/assistant/conversations",
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        
        # Verify they're different
        student_ids = [c["_id"] for c in student_convs.json()]
        teacher_ids = [c["_id"] for c in teacher_convs.json()]
        
        assert len(set(student_ids) & set(teacher_ids)) == 0


class TestAuthenticationRequired:
    """Test that all conversation routes require authentication"""
    
    @pytest.mark.asyncio
    async def test_get_conversations_requires_auth(self, client: AsyncClient):
        """Test that getting conversations requires authentication"""
        response = await client.get("/assistant/conversations")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_get_conversation_requires_auth(self, client: AsyncClient):
        """Test that getting specific conversation requires authentication"""
        fake_id = str(ObjectId())
        response = await client.get(f"/assistant/conversation/{fake_id}")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_delete_conversation_requires_auth(self, client: AsyncClient):
        """Test that deleting conversation requires authentication"""
        fake_id = str(ObjectId())
        response = await client.delete(f"/assistant/conversation/{fake_id}")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_clear_conversations_requires_auth(self, client: AsyncClient):
        """Test that clearing conversations requires authentication"""
        response = await client.delete("/assistant/conversations/clear")
        assert response.status_code == 401
