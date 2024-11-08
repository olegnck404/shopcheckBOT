
### README.md

```markdown
# Aiogram Product Management Bot

This is a Telegram bot built using the Aiogram framework that allows users to manage products through a simple and interactive interface. Users can search for products by SKU, view all available products, and administrators can add, edit, or delete products.

## Features

- **User Features**:
  - Search for products by SKU.
  - View all products in the database.

- **Admin Features**:
  - Admin login with password protection.
  - Add new products to the database.
  - Edit existing product details.
  - Delete products from the database.
  - View product details with inline buttons.

## Technologies Used

- [Python](https://www.python.org/)
- [Aiogram](https://docs.aiogram.dev/en/latest/)
- [SQLite](https://www.sqlite.org/index.html)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file or update your `config.py` with your Telegram bot token:
   ```python
   API_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

5. Run the bot:
   ```bash
   python main.py
   ```

## Usage

- Start the bot by sending the `/start` command in your Telegram chat.
- Follow the prompts to interact with the bot.

## Contributing

Contributions are welcome! Please create a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### requirements.txt

```plaintext
aiogram==3.14.0
```

