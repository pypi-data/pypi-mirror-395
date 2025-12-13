#!/usr/bin/env python3
"""
MCP Server for Mobile App Development
Tools for building Login, Home, and Settings pages
"""

import os
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Mobile App Builder")

# Get transport mode from environment
TRANSPORT = os.getenv("MCP_TRANSPORT", "stdio")  # "stdio" or "sse"
HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8080"))


@mcp.tool()
def build_login_page(
    framework: str = "react-native",
    auth_type: str = "email",
    include_social_login: bool = True,
    include_remember_me: bool = True,
    include_forgot_password: bool = True,
    styling: str = "modern"
) -> str:
    """
    Generate a login page for mobile apps.

    Args:
        framework: Target framework - 'react-native', 'flutter', 'swiftui', or 'kotlin'
        auth_type: Authentication type - 'email', 'phone', or 'username'
        include_social_login: Include social login buttons (Google, Apple, Facebook)
        include_remember_me: Include remember me checkbox
        include_forgot_password: Include forgot password link
        styling: Style theme - 'modern', 'minimal', or 'classic'

    Returns:
        Generated login page code
    """

    if framework == "react-native":
        return _generate_rn_login(auth_type, include_social_login, include_remember_me, include_forgot_password, styling)
    elif framework == "flutter":
        return _generate_flutter_login(auth_type, include_social_login, include_remember_me, include_forgot_password, styling)
    elif framework == "swiftui":
        return _generate_swiftui_login(auth_type, include_social_login, include_remember_me, include_forgot_password, styling)
    elif framework == "kotlin":
        return _generate_kotlin_login(auth_type, include_social_login, include_remember_me, include_forgot_password, styling)
    else:
        return f"Unsupported framework: {framework}. Use 'react-native', 'flutter', 'swiftui', or 'kotlin'"


@mcp.tool()
def build_home_page(
    framework: str = "react-native",
    layout: str = "dashboard",
    include_header: bool = True,
    include_bottom_nav: bool = True,
    include_search: bool = True,
    card_style: str = "grid"
) -> str:
    """
    Generate a home page for mobile apps.

    Args:
        framework: Target framework - 'react-native', 'flutter', 'swiftui', or 'kotlin'
        layout: Page layout - 'dashboard', 'feed', 'grid', or 'list'
        include_header: Include app header with title/logo
        include_bottom_nav: Include bottom navigation bar
        include_search: Include search functionality
        card_style: Card layout - 'grid', 'list', or 'carousel'

    Returns:
        Generated home page code
    """

    if framework == "react-native":
        return _generate_rn_home(layout, include_header, include_bottom_nav, include_search, card_style)
    elif framework == "flutter":
        return _generate_flutter_home(layout, include_header, include_bottom_nav, include_search, card_style)
    elif framework == "swiftui":
        return _generate_swiftui_home(layout, include_header, include_bottom_nav, include_search, card_style)
    elif framework == "kotlin":
        return _generate_kotlin_home(layout, include_header, include_bottom_nav, include_search, card_style)
    else:
        return f"Unsupported framework: {framework}. Use 'react-native', 'flutter', 'swiftui', or 'kotlin'"


@mcp.tool()
def build_settings_page(
    framework: str = "react-native",
    sections: list = None,
    include_profile_section: bool = True,
    include_theme_toggle: bool = True,
    include_notifications: bool = True,
    include_logout: bool = True
) -> str:
    """
    Generate a settings page for mobile apps.

    Args:
        framework: Target framework - 'react-native', 'flutter', 'swiftui', or 'kotlin'
        sections: Custom sections list e.g. ['account', 'privacy', 'about']
        include_profile_section: Include user profile section at top
        include_theme_toggle: Include dark/light theme toggle
        include_notifications: Include notification settings
        include_logout: Include logout button

    Returns:
        Generated settings page code
    """

    if sections is None:
        sections = ["account", "privacy", "notifications", "about"]

    if framework == "react-native":
        return _generate_rn_settings(sections, include_profile_section, include_theme_toggle, include_notifications, include_logout)
    elif framework == "flutter":
        return _generate_flutter_settings(sections, include_profile_section, include_theme_toggle, include_notifications, include_logout)
    elif framework == "swiftui":
        return _generate_swiftui_settings(sections, include_profile_section, include_theme_toggle, include_notifications, include_logout)
    elif framework == "kotlin":
        return _generate_kotlin_settings(sections, include_profile_section, include_theme_toggle, include_notifications, include_logout)
    else:
        return f"Unsupported framework: {framework}. Use 'react-native', 'flutter', 'swiftui', or 'kotlin'"


# ============== React Native Generators ==============

