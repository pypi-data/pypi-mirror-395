#!/usr/bin/env python3
"""Script to combine main.py parts with handler imports"""

# Read part 1 (before handlers)
with open('aird/main_part1.txt', 'r', encoding='utf-8') as f:
    part1 = f.read()

# Read part 2 (after handlers - make_app, main, etc.)
with open('aird/main_part2.txt', 'r', encoding='utf-8') as f:
    part2 = f.read()

# Handler imports to add
handler_imports = """
# Import handlers from modules
from aird.handlers.base_handler import BaseHandler
from aird.handlers.auth_handlers import (
    LDAPLoginHandler,
    LoginHandler,
    AdminLoginHandler,
    LogoutHandler,
    ProfileHandler,
)
from aird.handlers.admin_handlers import (
    AdminHandler,
    WebSocketStatsHandler,
    AdminUsersHandler,
    UserCreateHandler,
    UserEditHandler,
    UserDeleteHandler,
    LDAPConfigHandler,
    LDAPConfigCreateHandler,
    LDAPConfigEditHandler,
    LDAPConfigDeleteHandler,
    LDAPSyncHandler,
)
from aird.handlers.file_op_handlers import (
    UploadHandler,
    DeleteHandler,
    RenameHandler,
    EditHandler,
    EditViewHandler,
    CloudUploadHandler,
)
from aird.handlers.share_handlers import (
    ShareFilesHandler,
    ShareCreateHandler,
    ShareRevokeHandler,
    ShareUpdateHandler,
    TokenVerificationHandler,
    SharedListHandler,
    SharedFileHandler,
)
from aird.handlers.api_handlers import (
    FeatureFlagSocketHandler,
    FileStreamHandler,
    FileListAPIHandler,
    ShareListAPIHandler,
    UserSearchAPIHandler,
    ShareDetailsAPIHandler,
    ShareDetailsByIdAPIHandler,
    SuperSearchHandler,
    SuperSearchWebSocketHandler,
)
from aird.handlers.view_handlers import (
    RootHandler,
    MainHandler,
    CloudProvidersHandler,
    CloudFilesHandler,
    CloudDownloadHandler,
)

"""

# Combine all parts
combined = part1 + handler_imports + part2

# Write the new main.py
with open('aird/main_new.py', 'w', encoding='utf-8') as f:
    f.write(combined)

print("Successfully created main_new.py")
print(f"Part 1: {len(part1.splitlines())} lines")
print(f"Handler imports: {len(handler_imports.splitlines())} lines")
print(f"Part 2: {len(part2.splitlines())} lines")
print(f"Total: {len(combined.splitlines())} lines")

