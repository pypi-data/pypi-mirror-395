"""JIRA评论功能的单元测试.

遵循G7E6标准：
- AAA模式（Arrange-Act-Assert）
- pytest + pytest-mock框架
- 覆盖率目标：≥50%
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from jira_mcp.server import format_comment, get_issue_comments, add_comment


class TestFormatComment:
    """测试format_comment函数."""

    def test_format_comment_with_basic_fields(self):
        """测试格式化基本字段."""
        # Arrange - 准备测试数据
        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "这是一条测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:30:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        # Act - 执行测试
        result = format_comment(mock_comment)

        # Assert - 验证结果
        assert result["id"] == "12345"
        assert result["body"] == "这是一条测试评论"
        assert result["created"] == "2025-01-24T10:00:00.000+0800"
        assert result["updated"] == "2025-01-24T10:30:00.000+0800"

    def test_format_comment_with_empty_body(self):
        """测试空评论内容的处理."""
        # Arrange
        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = None
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证空内容被转换为空字符串
        assert result["body"] == ""

    def test_format_comment_with_author(self):
        """测试包含作者信息的评论."""
        # Arrange
        mock_author = Mock()
        mock_author.name = "zhangsan"
        mock_author.displayName = "张三"
        mock_author.emailAddress = "zhangsan@example.com"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = mock_author
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证作者信息
        assert "author" in result
        assert result["author"]["name"] == "zhangsan"
        assert result["author"]["display_name"] == "张三"
        assert result["author"]["email"] == "zhangsan@example.com"

    def test_format_comment_with_update_author(self):
        """测试包含更新者信息的评论."""
        # Arrange
        mock_update_author = Mock()
        mock_update_author.name = "lisi"
        mock_update_author.displayName = "李四"
        mock_update_author.emailAddress = "lisi@example.com"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:30:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = mock_update_author
        mock_comment.visibility = None

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证更新者信息
        assert "update_author" in result
        assert result["update_author"]["name"] == "lisi"
        assert result["update_author"]["display_name"] == "李四"
        assert result["update_author"]["email"] == "lisi@example.com"

    def test_format_comment_with_visibility_role(self):
        """测试包含角色可见性的评论."""
        # Arrange
        mock_visibility = Mock()
        mock_visibility.type = "role"
        mock_visibility.value = "Administrators"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "机密评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = None
        mock_comment.visibility = mock_visibility

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证可见性信息
        assert "visibility" in result
        assert result["visibility"]["type"] == "role"
        assert result["visibility"]["value"] == "Administrators"

    def test_format_comment_with_visibility_group(self):
        """测试包含组可见性的评论."""
        # Arrange
        mock_visibility = Mock()
        mock_visibility.type = "group"
        mock_visibility.value = "jira-developers"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "开发组可见评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = None
        mock_comment.visibility = mock_visibility

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证组可见性
        assert result["visibility"]["type"] == "group"
        assert result["visibility"]["value"] == "jira-developers"

    def test_format_comment_with_complete_metadata(self):
        """测试包含完整元数据的评论."""
        # Arrange - 创建完整的评论对象
        mock_author = Mock()
        mock_author.name = "zhangsan"
        mock_author.displayName = "张三"
        mock_author.emailAddress = "zhangsan@example.com"

        mock_update_author = Mock()
        mock_update_author.name = "lisi"
        mock_update_author.displayName = "李四"
        mock_update_author.emailAddress = "lisi@example.com"

        mock_visibility = Mock()
        mock_visibility.type = "role"
        mock_visibility.value = "Administrators"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "完整的测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:30:00.000+0800"
        mock_comment.author = mock_author
        mock_comment.updateAuthor = mock_update_author
        mock_comment.visibility = mock_visibility

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证所有字段都正确格式化
        assert result["id"] == "12345"
        assert result["body"] == "完整的测试评论"
        assert "author" in result
        assert "update_author" in result
        assert "visibility" in result

    def test_format_comment_with_missing_author_attributes(self):
        """测试作者对象缺少某些属性的情况."""
        # Arrange - 创建只有部分属性的作者
        mock_author = Mock(spec=["name"])  # 明确指定只有name属性
        mock_author.name = "zhangsan"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = mock_author
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证缺失的属性被处理为空字符串
        assert result["author"]["name"] == "zhangsan"
        assert result["author"]["display_name"] == ""
        assert result["author"]["email"] == ""

    def test_format_comment_without_author_attribute(self):
        """测试评论对象没有author属性的情况."""
        # Arrange
        mock_comment = Mock(spec=["id", "body", "created", "updated"])
        mock_comment.id = "12345"
        mock_comment.body = "测试评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"

        # Act
        result = format_comment(mock_comment)

        # Assert - 验证没有author字段
        assert "author" not in result


class TestGetIssueComments:
    """测试get_issue_comments工具函数."""

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_with_multiple_comments(self, mock_get_client):
        """测试获取多条评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        # 创建3条测试评论
        mock_comments = []
        for i in range(3):
            comment = Mock()
            comment.id = f"1234{i}"
            comment.body = f"测试评论{i+1}"
            comment.created = "2025-01-24T10:00:00.000+0800"
            comment.updated = "2025-01-24T10:00:00.000+0800"
            comment.author = None
            comment.updateAuthor = None
            comment.visibility = None
            mock_comments.append(comment)

        mock_client.comments.return_value = mock_comments

        # Act
        result = get_issue_comments("TEST-123")

        # Assert
        assert result["issue_key"] == "TEST-123"
        assert result["total"] == 3
        assert len(result["comments"]) == 3
        assert result["comments"][0]["body"] == "测试评论1"
        assert result["comments"][1]["body"] == "测试评论2"
        assert result["comments"][2]["body"] == "测试评论3"
        mock_client.comments.assert_called_once_with("TEST-123")

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_with_no_comments(self, mock_get_client):
        """测试没有评论的情况."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.comments.return_value = []

        # Act
        result = get_issue_comments("TEST-456")

        # Assert - 验证返回空列表
        assert result["issue_key"] == "TEST-456"
        assert result["total"] == 0
        assert result["comments"] == []

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_with_single_comment(self, mock_get_client):
        """测试单条评论的情况."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "唯一的评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:00:00.000+0800"
        mock_comment.author = None
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        mock_client.comments.return_value = [mock_comment]

        # Act
        result = get_issue_comments("TEST-789")

        # Assert
        assert result["total"] == 1
        assert result["comments"][0]["id"] == "12345"
        assert result["comments"][0]["body"] == "唯一的评论"

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_with_exception(self, mock_get_client):
        """测试异常处理."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.comments.side_effect = Exception("JIRA API错误")

        # Act
        result = get_issue_comments("TEST-ERROR")

        # Assert - 验证错误被捕获并返回
        assert "error" in result
        assert "JIRA API错误" in result["error"]

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_with_issue_not_found(self, mock_get_client):
        """测试问题不存在的情况."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.comments.side_effect = Exception("Issue Does Not Exist")

        # Act
        result = get_issue_comments("NOTFOUND-123")

        # Assert
        assert "error" in result
        assert "Issue Does Not Exist" in result["error"]

    @patch("jira_mcp.server.get_jira_client")
    def test_get_issue_comments_formats_all_fields(self, mock_get_client):
        """测试评论的所有字段都被正确格式化."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_author = Mock()
        mock_author.name = "zhangsan"
        mock_author.displayName = "张三"
        mock_author.emailAddress = "zhangsan@example.com"

        mock_comment = Mock()
        mock_comment.id = "12345"
        mock_comment.body = "详细评论"
        mock_comment.created = "2025-01-24T10:00:00.000+0800"
        mock_comment.updated = "2025-01-24T10:30:00.000+0800"
        mock_comment.author = mock_author
        mock_comment.updateAuthor = None
        mock_comment.visibility = None

        mock_client.comments.return_value = [mock_comment]

        # Act
        result = get_issue_comments("TEST-123")

        # Assert - 验证格式化包含作者信息
        comment = result["comments"][0]
        assert comment["author"]["name"] == "zhangsan"
        assert comment["author"]["display_name"] == "张三"

    @patch("jira_mcp.server.get_jira_client")
    @patch("jira_mcp.server.logger")
    def test_get_issue_comments_logs_correctly(self, mock_logger, mock_get_client):
        """测试日志记录功能."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.comments.return_value = []

        # Act
        get_issue_comments("TEST-LOG")

        # Assert - 验证日志调用
        mock_logger.info.assert_called_once_with("获取问题评论: TEST-LOG")

    @patch("jira_mcp.server.get_jira_client")
    @patch("jira_mcp.server.logger")
    def test_get_issue_comments_logs_error(self, mock_logger, mock_get_client):
        """测试错误日志记录."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.comments.side_effect = Exception("测试错误")

        # Act
        get_issue_comments("TEST-ERR")

        # Assert - 验证错误日志
        mock_logger.error.assert_called_once()


class TestAddComment:
    """测试add_comment工具函数."""

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_basic(self, mock_get_client):
        """测试添加基本评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_new_comment = Mock()
        mock_new_comment.id = "67890"
        mock_new_comment.body = "新添加的评论"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        result = add_comment("TEST-123", "新添加的评论")

        # Assert
        assert result["issue_key"] == "TEST-123"
        assert result["success"] is True
        assert result["comment"]["id"] == "67890"
        assert result["comment"]["body"] == "新添加的评论"
        mock_client.add_comment.assert_called_once_with(
            "TEST-123", "新添加的评论", visibility=None
        )

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_role_visibility(self, mock_get_client):
        """测试添加带角色可见性的评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_visibility = Mock()
        mock_visibility.type = "role"
        mock_visibility.value = "Administrators"

        mock_new_comment = Mock()
        mock_new_comment.id = "67891"
        mock_new_comment.body = "管理员可见评论"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = mock_visibility

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        result = add_comment(
            "TEST-123", "管理员可见评论", "role", "Administrators"
        )

        # Assert
        assert result["success"] is True
        assert result["comment"]["visibility"]["type"] == "role"
        assert result["comment"]["visibility"]["value"] == "Administrators"
        mock_client.add_comment.assert_called_once_with(
            "TEST-123",
            "管理员可见评论",
            visibility={"type": "role", "value": "Administrators"},
        )

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_group_visibility(self, mock_get_client):
        """测试添加带组可见性的评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_visibility = Mock()
        mock_visibility.type = "group"
        mock_visibility.value = "jira-developers"

        mock_new_comment = Mock()
        mock_new_comment.id = "67892"
        mock_new_comment.body = "开发组可见"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = mock_visibility

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        result = add_comment("TEST-456", "开发组可见", "group", "jira-developers")

        # Assert
        mock_client.add_comment.assert_called_once_with(
            "TEST-456",
            "开发组可见",
            visibility={"type": "group", "value": "jira-developers"},
        )

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_exception(self, mock_get_client):
        """测试添加评论时的异常处理."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.add_comment.side_effect = Exception("权限不足")

        # Act
        result = add_comment("TEST-ERROR", "测试评论")

        # Assert - 验证错误被捕获
        assert "error" in result
        assert "权限不足" in result["error"]

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_only_visibility_type(self, mock_get_client):
        """测试只提供visibility_type参数的情况."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_new_comment = Mock()
        mock_new_comment.id = "67893"
        mock_new_comment.body = "测试"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act - 只提供type，不提供value
        result = add_comment("TEST-123", "测试", visibility_type="role")

        # Assert - 验证visibility为None（因为缺少value）
        mock_client.add_comment.assert_called_once_with(
            "TEST-123", "测试", visibility=None
        )

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_only_visibility_value(self, mock_get_client):
        """测试只提供visibility_value参数的情况."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_new_comment = Mock()
        mock_new_comment.id = "67894"
        mock_new_comment.body = "测试"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act - 只提供value，不提供type
        result = add_comment("TEST-123", "测试", visibility_value="Administrators")

        # Assert - 验证visibility为None（因为缺少type）
        mock_client.add_comment.assert_called_once_with(
            "TEST-123", "测试", visibility=None
        )

    @patch("jira_mcp.server.get_jira_client")
    @patch("jira_mcp.server.logger")
    def test_add_comment_logs_correctly(self, mock_logger, mock_get_client):
        """测试添加评论的日志记录."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_new_comment = Mock()
        mock_new_comment.id = "67895"
        mock_new_comment.body = "测试"
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        add_comment("TEST-LOG", "测试日志")

        # Assert - 验证日志调用
        mock_logger.info.assert_called_once_with("添加评论到问题 TEST-LOG")

    @patch("jira_mcp.server.get_jira_client")
    @patch("jira_mcp.server.logger")
    def test_add_comment_logs_error(self, mock_logger, mock_get_client):
        """测试添加评论错误的日志记录."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.add_comment.side_effect = Exception("测试错误")

        # Act
        add_comment("TEST-ERR", "测试")

        # Assert - 验证错误日志
        mock_logger.error.assert_called_once()

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_empty_body(self, mock_get_client):
        """测试添加空内容评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        mock_new_comment = Mock()
        mock_new_comment.id = "67896"
        mock_new_comment.body = ""
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        result = add_comment("TEST-123", "")

        # Assert - 验证可以添加空评论
        assert result["success"] is True
        assert result["comment"]["body"] == ""

    @patch("jira_mcp.server.get_jira_client")
    def test_add_comment_with_long_body(self, mock_get_client):
        """测试添加长文本评论."""
        # Arrange
        mock_client = Mock()
        mock_get_client.return_value = mock_client

        long_text = "这是一个很长的评论内容" * 100

        mock_new_comment = Mock()
        mock_new_comment.id = "67897"
        mock_new_comment.body = long_text
        mock_new_comment.created = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.updated = "2025-01-24T11:00:00.000+0800"
        mock_new_comment.author = None
        mock_new_comment.updateAuthor = None
        mock_new_comment.visibility = None

        mock_client.add_comment.return_value = mock_new_comment

        # Act
        result = add_comment("TEST-123", long_text)

        # Assert - 验证长文本被正确处理
        assert result["success"] is True
        assert len(result["comment"]["body"]) == len(long_text)