def _generate_rn_login(auth_type, social, remember, forgot, styling):
    social_buttons = """
      {/* Social Login */}
      <View style={styles.socialContainer}>
        <TouchableOpacity style={styles.socialButton}>
          <Text style={styles.socialText}>Continue with Google</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.socialButton}>
          <Text style={styles.socialText}>Continue with Apple</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.divider}>
        <View style={styles.dividerLine} />
        <Text style={styles.dividerText}>or</Text>
        <View style={styles.dividerLine} />
      </View>""" if social else ""

    remember_section = """
        <View style={styles.rememberContainer}>
          <TouchableOpacity
            style={styles.checkbox}
            onPress={() => setRememberMe(!rememberMe)}
          >
            {rememberMe && <View style={styles.checkboxChecked} />}
          </TouchableOpacity>
          <Text style={styles.rememberText}>Remember me</Text>
        </View>""" if remember else ""

    forgot_section = """
        <TouchableOpacity onPress={() => navigation.navigate('ForgotPassword')}>
          <Text style={styles.forgotText}>Forgot Password?</Text>
        </TouchableOpacity>""" if forgot else ""

    input_field = "email" if auth_type == "email" else ("phone" if auth_type == "phone" else "username")
    input_placeholder = "Email address" if auth_type == "email" else ("Phone number" if auth_type == "phone" else "Username")
    keyboard_type = "email-address" if auth_type == "email" else ("phone-pad" if auth_type == "phone" else "default")

    return f'''import React, {{ useState }} from 'react';
import {{
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
}} from 'react-native';

const LoginScreen = ({{ navigation }}) => {{
  const [{input_field}, set{input_field.capitalize()}] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async () => {{
    setIsLoading(true);
    try {{
      // TODO: Implement your authentication logic here
      console.log('Login with:', {{ {input_field}, password }});
    }} catch (error) {{
      console.error('Login error:', error);
    }} finally {{
      setIsLoading(false);
    }}
  }};

  return (
    <SafeAreaView style={{styles.container}}>
      <KeyboardAvoidingView
        behavior={{Platform.OS === 'ios' ? 'padding' : 'height'}}
        style={{styles.keyboardView}}
      >
        <View style={{styles.content}}>
          {{/* Header */}}
          <View style={{styles.header}}>
            <Text style={{styles.title}}>Welcome Back</Text>
            <Text style={{styles.subtitle}}>Sign in to continue</Text>
          </View>
{social_buttons}
          {{/* Input Fields */}}
          <View style={{styles.inputContainer}}>
            <Text style={{styles.label}}>{input_placeholder}</Text>
            <TextInput
              style={{styles.input}}
              placeholder="Enter your {input_field}"
              placeholderTextColor="#999"
              value={{{input_field}}}
              onChangeText={{set{input_field.capitalize()}}}
              keyboardType="{keyboard_type}"
              autoCapitalize="none"
            />
          </View>

          <View style={{styles.inputContainer}}>
            <Text style={{styles.label}}>Password</Text>
            <TextInput
              style={{styles.input}}
              placeholder="Enter your password"
              placeholderTextColor="#999"
              value={{password}}
              onChangeText={{setPassword}}
              secureTextEntry
            />
          </View>

          {{/* Remember & Forgot */}}
          <View style={{styles.optionsContainer}}>
{remember_section}
{forgot_section}
          </View>

          {{/* Login Button */}}
          <TouchableOpacity
            style={{[styles.loginButton, isLoading && styles.loginButtonDisabled]}}
            onPress={{handleLogin}}
            disabled={{isLoading}}
          >
            <Text style={{styles.loginButtonText}}>
              {{isLoading ? 'Signing in...' : 'Sign In'}}
            </Text>
          </TouchableOpacity>

          {{/* Sign Up Link */}}
          <View style={{styles.signupContainer}}>
            <Text style={{styles.signupText}}>Don't have an account? </Text>
            <TouchableOpacity onPress={{() => navigation.navigate('SignUp')}}>
              <Text style={{styles.signupLink}}>Sign Up</Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#FFFFFF',
  }},
  keyboardView: {{
    flex: 1,
  }},
  content: {{
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: 'center',
  }},
  header: {{
    marginBottom: 32,
  }},
  title: {{
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1a1a1a',
    marginBottom: 8,
  }},
  subtitle: {{
    fontSize: 16,
    color: '#666',
  }},
  socialContainer: {{
    gap: 12,
    marginBottom: 16,
  }},
  socialButton: {{
    backgroundColor: '#f5f5f5',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  }},
  socialText: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  }},
  divider: {{
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 20,
  }},
  dividerLine: {{
    flex: 1,
    height: 1,
    backgroundColor: '#e0e0e0',
  }},
  dividerText: {{
    marginHorizontal: 16,
    color: '#999',
    fontSize: 14,
  }},
  inputContainer: {{
    marginBottom: 16,
  }},
  label: {{
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  }},
  input: {{
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderRadius: 12,
    fontSize: 16,
    color: '#1a1a1a',
  }},
  optionsContainer: {{
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  }},
  rememberContainer: {{
    flexDirection: 'row',
    alignItems: 'center',
  }},
  checkbox: {{
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: '#007AFF',
    borderRadius: 4,
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
  }},
  checkboxChecked: {{
    width: 12,
    height: 12,
    backgroundColor: '#007AFF',
    borderRadius: 2,
  }},
  rememberText: {{
    color: '#666',
    fontSize: 14,
  }},
  forgotText: {{
    color: '#007AFF',
    fontSize: 14,
    fontWeight: '600',
  }},
  loginButton: {{
    backgroundColor: '#007AFF',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginBottom: 24,
  }},
  loginButtonDisabled: {{
    opacity: 0.7,
  }},
  loginButtonText: {{
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  }},
  signupContainer: {{
    flexDirection: 'row',
    justifyContent: 'center',
  }},
  signupText: {{
    color: '#666',
    fontSize: 14,
  }},
  signupLink: {{
    color: '#007AFF',
    fontSize: 14,
    fontWeight: '600',
  }},
}});

export default LoginScreen;
'''


def _generate_rn_home(layout, header, bottom_nav, search, card_style):
    header_section = """
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Hello,</Text>
            <Text style={styles.username}>John Doe</Text>
          </View>
          <TouchableOpacity style={styles.profileButton}>
            <View style={styles.avatar} />
          </TouchableOpacity>
        </View>""" if header else ""

    search_section = """
        {/* Search Bar */}
        <View style={styles.searchContainer}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search..."
            placeholderTextColor="#999"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>""" if search else ""

    bottom_nav_section = """
      {/* Bottom Navigation */}
      <View style={styles.bottomNav}>
        <TouchableOpacity style={styles.navItem}>
          <Text style={[styles.navIcon, styles.navActive]}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>Search</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>Favorites</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Text style={styles.navIcon}>Profile</Text>
        </TouchableOpacity>
      </View>""" if bottom_nav else ""

    num_columns = "2" if card_style == "grid" else "1"

    return f'''import React, {{ useState }} from 'react';
import {{
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  FlatList,
  RefreshControl,
}} from 'react-native';

const SAMPLE_DATA = [
  {{ id: '1', title: 'Item 1', description: 'Description for item 1', category: 'Category A' }},
  {{ id: '2', title: 'Item 2', description: 'Description for item 2', category: 'Category B' }},
  {{ id: '3', title: 'Item 3', description: 'Description for item 3', category: 'Category A' }},
  {{ id: '4', title: 'Item 4', description: 'Description for item 4', category: 'Category C' }},
  {{ id: '5', title: 'Item 5', description: 'Description for item 5', category: 'Category B' }},
  {{ id: '6', title: 'Item 6', description: 'Description for item 6', category: 'Category A' }},
];

const HomeScreen = ({{ navigation }}) => {{
  const [searchQuery, setSearchQuery] = useState('');
  const [refreshing, setRefreshing] = useState(false);
  const [data, setData] = useState(SAMPLE_DATA);

  const onRefresh = async () => {{
    setRefreshing(true);
    // TODO: Implement your refresh logic here
    setTimeout(() => setRefreshing(false), 1500);
  }};

  const filteredData = data.filter(item =>
    item.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderCard = ({{ item }}) => (
    <TouchableOpacity
      style={{styles.card}}
      onPress={{() => navigation.navigate('Detail', {{ item }})}}
    >
      <View style={{styles.cardImage}} />
      <View style={{styles.cardContent}}>
        <Text style={{styles.cardTitle}}>{{item.title}}</Text>
        <Text style={{styles.cardDescription}}>{{item.description}}</Text>
        <View style={{styles.cardFooter}}>
          <Text style={{styles.cardCategory}}>{{item.category}}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={{styles.container}}>
{header_section}
{search_section}
        {{/* Content */}}
        <FlatList
          data={{filteredData}}
          renderItem={{renderCard}}
          keyExtractor={{item => item.id}}
          numColumns={{{num_columns}}}
          contentContainerStyle={{styles.listContent}}
          showsVerticalScrollIndicator={{false}}
          refreshControl={{
            <RefreshControl refreshing={{refreshing}} onRefresh={{onRefresh}} />
          }}
          ListEmptyComponent={{
            <View style={{styles.emptyContainer}}>
              <Text style={{styles.emptyText}}>No items found</Text>
            </View>
          }}
        />
{bottom_nav_section}
    </SafeAreaView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f8f9fa',
  }},
  header: {{
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#FFFFFF',
  }},
  greeting: {{
    fontSize: 14,
    color: '#666',
  }},
  username: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1a1a1a',
  }},
  profileButton: {{
    padding: 4,
  }},
  avatar: {{
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#007AFF',
  }},
  searchContainer: {{
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
  }},
  searchInput: {{
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    fontSize: 16,
    color: '#1a1a1a',
  }},
  listContent: {{
    padding: 16,
  }},
  card: {{
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    margin: 6,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 2 }},
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  }},
  cardImage: {{
    height: 120,
    backgroundColor: '#e0e0e0',
  }},
  cardContent: {{
    padding: 12,
  }},
  cardTitle: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  }},
  cardDescription: {{
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
  }},
  cardFooter: {{
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  }},
  cardCategory: {{
    fontSize: 12,
    color: '#007AFF',
    fontWeight: '500',
  }},
  emptyContainer: {{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 40,
  }},
  emptyText: {{
    fontSize: 16,
    color: '#999',
  }},
  bottomNav: {{
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
  }},
  navItem: {{
    flex: 1,
    alignItems: 'center',
  }},
  navIcon: {{
    fontSize: 12,
    color: '#999',
    fontWeight: '500',
  }},
  navActive: {{
    color: '#007AFF',
  }},
}});

export default HomeScreen;
'''


