# iyzico Payment Provider for Pretix - Detailed Setup Guide

This plugin integrates the **iyzico** payment gateway into self-hosted Pretix installations.

## Installation for Self-hosted Pretix

### 1. Prepare Your Pretix Virtual Environment

```bash
# Activate the virtual environment of your Pretix installation
source /path/to/your/pretix/.venv/bin/activate

# Example: If your pretix is in the pretix-dev folder
source /Users/emircankartal/dev/pretix-dev/pretix/.venv/bin/activate
```

### 2. Download and Install the Plugin

```bash
# Clone the repository
git clone https://github.com/EmircanKartal/pretix-iyzico.git
cd pretix-iyzico

# Install the plugin in editable mode
pip install -e .
```

### 3. Restart Pretix

```bash
# Restart the Pretix server
cd /path/to/your/pretix/src
python manage.py runserver
```

## iyzico API Keys

To use this plugin, you need to obtain your API keys from the iyzico Merchant Panel.

### Sandbox (Test) Keys
For iyzico sandbox (test) accounts:
- **API Key:** Found in Settings > Developer Settings
- **Secret Key:** Found in Settings > Developer Settings
- **Sandbox Mode:** ✅ Checked

### Production Keys
For live iyzico production accounts:
- **API Key:** Found in Settings > Developer Settings
- **Secret Key:** Found in Settings > Developer Settings
- **Sandbox Mode:** ❌ Unchecked

## Configuration

1.  **Open Pretix Panel:** Go to your Pretix instance (e.g., http://localhost:8000).
2.  **Enable Plugin:** Go to **Settings** -> **Plugins** and enable the **iyzico** plugin.
3.  **Configure Payment:**
    - Go to **Settings** -> **Payment providers**.
    - Select **iyzico**.
4.  **Enter Credentials:**
    - Paste your **API Key** and **Secret Key**.
5.  **Select Mode:**
    - Check **Use Sandbox** for testing.
    - Uncheck it for real payments.

## Test Cards

Use these cards to test payments in Sandbox mode:

### Sandbox Test Cards:
- **Successful Payment:** `5528790000000008`
- **CVV:** `123`
- **Expiry Date:** `12/30` (or any future date)

## Features

- Pay with iyzico full integration
- Sandbox and Production modes
- Automatic payment confirmation
- Webhook support
- Error handling
- Logging

## URL Endpoints

Ensure these endpoints are reachable for callbacks:

- **Return URL:** `/iyzico/return/`
- **Webhook URL:** `/iyzico/webhook/`

## Troubleshooting

### Plugin not showing up:
Run this command to check if the entry point is registered:
```bash
python -c "import pkg_resources; print([e.name for e in pkg_resources.iter_entry_points('pretix.plugin')])"
```

### API Error:
- Double-check your API keys.
- Ensure you are in the correct mode (Sandbox vs Production).
- Check Pretix logs.

### Payment Failed:
- Use the correct test cards.
- Verify CVV and expiry dates.
- Ensure Webhook URLs are accessible from the internet.
