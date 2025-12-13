# MCP Mobile App Builder

MCP Server for Mobile App Development - Generate Login, Home, and Settings pages for React Native, Flutter, SwiftUI, and Kotlin/Jetpack Compose.

## Installation

```bash
pip install mcp-mobile-app
```

Or run directly with:
```bash
uvx mcp-mobile-app
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mobile-app-builder": {
      "command": "uvx",
      "args": ["mcp-mobile-app"]
    }
  }
}
```

### VSCode (Copilot)

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "mobile-app-builder": {
      "command": "uvx",
      "args": ["mcp-mobile-app"]
    }
  }
}
```

## Available Tools

### `build_login_page`

Generate a login page for mobile apps.

**Parameters:**
- `framework`: Target framework - `react-native`, `flutter`, `swiftui`, or `kotlin`
- `auth_type`: Authentication type - `email`, `phone`, or `username`
- `include_social_login`: Include social login buttons (Google, Apple)
- `include_remember_me`: Include remember me checkbox
- `include_forgot_password`: Include forgot password link
- `styling`: Style theme - `modern`, `minimal`, or `classic`

### `build_home_page`

Generate a home page for mobile apps.

**Parameters:**
- `framework`: Target framework
- `layout`: Page layout - `dashboard`, `feed`, `grid`, or `list`
- `include_header`: Include app header with title/logo
- `include_bottom_nav`: Include bottom navigation bar
- `include_search`: Include search functionality
- `card_style`: Card layout - `grid`, `list`, or `carousel`

### `build_settings_page`

Generate a settings page for mobile apps.

**Parameters:**
- `framework`: Target framework
- `sections`: Custom sections list e.g. `['account', 'privacy', 'about']`
- `include_profile_section`: Include user profile section at top
- `include_theme_toggle`: Include dark/light theme toggle
- `include_notifications`: Include notification settings
- `include_logout`: Include logout button

## Usage Examples

In Claude or Copilot, simply ask:

- "Build me a Flutter login page with email authentication"
- "Create a React Native home page with a grid layout and search"
- "Generate a SwiftUI settings page with dark mode toggle"

## License

MIT