def _generate_rn_settings(sections, profile, theme, notifications, logout):
    profile_section = """
        {/* Profile Section */}
        <TouchableOpacity style={styles.profileSection}>
          <View style={styles.avatar} />
          <View style={styles.profileInfo}>
            <Text style={styles.profileName}>John Doe</Text>
            <Text style={styles.profileEmail}>john.doe@example.com</Text>
          </View>
          <Text style={styles.chevron}>›</Text>
        </TouchableOpacity>""" if profile else ""

    theme_item = """
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Dark Mode</Text>
            <Switch
              value={darkMode}
              onValueChange={setDarkMode}
              trackColor={{ false: '#e0e0e0', true: '#007AFF' }}
              thumbColor="#FFFFFF"
            />
          </View>""" if theme else ""

    notifications_item = """
          <View style={styles.settingItem}>
            <Text style={styles.settingLabel}>Push Notifications</Text>
            <Switch
              value={notificationsEnabled}
              onValueChange={setNotificationsEnabled}
              trackColor={{ false: '#e0e0e0', true: '#007AFF' }}
              thumbColor="#FFFFFF"
            />
          </View>""" if notifications else ""

    logout_section = """
        {/* Logout */}
        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.logoutText}>Log Out</Text>
        </TouchableOpacity>""" if logout else ""

    sections_str = str(sections)

    return f'''import React, {{ useState }} from 'react';
import {{
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Switch,
  Alert,
}} from 'react-native';

const SETTINGS_SECTIONS = {sections_str};

const SettingsScreen = ({{ navigation }}) => {{
  const [darkMode, setDarkMode] = useState(false);
  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  const handleLogout = () => {{
    Alert.alert(
      'Log Out',
      'Are you sure you want to log out?',
      [
        {{ text: 'Cancel', style: 'cancel' }},
        {{
          text: 'Log Out',
          style: 'destructive',
          onPress: () => {{
            // TODO: Implement logout logic
            navigation.reset({{
              index: 0,
              routes: [{{ name: 'Login' }}],
            }});
          }}
        }},
      ]
    );
  }};

  const renderSettingItem = (label, onPress, showChevron = true) => (
    <TouchableOpacity style={{styles.settingItem}} onPress={{onPress}}>
      <Text style={{styles.settingLabel}}>{{label}}</Text>
      {{showChevron && <Text style={{styles.chevron}}>›</Text>}}
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={{styles.container}}>
      <ScrollView showsVerticalScrollIndicator={{false}}>
        {{/* Header */}}
        <Text style={{styles.headerTitle}}>Settings</Text>
{profile_section}

        {{/* Account Section */}}
        <View style={{styles.section}}>
          <Text style={{styles.sectionTitle}}>Account</Text>
          <View style={{styles.sectionContent}}>
            {{renderSettingItem('Edit Profile', () => navigation.navigate('EditProfile'))}}
            {{renderSettingItem('Change Password', () => navigation.navigate('ChangePassword'))}}
            {{renderSettingItem('Privacy', () => navigation.navigate('Privacy'))}}
          </View>
        </View>

        {{/* Preferences Section */}}
        <View style={{styles.section}}>
          <Text style={{styles.sectionTitle}}>Preferences</Text>
          <View style={{styles.sectionContent}}>
{theme_item}
{notifications_item}
            {{renderSettingItem('Language', () => navigation.navigate('Language'))}}
          </View>
        </View>

        {{/* Support Section */}}
        <View style={{styles.section}}>
          <Text style={{styles.sectionTitle}}>Support</Text>
          <View style={{styles.sectionContent}}>
            {{renderSettingItem('Help Center', () => navigation.navigate('Help'))}}
            {{renderSettingItem('Contact Us', () => navigation.navigate('Contact'))}}
            {{renderSettingItem('Terms of Service', () => navigation.navigate('Terms'))}}
            {{renderSettingItem('Privacy Policy', () => navigation.navigate('PrivacyPolicy'))}}
          </View>
        </View>

        {{/* About Section */}}
        <View style={{styles.section}}>
          <Text style={{styles.sectionTitle}}>About</Text>
          <View style={{styles.sectionContent}}>
            {{renderSettingItem('App Version', () => {{}}, false)}}
            <Text style={{styles.versionText}}>1.0.0</Text>
          </View>
        </View>
{logout_section}

        <View style={{styles.bottomPadding}} />
      </ScrollView>
    </SafeAreaView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f8f9fa',
  }},
  headerTitle: {{
    fontSize: 34,
    fontWeight: 'bold',
    color: '#1a1a1a',
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 16,
  }},
  profileSection: {{
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    padding: 16,
    borderRadius: 16,
    marginBottom: 24,
  }},
  avatar: {{
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#007AFF',
  }},
  profileInfo: {{
    flex: 1,
    marginLeft: 16,
  }},
  profileName: {{
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
  }},
  profileEmail: {{
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  }},
  chevron: {{
    fontSize: 24,
    color: '#999',
  }},
  section: {{
    marginBottom: 24,
  }},
  sectionTitle: {{
    fontSize: 14,
    fontWeight: '600',
    color: '#666',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
    paddingHorizontal: 20,
    marginBottom: 8,
  }},
  sectionContent: {{
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    borderRadius: 16,
    overflow: 'hidden',
  }},
  settingItem: {{
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  }},
  settingLabel: {{
    fontSize: 16,
    color: '#1a1a1a',
  }},
  versionText: {{
    fontSize: 14,
    color: '#999',
    paddingHorizontal: 16,
    paddingBottom: 14,
  }},
  logoutButton: {{
    backgroundColor: '#FFFFFF',
    marginHorizontal: 20,
    padding: 16,
    borderRadius: 16,
    alignItems: 'center',
  }},
  logoutText: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#FF3B30',
  }},
  bottomPadding: {{
    height: 40,
  }},
}});

export default SettingsScreen;
'''


