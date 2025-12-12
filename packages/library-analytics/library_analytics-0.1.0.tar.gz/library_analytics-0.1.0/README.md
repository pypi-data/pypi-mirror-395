# Library Analytics

A Python package for library management analytics, designed to work seamlessly with Django-based library systems.

## Features

- **Inventory Summary**: Get real-time statistics on total books, available stock, and out-of-stock items
- **Checkout Reports**: Track weekly/daily checkout trends
- **Popular Books**: Identify most and least borrowed books
- **Overdue Tracking**: Monitor overdue book returns
- **Genre Analysis**: Analyze book distribution by genre
- **User Activity**: Track individual user borrowing patterns

## Installation

```bash
pip install library-analytics
```

For Django integration:
```bash
pip install library-analytics[django]
```

## Quick Start

### With Django

```python
from library_analytics import LibraryAnalytics

# Initialize (auto-detects Django models)
analytics = LibraryAnalytics()

# Get inventory summary
summary = analytics.inventory_summary()
print(f"Total books: {summary['total_books']}")
print(f"Available: {summary['stock_in']}")
print(f"Out of stock: {summary['stock_out']}")

# Get weekly checkout report
weekly_checkouts = analytics.weekly_checkout_report(days=7)
print(f"Checkouts this week: {weekly_checkouts}")

# Get popular books
popular = analytics.popular_books(limit=10)
for book in popular:
    print(f"{book.title} - {book.checkout_count} checkouts")
```

### With Custom Models

```python
from library_analytics import LibraryAnalytics
from myapp.models import Book, Transaction
from django.utils import timezone

# Initialize with custom models
analytics = LibraryAnalytics(
    book_model=Book,
    transaction_model=Transaction,
    timezone_module=timezone
)

# Use the same methods as above
summary = analytics.inventory_summary()
```

## Available Methods

### `inventory_summary()`
Returns a dictionary with inventory statistics:
- `total_books`: Total number of unique book titles
- `stock_in`: Books currently available for checkout
- `stock_out`: Books currently out of stock
- `total_copies`: Total number of book copies

### `weekly_checkout_report(days=7)`
Returns the number of checkouts in the last N days.

### `popular_books(limit=10)`
Returns a list of most frequently borrowed books.

### `least_borrowed_books(limit=10)`
Returns a list of least frequently borrowed books.

### `overdue_books()`
Returns a list of transactions with overdue books.

### `genre_distribution()`
Returns a dictionary mapping genres to book counts.

### `user_activity(user_id)`
Returns borrowing statistics for a specific user.

## Django Integration

The package automatically detects Django models named `BookLog` and `Transaction` from a `books` app.

Your models should have the following structure:

```python
class BookLog(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    number_of_books_available = models.IntegerField(default=0)
    # ... other fields

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(BookLog, related_name='transactions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_checkout = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    # ... other fields
```

## Requirements

- Python >= 3.8
- Django >= 4.0 (optional, for Django integration)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
