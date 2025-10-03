# 🎮 Discord Coin Reward Bot

A fun and interactive Discord bot that rewards users with coins for participating in voice channels. Users can earn coins by joining and staying in voice channels, then spend them in the shop to unlock special items!

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 💰 **Automatic Coin Rewards** - Earn 20 coins instantly when joining a voice channel
- ⏱️ **Time-Based Earnings** - Get 10 coins per minute while in voice channels
- 🛒 **Shop System** - Purchase exclusive items with earned coins
- 💾 **Persistent Storage** - Coin balances are saved and persist across bot restarts
- 🎁 **Image Rewards** - Shop items can include custom images sent to users
- 📊 **Balance Tracking** - Check your coin balance anytime
- 🔧 **Easy Configuration** - Simple setup with environment variables
- 🎯 **User-Friendly Commands** - Intuitive command structure with help system

---

## 🎯 How It Works

### Earning Coins

1. **Join Bonus**: Get **20 coins** immediately when you join any voice channel
2. **Time Reward**: Earn **10 coins per minute** while staying in the voice channel
3. **Leave Payout**: Receive your accumulated time-based coins when you leave

### Example Earning Scenario

```
User joins voice channel → +20 coins (instant)
User stays for 5 minutes → +50 coins (10 coins/min × 5 min)
User leaves → Total earned: 70 coins
```

---