# ============== Flutter Generators ==============

def _generate_flutter_login(auth_type, social, remember, forgot, styling):
    input_field = "email" if auth_type == "email" else ("phone" if auth_type == "phone" else "username")
    input_hint = "Email address" if auth_type == "email" else ("Phone number" if auth_type == "phone" else "Username")
    keyboard_type = "TextInputType.emailAddress" if auth_type == "email" else ("TextInputType.phone" if auth_type == "phone" else "TextInputType.text")

    social_section = """
          // Social Login Buttons
          _buildSocialButton('Continue with Google', () {}),
          const SizedBox(height: 12),
          _buildSocialButton('Continue with Apple', () {}),
          const SizedBox(height: 24),
          Row(
            children: [
              const Expanded(child: Divider()),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Text('or', style: TextStyle(color: Colors.grey[600])),
              ),
              const Expanded(child: Divider()),
            ],
          ),
          const SizedBox(height: 24),""" if social else ""

    remember_section = """
            Row(
              children: [
                Checkbox(
                  value: _rememberMe,
                  onChanged: (value) => setState(() => _rememberMe = value!),
                  activeColor: const Color(0xFF007AFF),
                ),
                const Text('Remember me'),
              ],
            ),""" if remember else ""

    forgot_section = """
            TextButton(
              onPressed: () => Navigator.pushNamed(context, '/forgot-password'),
              child: const Text(
                'Forgot Password?',
                style: TextStyle(color: Color(0xFF007AFF)),
              ),
            ),""" if forgot else ""

    return f'''import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {{
  const LoginScreen({{super.key}});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}}

class _LoginScreenState extends State<LoginScreen> {{
  final _{input_field}Controller = TextEditingController();
  final _passwordController = TextEditingController();
  bool _rememberMe = false;
  bool _isLoading = false;
  bool _obscurePassword = true;

  @override
  void dispose() {{
    _{input_field}Controller.dispose();
    _passwordController.dispose();
    super.dispose();
  }}

  Future<void> _handleLogin() async {{
    setState(() => _isLoading = true);
    try {{
      // TODO: Implement your authentication logic here
      debugPrint('Login with: ${{_{input_field}Controller.text}}');
      await Future.delayed(const Duration(seconds: 2));
    }} finally {{
      setState(() => _isLoading = false);
    }}
  }}

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 60),
              // Header
              const Text(
                'Welcome Back',
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1a1a1a),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Sign in to continue',
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 40),
{social_section}
              // Input Fields
              Text(
                '{input_hint}',
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _{input_field}Controller,
                keyboardType: {keyboard_type},
                decoration: InputDecoration(
                  hintText: 'Enter your {input_field}',
                  filled: true,
                  fillColor: Colors.grey[100],
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Password',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 8),
              TextField(
                controller: _passwordController,
                obscureText: _obscurePassword,
                decoration: InputDecoration(
                  hintText: 'Enter your password',
                  filled: true,
                  fillColor: Colors.grey[100],
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword ? Icons.visibility_off : Icons.visibility,
                    ),
                    onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              // Remember & Forgot
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
{remember_section}
{forgot_section}
                ],
              ),
              const SizedBox(height: 24),
              // Login Button
              ElevatedButton(
                onPressed: _isLoading ? null : _handleLogin,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF007AFF),
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: Text(
                  _isLoading ? 'Signing in...' : 'Sign In',
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              const SizedBox(height: 24),
              // Sign Up Link
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "Don't have an account? ",
                    style: TextStyle(color: Colors.grey[600]),
                  ),
                  TextButton(
                    onPressed: () => Navigator.pushNamed(context, '/signup'),
                    child: const Text(
                      'Sign Up',
                      style: TextStyle(
                        color: Color(0xFF007AFF),
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }}

  Widget _buildSocialButton(String text, VoidCallback onPressed) {{
    return OutlinedButton(
      onPressed: onPressed,
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        backgroundColor: Colors.grey[100],
        side: BorderSide.none,
      ),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: Color(0xFF333333),
        ),
      ),
    );
  }}
}}
'''


def _generate_flutter_home(layout, header, bottom_nav, search, card_style):
    return '''import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _searchController = TextEditingController();
  int _currentIndex = 0;
  bool _isRefreshing = false;

  final List<Map<String, String>> _items = [
    {'id': '1', 'title': 'Item 1', 'description': 'Description for item 1', 'category': 'Category A'},
    {'id': '2', 'title': 'Item 2', 'description': 'Description for item 2', 'category': 'Category B'},
    {'id': '3', 'title': 'Item 3', 'description': 'Description for item 3', 'category': 'Category A'},
    {'id': '4', 'title': 'Item 4', 'description': 'Description for item 4', 'category': 'Category C'},
    {'id': '5', 'title': 'Item 5', 'description': 'Description for item 5', 'category': 'Category B'},
    {'id': '6', 'title': 'Item 6', 'description': 'Description for item 6', 'category': 'Category A'},
  ];

  Future<void> _onRefresh() async {
    setState(() => _isRefreshing = true);
    await Future.delayed(const Duration(seconds: 2));
    setState(() => _isRefreshing = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(20),
              color: Colors.white,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Hello,',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                      const Text(
                        'John Doe',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const CircleAvatar(
                    radius: 22,
                    backgroundColor: Color(0xFF007AFF),
                  ),
                ],
              ),
            ),
            // Search Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              color: Colors.white,
              child: TextField(
                controller: _searchController,
                decoration: InputDecoration(
                  hintText: 'Search...',
                  filled: true,
                  fillColor: Colors.grey[100],
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                  prefixIcon: const Icon(Icons.search),
                ),
              ),
            ),
            // Content Grid
            Expanded(
              child: RefreshIndicator(
                onRefresh: _onRefresh,
                child: GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: 0.8,
                  ),
                  itemCount: _items.length,
                  itemBuilder: (context, index) => _buildCard(_items[index]),
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) => setState(() => _currentIndex = index),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF007AFF),
        unselectedItemColor: Colors.grey,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.favorite), label: 'Favorites'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }

  Widget _buildCard(Map<String, String> item) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: () => Navigator.pushNamed(context, '/detail', arguments: item),
        borderRadius: BorderRadius.circular(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              height: 100,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item['title']!,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    item['description']!,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[600],
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    item['category']!,
                    style: const TextStyle(
                      fontSize: 12,
                      color: Color(0xFF007AFF),
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
'''


def _generate_flutter_settings(sections, profile, theme, notifications, logout):
    return '''import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _darkMode = false;
  bool _notificationsEnabled = true;

  void _handleLogout() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Log Out'),
        content: const Text('Are you sure you want to log out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pushNamedAndRemoveUntil(context, '/login', (route) => false);
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Log Out'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA),
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              const Padding(
                padding: EdgeInsets.all(20),
                child: Text(
                  'Settings',
                  style: TextStyle(
                    fontSize: 34,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              // Profile Section
              Container(
                margin: const EdgeInsets.symmetric(horizontal: 20),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  children: [
                    const CircleAvatar(
                      radius: 30,
                      backgroundColor: Color(0xFF007AFF),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'John Doe',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          Text(
                            'john.doe@example.com',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey[600],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.chevron_right, color: Colors.grey),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              // Account Section
              _buildSection('Account', [
                _buildSettingItem('Edit Profile', Icons.person_outline, () {}),
                _buildSettingItem('Change Password', Icons.lock_outline, () {}),
                _buildSettingItem('Privacy', Icons.shield_outlined, () {}),
              ]),
              // Preferences Section
              _buildSection('Preferences', [
                _buildSwitchItem('Dark Mode', _darkMode, (value) {
                  setState(() => _darkMode = value);
                }),
                _buildSwitchItem('Push Notifications', _notificationsEnabled, (value) {
                  setState(() => _notificationsEnabled = value);
                }),
                _buildSettingItem('Language', Icons.language, () {}),
              ]),
              // Support Section
              _buildSection('Support', [
                _buildSettingItem('Help Center', Icons.help_outline, () {}),
                _buildSettingItem('Contact Us', Icons.mail_outline, () {}),
                _buildSettingItem('Terms of Service', Icons.description_outlined, () {}),
              ]),
              // Logout Button
              Padding(
                padding: const EdgeInsets.all(20),
                child: SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _handleLogout,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.red,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                    ),
                    child: const Text(
                      'Log Out',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          child: Text(
            title.toUpperCase(),
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: Colors.grey[600],
              letterSpacing: 0.5,
            ),
          ),
        ),
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 20),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Column(children: items),
        ),
        const SizedBox(height: 24),
      ],
    );
  }

  Widget _buildSettingItem(String label, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: Colors.grey[700]),
      title: Text(label),
      trailing: const Icon(Icons.chevron_right, color: Colors.grey),
      onTap: onTap,
    );
  }

  Widget _buildSwitchItem(String label, bool value, ValueChanged<bool> onChanged) {
    return ListTile(
      title: Text(label),
      trailing: Switch(
        value: value,
        onChanged: onChanged,
        activeColor: const Color(0xFF007AFF),
      ),
    );
  }
}
'''


# ============== SwiftUI Generators ==============

def _generate_swiftui_login(auth_type, social, remember, forgot, styling):
    input_field = "email" if auth_type == "email" else ("phone" if auth_type == "phone" else "username")
    input_placeholder = "Email address" if auth_type == "email" else ("Phone number" if auth_type == "phone" else "Username")
    keyboard_type = ".emailAddress" if auth_type == "email" else (".phonePad" if auth_type == "phone" else ".default")

    social_section = """
            // Social Login
            VStack(spacing: 12) {
                SocialButton(title: "Continue with Google") { }
                SocialButton(title: "Continue with Apple") { }
            }

            HStack {
                Rectangle().fill(Color.gray.opacity(0.3)).frame(height: 1)
                Text("or").foregroundColor(.gray).padding(.horizontal)
                Rectangle().fill(Color.gray.opacity(0.3)).frame(height: 1)
            }
            .padding(.vertical)""" if social else ""

    remember_section = """
                    Toggle("Remember me", isOn: $rememberMe)
                        .toggleStyle(CheckboxToggleStyle())""" if remember else ""

    forgot_section = """
                    Button("Forgot Password?") {
                        // Navigate to forgot password
                    }
                    .foregroundColor(.blue)""" if forgot else ""

    return f'''import SwiftUI

struct LoginView: View {{
    @State private var {input_field} = ""
    @State private var password = ""
    @State private var rememberMe = false
    @State private var isLoading = false
    @State private var showPassword = false

    var body: some View {{
        NavigationView {{
            ScrollView {{
                VStack(spacing: 24) {{
                    Spacer().frame(height: 40)

                    // Header
                    VStack(alignment: .leading, spacing: 8) {{
                        Text("Welcome Back")
                            .font(.system(size: 32, weight: .bold))
                        Text("Sign in to continue")
                            .foregroundColor(.gray)
                    }}
                    .frame(maxWidth: .infinity, alignment: .leading)
{social_section}
                    // Input Fields
                    VStack(alignment: .leading, spacing: 8) {{
                        Text("{input_placeholder}")
                            .font(.system(size: 14, weight: .semibold))
                        TextField("Enter your {input_field}", text: ${input_field})
                            .textFieldStyle(CustomTextFieldStyle())
                            .keyboardType({keyboard_type})
                            .autocapitalization(.none)
                    }}

                    VStack(alignment: .leading, spacing: 8) {{
                        Text("Password")
                            .font(.system(size: 14, weight: .semibold))
                        HStack {{
                            if showPassword {{
                                TextField("Enter your password", text: $password)
                            }} else {{
                                SecureField("Enter your password", text: $password)
                            }}
                            Button(action: {{ showPassword.toggle() }}) {{
                                Image(systemName: showPassword ? "eye.slash" : "eye")
                                    .foregroundColor(.gray)
                            }}
                        }}
                        .textFieldStyle(CustomTextFieldStyle())
                    }}

                    // Options
                    HStack {{
{remember_section}
                        Spacer()
{forgot_section}
                    }}

                    // Login Button
                    Button(action: handleLogin) {{
                        HStack {{
                            if isLoading {{
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                            }}
                            Text(isLoading ? "Signing in..." : "Sign In")
                                .fontWeight(.semibold)
                        }}
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 16)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(12)
                    }}
                    .disabled(isLoading)

                    // Sign Up Link
                    HStack {{
                        Text("Don't have an account?")
                            .foregroundColor(.gray)
                        NavigationLink("Sign Up", destination: Text("Sign Up View"))
                            .foregroundColor(.blue)
                            .fontWeight(.semibold)
                    }}
                }}
                .padding(.horizontal, 24)
            }}
            .navigationBarHidden(true)
        }}
    }}

    func handleLogin() {{
        isLoading = true
        // TODO: Implement authentication logic
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {{
            isLoading = false
        }}
    }}
}}

struct CustomTextFieldStyle: TextFieldStyle {{
    func _body(configuration: TextField<Self._Label>) -> some View {{
        configuration
            .padding()
            .background(Color.gray.opacity(0.1))
            .cornerRadius(12)
    }}
}}

struct SocialButton: View {{
    let title: String
    let action: () -> Void

    var body: some View {{
        Button(action: action) {{
            Text(title)
                .fontWeight(.semibold)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 14)
                .background(Color.gray.opacity(0.1))
                .foregroundColor(.primary)
                .cornerRadius(12)
        }}
    }}
}}

struct CheckboxToggleStyle: ToggleStyle {{
    func makeBody(configuration: Configuration) -> some View {{
        HStack {{
            Image(systemName: configuration.isOn ? "checkmark.square.fill" : "square")
                .foregroundColor(configuration.isOn ? .blue : .gray)
                .onTapGesture {{ configuration.isOn.toggle() }}
            configuration.label
        }}
    }}
}}

#Preview {{
    LoginView()
}}
'''