## 📦 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package manager)
- A **Discord Account** and **Discord Server** where you have admin permissions
- A **Discord Bot Token** from the [Discord Developer Portal](https://discord.com/developers/applications)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/MrHunt18/discord-Bot.git
cd discord-Bot
```

### Step 2: Install Dependencies

```bash
pip install discord.py python-dotenv
```

**Required packages:**
- `discord.py` - Discord API wrapper
- `python-dotenv` - Environment variable management

### Step 3: Create Environment File

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Discord bot token:

```env
DISCORD_TOKEN=your_bot_token_here
```

> ⚠️ **Important:** Never commit your `.env` file to version control!

### Step 4: Set Up Image Folder

Create an `images` folder and add your shop item images:

```bash
mkdir images
```

Add your images to this folder (e.g., `item1.png`, `item2.png`, `item3.png`)

---

## 🔧 Configuration

### Getting Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Navigate to the **"Bot"** section
4. Click **"Add Bot"**
5. Under the token section, click **"Copy"** to get your token
6. Paste it in your `.env` file

### Bot Permissions

Your bot needs these permissions:
- ✅ Read Messages/View Channels
- ✅ Send Messages
- ✅ Attach Files
- ✅ Connect to Voice Channels
- ✅ View Voice Channel Members

**Invite URL Format:**
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=3148800&scope=bot
```

Replace `YOUR_CLIENT_ID` with your bot's Application ID from the Developer Portal.

### Required Intents

The bot requires these Discord Gateway Intents (already configured in code):
- `message_content` - To read messages
- `members` - To track member information
- `voice_states` - To detect voice channel joins/leaves

Enable these in the Discord Developer Portal under **Bot → Privileged Gateway Intents**.

---

## 💻 Usage

### Running the Bot

```bash
python bot.py
```

You should see:
```
✅ Logged in as YourBotName#1234
```

### Stopping the Bot

Press `Ctrl + C` in the terminal.

---

## 🎮 Commands

All commands use the prefix `!`

| Command | Description | Example |
|---------|-------------|---------|
| `!balance` | Check your current coin balance | `!balance` |
| `!shop` | View all available shop items | `!shop` |
| `!buy <item>` | Purchase an item from the shop | `!buy friend1` |
| `!commands` | List all available commands | `!commands` |
| `!help [command]` | Get help for a specific command | `!help buy` |

### Command Examples

#### Check Balance
```
User: !balance
Bot: 💰 @User, you have 150 coins.
```

#### View Shop
```
User: !shop
Bot: **Shop Items:**
     🛒 item1 (item1.png)
     🛒 item2 (item2.png)
     🛒 item3 (item3.png)
     
     Use !buy item_name to purchase.
```

#### Purchase Item
```
User: !buy item1
Bot: ✅ @User purchased item1! [Image attached]
```

---

## 📁 Project Structure

```
discord-Bot/
│
├── bot.py                 # Main bot application
├── .env                   # Environment variables (not in repo)
├── .gitignore            # Git ignore file
├── coins.json            # User coin balances (auto-generated)
├── images/               # Shop item images folder
│   ├── item1.png
│   ├── item2.png
│   └── item3.png
│
└── README.md            # This file
```

### File Descriptions

- **bot.py**: Main bot logic with commands and event handlers
- **.env**: Stores sensitive configuration (Discord token)
- **coins.json**: Persists user coin balances (created automatically)
- **images/**: Contains shop item images

---

## 🎨 Customization

### Changing Coin Rates

Edit the global settings in `bot.py`:

```python
# ---------------- GLOBAL SETTINGS ----------------
COINS_PER_MINUTE = 10  # Change this value
```

### Modifying Join Bonus

Find the `on_voice_state_update` function:

```python
# Give 20 coins on join (change the value here)
coins[str(member.id)] = coins.get(str(member.id), 0) + 20
```

### Adding Shop Items

Edit the `shop_items` dictionary:

```python
shop_items = {
    "item1": "item1.png",
    "item2": "item2.png",
    "item3": "item3.png",
    "new_item": "new_image.png",  # Add your new item
}
```

### Setting Item Prices

Currently, all items cost 10 coins. To add variable pricing:

```python
# Add a price dictionary
shop_prices = {
    "item1": 50,
    "item2": 100,
    "item3": 150,
}

# Modify the buy command to use shop_prices[item_name]
```

### Changing the Command Prefix

Modify the bot initialization:

```python
bot = commands.Bot(command_prefix="!", intents=intents)  # Change "!" to any prefix
```

### Customizing Text Channel for Notifications

Currently set to `"general"`. Change it in the event handler:

```python
text_channel = discord.utils.get(member.guild.text_channels, name="your-channel-name")
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Bot doesn't respond to commands
- **Solution**: Make sure you've enabled the "Message Content Intent" in Discord Developer Portal
- Verify the bot has permission to read and send messages in the channel

#### Bot can't find images
```
⚠️ Sorry, the file for this item is missing.
```
- **Solution**: Ensure images are in the `images/` folder
- Check that filenames in `shop_items` match exactly (case-sensitive)

#### Bot disconnects frequently
- **Solution**: Check your internet connection
- Ensure your hosting service (if using one) is stable

#### Token errors
```
discord.errors.LoginFailure: Improper token has been passed.
```
- **Solution**: Verify your `.env` file has the correct token
- Make sure there are no spaces or quotes around the token

#### Permission errors
- **Solution**: Re-invite the bot with proper permissions
- Check server roles and ensure the bot role has necessary permissions

---

## 📊 Data Persistence

### coins.json Structure

```json
{
    "user_id_1": 150,
    "user_id_2": 300,
    "user_id_3": 75
}
```

- Keys are Discord user IDs (as strings)
- Values are coin balances (integers)
- File is automatically created on first use
- Updates happen in real-time

---

## 🔒 Security Best Practices

1. **Never commit `.env` files**
   ```bash
   # Add to .gitignore
   .env
   ```

2. **Regenerate tokens if exposed**
   - Go to Discord Developer Portal
   - Reset your bot token immediately

3. **Limit bot permissions**
   - Only grant necessary permissions
   - Use role hierarchies properly

4. **Backup your data**
   - Regularly backup `coins.json`
   - Consider implementing database storage for production

---

## 🚀 Future Enhancements

Ideas for extending the bot:

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Leaderboard system
- [ ] Daily coin bonuses
- [ ] Mini-games for earning coins
- [ ] Trading system between users
- [ ] Tiered shop items with different prices
- [ ] Admin commands for managing coins
- [ ] Statistics and analytics
- [ ] Cooldown systems
- [ ] Achievement system

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**MrHunt18**
- GitHub: [@MrHunt18](https://github.com/MrHunt18)

---

## 🙏 Acknowledgments

- [Discord.py](https://discordpy.readthedocs.io/) - Python Discord API wrapper
- Discord Developer Community
- All contributors and users

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on [GitHub Issues](https://github.com/MrHunt18/discord-Bot/issues)
3. Join the Discord.py community for general Discord bot help

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Happy Botting! 🎉**