def _generate_swiftui_home(layout, header, bottom_nav, search, card_style):
    return '''import SwiftUI

struct HomeView: View {
    @State private var searchText = ""
    @State private var selectedTab = 0

    let items: [Item] = [
        Item(id: "1", title: "Item 1", description: "Description for item 1", category: "Category A"),
        Item(id: "2", title: "Item 2", description: "Description for item 2", category: "Category B"),
        Item(id: "3", title: "Item 3", description: "Description for item 3", category: "Category A"),
        Item(id: "4", title: "Item 4", description: "Description for item 4", category: "Category C"),
        Item(id: "5", title: "Item 5", description: "Description for item 5", category: "Category B"),
        Item(id: "6", title: "Item 6", description: "Description for item 6", category: "Category A"),
    ]

    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationView {
                VStack(spacing: 0) {
                    // Header
                    HStack {
                        VStack(alignment: .leading) {
                            Text("Hello,")
                                .foregroundColor(.gray)
                            Text("John Doe")
                                .font(.title)
                                .fontWeight(.bold)
                        }
                        Spacer()
                        Circle()
                            .fill(Color.blue)
                            .frame(width: 44, height: 44)
                    }
                    .padding()
                    .background(Color.white)

                    // Search Bar
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(.gray)
                        TextField("Search...", text: $searchText)
                    }
                    .padding()
                    .background(Color.gray.opacity(0.1))
                    .cornerRadius(12)
                    .padding(.horizontal)
                    .padding(.bottom)
                    .background(Color.white)

                    // Content Grid
                    ScrollView {
                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 16) {
                            ForEach(filteredItems) { item in
                                NavigationLink(destination: Text("Detail: \\(item.title)")) {
                                    CardView(item: item)
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                        .padding()
                    }
                    .background(Color(UIColor.systemGray6))
                }
                .navigationBarHidden(true)
            }
            .tabItem {
                Image(systemName: "house.fill")
                Text("Home")
            }
            .tag(0)

            Text("Search")
                .tabItem {
                    Image(systemName: "magnifyingglass")
                    Text("Search")
                }
                .tag(1)

            Text("Favorites")
                .tabItem {
                    Image(systemName: "heart.fill")
                    Text("Favorites")
                }
                .tag(2)

            Text("Profile")
                .tabItem {
                    Image(systemName: "person.fill")
                    Text("Profile")
                }
                .tag(3)
        }
        .accentColor(.blue)
    }
}

struct Item: Identifiable {
    let id: String
    let title: String
    let description: String
    let category: String
}

struct CardView: View {
    let item: Item

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            Rectangle()
                .fill(Color.gray.opacity(0.3))
                .frame(height: 100)

            VStack(alignment: .leading, spacing: 4) {
                Text(item.title)
                    .font(.system(size: 16, weight: .semibold))
                Text(item.description)
                    .font(.system(size: 14))
                    .foregroundColor(.gray)
                    .lineLimit(2)
                Text(item.category)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(.blue)
                    .padding(.top, 4)
            }
            .padding(12)
        }
        .background(Color.white)
        .cornerRadius(16)
        .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 2)
    }
}

#Preview {
    HomeView()
}
'''


def _generate_swiftui_settings(sections, profile, theme, notifications, logout):
    return '''import SwiftUI

struct SettingsView: View {
    @State private var darkMode = false
    @State private var notificationsEnabled = true
    @State private var showLogoutAlert = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // Profile Section
                    HStack {
                        Circle()
                            .fill(Color.blue)
                            .frame(width: 60, height: 60)

                        VStack(alignment: .leading) {
                            Text("John Doe")
                                .font(.system(size: 18, weight: .semibold))
                            Text("john.doe@example.com")
                                .font(.system(size: 14))
                                .foregroundColor(.gray)
                        }

                        Spacer()

                        Image(systemName: "chevron.right")
                            .foregroundColor(.gray)
                    }
                    .padding()
                    .background(Color.white)
                    .cornerRadius(16)

                    // Account Section
                    SettingsSection(title: "Account") {
                        SettingsRow(icon: "person", title: "Edit Profile")
                        SettingsRow(icon: "lock", title: "Change Password")
                        SettingsRow(icon: "shield", title: "Privacy")
                    }

                    // Preferences Section
                    SettingsSection(title: "Preferences") {
                        Toggle(isOn: $darkMode) {
                            HStack {
                                Image(systemName: "moon")
                                    .foregroundColor(.gray)
                                Text("Dark Mode")
                            }
                        }
                        .padding(.horizontal)
                        .padding(.vertical, 12)

                        Divider().padding(.leading)

                        Toggle(isOn: $notificationsEnabled) {
                            HStack {
                                Image(systemName: "bell")
                                    .foregroundColor(.gray)
                                Text("Push Notifications")
                            }
                        }
                        .padding(.horizontal)
                        .padding(.vertical, 12)

                        Divider().padding(.leading)

                        SettingsRow(icon: "globe", title: "Language")
                    }

                    // Support Section
                    SettingsSection(title: "Support") {
                        SettingsRow(icon: "questionmark.circle", title: "Help Center")
                        SettingsRow(icon: "envelope", title: "Contact Us")
                        SettingsRow(icon: "doc.text", title: "Terms of Service")
                    }

                    // About Section
                    SettingsSection(title: "About") {
                        HStack {
                            Text("App Version")
                            Spacer()
                            Text("1.0.0")
                                .foregroundColor(.gray)
                        }
                        .padding()
                    }

                    // Logout Button
                    Button(action: { showLogoutAlert = true }) {
                        Text("Log Out")
                            .fontWeight(.semibold)
                            .foregroundColor(.red)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.white)
                            .cornerRadius(16)
                    }
                }
                .padding()
            }
            .background(Color(UIColor.systemGray6))
            .navigationTitle("Settings")
            .alert("Log Out", isPresented: $showLogoutAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Log Out", role: .destructive) {
                    // Handle logout
                }
            } message: {
                Text("Are you sure you want to log out?")
            }
        }
    }
}

struct SettingsSection<Content: View>: View {
    let title: String
    @ViewBuilder let content: () -> Content

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title.uppercased())
                .font(.system(size: 14, weight: .semibold))
                .foregroundColor(.gray)
                .padding(.horizontal, 4)

            VStack(spacing: 0) {
                content()
            }
            .background(Color.white)
            .cornerRadius(16)
        }
    }
}

struct SettingsRow: View {
    let icon: String
    let title: String

    var body: some View {
        Button(action: {}) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(.gray)
                    .frame(width: 24)
                Text(title)
                    .foregroundColor(.primary)
                Spacer()
                Image(systemName: "chevron.right")
                    .foregroundColor(.gray)
            }
            .padding()
        }
        Divider().padding(.leading, 56)
    }
}

#Preview {
    SettingsView()
}
'''


# ============== Kotlin/Jetpack Compose Generators ==============

def _generate_kotlin_login(auth_type, social, remember, forgot, styling):
    input_field = "email" if auth_type == "email" else ("phone" if auth_type == "phone" else "username")
    input_label = "Email address" if auth_type == "email" else ("Phone number" if auth_type == "phone" else "Username")
    keyboard_type = "KeyboardType.Email" if auth_type == "email" else ("KeyboardType.Phone" if auth_type == "phone" else "KeyboardType.Text")

    return f'''package com.example.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun LoginScreen(
    onNavigateToSignUp: () -> Unit,
    onNavigateToForgotPassword: () -> Unit,
    onLoginSuccess: () -> Unit
) {{
    var {input_field} by remember {{ mutableStateOf("") }}
    var password by remember {{ mutableStateOf("") }}
    var rememberMe by remember {{ mutableStateOf(false) }}
    var isLoading by remember {{ mutableStateOf(false) }}
    var passwordVisible by remember {{ mutableStateOf(false) }}

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {{
        Spacer(modifier = Modifier.height(60.dp))

        // Header
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.Start
        ) {{
            Text(
                text = "Welcome Back",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1A1A1A)
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Sign in to continue",
                fontSize = 16.sp,
                color = Color.Gray
            )
        }}

        Spacer(modifier = Modifier.height(40.dp))

        // Social Login Buttons
        SocialButton(text = "Continue with Google") {{ }}
        Spacer(modifier = Modifier.height(12.dp))
        SocialButton(text = "Continue with Apple") {{ }}

        Spacer(modifier = Modifier.height(24.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {{
            HorizontalDivider(modifier = Modifier.weight(1f))
            Text(
                text = "or",
                modifier = Modifier.padding(horizontal = 16.dp),
                color = Color.Gray
            )
            HorizontalDivider(modifier = Modifier.weight(1f))
        }}

        Spacer(modifier = Modifier.height(24.dp))

        // Input Fields
        Text(
            text = "{input_label}",
            fontSize = 14.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = {input_field},
            onValueChange = {{ {input_field} = it }},
            placeholder = {{ Text("Enter your {input_field}") }},
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            keyboardOptions = KeyboardOptions(keyboardType = {keyboard_type}),
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                unfocusedContainerColor = Color(0xFFF5F5F5),
                focusedContainerColor = Color(0xFFF5F5F5),
                unfocusedBorderColor = Color.Transparent,
                focusedBorderColor = Color(0xFF007AFF)
            )
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "Password",
            fontSize = 14.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = password,
            onValueChange = {{ password = it }},
            placeholder = {{ Text("Enter your password") }},
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
            singleLine = true,
            colors = OutlinedTextFieldDefaults.colors(
                unfocusedContainerColor = Color(0xFFF5F5F5),
                focusedContainerColor = Color(0xFFF5F5F5),
                unfocusedBorderColor = Color.Transparent,
                focusedBorderColor = Color(0xFF007AFF)
            )
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Remember Me & Forgot Password
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {{
            Row(verticalAlignment = Alignment.CenterVertically) {{
                Checkbox(
                    checked = rememberMe,
                    onCheckedChange = {{ rememberMe = it }},
                    colors = CheckboxDefaults.colors(checkedColor = Color(0xFF007AFF))
                )
                Text(text = "Remember me", color = Color.Gray)
            }}
            TextButton(onClick = onNavigateToForgotPassword) {{
                Text(
                    text = "Forgot Password?",
                    color = Color(0xFF007AFF),
                    fontWeight = FontWeight.SemiBold
                )
            }}
        }}

        Spacer(modifier = Modifier.height(24.dp))

        // Login Button
        Button(
            onClick = {{
                isLoading = true
                // TODO: Implement login logic
            }},
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            shape = RoundedCornerShape(12.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF007AFF)),
            enabled = !isLoading
        ) {{
            if (isLoading) {{
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = Color.White
                )
            }} else {{
                Text(
                    text = "Sign In",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }}
        }}

        Spacer(modifier = Modifier.height(24.dp))

        // Sign Up Link
        Row(verticalAlignment = Alignment.CenterVertically) {{
            Text(text = "Don't have an account? ", color = Color.Gray)
            TextButton(onClick = onNavigateToSignUp) {{
                Text(
                    text = "Sign Up",
                    color = Color(0xFF007AFF),
                    fontWeight = FontWeight.SemiBold
                )
            }}
        }}
    }}
}}

@Composable
fun SocialButton(text: String, onClick: () -> Unit) {{
    OutlinedButton(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .height(50.dp),
        shape = RoundedCornerShape(12.dp),
        colors = ButtonDefaults.outlinedButtonColors(
            containerColor = Color(0xFFF5F5F5)
        ),
        border = null
    ) {{
        Text(
            text = text,
            fontWeight = FontWeight.SemiBold,
            color = Color(0xFF333333)
        )
    }}
}}
'''


def _generate_kotlin_home(layout, header, bottom_nav, search, card_style):
    return '''package com.example.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

data class Item(
    val id: String,
    val title: String,
    val description: String,
    val category: String
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onNavigateToDetail: (Item) -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedTab by remember { mutableIntStateOf(0) }

    val items = remember {
        listOf(
            Item("1", "Item 1", "Description for item 1", "Category A"),
            Item("2", "Item 2", "Description for item 2", "Category B"),
            Item("3", "Item 3", "Description for item 3", "Category A"),
            Item("4", "Item 4", "Description for item 4", "Category C"),
            Item("5", "Item 5", "Description for item 5", "Category B"),
            Item("6", "Item 6", "Description for item 6", "Category A"),
        )
    }

    val filteredItems = items.filter {
        it.title.contains(searchQuery, ignoreCase = true)
    }

    Scaffold(
        bottomBar = {
            NavigationBar {
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                    label = { Text("Home") },
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                    label = { Text("Search") },
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Favorite, contentDescription = "Favorites") },
                    label = { Text("Favorites") },
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 }
                )
                NavigationBarItem(
                    icon = { Icon(Icons.Default.Person, contentDescription = "Profile") },
                    label = { Text("Profile") },
                    selected = selectedTab == 3,
                    onClick = { selectedTab = 3 }
                )
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .background(Color(0xFFF8F9FA))
        ) {
            // Header
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(20.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "Hello,",
                        fontSize = 14.sp,
                        color = Color.Gray
                    )
                    Text(
                        text = "John Doe",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
                Box(
                    modifier = Modifier
                        .size(44.dp)
                        .clip(CircleShape)
                        .background(Color(0xFF007AFF))
                )
            }

            // Search Bar
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                placeholder = { Text("Search...") },
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color.White)
                    .padding(horizontal = 20.dp, vertical = 12.dp),
                shape = RoundedCornerShape(12.dp),
                leadingIcon = {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                },
                colors = OutlinedTextFieldDefaults.colors(
                    unfocusedContainerColor = Color(0xFFF5F5F5),
                    focusedContainerColor = Color(0xFFF5F5F5),
                    unfocusedBorderColor = Color.Transparent,
                    focusedBorderColor = Color(0xFF007AFF)
                ),
                singleLine = true
            )

            // Content Grid
            LazyVerticalGrid(
                columns = GridCells.Fixed(2),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                items(filteredItems) { item ->
                    ItemCard(item = item, onClick = { onNavigateToDetail(item) })
                }
            }
        }
    }
}

@Composable
fun ItemCard(item: Item, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(100.dp)
                    .background(Color(0xFFE0E0E0))
            )
            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    text = item.title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = item.description,
                    fontSize = 14.sp,
                    color = Color.Gray,
                    maxLines = 2
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = item.category,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium,
                    color = Color(0xFF007AFF)
                )
            }
        }
    }
}
'''


def _generate_kotlin_settings(sections, profile, theme, notifications, logout):
    return '''package com.example.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun SettingsScreen(
    onNavigateToLogin: () -> Unit
) {
    var darkMode by remember { mutableStateOf(false) }
    var notificationsEnabled by remember { mutableStateOf(true) }
    var showLogoutDialog by remember { mutableStateOf(false) }

    if (showLogoutDialog) {
        AlertDialog(
            onDismissRequest = { showLogoutDialog = false },
            title = { Text("Log Out") },
            text = { Text("Are you sure you want to log out?") },
            confirmButton = {
                TextButton(
                    onClick = {
                        showLogoutDialog = false
                        onNavigateToLogin()
                    }
                ) {
                    Text("Log Out", color = Color.Red)
                }
            },
            dismissButton = {
                TextButton(onClick = { showLogoutDialog = false }) {
                    Text("Cancel")
                }
            }
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFFF8F9FA))
            .verticalScroll(rememberScrollState())
    ) {
        // Header
        Text(
            text = "Settings",
            fontSize = 34.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(20.dp)
        )

        // Profile Section
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(Color.White)
                .clickable { }
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(60.dp)
                    .clip(CircleShape)
                    .background(Color(0xFF007AFF))
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "John Doe",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    text = "john.doe@example.com",
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }
            Icon(
                Icons.AutoMirrored.Filled.KeyboardArrowRight,
                contentDescription = null,
                tint = Color.Gray
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        // Account Section
        SettingsSection(title = "Account") {
            SettingsItem(icon = Icons.Default.Person, title = "Edit Profile")
            SettingsItem(icon = Icons.Default.Lock, title = "Change Password")
            SettingsItem(icon = Icons.Default.Shield, title = "Privacy")
        }

        // Preferences Section
        SettingsSection(title = "Preferences") {
            SettingsToggleItem(
                title = "Dark Mode",
                checked = darkMode,
                onCheckedChange = { darkMode = it }
            )
            SettingsToggleItem(
                title = "Push Notifications",
                checked = notificationsEnabled,
                onCheckedChange = { notificationsEnabled = it }
            )
            SettingsItem(icon = Icons.Default.Language, title = "Language")
        }

        // Support Section
        SettingsSection(title = "Support") {
            SettingsItem(icon = Icons.Default.Help, title = "Help Center")
            SettingsItem(icon = Icons.Default.Email, title = "Contact Us")
            SettingsItem(icon = Icons.Default.Description, title = "Terms of Service")
        }

        // About Section
        SettingsSection(title = "About") {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text("App Version")
                Text("1.0.0", color = Color.Gray)
            }
        }

        // Logout Button
        Button(
            onClick = { showLogoutDialog = true },
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            shape = RoundedCornerShape(16.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color.White)
        ) {
            Text(
                text = "Log Out",
                color = Color.Red,
                fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(vertical = 8.dp)
            )
        }

        Spacer(modifier = Modifier.height(20.dp))
    }
}

@Composable
fun SettingsSection(
    title: String,
    content: @Composable ColumnScope.() -> Unit
) {
    Column(modifier = Modifier.padding(bottom = 24.dp)) {
        Text(
            text = title.uppercase(),
            fontSize = 14.sp,
            fontWeight = FontWeight.SemiBold,
            color = Color.Gray,
            letterSpacing = 0.5.sp,
            modifier = Modifier.padding(horizontal = 24.dp, vertical = 8.dp)
        )
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(Color.White)
        ) {
            content()
        }
    }
}

@Composable
fun SettingsItem(
    icon: ImageVector,
    title: String,
    onClick: () -> Unit = {}
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            icon,
            contentDescription = null,
            tint = Color.Gray,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(
            text = title,
            modifier = Modifier.weight(1f)
        )
        Icon(
            Icons.AutoMirrored.Filled.KeyboardArrowRight,
            contentDescription = null,
            tint = Color.Gray
        )
    }
    HorizontalDivider(modifier = Modifier.padding(start = 56.dp))
}

@Composable
fun SettingsToggleItem(
    title: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            modifier = Modifier.weight(1f)
        )
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = Color.White,
                checkedTrackColor = Color(0xFF007AFF)
            )
        )
    }
    HorizontalDivider()
}
'''


def main():
    """Entry point for the MCP server."""
    if TRANSPORT == "sse":
        # Run as HTTP server with SSE transport
        mcp.run(transport="sse", host=HOST, port=PORT)
    else:
        # Run as stdio (default for local use)
        mcp.run()


if __name__ == "__main__":
    main()
